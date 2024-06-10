# Python script to use Portblocker on a remote server #

import tkinter
import paramiko
import re
import time
import datetime
import subprocess
from tkinter import ttk
import socket

from paramiko.ssh_exception import AuthenticationException


def status():
    my_progress.start()
    my_progress["value"] = 10
    window.update_idletasks()
    portbloker()


def portbloker():
    global today
    global eth1,eth2,eth3,eth4
    global path
    path = path_var.get()
    hostname = hostname_var.get()
    psw = psw_var.get()
    install_port_blocker(hostname,path,psw)
    server_eth = collect_NICs(hostname,path,psw)
    eth1="".join(server_eth.get('eth1')).strip("-")
    eth2="".join(server_eth.get('eth2')).strip("-")
    eth3="".join(server_eth.get('eth3')).strip("-")
    eth4="".join(server_eth.get('eth4')).strip("-")
    my_progress["value"] = 60
    window.update_idletasks()
    window.update()
    block_Ports(hostname, eth1, eth2, eth3, eth4, psw)
    cmd = f"del {path}\\hosts.txt"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    remove_portblocker(hostname,psw)
    return None


def install_port_blocker(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        installLab = tkinter.Label(window,text=f"ftp connection installing portblocker \n")
        installLab.grid(row=13, column=1)
        window.update()
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
                installLab1 = tkinter.Label(window, text=f"{line} \n")
                installLab1.grid(row=14, column=1)
                print(line)
        file_err = stderr.readlines()
        for err in file_err:
            if err in file_err:
                installLab2 = tkinter.Label(window, text=f"{err}\n Portblocker in not installed on your machine\n make sure 'portblocker.tar' file is in your working path")
                installLab2.grid(row=15, column=1)
                ssh.close()
        my_progress["value"] = 30
        window.update_idletasks()
        window.update()
        return None
    except socket.gaierror:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=22, column=1)
        raise
    except TimeoutError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=22, column=1)
        raise
    except FileNotFoundError:
        err = tkinter.Label(window,
                            text=f"PortBlocker file not found make sure the server ip and local path provided are correct\n \nPlease double check Poerbloker.tar file is located into provided direcotry\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=22, column=1)
        raise
    except ConnectionError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=22, column=1)
        raise
    except ConnectionRefusedError:
        err = tkinter.Label(window,
                            text=f"connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=22, column=1)
        raise
    except AuthenticationException:
        err = tkinter.Label(window,
                            text=f"Connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=22, column=1)
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.grid(row=22,column=1)
        window.update()
        raise
    finally:
        my_progress.stop()


def collect_NICs(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        NICLab = tkinter.Label(window, text=f"ftp colletting server NICs information \n")
        NICLab.grid(row=16, column=1)
        ftp.get("/etc/hosts", path+"\\hosts.txt")
        ftp.close()
        ssh.close()  # close connection
        # patt=r"\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}" # patt tofind ip addresses
        patt1 = r"\bDDNA-eth\d"
        patt2 = r"\bDDNB-eth\d"
        patt3 = r"\bEXCHIPA-eth\d"
        patt4 = r"\bEXCHIPB-eth\d"
        fo = open(path+"\\hosts.txt", "r")  # open hosts file in read mode
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
        NICLab1 = tkinter.Label(window, text=f"NIC Card for DDNA is {server_eth.get('eth1')}\n" 
                f"NIC Card for DDNB is {server_eth.get('eth2')}\n" f"NIC Card for EXCHA is {server_eth.get('eth3')}\n" f"NIC Card for EXCHB is {server_eth.get('eth4')}")
        NICLab1.grid(row=17, column=1)
        ssh.close()
        my_progress["value"] = 50
        window.update_idletasks()
        window.update()
        return server_eth
    except socket.gaierror:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=23, column=1)
        raise
    except TimeoutError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=23, column=1)
        raise
    except FileNotFoundError:
        err = tkinter.Label(window,
                            text=f"Host file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=23, column=1)
        raise
    except ConnectionError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=23, column=1)
        raise
    except ConnectionRefusedError:
        err = tkinter.Label(window,
                            text=f"connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=23, column=1)
        raise
    except AuthenticationException:
        err = tkinter.Label(window,
                            text=f"Connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=23, column=1)
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.grid(row=23, column=1)
        window.update()
        raise
    finally:
        my_progress.stop()


def block_Ports(hostname,eth1,eth2,eth3,eth4,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        a = a_var.get()
        b = b_var.get()
        c = c_var.get()
        try:
          wait= int(seconds_var.get())
        except ValueError:
            err = tkinter.Label(window, text=f"Please provide time in seconds Close this Window and restart")
            err.grid(row=27, column=1)
            my_progress.stop()
            raise
        seconds = str(wait)
######## Both NIC will be blocked ######


        if a == "DDN" and b == "B" and c == "BS":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r B -s B -d B -e B -t " + seconds + " -f 1 -a")
            PortLab = tkinter.Label(window, text=f"All DDN NIC cards traffic is blocked for {wait} seconds\n")
            PortLab.grid(row=19, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=20, column=1)
            ssh.close()
        elif a == "DDN" and b == "U" and c == "BS":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r U -s U -d B -e B -t " + seconds + " -f 1 -a")
            PortLab = tkinter.Label(window, text=f"All UPD Traffic is blocked on DDN NIC for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        elif a == "DDN" and b == "T" and c == "BS":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r T -s T -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN NIC for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All TCP Traffic is blocked on DDN NIC for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        elif a == "EXCH" and b == "B" and c == "BS":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r B -s B -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All Exchange NIC cards traffic are blocked for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All Exchange NIC cards traffic are blocked for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            window.update()
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        elif a == "EXCH" and b == "U" and c == "BS":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r U -s U -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All UPD Traffic is blocked on Exchange NIC for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "EXCH" and b == "T" and c == "BS":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r T -s T -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All TCP Traffic is blocked on Exchange NIC for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()

###### Only A NIC will be block #############

        elif a == "DDN" and b == "B" and c == "AN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1  + " -r B -d B -t " + seconds + " -f 1 -a")
            PortLab = tkinter.Label(window, text=f"A DDN NIC card traffic is blocked for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "DDN" and b == "U" and c == "AN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -r U -d B -t " + seconds + " -f 1 -a")
            PortLab = tkinter.Label(window, text=f"All UPD Traffic is blocked on DDN-A NIC for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "DDN" and b == "T" and c == "AN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN-A NIC for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All TCP Traffic is blocked on DDN-A NIC for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "EXCH" and b == "B" and c == "AN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -r B -d B -t " + seconds + " -f 1 -a")
            PortLab = tkinter.Label(window, text=f"All Exchange NIC-A cards traffic are blocked for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            window.update()
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "EXCH" and b == "U" and c == "AN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC-A for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All UPD Traffic is blocked on Exchange NIC-A for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "EXCH" and b == "T" and c == "AN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + "-r T -d B -t " + seconds + " -f 1 -a")
            PortLab = tkinter.Label(window, text=f"All TCP Traffic is blocked on Exchange NIC-A for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()

######## only B NIC will be blocked #######################


        elif a == "DDN" and b == "B" and c == "BN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"All traffic on DDN-B NIC card is blocked for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All traffic on DDN-B NIC card is blocked for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "DDN" and b == "U" and c =="BN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on DDN NIC-B for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All UPD Traffic is blocked on DDN NIC-B for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "DDN" and b == "T" and c =="BN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth2 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN NIC-B for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All TCP Traffic is blocked on DDN NIC-B for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "EXCH" and b == "B" and c =="BN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r B -d B -t " + seconds + " -f 1 -a")
            print(f"All traffic on Exchange NIC-B cards is blocked for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All traffic on Exchange NIC-B cards is blocked for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            window.update()
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channels are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "EXCH" and b== "U" and c =="BN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r U -d B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC-B for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All UPD Traffic is blocked on Exchange NIC-B for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()
        elif a == "EXCH" and b == "T" and c == "BN":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth4 + " -r T -d B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC-B for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All TCP Traffic is blocked on Exchange NIC-B for {wait} seconds\n")
            PortLab.grid(row=21, column=1)
            time.sleep(wait + 10)
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=22, column=1)
            ssh.close()

        else:
            PortLab3 = tkinter.Label(window, text=f"WRONG SELECTIONS\n Your current selection is:\n NIC Cards to Block={a}\n Protocol:{b},please check all the inforamtion are correct \n")
            PortLab3.grid(row=21, column=1)
            print(f"WRONG SELECTIONS\n Your current selection is:\n NIC Cards to Block={a}\n Protocol:{b}\n NIC:{c}\n Please check all the inforamtion are correct")
        ssh.close()
        my_progress["value"] = 70
        window.update_idletasks()
        return None
    except socket.gaierror:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=24, column=1)
        raise
    except TimeoutError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=24, column=1)
        raise
    except ConnectionError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=24, column=1)
        raise
    except ConnectionRefusedError:
        err = tkinter.Label(window,
                            text=f"connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=24, column=1)
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.grid(row=24,column=1)
        window.update()
        raise
    finally:
        my_progress.stop()

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
                UninLab = tkinter.Label(window, text=f" {line}\n")
                UninLab.grid(row=23, column=1)
                print(line)
        file_err = stderr.readlines()
        for err in file_err:
            if err in file_err:
                UninLab = tkinter.Label(window, text=f"{err}\n Portblocker has been uninstalled\n \n\n CLOSE THE WINDOW TO END THE SCRIPT")
                UninLab.grid(row=23, column=1)
              #  print(f"{err}\n Portblocker has been uninstalled")
                ssh.close()
        my_progress["value"] = 80
        window.update_idletasks()
        time.sleep(5)
        my_progress.stop()
        return None
    except socket.gaierror:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=25, column=1)
        raise
    except TimeoutError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=25, column=1)
        raise
    except FileNotFoundError:
        err = tkinter.Label(window,
                            text=f"PoerBlocker not installed found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=25, column=1)
        raise
    except ConnectionError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=25, column=1)
        raise
    except ConnectionRefusedError:
        err = tkinter.Label(window,
                            text=f"Connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=25, column=1)
    except AuthenticationException:
        err = tkinter.Label(window,
                            text=f"Connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.grid(row=25, column=1)
        raise

    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.grid(row=25,column=1)
        window.update()
        raise
    finally:
        my_progress.stop()


window=tkinter.Tk()
window.geometry("1200x800")
path_var=tkinter.StringVar()
hostname_var=tkinter.StringVar()
psw_var=tkinter.StringVar()
a_var=tkinter.StringVar()
b_var=tkinter.StringVar()
c_var=tkinter.StringVar()
seconds_var=tkinter.StringVar()
window.title("PortBlocker")
label=tkinter.Label(window,text="Portblocker Configurations: ")
label.grid(row=0,column=1)
label1=tkinter.Label(window,text="!!!WARNING: make sure 'portblocker.tar' is available in your working path!!!")
label1.grid(row=1,column=1)

getPathLable=tkinter.Label(window,text="Enter your path: ",font=('calibre', 10, 'normal'))
getPathLable.grid(row=2, column=0)
getPathEntry=tkinter.Entry(window, textvariable=path_var,width=30,font=('calibre', 10, 'normal'))
getPathEntry.grid(row=2, column=1)

getHostLabel=tkinter.Label(window,text="Enter your host ip: ",font=('calibre', 10, 'normal'))
getHostLabel.grid(row=3,column=0)
getHostEntry=tkinter.Entry(window, textvariable=hostname_var,width=20,font=('calibre', 10, 'normal'))
getHostEntry.grid(row=3,column=1)

gepswLabel=tkinter.Label(window,text="Enter password for your server: ",font=('calibre', 10, 'normal'))
gepswLabel.grid(row=4,column=0)
getpswEntry=tkinter.Entry(window, textvariable=psw_var,width=15,font=('calibre', 10, 'normal'))
getpswEntry.grid(row=4,column=1)

getTimeLabel=tkinter.Label(window,text="Enter port blocking time in seconds: ",font=('calibre', 10, 'normal'))
getTimeLabel.grid(row=5,column=0)
getTimeEntry=tkinter.Entry(window, textvariable=seconds_var,width=10,font=('calibre', 10, 'normal'))
getTimeEntry.grid(row=5,column=1)

c1 = tkinter.Checkbutton(window, text='Select Protocol UDP',variable=b_var, onvalue="U", offvalue="T")
c1.grid(row=7,column=1)
c1.deselect()
c2 = tkinter.Checkbutton(window, text='Select Protolcol TCP',variable=b_var, onvalue="T", offvalue="U")
c2.grid(row=7,column=2)
c2.deselect()

c3 = tkinter.Checkbutton(window, text='Both UDP and TCP',variable=b_var, onvalue="B", offvalue="U")
c3.grid(row=7,column=3)
c4 = tkinter.Checkbutton(window ,variable=c_var, onvalue="AN",text='NIC-A')
c4.grid(row=8,column=1)
c4.deselect()
c5 = tkinter.Checkbutton(window ,variable=c_var, onvalue="BN",text='NIC-B')
c5.grid(row=8,column=2)
c5.deselect()
c6 = tkinter.Checkbutton(window ,variable=c_var, onvalue="BS",text='All NIC')
c6.grid(row=8,column=3)
c6.select()
c7 = tkinter.Checkbutton(window, text='Select NIC to BLock EXCH',variable=a_var, onvalue="EXCH", offvalue="DDN")
c7.grid(row=9,column=1)
c8 = tkinter.Checkbutton(window ,variable=a_var, onvalue="DDN", offvalue="EXCH",text='Select NIC to block DDN')
c8.grid(row=9,column=2)
c8.deselect()

executeButton=tkinter.Button(window,text="Execute",command=status)
executeButton.grid(row=10,column=1)
my_progress = ttk.Progressbar(window, orient="horizontal", length="300", mode="determinate")
my_progress.grid(row=11,column=1)


window.mainloop()


