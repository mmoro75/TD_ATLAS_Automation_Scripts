"""
This script allows the user to create and download the DumpCache file for a desired venue and to get from it the most
active RIC for every CID and Domain.
"""
import paramiko
from paramiko.ssh_exception import AuthenticationException
import paramiko.sftp
import socket
import time
import datetime
import pandas as pd
import re
import csv
import os
import sys

def main():
    global output_host
    hostname = sys.argv[1]
    password = sys.argv[2]
    LH_name = sys.argv[3]
    LH_name = LH_name.split()
    type = sys.argv[4]
    output_host = output_host(hostname, password)
    local_path = f"C:\\Users\\U6017127\\.jenkins\\workspace\\Get_Dumpcache\\{output_host}\\"
    os.makedirs(local_path,exist_ok=True)
    today = datetime.datetime.now().strftime("%Y%m%d")
    fo4 = open(local_path + "Sample_RICs.txt", "w")
    fo4.write(f"Sample RICs for:\n\n")
    fo4.close()

    for LH in LH_name:
        if type == "ATLAS":
            dumpcache_file = download_dumpcache_atlas(hostname, password, LH, local_path, today, output_host)
            CID = find_CID_dumpcache(local_path, dumpcache_file)
            sample_RIC_per_CID(type, local_path, dumpcache_file, CID, LH)
        elif type == "TD":
            dumpcache_file = download_dumpcache(hostname, password, LH, local_path, today ,output_host)
            CID = find_CID_dumpcache(local_path, dumpcache_file)
            sample_RIC_per_CID(type, local_path, dumpcache_file, CID, LH)
    os.remove(local_path + "new_dump_file.csv")

def output_host(hostname, password):
    ssh = paramiko.SSHClient()  # create ssh client
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username="root", password=password, port=22)
    stdin, stdout, stderr = ssh.exec_command(f"hostname")
    time.sleep(2)
    host = stdout.read()
    host = host.decode(encoding="utf-8")
    output_host = ''.join(c for c in host if c.isprintable())
    return output_host


# this function is to download the DumpCache and FidFilter files to your local machine#
# this function is to download the DumpCache and FidFilter files to your local machine#
def download_dumpcache(hostname, password, LH, local_path, today ,output_host):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=password, port=22)
        print("I am connected to download DumpCache file")
        stdin, stdout, stderr = ssh.exec_command(f"cd /data/che/bin ; pwd ; ./Commander -n linehandler -c 'dumpcache {LH}'")
        time.sleep(10)
        outp = stdout.readlines()
        dumpcache_file = LH + "_" + today + ".csv"
        print(dumpcache_file)
        stdin, stdout, stderr = ssh.exec_command(f"find / -name " + dumpcache_file)
        time.sleep(2)
        config_ph = stdout.read()
        config_ph = config_ph.decode(encoding="utf-8")
        config_ph = ''.join(c for c in config_ph if c.isprintable())
        sftp_client = ssh.open_sftp()
        print("DumpCache file is downloading")
        sftp_client.get(config_ph, local_path + output_host + "_" + dumpcache_file)
        dumpcache_file = output_host + "_" + dumpcache_file
        print("Dumpcache file - download completed")
        sftp_client.close()
        ssh.close
        return dumpcache_file


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
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

def download_dumpcache_atlas(hostname, password, LH, local_path, today, output_host):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=password, port=22)
        print("I am connected to download DumpCache file")
        stdin, stdout, stderr = ssh.exec_command(f"cd .. ; cd tmp ; commander.sh {LH} cache dump > {LH}_{today}.csv")
        time.sleep(10)
        outp = stdout.readlines()
        dumpcache_file = LH + "_" + today + ".csv"
        print(dumpcache_file)
        sftp_client = ssh.open_sftp()
        print("DumpCache file is downloading")
        path = "/tmp/" + dumpcache_file
        sftp_client.get(path, local_path + output_host + "_" + dumpcache_file)
        dumpcache_file = output_host + "_" + dumpcache_file
        print("Dumpcache file - download completed")
        sftp_client.close()
        ssh.close
        return dumpcache_file

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
        print(f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

def find_CID_dumpcache(local_path, dumpcache_file):
    file = local_path + dumpcache_file
    def getColumn(name):
        return [row[name] for row in data]

    with open(file, newline='') as new_csv_file:
        new_csv_file = csv.DictReader(new_csv_file)
        data = list(new_csv_file)
    CID_all = []

    for u in getColumn('CONTEXT_ID'):
        CID_all.append(u)

    while ("" in CID_all):
        CID_all.remove("")
    CID = list(set((CID_all)))
    return CID


def sample_RIC_per_CID(type, local_path, dumpcache_file, CID, LH):
    data = pd.read_csv(local_path + dumpcache_file)
    if type == "TD":
        columns_to_drop = ['ITEM_ID', 'LAST_UPDATED', 'LAST_ACTIVITY', 'TIME_CREATED', 'VEHICLEID']
    elif type == "ATLAS":
        columns_to_drop = ['VEHICLE_ID', 'LAST_UPDATED', 'LAST_ACTIVITY', 'TIME_CREATED', 'ISSUTYPE']
    data.drop(columns=columns_to_drop, inplace=True, axis=1)
    data.to_csv(local_path + 'new_dump_file.csv', index=False)
    new_dump_file = 'new_dump_file.csv'
    fo = open(local_path + new_dump_file, "r")
    content = fo.readlines()
    fo4 = open(local_path + "Sample_RICs.txt", "a")
    fo4.write(f"*** {LH} ***\n")
    for c in CID:
        fo1 = open(local_path + "CID_" + c + "_RIC_LIST.csv", "w")
        fo1.write(list(content)[0])
        patt1 = r"\b" + c + "\\b"
        for line in content:
            if re.findall(patt1, line):
                fo1.writelines(line)
        fo1.close()
        data = pd.read_csv(local_path + "CID_" + c + "_RIC_LIST.csv")
        CURR_SEQ_NUM = data["CURR_SEQ_NUM"].tolist()
        CURR_SEQ_NUM.sort()
        highest = CURR_SEQ_NUM[-1]
        highest = str(highest)
        fo2 = open(local_path + "CID_" + c + "_RIC_LIST.csv", "r")
        content_highest = fo2.readlines()
        fo3 = open(local_path + c + "_Sample_RIC.csv", "w", newline="")
        fo3.write(list(content)[0])
        patt2 = r"\b" + highest + "\\b"
        for l in content_highest:
            if re.findall(patt2, l):
                fo3.writelines(l, )
        fo2.close()
        fo3.close()
        Sample_RIC = pd.read_csv(f"{local_path}{c}_Sample_RIC.csv")
        PUBLISH_KEY = Sample_RIC["PUBLISH_KEY"].tolist()
        DOMAIN = Sample_RIC["DOMAIN"].tolist()
        for K in PUBLISH_KEY:
            for D in DOMAIN:
                fo4.write(f"{D} - {c} - {K} \n")
                break
            break
        os.remove(local_path + "CID_" + c + "_RIC_LIST.csv")
        os.remove(local_path + c + "_Sample_RIC.csv")
        
    fo4.close()


main()
