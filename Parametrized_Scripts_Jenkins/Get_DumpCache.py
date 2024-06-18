import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket
import time
import datetime
import sys

def main():
    hostname = sys.argv[1]
    password = sys.argv[2]
    LH_name = sys.argv[3]
    LH_name = LH_name.split()
    global output_host
    today=datetime.datetime.now().strftime("%Y%m%d")
    output_host = output_host(hostname, password)
    local_path = "C:\\Users\\U6017127\\.jenkins\\workspace\\Get_Dumpcache\\"
    for lh in LH_name:
        download_dumpcache(hostname,password,lh,output_host,today,local_path)
  

def output_host(hostname, password):
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=password, port=22)
        stdin, stdout, stderr = ssh.exec_command(f"hostname")
        time.sleep(2)
        host = stdout.read()
        host = host.decode(encoding="utf-8")
        output_host = ''.join(c for c in host if c.isprintable())
        ftp = ssh.open_sftp()
        return output_host

# this function is to download the DumpCache and FidFilter files to your local machine#

def download_dumpcache(hostname,password,lh,output_host,today,local_path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=password,port=22)
        print("I am connected to download DumpCache file")

        stdin, stdout, stderr = ssh.exec_command(f"cd /data/che/bin ; pwd ; ./Commander -n linehandler -c 'dumpcache {lh}'")
        time.sleep(10)
        outp = stdout.readlines()
        print(outp)
        dumpcache_file = lh + "_" + today + ".csv"
        print(dumpcache_file)
        stdin, stdout, stderr = ssh.exec_command(f"find / -name " + dumpcache_file)
        time.sleep(2)
        config_ph = stdout.read()
        print(config_ph)
        config_ph = config_ph.decode(encoding="utf-8")
        config_ph = ''.join(c for c in config_ph if c.isprintable())
        print(config_ph)

        sftp_client = ssh.open_sftp()
        print("DumpCache file is downloading")
        sftp_client.get(config_ph, local_path + output_host + "_" + dumpcache_file)
#       sftp_client.get(config_path + dumpcache_file, "C:\PMAT\\x64\\" + dumpcache_file)
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