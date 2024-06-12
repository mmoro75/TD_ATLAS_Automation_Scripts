import sys
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
    path=sys.argv[1]
    hostname=sys.argv[2]
    psw = sys.argv[3]
    Venue_name = sys.argv[4]
    filesDownload(hostname,path,psw,Venue_name)
    FMSClientDownload(hostname,path,psw,Venue_name)
    SCWDownload(hostname,path,psw,Venue_name)
    files=fileList(path)
    Find_Exceptions(path,files,today)
    Find_Critical(path,files,today)
    print(f"Completed find your files at: {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
    return None

def filesDownload(hostname,path,psw,Venue_name):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print(f"ftp connection established executing\n")
        apath = '/data/che'
        apattern = '"*.log"'
        rawcommand = 'find {path} -name {pattern}'
        command = rawcommand.format(path=apath, pattern=apattern)
        stdin, stdout, stderr = ssh.exec_command(command)
        filelist = stdout.read().splitlines()

        ftp = ssh.open_sftp()
        for afile in filelist:
            (head, filename) = os.path.split(afile)
            ftp.get(afile, path + "\\" +Venue_name+ "_" + str(filename))

        ftp.close()
        ssh.close()  # close connection
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
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(
            f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def FMSClientDownload(hostname,path,psw,Venue_name):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=psw,port=22)
        ftp=ssh.open_sftp()
        ftp.get("/data/FMSClient/FMSClient.log",path+"\\" +Venue_name+ "_FMSClient.log")
        ftp.close()
        ssh.close() # close connection
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
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(
            f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

def SCWDownload(hostname,path,psw,Venue_name):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=psw,port=22)
        ftp=ssh.open_sftp()
        todaysmf=ftp.get("/data/SCWatchdog/logs/SCWatchdog.log",path+"\\" +Venue_name+ "_SCWatchdog.log")
        ftp.close()
        ssh.close() # close connection
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
        print("connection is refused make sure password for the server is correct")
        quit()
    except AuthenticationException:
        print(
            f"The password '{password}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()

def fileList(path):
    my_dir = path

    files = []
    for (dirpath, dirnames, filenames) in walk(my_dir):
        files.extend(filenames)
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
         print(f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
    except FileNotFoundError:
        print(f"File not found make sure {persist_file} file to analyze is downloaded at C:\\PMAT\\x64")
        quit()
    except Exception as e:
        print(e)
        quit()


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
         print(f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
    except FileNotFoundError:
        print(f"File not found make sure {persist_file} file to analyze is downloaded at C:\\PMAT\\x64")
        quit()
    except Exception as e:
        print(e)
        quit()



CoreLogs()