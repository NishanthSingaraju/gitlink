# GitLink

GitLink is a tool designed to simplify the process of connecting your Git Large File Storage (LFS) to your Amazon Web Services (AWS) or Google Cloud Platform (GCP) backends. With GitLink, you can easily store large files in your cloud storage buckets, reducing the storage burden on your Git repositories.

GitLink supports multiple cloud storage backends, including AWS S3 and GCP Cloud Storage, and provides a convenient command-line interface for managing your repositories and deploying them to the cloud. The tool is built on top of Docker and can be deployed to various platforms, including AWS Elastic Beanstalk and Google App Engine.

To get started with GitLink, clone the repository, install the required dependencies, and configure your cloud storage backend using the provided configuration file. Then, you can use the GitLink command-line interface to build, run, and deploy your repositories to the cloud.

Whether you're working on a large-scale software project or need to store and share large files, GitLink makes it easy to connect your Git LFS to your AWS or GCP backend.

Special thanks to the teams behind the Truss and Giftless repositories for their architectural inspirations. Their work has been invaluable in guiding the development of this project."

# Installing Git LFS
Git LFS is a command-line extension for git that allows storing large files separately from your Git repository. Here's how you can install Git LFS:

1) Visit the Git LFS website: https://git-lfs.github.com/
2) Click on the "Download" button to download the installer for your operating system.
3) Follow the instructions in the installer to complete the installation process.

Once you've installed Git LFS, you can use it to manage large files in your Git repository.

# Installing and Setting Up Poetry
Poetry is a tool for dependency management and packaging in Python. It allows you to easily manage and install the packages required by your Python projects. Here's how you can install and set up Poetry:

1) Visit the Poetry website: https://python-poetry.org/
2) Follow the installation instructions for your operating system.
For example, on macOS, you can use Homebrew to install Poetry by running brew install poetry.
3) Once you've installed Poetry, navigate to the root directory of our project in a terminal.
4) Run poetry install, then poetry shell in the terminal


# Cloning the GitLink Repository
Open a terminal and navigate to the directory where you want to clone the GitLink repository.

Run the following command to clone the repository:
    git clone https://github.com/NishanthSingaraju/gitlink.git
This will clone the GitLink repository to your local machine.

# Creating a Configuration File
After cloning the GitLink repository, you need to create a config.yaml file to configure GitLink with your backend.

1) In a directory outside the GitLink repository i.e.e, anywhere, create a new file called config. yaml.

2) Copy the following YAML code into the file:

name: test
plugins:
- AWSStorageHandler
storage_handler: AWSStorageHandler
vars: 
  bucket_name:
   value: test-git-flow
   type: string
  access_key: 
    value: AWS_ACCESS_KEY_ID
    type: secret
  secret_key:
    value: AWS_SECRET_ACCESS_KEY
    type: secret
secrets: 
  names:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
  source: env
  drain: mount

The access and secret key are just the strings themselves, not a proxy for the values. You must add your secret for AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in your environment variables. Then, specify the needed secrets for the given backend.

3) In the vars section, replace the bucket_name value with the name of the S3 bucket you want to use for storing Git LFS objects. For example, if you are using GCP, replace AWSStorageHandler with GCPStorageHandler.


# Using GitLink Locally

Once you've cloned the GitLink repository and created a config.yaml file, you can use GitLink locally on your machine.

1) Navigate to the root directory of the GitLink repository and run the poetry shell command to activate the project's virtual environment.

2) Navigate to the config.yaml file. 

3) Run the following command to build and run a Docker image with the required plugins and dependencies:

    gink run-image config.yaml . --tag my-image --port 8080 --attach
This command runs the Docker image locally and attaches it to your terminal.

The --port option specifies the port the API will run on. In this example, we are using port 8080. Of course, you can use any port available on your machine.

Once the container is running, you can access the API at http://localhost:8080. The API endpoint will provide you with the URL for Git LFS.

4) Set the Git LFS endpoint URL to the URL of the GitLink server by running the following command:

    git config -f .lfsconfig lfs.url http://localhost:8080
Run this command in the repository with your large objects.

5) Track the files that you want to store in Git LFS. You can do this by running the following command:

    git lfs track "*.extension."
    Replace *.extension with the file extension of the files that you want to track. For example, if you want to track all mp4 files, you would use git lfs track "*.mp4".

