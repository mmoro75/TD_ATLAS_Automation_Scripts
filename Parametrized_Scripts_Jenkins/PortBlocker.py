# this scrip will allow you to use portblocker on remote server

import paramiko
import re
import time
import subprocess
import socket
from paramiko.ssh_exception import AuthenticationException
import sys


def portbloker():
    global today
    global eth1,eth2,eth3,eth4
    global path
    print("!!!WARNING: make sure 'portblocker.tar' is available in your working path!!! ")
    path = "C:\\Users\\U6017127\\.jenkins\\workspace\\PortBlocker_Tool\\"
    hostname = sys.argv[1]
    psw = sys.argv[2]
    install_port_blocker(hostname,path,psw)
    server_eth = collect_NICs(hostname,path,psw)
    eth1="".join(server_eth.get('eth1')).strip("-")
    eth2="".join(server_eth.get('eth2')).strip("-")
    eth3="".join(server_eth.get('eth3')).strip("-")
    eth4="".join(server_eth.get('eth4')).strip("-")
    block_Ports(hostname, eth1, eth2, eth3, eth4 ,psw)
    cmd = "del C:\\Users\\u6017127\\Documents\\Eikon\\Project\\TestPython\\hosts.txt"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    remove_portblocker(hostname,psw)
    return None


def install_port_blocker(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print("ftp connection installing portblocker")
        print(path + "\\portblocker.tar")
        ftp.put(path+"\\portblocker.tar", "/root/portblocker.tar")
        time.sleep(15)
        ftp.close()
        print("Upload file completed ")
        stdin, stdout, stderr = ssh.exec_command("tar -vxf portblocker.tar")
        print("portblocker.tar unzipped checking version:")
        stdin, stdout, stderr = ssh.exec_command("chmod a+x portblocker")
        stdin, stdout, stderr = ssh.exec_command("chmod a+x PortBlocker_Eng.ko")
        stdin, stdout, stderr = ssh.exec_command("./portblocker -version")

        file_out = stdout.readlines()
        for line in file_out:
            if line in file_out:
                print(line)
        file_err = stderr.readlines()
        for err in file_err:
            if err in file_err:
                print(
                    f"{err}\n Portblocker in not installed on your machine\n make sure 'portblocker.tar' file is in your working path")
                ssh.close()
        return None
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except TimeoutError:
        print("PoertBlocker file not found make sure the server ip and local path provided are correct\n Plese double check Portblocket.tar File is located in given Directory")
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
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def collect_NICs(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print("ftp colletting server NICs information")
        ftp.get("/etc/hosts", path+"\\hosts.txt")
        ftp.close()
        ssh.close()  # close connection
        # patt=r"\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}" # patt tofind ip addresses
        patt1 = r"\bDDNA-eth\d"
        patt2 = r"\bDDNB-eth\d"
        patt3 = r"\bEXCHIPA-eth\d"
        patt4 = r"\bEXCHIPB-eth\d"
        fo = open(path+"\\hosts.txt",
                  "r")  # open hosts file in read mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        server_eth = {"eth1": [], "eth2": [], "eth3": [], "eth4": []}
        for each_line in files_lines:  # loop into list created
            if re.findall(patt1, each_line):  # only print when you fine key word DDNA
                server_eth["eth1"].append(each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt2, each_line):
                server_eth["eth2"].append(each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt3, each_line):
                server_eth["eth3"].append(each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt4, each_line):
                server_eth["eth4"].append(each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
        fo.close()
        print(f"NIC Card for DDNA is {server_eth.get('eth1')}")
        print(f"NIC Card for DDNB is {server_eth.get('eth2')}")
        print(f"NIC Card for EXCHA is {server_eth.get('eth3')}")
        print(f"NIC Card for EXCHB is {server_eth.get('eth4')}")
        ssh.close()
        return server_eth
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
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def block_Ports(hostname,eth1,eth2,eth3,eth4,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        print("Connected to remote host")
        a = sys.argv[3] # input("Please provide NIC Card to block: DDN or EXCH?: ").upper()
        b = sys.argv[4] #("Please provide protocol you want to block UDP, TCP, BOTH: U,T,B: ").upper()
        c = sys.argv[5] #("Please specify which NIC card you want to block: A, B or All ").upper()
        try:
          wait=sys.argv[6]
          wait = int(wait)
        except ValueError:
            print("please provide time in seconds")
        seconds = str(wait)
        if a == "DDN" and b=="B" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r B -s B -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All DDN NIC cards traffic is blocked ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "DDN" and b== "U" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r U -s U -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on DDN NIC ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "DDN" and b == "T" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r T -s T -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN NIC")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "EXCH" and b == "B" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r B -s B -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All Exchange NIC cards traffic is blocked for")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "EXCH" and b== "U" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r U -s U -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")
        elif a == "EXCH" and b == "T" and c=="All":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r T -s T -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
            print("Portblocker stopped all the traffic is now restored")

###### Only A NIC will be block #############

        elif a == "DDN" and b == "B" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"A DDN NIC card traffic is blocked ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "DDN" and b == "U" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on DDN-A NIC ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "DDN" and b == "T" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN-A NIC ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "B" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"All Exchange NIC-A cards traffic are blocked")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "U" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC-A ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "T" and c == "A":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + "-r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC-A ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()

######## only B NIC will be blocked #######################

        elif a == "DDN" and b == "B" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"All traffic on DDN-B NIC card is blocked ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "DDN" and b == "U" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on DDN NIC-B ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "DDN" and b == "T" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN NIC-B ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "B" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"All traffic on Exchange NIC-B cards is blocked")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "U" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC-B")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()
        elif a == "EXCH" and b == "T" and c == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC-B ")
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            ssh.close()

        else:
            print(f"WRONG SELECTIONS\n Your current selection is:\n NIC Cards to Block={a}\n Protocol:{b},please check all the inforamtion are correct")
            block_Ports(hostname,eth1,eth2,eth3,eth4,psw)
        ssh.close()
        return None
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except TimeoutError:
        print("Host file not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def remove_portblocker(hostname,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        stdin, stdout, stderr = ssh.exec_command("rm portblocker.tar")
        stdin, stdout, stderr = ssh.exec_command("rm portblocker")
        stdin, stdout, stderr = ssh.exec_command("rm PortBlocker_Eng.ko")
        stdin, stdout, stderr = ssh.exec_command("./portblocker -version")

        file_out = stdout.readlines()
        for line in file_out:
            if line in file_out:
                print(line)
        file_err = stderr.readlines()
        for err in file_err:
            if err in file_err:
                print(f"{err}\n Portblocker has been uninstalled")
                ssh.close()
        return None
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except TimeoutError:
        print("Host file not found make sure the server ip and local path provided are correct")
        quit()
    except FileNotFoundError:
        print("PortBlocker is not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


portbloker()


if __name__=="__portblocker__":
    ErrorLogs()


