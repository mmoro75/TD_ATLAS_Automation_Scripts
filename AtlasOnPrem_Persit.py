import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException
import socket
import os

print("WARNING: Please make sure PMAT is installed into your local machine at: C:\\PMAT\\")

def main():
    hostname = input("Provide server IP: ")
    password = input("Provide password: ")
 #   ric_list = input('Enter List of RICs separated by space: ').split()
    lh_name = input("Provide LH name: ")

    upload_and_run_script(hostname, password, lh_name)

    config_path = f"/tmp/"
    persist_file = f"{lh_name}_persist.txt"

    if download_persist(hostname, password, config_path, persist_file):
        check_persist(ric_list, persist_file)
        delete_txt_files(hostname, password, config_path)

def upload_and_run_script(hostname, password, lh_name):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {hostname}...")
        ssh.connect(hostname=hostname, username="root", password=password, port=22)

        sftp_client = ssh.open_sftp()
        local_script_path = "run_persist_viewer.sh"
        remote_script_path = f"/tmp/run_persist_viewer.sh"
        
        print(f"Uploading {local_script_path} to {remote_script_path}...")
        sftp_client.put(local_script_path, remote_script_path)
        sftp_client.chmod(remote_script_path, 0o755)

        command = f"/tmp/run_persist_viewer.sh {lh_name}"
        command2 = f"chmod +x /tmp/persist_viewer.sh"
        command3 = f"sudo chmod 775 /tmp/run_persist_viewer.sh"
        print(f"Giving Permission: {command2}")
        ssh.exec_command(command2)
        ssh.exec_command(command3)
        print(f"Running command: {command}")
        stdin, stdout, stderr = ssh.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()  # Wait for command to complete

        if exit_status == 0:
            print("Shell script executed successfully.")
            print(f"Output: {stdout.read().decode()}")
        else:
            print(f"Shell script failed with exit status {exit_status}.")
            print(f"Errors: {stderr.read().decode()}")
            return False

        sftp_client.close()
        ssh.close()
        return True

    except (socket.gaierror, TimeoutError, FileNotFoundError, ConnectionError, ConnectionRefusedError, AuthenticationException, SSHException) as e:
        print(f"Error during SSH operation: {e}")
        return False

def download_persist(hostname, password, config_path, persist_file):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {hostname} for file download...")
        ssh.connect(hostname=hostname, username="root", password=password, port=22)

        sftp_client = ssh.open_sftp()
        remote_file_path = config_path + persist_file
        local_file_path = f"C:\\PMAT\\x64\\{persist_file}"

        print(f"Checking if the remote file {remote_file_path} exists...")
        try:
            sftp_client.stat(remote_file_path)
            print(f"File {remote_file_path} exists. Proceeding with download.")
        except FileNotFoundError:
            print(f"File {remote_file_path} does not exist.")
            sftp_client.close()
            ssh.close()
            return False

        print(f"Downloading file {persist_file} from {remote_file_path} to {local_file_path}")
        sftp_client.get(remote_file_path, local_file_path)
        print(f"Download completed. Find the file {persist_file} at C:\\PMAT\\x64")
       
        sftp_client.close()
        ssh.close()
        return True

    except (socket.gaierror, TimeoutError, FileNotFoundError, ConnectionError, ConnectionRefusedError, AuthenticationException, SSHException) as e:
        print(f"Error during SFTP operation: {e}")
        return False

def delete_txt_files(hostname, password, config_path):
    ssh = paramiko.SSHClient()  # create ssh client
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(hostname=hostname, username="root", password=password, port=22)
        
        stdin, stdout, stderr = ssh.exec_command(f"rm {config_path}*.txt")
        stdout.channel.recv_exit_status()  # Ensure command execution is complete
        
        print("The persist  file in the remote /tmp directory has been removed correctly")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        ssh.close()
        
    return None

def check_persist(ric_list, persist_file):
    try:
        os.chdir("C:\\PMAT\\x64")

        for r in ric_list:
            os.system(f"PMAT dump --dll schema_V9.dll --db {persist_file} --ric {r} > {r}.txt")
            filename = f"C:\\PMAT\\x64\\{r}.txt"
            os.startfile(filename)

    except FileNotFoundError:
        print(f"File not found. Make sure {persist_file} file to analyze is downloaded at C:\\PMAT\\x64")
        quit()
    except Exception as e:
        print(e)
        quit()

if __name__ == "__main__":
    main()