Add the tracked files to your repository and push the changes to the remote repository:

6)
git add .
git commit -m "Add large files to LFS"
git push
That's it! Now the large files that you've tracked using Git LFS will be stored in the GitLink server backend that you configured in the config.yaml file.

# Using GitLink Remotely
Once you've set up the config.yaml file with your desired configuration, you can deploy your container to AWS, GCP, or other cloud platforms and access it remotely. Here's how to do it:

1) Set up your config. yaml file as described in the previous section.

2) Run the following command to build a folder with the Docker image and all the files needed for the API:

Option 1# 
gink build-context <config_file> <build_dir>
Replace <config_file> with the path to your config.yaml file and <build_dir> with the path where the Docker image and other API files should be stored. This command will install the necessary plugins and dependencies and create a Dockerfile in the specified build directory.

Once the context is built, then:

3) Install AWS Copilot by following the instructions provided in the AWS Copilot documentation.
4) Navigate to the build directory where the Dockerfile is located. This is the directory specified in the gink build-context command.
5) Run the following command to initialize the AWS Copilot app:
Copilot app init
Follow the prompts to create a new app or select an existing app, choose the default deployment environment, and select the workload type as "Load Balanced Web Service."

When prompted to choose a Dockerfile, enter the relative path to the Dockerfile in the build directory, for example, ./Dockerfile.
Enter a name for the service and follow the prompts to choose a service type, configure the load balancer, and configure the VPC and subnets.

Option 1# (only works for AWS ECR)

gink deploy <config_file> 
Replace <config_file> with the path to your config.yaml file. This command will build the docker image and save it to your ECR registry.

# Configuration schema

The gink command line tool requires a configuration file to build and deploy the application. The configuration file specifies the server's name, plugins, and the storage backend to use. It also includes variables and secrets that the backend and plugins will use.

Here is an example configuration file:

name: {name of the server}
plugins:
- {list of plugin names}
storage_handler: {backend to upload assets to}
vars: 
  {variable name}:
   value: {variable value}
   type: {variable type}
secrets: 
  names:
    - {list of secret names}
  source: {source of secrets}
  drain: {drain of secrets}

- name: The name of the server
- plugins: The list of plugins to install on the server
- storage_handler: The backend to upload assets to
- vars: Variables that are used by the backend/plugins
- secrets:
    - names: A list of secret names, not the values
    - source: Where the secrets are coming from. The only option currently supported is "env".
    - drain: Where the secrets will be pulled from in the Docker image. The only option currently supported is "mount."

# Commands
GitLink provides four different commands that can be run from the command line:

gink build-context [config] {build-dir}
This command builds a folder with the Docker image and all files needed for the API, including installing the plugins. The {config} argument specifies the path to the configuration file, and the optional {build-dir} argument specifies the path to the directory where the build context will be created. The command will use a default directory if no {build-dir} is provided.

Example usage:
gink build-context config.yaml

gink build-image [config] {build-dir} --tag {tag}
This command builds a Docker image based on the built context. The {config} argument specifies the path to the configuration file, and the optional {build-dir} argument specifies the path to the directory where the build context is located. The --tag flag specifies the tag for the Docker image.

Example usage:
gink build-image config.yaml --tag my-image: latest

gink run-image [config] {build-dir} --tag {tag} --port {port} --attach {attach}
This command runs the Docker image locally. The {config} argument specifies the path to the configuration file, and the optional {build-dir} argument specifies the path to the directory where the build context is located. The --tag flag specifies the tag of the Docker image to be run. The --port flag specifies which port to run the server on, and then the --attach flag specifies whether to attach to the container.

Example usage:
gink run-image config.yaml --tag my-image:latest --port 8000 --attach true

gink deploy {config}
This command deploys the container to AWS, GCP, etc., and generates an API to work with. The {config} argument specifies the path to the configuration file.

Example usage:
gink deploy config.yaml

# Contributing

We welcome contributions to gitlink! If you find a bug, have a feature request or want to contribute code, please open an issue or a pull request on our GitHub repository.

# License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

# Contact
If you have any questions or feedback, please feel free to reach out to the project maintainer at nish@unstatiq.com. You can also open an issue on the GitHub repository if you encounter any problems or have suggestions for improvement.

Thank you for using gitlink!