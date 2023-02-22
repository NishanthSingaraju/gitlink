from gitlink.deployers.AWSEcrDeployer import AWSEcrDeployer

deployment_types = {
    "aws_ecr_deploy": AWSEcrDeployer
}

def get_deployer(deploy_type):
    if deploy_type not in deployment_types:
        raise ValueError(f"Deploy Type: {deploy_type} does not exist")
    return deployment_types[deploy_type]

    
