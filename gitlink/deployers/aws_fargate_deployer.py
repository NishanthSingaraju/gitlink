
import boto3
import base64
import botocore

from gitlink.constants import SERVER_PORT, GIT_LINK
from gitlink.docker import Docker


class AWSFargateDeployer:
    def __init__(self, access_key, secret_key, *args, **kwargs):
        # Authenticate boto3 clients using the provided access token and secret key
        self.ecr = boto3.client("ecr", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.ecs = boto3.client("ecs", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.elbv2 = boto3.client("elbv2", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        try:
            Docker.client().login_ecr(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        except botocore.exceptions.NoCredentialsError as e:
            raise Exception("AWS credentials not found. Please configure AWS CLI or set environment variables.")

    def deploy(self, image, deployment_config):
        repository = deployment_config.get("repository_uri", GIT_LINK)
        try:
            repository_uri = self.ecr.describe_repositories(repositoryNames=[repository])["repositories"][0]['repositoryUri']
        except self.ecr.exceptions.RepositoryNotFoundException:
            repository_uri = self.ecr.create_repository(repositoryName=repository)['repositoryUri']
        except Exception as e:
            raise Exception("An error occurred while checking or creating the ECR registry and repository.")

        registry = repository_uri[:12]

        # Tag the Docker image with the registry, repository and version
        image_tag = "{}:{}".format(repository_uri, "latest")
        Docker.client().image.tag(image.id, image_tag)
        Docker.client().image.push(image_tag)

        # Connect to the AWS Fargate service
        ecs = self.ecs

        # Create or update the Fargate task definition
        task_definition = ecs.register_task_definition(
            family=deployment_config.get("task_definition_family", "default_task_definition_family"),
            containerDefinitions=[
                {
                    "name": deployment_config.get("container_name", "default_container"),
                    "image": f"{registry}/{repository}:{deployment_config.get('version', 'latest')}",
                    "cpu": deployment_config.get("cpu", 128),
                    "memory": deployment_config.get("memory", 512),
                    "portMappings": [
                        {
                            "containerPort": SERVER_PORT,
                            "hostPort": deployment_config.get("host_port", 8080),
                            "protocol": "tcp"
                        },
                    ],
                    "essential": True,
                },
            ],
        )

        cluster_name = deployment_config.get("cluster", GIT_LINK)
        # Check if the cluster exists
        response = ecs.describe_clusters(clusters=[cluster_name])
        if not response["clusters"]:
            cluster_exists = False
        else:
            cluster_exists = True
        if not cluster_exists:
            # If the cluster doesn't exist, create it
            service = self.create_cluster(cluster_name, deployment_config, task_definition)
        else:
            cluster_status = response['clusters'][0]['status']
            print(cluster_status)
            if cluster_status == 'INACTIVE':
                service = self.create_cluster(cluster_name, deployment_config, task_definition)
            else:
                service = ecs.update_service(
                    cluster=cluster_name,
                    service=deployment_config.get("service_name", "default_service"),
                    taskDefinition=task_definition["taskDefinition"]["taskDefinitionArn"],
                    desiredCount=deployment_config.get("desired_count", 1)
                )

        # Return the public endpoint of the Fargate service
        return f"http://{service['service']['loadBalancers'][0]['containerName']}.{service['service']['clusterArn']}.elb.amazonaws.com:{SERVER_PORT}/"

    def create_cluster(self, cluster_name, deployment_config, task_definition):
        self.ecs.create_cluster(clusterName=cluster_name)
        # Create or update the Fargate service
        target_group_response = self.elbv2.create_target_group(
            targetGroupName=deployment_config.get("target_group_name", "default_target_group"),
        targets=[{
            'id': deployment_config.get("container_name", "default_container"),
            'port': SERVER_PORT
        }]
        )
        TARGET_GROUP_ARN = target_group_response['targetGroups'][0]['targetGroupArn']

        # create service with the target group
        service = self.ecs.create_service(
                        cluster=cluster_name,
                        serviceName=deployment_config.get("service_name", "default_service"),
                        taskDefinition=task_definition["taskDefinition"]["taskDefinitionArn"],
                        desiredCount=deployment_config.get("desired_count", 1),
                        loadBalancers=[{
                            'targetGroupArn': TARGET_GROUP_ARN,
                            'containerName': deployment_config.get("container_name", "default_container"),
                            'containerPort': SERVER_PORT}]
                        )
        return service
            