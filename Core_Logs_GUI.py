import tkinter
import paramiko
import re
import datetime
import os
from os import listdir
from os import walk
import socket

from paramiko.ssh_exception import AuthenticationException


def CoreLogs():
    global today
    today=datetime.datetime.now().strftime("%Y%m%d")
    path=path_var.get()
    hostname=hostname_var.get()
    psw = psw_var.get()
    filesDownload(hostname,path,psw)
    FMSClientDownload(hostname,path,psw)
    SCWDownload(hostname,path,psw)
    files=fileList(path)
    Find_Exceptions(path,files,today)
    Find_Critical(path,files,today)
    output = tkinter.Label(window, text=f"Completed find your files at: {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
    output.pack()
    return None

def filesDownload(hostname,path,psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        Label = tkinter.Label(window, text=f"ftp connection established executing\n")
        Label.pack()
        window.update()
        apath = '/data/che'
        apattern = '"*.log"'
        rawcommand = 'find {path} -name {pattern}'
        command = rawcommand.format(path=apath, pattern=apattern)
        stdin, stdout, stderr = ssh.exec_command(command)
        filelist = stdout.read().splitlines()

        ftp = ssh.open_sftp()
        for afile in filelist:
            (head, filename) = os.path.split(afile)
            ftp.get(afile, path + "\\" + str(filename))

        ftp.close()
        ssh.close()  # close connection
        return None
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
                            text=f"file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
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
                            text=f"connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise


def FMSClientDownload(hostname,path,psw):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=psw,port=22)
        ftp=ssh.open_sftp()
        ftp.get("/data/FMSClient/FMSClient.log",path+"\\FMSClient.log")
        ftp.close()
        ssh.close() # close connection
        return None
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
                            text=f"FMSClient file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
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
                            text=f"connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise

def SCWDownload(hostname,path,psw):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=psw,port=22)
        ftp=ssh.open_sftp()
        window.update()
        todaysmf=ftp.get("/data/SCWatchdog/logs/SCWatchdog.log",path+"\\SCWatchdog.log")
        ftp.close()
        ssh.close() # close connection
        return None
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
                            text=f"SCW file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
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

def fileList(path):
    my_dir = path

    files = []
    for (dirpath, dirnames, filenames) in walk(my_dir):
        files.extend(filenames)
        window.update()
        return files

def Find_Critical(path,files,today):
    try:
        my_dir = path
        patt = r"\bCritical\b"
        for f in files:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\Critical-log-"+today+".txt", "a")
            fo1.write(f"\n CRITICAL ERRORS IN  {f}\n ")
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:  # loop into list crreated
                if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                    if each_line != "":
                        fo1.write(each_line)  # write line on errorlog file
        fo.close()
        fo1.close()
        return None

    except TimeoutError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except FileNotFoundError:
        err = tkinter.Label(window,
                            text=f"file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise

def Find_Exceptions(path,files,today):
    try:
        my_dir = path
        patt = r"\bException\b"
        for f in files:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\Exception_log-"+today+".txt", "a")
            fo1.write(f"\n EXCEPTION ERRORS IN  {f}\n \n")
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:  # loop into list crreated
                if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                    if each_line != "":
                        fo1.write(each_line)  # write line on errorlog file
        fo.close()
        fo1.close()

    except TimeoutError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except FileNotFoundError:
        err = tkinter.Label(window,
                            text=f"file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise


window=tkinter.Tk()
window.geometry("700x500")
path_var=tkinter.StringVar()
hostname_var=tkinter.StringVar()
psw_var = tkinter.StringVar()
window.title("CORE LOGs")
label=tkinter.Label(window,text="Find Errors on CHE Core Logs")
label.pack()

getPathLable=tkinter.Label(window,text="enter your path: ",font=('calibre', 10, 'normal'))
getPathLable.pack()
getPathEntry=tkinter.Entry(window, textvariable=path_var,width=50,font=('calibre', 10, 'normal'))
getPathEntry.pack()
getHostLabel=tkinter.Label(window,text="enter your host ip: ",font=('calibre', 10, 'normal'))
getHostLabel.pack()
getHostEntry=tkinter.Entry(window, textvariable=hostname_var,width=15,font=('calibre', 10, 'normal'))
getHostEntry.pack()
getpsw=tkinter.Label(window,text="Enter password for your server: ",font=('calibre', 10, 'normal'))
getpsw.pack()
getpsw=tkinter.Entry(window, textvariable=psw_var,width=15,font=('calibre', 10, 'normal'))
getpsw.pack()
executeButton=tkinter.Button(window,text="Execute",command=CoreLogs)
executeButton.pack()

window.mainloop()
