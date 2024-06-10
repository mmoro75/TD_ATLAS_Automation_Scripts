
import tkinter
from tkinter import ttk
import paramiko
import re
import time
import datetime
import subprocess
import socket

from paramiko.ssh_exception import AuthenticationException


def status():
    my_progress["value"] = 20
    get_pcap()
    window.update_idletasks()

def get_pcap():
    global filename
    global seconds
    global path
    today = datetime.datetime.now().strftime("%Y%m%d")
    filename = "DDNA-" + today + ".pcap"
    my_progress.start(10)
    window.update_idletasks()
    path = path_var.get()
    try:
      seconds=int(seconds_var.get())
    except ValueError:
        err = tkinter.Label(window,text=f"Please provide time in seconds and press Execute to continue")
        err.pack()
        my_progress.stop()
        raise
    hostname = hostname_var.get()
    psw = psw_var.get()
    if NIC_var.get() == "DDNA":
       eth_ddn = find_eth_ddna(hostname,path,psw)
       tcpdump_installation(hostname,psw)
       filename = "DDNA_Capture-" + today + ".pcap"
       collect_pcap_ddna(hostname, eth_ddn, filename, seconds, path,psw)
       Rm_file(hostname, filename, psw)
       my_progress["value"] = 100
       window.update_idletasks()
       window.update()

    elif NIC_var.get() == "EXCHA":
        eth_exch = find_eth_exch(hostname, path,psw)
        tcpdump_installation(hostname,psw)
        filename = "EXCHA_Capture-" + today + ".pcap"
        collect_pcap_exch(hostname,eth_exch,filename,seconds,path,psw)

        Rm_file(hostname, filename, psw)
        my_progress["value"] = 100
        window.update_idletasks()
        window.update()
    cmd = f"del {path}\\hosts.txt"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return None


