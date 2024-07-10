"""
This script allows the user to download the PERSIT file from a desired venue and check if the given RIC is persisted
both for MARKET_PRICE , MARKET_BY_PRICE or MARKET_BY_ORDER
"""
import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket
import os
import sys
import time

print("WARNING: Please make sure PMAT is installed into your local machine at: C:\PMAT\"")

def main():
    hostname=sys.argv[1]
    password=sys.argv[2]
    ric_list = sys.argv[3]
    ric_list = ric_list.split()
    Lh_name=sys.argv[4]
    choice = sys.argv[5]
    if choice == "DAT":
        persist_file = "PERSIST_" + Lh_name +".DAT"
    else:
        persist_file = "PERSIST_" + Lh_name + ".DAT.LOADED"
    download_Persist(hostname,password,persist_file)
    check_persist(ric_list,persist_file)

# this function is to download the PMAT file to your local machine#

def download_Persist(hostname,password,persist_file):

    try:

        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=password,port=22)

        stdin, stdout, stderr = ssh.exec_command(f"find / -name " + persist_file)
        time.sleep(2)
        config_ph = stdout.read()
        print(config_ph)
        config_ph = config_ph.decode(encoding="utf-8")
        config_ph = ''.join(c for c in config_ph if c.isprintable())  ### THIS IS WORKING
        print(config_ph)

        sftp_client = ssh.open_sftp()
        print(f"File {persist_file} is downloading")
        sftp_client.get(config_ph, "C:\PMAT\\x64\\" + persist_file)
        print(f"Download completed find file {persist_file} at C:\PMAT\\x64")
        sftp_client.close()
        ssh.close
        return None

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
        print("Connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def check_persist(ric_list,persist_file):
    try:
        for r in ric_list:
            persist_file
            os.chdir("C:\\PMAT\\x64")

            os.system(f"PMAT dump --dll schema_V9.dll --db {persist_file} --ric {r} --MARKET_PRICE> {r}")
            filename = f"C:\\PMAT\\x64\\{r}"
            os.system(f"copy {filename} C:\\Users\\U6017127\\.jenkins\\workspace\\RICs_Persist_File")

    except FileNotFoundError:
        print(f"File not found make sure {persist_file} file to analyze is downloaded at C:\\Users\\U6017127\\.jenkins\\workspace\\RICs_Persist_File")
        quit()
    except Exception as e:
        print(e)
        quit()

main()