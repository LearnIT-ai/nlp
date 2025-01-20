#!/usr/bin/python
import subprocess
import sys
import os


def start_instance():
    print('Starting EC2 instance...')
    command = [
        "aws", "ec2", "run-instances", 
        "--image-id", "ami-053b0d53c279acc90", 
        "--instance-type", "t2.micro", 
        "--key-name", "DevOpsKeyTest", 
        "--security-group-ids", "sg-0fe206434aba106f4", 
        "--subnet-id", "subnet-04d16a985f4ad7c13", 
        "--user-data", "file://./userdata",
        "--region", "us-east-1",
        "--iam-instance-profile", "Name=ec2-default-profile",
        "--query", "Instances[0].InstanceId",
        "--output", "text"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print('Instance is running! Instance ID:', result.stdout.strip())
        with open("instance.txt", "w") as f:
            f.write(result.stdout.strip())
    else:
        print('Failed to start instance:', result.stderr)


def log_in():
    print("Choose login method:")
    print("1. SSH")
    print("2. Session Manager")
    method = input("Enter your choice (1/2): ").strip()

    if method == "1":
        ec2_ip = input("Enter EC2 IP address: ").strip()
        command = [
            "ssh", "-i", "~/.ssh/DevOpsKeyTest.pem", f"ubuntu@{ec2_ip}"
        ]
        try:
            subprocess.run(command, check=True)
            print("SSH connection was successful.")
        except subprocess.CalledProcessError as e:
            print("Could not connect due to SSH error:", e)
    elif method == "2":
        instance_id = read_instance_id()
        if not instance_id:
            print("Instance ID not found. Start an instance first.")
            return
        command = [
            "aws", "ssm", "start-session",
            "--target", instance_id
        ]
        try:
            subprocess.run(command, check=True)
            print("Session Manager connection was successful.")
        except subprocess.CalledProcessError as e:
            print("Could not connect via Session Manager:", e)
    else:
        print("Invalid choice. Please select 1 for SSH or 2 for Session Manager.")


def terminate_instance():
    inst_id_file = 'instance.txt'
    if os.path.isfile(inst_id_file):
        with open(inst_id_file, 'r') as f:
            inst_id = f.read().strip()
        print('Terminating instance with ID:', inst_id)
        command = [
            "aws", "ec2",
            "terminate-instances",
            "--instance-ids", inst_id
        ]
        subprocess.run(command, capture_output=True, text=True)
        os.remove(inst_id_file)
        print('Instance terminated!')
    else:
        print('File with instance ID not found. You need to start an instance first.')


def read_instance_id():
    """Read the instance ID from the file."""
    inst_id_file = 'instance.txt'
    if os.path.isfile(inst_id_file):
        with open(inst_id_file, 'r') as f:
            return f.read().strip()
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py {start|terminate|login}")
        sys.exit(1)
    if sys.argv[1] == "start":
        start_instance()
    elif sys.argv[1] == "terminate":
        terminate_instance()
    elif sys.argv[1] == "login":
        log_in()
    else:
        print("Invalid command. Use 'start', 'terminate', or 'login'.")


if __name__ == "__main__":
    main()