def find_eth_ddna(hostname, path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        my_progress.step(20)
        window.update_idletasks()
        ddnalab = tkinter.Label(window, text=f"ftp connection estabilished collecting NIC card value for DDNA\n")
        ddnalab.pack()
        ftp.get("/etc/hosts", path + "\\hosts.txt")
        ftp.close()
        ssh.close()  # close connection
        patt = r"DDNA-eth\d"
        fo = open(path + "\\hosts.txt", "r")  # open hosts file in read mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        for each_line in files_lines:  # loop into list created
            if re.findall(patt, each_line):  # only print when you fine key word DDNA
                eth_ddn = (each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2]).strip("-")
                break
        fo.close()
        ddnalab2 = tkinter.Label(window, text=f"Reading completed: NIC for DDNA is {eth_ddn}\n")
        ddnalab2.pack()
        my_progress["value"] = 30
        window.update_idletasks()
        window.update()
        time.sleep(5)
        return str(eth_ddn)
    except socket.gaierror:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except TimeoutError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except FileNotFoundError:
        err = tkinter.Label(window,
                            text=f"Host file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except ConnectionError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except ConnectionRefusedError:
        err = tkinter.Label(window,
                            text=f"connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except AuthenticationException:
        err = tkinter.Label(window,
                            text=f"Connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    finally:
        my_progress.stop()



def find_eth_exch(hostname, path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        my_progress.step(20)
        window.update_idletasks()
        ddnalab = tkinter.Label(window, text=f"ftp connection estabilished collecting NIC card value for EXCHA\n")
        ddnalab.pack()
        ftp.get("/etc/hosts", path + "\\hosts.txt")
        ftp.close()
        ssh.close()  # close connection
        patt = r"EXCHIPA-eth\d"
        fo = open(path + "\\hosts.txt", "r")  # open hosts file in read mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        for each_line in files_lines:  # loop into list created
            if re.findall(patt, each_line):  # only print when you fine key word DDNA
                eth_exch = (each_line[-6] + each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2]).strip("-")
                break
        fo.close()
        ddnalab2 = tkinter.Label(window, text=f"Reading completed: NIC for EXCHA is {eth_exch}\n")
        ddnalab2.pack()
        my_progress["value"] = 30
        window.update_idletasks()
        window.update()
        time.sleep(5)
        return str(eth_exch)
    except socket.gaierror:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except TimeoutError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except FileNotFoundError:
        err = tkinter.Label(window,
                            text=f"Host file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except ConnectionError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except ConnectionRefusedError:
        err = tkinter.Label(window,
                            text=f"connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except AuthenticationException:
        err = tkinter.Label(window,
                            text=f"Connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    finally:
        my_progress.stop()



def tcpdump_installation(hostname,psw):
   try:
       ssh = paramiko.SSHClient()  # create ssh client
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       ssh.connect(hostname=hostname, username="root", password=psw, port=22)
       tcpdumpLab = tkinter.Label(window, text=f"Checking tcpdump version installed on remote server\n")
       tcpdumpLab.pack()
       stdin, stdout, stderr = ssh.exec_command("tcpdump --help")
       file_lines = stderr.readlines()
       patt = r"\btcpdump version\b"
       for line in file_lines:
         if re.findall(patt, line):
            line
            break
         else:
            line = ""

       if bool(line) == True:
           tcpdumpLab = tkinter.Label(window, text=f"The version installed is: {line}\n")
           tcpdumpLab.pack()
       else:
         tcpdumpLab2 = tkinter.Label(window, text=f"tcpdump not installed on your machine installing now\n")
         tcpdumpLab2.pack()
         window.update()
         stdin, stdout, stderr = ssh.exec_command("yum -y install tcpdump")
         time.sleep(20)
         window.update()
         tcpdumpLab3 = tkinter.Label(window, text=f"Installation completed\n")
         tcpdumpLab3.pack()
         window.update()
         stdin, stdout, stderr = ssh.exec_command("tcpdump --help")
         file_lines = stderr.readlines()
         patt = r"\btcpdump version\b"
         for line in file_lines:
             if re.findall(patt, line):
                 line
                 break
             else:
                 line = ""
         if bool(line) == True:
            tcpdumpLab = tkinter.Label(window, text=f"The version installed is: {line}\n")
            tcpdumpLab.pack()
            ssh.close()
         my_progress["value"] = 40
         window.update_idletasks()
         window.update()
         return None
   except Exception as e:
       err = tkinter.Label(window, text=f"{e}\n")
       err.pack()
       window.update()
   finally:
       my_progress.stop()


def collect_pcap_ddna(hostname,eth_ddn,filename,seconds,path,psw):
   try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        stdin, stdout, stderr = ssh.exec_command(f"tcpdump -i  {eth_ddn}  port  7777 -w {filename}")
    #    pcapLab = tkinter.Label(window, text=f"Capturing {filename}\n")
    #    pcapLab.pack()
        pcapLab = tkinter.Label(window, text=f"Please wait whilst capturing pcap file on DDNA\n")
        pcapLab.pack()
        my_progress["value"] = 50
        window.update_idletasks()
        window.update()
        time.sleep(seconds)
        stdin, stdout, stderr = ssh.exec_command("pkill -f tcpdump")
        pcapLab2 = tkinter.Label(window, text=f"{filename} capture completed\n")
        pcapLab2.pack()
        my_progress["value"] = 60
        window.update_idletasks()
        window.update()
        ftp = ssh.open_sftp()
        pcapLab3 = tkinter.Label(window, text=f"ftp connection established downloading {filename}\n")
        pcapLab3.pack()
        my_progress["value"] = 80
        window.update_idletasks()
        window.update()
        ftp.get(filename,path+"\\"+filename)
        ftp.close()
        ssh.close()  # close connection
        pcapLab5 = tkinter.Label(window, text=f"Download completed, you can find your {filename} at {path}\n ")
        pcapLab5.pack()
        cmd = f"del {path}+\\hosts.txt"
        sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        my_progress["value"] = 90
        window.update_idletasks()
        time.sleep(5)
        my_progress.stop()
        return None
   except FileNotFoundError:
       err = tkinter.Label(window,
                           text=f"Pcap file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
       err.pack()
       raise
   except Exception as e:
       err = tkinter.Label(window, text=f"{e}\n")
       err.pack()
       window.update()
   finally:
       my_progress.stop()

def collect_pcap_exch(hostname,eth_exch,filename,seconds,path,psw):
   try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        stdin, stdout, stderr = ssh.exec_command(f"tcpdump -i  {eth_exch} -w {filename}")
        pcapLab = tkinter.Label(window, text=f"Please wait whilst capturing pcap file on EXCHA\n")
        pcapLab.pack()
        my_progress["value"] = 50
        window.update_idletasks()
        window.update()
        time.sleep(seconds)
        stdin, stdout, stderr = ssh.exec_command("pkill -f tcpdump")
        pcapLab2 = tkinter.Label(window, text=f"{filename} capture completed\n")
        pcapLab2.pack()
        my_progress["value"] = 60
        window.update_idletasks()
        window.update()
        ftp = ssh.open_sftp()
        pcapLab3 = tkinter.Label(window, text=f"ftp connection established downloading {filename}\n")
        pcapLab3.pack()
        my_progress["value"] = 80
        window.update_idletasks()
        window.update()
        ftp.get(filename,path+"\\"+filename)
        ftp.close()
        ssh.close()  # close connection
        pcapLab5 = tkinter.Label(window, text=f"Download completed, you can find your {filename} at {path}\n \n")
        pcapLab5.pack()
        cmd = f"del {path}+\\hosts.txt"
        sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        my_progress["value"] = 90
        window.update_idletasks()
        time.sleep(5)
        my_progress.stop()
        return None
   except FileNotFoundError:
       err = tkinter.Label(window,
                           text=f"Pcap file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
       err.pack()
       raise
   except Exception as e:
       err = tkinter.Label(window, text=f"{e}\n")
       err.pack()
       window.update()
   finally:
       my_progress.stop()

def Rm_file(hostname, filename, psw):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username="root", password=psw, port=22)
    stdin, stdout, stderr = ssh.exec_command(f"rm -- {filename}")
    pcapLab = tkinter.Label(window, text=f"{filename} Deleted from remtoe server \n \n \nCLOSE THE WINDOW TO END THE SCRIPT")
    pcapLab.pack()
    ssh.close()
    return None


window=tkinter.Tk()
window.geometry("900x800")
path_var=tkinter.StringVar()
hostname_var=tkinter.StringVar()
psw_var=tkinter.StringVar()
seconds_var=tkinter.StringVar()
NIC_var=tkinter.StringVar()
window.title("DDNA PCAP CAPTURE")
label=tkinter.Label(window,text="Pcap Files Capture")
label.pack()

getPathLable=tkinter.Label(window,text="Enter your local path: ",font=('calibre', 10, 'normal'))
getPathLable.pack()
getPathEntry=tkinter.Entry(window, textvariable=path_var,width=50,font=('calibre', 10, 'normal'))
getPathEntry.pack()

getHostLabel=tkinter.Label(window,text="Enter your host ip: ",font=('calibre', 10, 'normal'))
getHostLabel.pack()
getHostEntry=tkinter.Entry(window, textvariable=hostname_var,width=15,font=('calibre', 10, 'normal'))
getHostEntry.pack()

getpsw=tkinter.Label(window,text="Enter password for your server: ",font=('calibre', 10, 'normal'))
getpsw.pack()
getpsw=tkinter.Entry(window, textvariable=psw_var,width=15,font=('calibre', 10, 'normal'))
getpsw.pack()


getTimeLabel=tkinter.Label(window,text="Enter pcap duration in seconds: ",font=('calibre', 10, 'normal'))
getTimeLabel.pack()
getTimeLabel=tkinter.Entry(window, textvariable=seconds_var,width=15,font=('calibre', 10, 'normal'))
getTimeLabel.pack()

getDDNALabel=tkinter.Checkbutton(window, variable=NIC_var,onvalue="DDNA", offvalue="EXCHA",text="DDNA NIC:")
getDDNALabel.select()
getDDNALabel.pack()

getEXCHALabel=tkinter.Checkbutton(window, variable=NIC_var,onvalue="EXCHA", offvalue="DDNA",text="EXCH-A -NIC :")
getEXCHALabel.deselect()
getEXCHALabel.pack()

my_progress = ttk.Progressbar(window, orient="horizontal", length="300", mode="determinate")
my_progress.pack(pady=20)



executeButton=tkinter.Button(window,text="Execute",command=status)
executeButton.pack()

window.mainloop()

