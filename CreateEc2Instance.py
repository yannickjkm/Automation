""" Lambda to launch Jenkins ec2-instance """
import boto3

REGION = 'eu-west-1' # region to launch instance.
AMI = 'ami-0fc970315c2d38f01'
INSTANCE_TYPE = 't2.micro' # instance type to launch.
KEY_NAME = 'muna3ec2'

EC2 = boto3.client('ec2', region_name=REGION)

def lambda_handler(event, context):
    """ Lambda handler taking [message] and creating a httpd instance with an echo. """
    #message = event[message]

    # bash script to run:
    #  - Install Jenkins
    #  - Reload systemctl daemon
    #  - set the system to shutdown the instance in 60 minutes.
    init_script = """#!/bin/bash
yum update -y
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
sudo yum upgrade
sudo yum install jenkins java-1.8.0-openjdk-devel
sudo systemctl daemon-reload
sudo systemctl start jenkins
sudo systemctl status jenkins
shutdown -P +60"""

    print("Running script:")
    print(init_script)

    instance = EC2.run_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        KeyName = KEY_NAME,
        MinCount=1, # required by boto, even though it's kinda obvious.
        MaxCount=1,
        InstanceInitiatedShutdownBehavior='terminate', # make shutdown in script terminate ec2
        UserData=init_script # file to run on instance init.
    )

    print("New instance created.")
    instance_id = instance['Instances'][0]['InstanceId']
    print(instance_id)

    return instance_id
