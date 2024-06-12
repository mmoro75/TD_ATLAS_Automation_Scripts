import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket
import time
import datetime
import sys

def main():
    hostname = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    LH_name = sys.argv[4]
    venue_name = sys.argv[5]
    config_path = "/data/Venues/" + venue_name + "/config/"
    local_path = sys.argv[6]
    today=datetime.datetime.now().strftime("%Y%m%d")
    dumpcache_file = LH_name + "_" + today + ".csv"
    download_dumpcache(hostname,username,password,LH_name,venue_name,config_path,local_path,dumpcache_file)




# this function is to download the DumpCache and FidFilter files to your local machine#

def download_dumpcache(hostname,username,password,LH_name,venue_name,config_path,local_path,dumpcache_file):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username=username,password=password,port=22)
        print("I am connected to download DumpCache file")

        stdin, stdout, stderr = ssh.exec_command(f"cd /data/che/bin ; pwd ; ./Commander -n linehandler -c 'dumpcache {LH_name}'")
        time.sleep(10)
        outp = stdout.readlines()

        sftp_client = ssh.open_sftp()
        print("DumpCache file is downloading")
        sftp_client.get(config_path + dumpcache_file, local_path + "\\" + dumpcache_file)
#       sftp_client.get(config_path + dumpcache_file, "C:\\Temp\\" + dumpcache_file)
        print("Dumpcache file - download completed")
        sftp_client.close()
        ssh.close

    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except TimeoutError:
        print("Host file not found make sure the server ip and local path provided are correct")
        quit()
    except FileNotFoundError:
        print("Host file not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(
            f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

main()