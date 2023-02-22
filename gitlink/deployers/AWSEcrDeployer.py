import boto3
import base64
import botocore
import time
import json

from gitlink.constants import SERVER_PORT, GIT_LINK
from gitlink.docker import Docker


class AWSFargateDeployer:
    def __init__(self, access_key, secret_key, *args, **kwargs):
        # Authenticate boto3 clients using the provided access token and secret key
        self.ecr = boto3.client("ecr", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.ecs = boto3.client("ecs", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.elbv2 = boto3.client("elbv2", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.iam = boto3.client('iam', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
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