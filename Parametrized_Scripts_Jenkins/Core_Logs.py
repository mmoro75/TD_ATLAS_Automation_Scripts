import sys
import paramiko
import re
import datetime
import os
from os import listdir
from os import walk
import socket
import time

from paramiko.ssh_exception import AuthenticationException


def CoreLogs():
    global today
    global output_host
    today=datetime.datetime.now().strftime("%Y%m%d")
    path="C:\\Users\\U6017127\\.jenkins\\workspace\\Venue_Core_Logs_Check\\"
    hostname=sys.argv[1]
    psw = sys.argv[2]
    output_host = output_host(hostname, psw)
    filesDownload(hostname,path,psw,output_host)
    FMSClientDownload(hostname,path,psw,output_host)
    SCWDownload(hostname,path,psw,output_host)
    files=fileList(path)
    Find_Exceptions(path,files,today,output_host)
    Find_Critical(path,files,today,output_host)
    print(f"Completed find your files at: {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
    return None
    
def output_host(hostname, psw):
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        stdin, stdout, stderr = ssh.exec_command(f"hostname")
        time.sleep(2)
        host = stdout.read()
        host = host.decode(encoding="utf-8")
        output_host = ''.join(c for c in host if c.isprintable())
        ftp = ssh.open_sftp()
        return output_host   


def filesDownload(hostname,path,psw,output_host):
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
            ftp.get(afile, path + "\\" +output_host+ "_" + str(filename))

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


def FMSClientDownload(hostname,path,psw,output_host):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=psw,port=22)
        ftp=ssh.open_sftp()
        ftp.get("/data/FMSClient/FMSClient.log",path+"\\" +output_host+ "_FMSClient.log")
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

def SCWDownload(hostname,path,psw,output_host):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=psw,port=22)
        ftp=ssh.open_sftp()
        todaysmf=ftp.get("/data/SCWatchdog/logs/SCWatchdog.log",path+"\\" +output_host+ "_SCWatchdog.log")
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

def Find_Critical(path,files,today,output_host):
    try:
        my_dir = path
        patt = r"\bCritical\b"
        for f in files:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\" + output_host + "_CRITICAL-log-"+today+".txt", "a")
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


def Find_Exceptions(path,files,today,output_host):
    try:
        my_dir = path
        patt = r"\bException\b"
        for f in files:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\" + output_host + "_EXEPTIONS_log-"+today+".txt", "a")
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