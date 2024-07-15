import paramiko
import os

def main():
    # Get user input
    host_ip = input("Enter the host IP address: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    docker_name = input("Enter the Docker container name: ")
    file_to_find = input("Enter the file to find inside the Docker container (or type 'custom' to specify a custom file name): ")

    if file_to_find.lower() == 'custom':
        custom_file_to_find = input("Enter the custom file name to find: ")
    else:
        custom_file_to_find = file_to_find

    try:
        ssh = connect_ssh(host_ip, username, password)
        hostname = get_hostname(ssh)
        download_path = os.path.join("c:\\tmp\\", f"{hostname}-{docker_name}")
        
        # Verify Docker container access
        verify_docker_access(ssh, docker_name)
        
        file_path = find_file_in_docker(ssh, docker_name, custom_file_to_find)
        if file_path:
            print(f"File found: {file_path}")
            download_file_from_docker(ssh, docker_name, file_path, download_path)
        else:
            print(f"File not found or an error occurred.")
        ssh.close()
    except Exception as e:
        print(f"An error occurred: {e}")

def connect_ssh(host_ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host_ip, username=username, password=password)
    return ssh

def get_hostname(ssh):
    stdin, stdout, stderr = ssh.exec_command("hostname")
    return stdout.read().decode('utf-8').strip()

def verify_docker_access(ssh, docker_name):
    command = f"docker ps -f name={docker_name}"
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode('utf-8').strip()
    if not result:
        raise Exception(f"Cannot access Docker container {docker_name}. Please check the container name and permissions.")
    print(f"Docker container {docker_name} is accessible.")

def find_file_in_docker(ssh, docker_name, file_to_find):
    # Find the file in the Docker container
    command = f"docker exec {docker_name} find / -name {file_to_find} 2>/dev/null"
    print(f"Running command: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode('utf-8').strip()
    error = stderr.read().decode('utf-8').strip()
    if error:
        print(f"Error output: {error}")
    if result:
        return result.split('\n')[0]  # Return the first match
    return None

def download_file_from_docker(ssh, docker_name, file_path, local_path):
    sftp = ssh.open_sftp()
    try:
        docker_file_path = f"/{file_path.lstrip('/')}"
        temp_file_path = f"/tmp/{os.path.basename(file_path)}"
        
        # Copy the file from the Docker container to the host's /tmp directory
        copy_command = f"docker cp {docker_name}:{docker_file_path} {temp_file_path}"
        print(f"Running command: {copy_command}")
        stdin, stdout, stderr = ssh.exec_command(copy_command)
        exit_status = stdin.channel.recv_exit_status()
        if exit_status != 0:
            error_message = stderr.read().decode('utf-8').strip()
            raise Exception(f"Error copying file from Docker container: {error_message}")
        
        # Ensure the local path exists
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        
        # Construct the full local file path
        local_file_path = os.path.join(local_path, os.path.basename(file_path))
        
        # Download the file from the host's /tmp directory to the local machine
        sftp.get(temp_file_path, local_file_path)
        
        # Clean up the temporary file on the host
        ssh.exec_command(f"rm {temp_file_path}")
        
        print(f"File downloaded to: {local_file_path}")
        
        # Create the command file to copy back to the Docker container
        create_copy_back_command(local_file_path, docker_name, docker_file_path)
        
    except Exception as e:
        print(f"Failed to download file: {e}")
    finally:
        sftp.close()

def create_copy_back_command(local_file_path, docker_name, docker_file_path):
    file_name_without_ext = os.path.splitext(os.path.basename(local_file_path))[0]
    file_name_upper = file_name_without_ext.upper()
    command_file_path = os.path.join(os.path.dirname(local_file_path), f"{file_name_upper}_copy_back-Instructions.txt")
    command = f"docker cp {os.path.basename(local_file_path)} {docker_name}:{docker_file_path}"
    instructions = (
        f"1. Copy the file {os.path.basename(local_file_path)} into the /tmp/ directory.\n"
        f"2. Using Putty, connect to the host server, cd to the /tmp/ directory, and run the following command:\n"
        f"3. {command}\n"
    )
    with open(command_file_path, 'w') as f:
        f.write(instructions)
    print(f"Copy back command saved to: {command_file_path}")

if __name__ == "__main__":
    main()
