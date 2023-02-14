from gitlink.deployers.aws_fargate_deployer import AWSFargateDeployer

deployment_types = {
    "aws_fargate_deployer": AWSFargateDeployer
}

def get_deployer(deploy_type):
    if deploy_type not in deployment_types:
        raise ValueError(f"Deploy Type: {deploy_type} does not exist")
    return deployment_types[deploy_type]

    
