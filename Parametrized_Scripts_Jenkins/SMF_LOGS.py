import paramiko
import datetime
import time
import re
import socket
from paramiko.ssh_exception import AuthenticationException
import sys
import pandas as pd


def ErrorLogs():
    global filename
    global today
    global date
    global output_host

    today = datetime.datetime.now().strftime("%Y%m%d")
    path = "C:\\Users\\U6017127\\.jenkins\\workspace\\SMF_Logs_Analysis\\"
    hostname = sys.argv[1]
    psw = sys.argv[2]
    output_host = output_host(hostname, psw)
    options = sys.argv[3]

    print(options)
    if options == "TODAY_LOG":
        filename = "smf-log-files." + today + ".txt"
        todaysmf = FileDownload(hostname, path, psw)
        Find_Critical(path, today)
        Find_Warning(path, today)
    else:
        start_date = sys.argv[4]
        end_date = sys.argv[5]

        fileList = DateRange(start_date,end_date)
        FilesDownload(hostname, path, fileList, psw)
        Find_Critical_Files(path, fileList)
        Find_Warning_Files(path, fileList)
    print("Completed find your files at: ", path)
    return None


def DateRange(start_date,end_date):
    daterange = pd.date_range(start_date, end_date)

    date_ls = []
    for single_date in daterange:
        single_date = str(single_date.strftime("%Y%m%d"))
        date_ls.append(single_date)


    fileList = []
    for date in date_ls:
       if date == today:
          filename = "smf-log-files." + date + ".txt"
          fileList.append(filename)
       else:
          filename = "smf-log-files." + date + "_235959.txt"
          fileList.append(filename)
    
  
    return fileList

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


def FileDownload(hostname, path, psw):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print("ftp connection established executing:")
        todaysmf = ftp.get("/ThomsonReuters/smf/log/" + filename,
                           path + "\\" + output_host + "_smf-log-files." + today + ".txt")
        ftp.close()
        ssh.close()  # close connection
        return todaysmf
    except TimeoutError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except FileNotFoundError:
        print("SMF file not found make sure the server ip and local path provided are correct")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except AuthenticationException:
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
    except Exception as e:
        print(e)
        quit()


def FilesDownload(hostname, path, fileList, psw):
    try:
        fileList
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print(f"ftp connection established executing\n")
        ftp = ssh.open_sftp()
        for file in fileList:
            ftp.get("/ThomsonReuters/smf/log/" + file, path + "\\" + output_host + "_" + file)
        ftp.close()
        ssh.close()  # close connection
        return None
        return todaysmf
    except TimeoutError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except socket.gaierror:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except FileNotFoundError:
        print(
            "SMF file not found make sure the server ip and local path provided are correct\n double check dates and days range provided are also in the correct format")
        quit()
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
        quit()
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except AuthenticationException:
        print(f"The password '{psw}' provided is not correct for the selected server, try again with correct password")
        quit()
        quit()
    except Exception as e:
        print(e)
        quit()


def Find_Critical(path, today):
    try:
        patt = r"\bCritical\b"
        fo = open(path + "\\" + output_host + "_smf-log-files." + today + ".txt", "r")  # open host file in read mode
        fo2 = open(path + "\\" + output_host + "_CRITICAL_log-" + today + ".txt", "w")  # open file in write mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        for each_line in files_lines:  # loop into list crreated
            if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                fo2.write(each_line)  # write line on errorlog file
        fo.close()
        fo2.close()
        return None
    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        quit()
    except Exception as e:
        print(e)
        quit()


def Find_Warning(path, today):
    try:
        patt = r"\bWarning\b"
        fo = open(path + "\\" + output_host + "_smf-log-files." + today + ".txt", "r")  # open host file in read mode
        fo2 = open(path + "\\" + output_host + "_WARNING_log-" + today + ".txt", "w")  # open file in write mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        for each_line in files_lines:  # loop into list crreated
            if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                fo2.write(each_line)  # write line on errorlog file
        fo.close()
        fo2.close()
        return None
    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        quit()
    except Exception as e:
        print(e)
        quit()


def Find_Critical_Files(path, fileList):
    try:
        my_dir = path
        patt = r"\bCritical\b"
        files = []
        for f in fileList:
            files.append("".join(output_host + "_" + f))
        for f in files:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\" + output_host + "_CRITICAL-logs-MULTIPLE_FILES.txt", "a")
            fo1.write(f"\n CRITICAL ERRORS IN  {f}\n \n")
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:
                if re.findall(patt, each_line):
                    if each_line != "":
                        fo1.write(each_line)  # write line on errorlog file
        fo.close()
        fo1.close()
        return None

    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        quit()
    except Exception as e:
        print(e)
        quit()


def Find_Warning_Files(path, fileList):
    try:
        my_dir = path
        patt = r"\bWarning\b"
        files = []
        for f in fileList:
            files.append("".join(output_host + "_" + f))
        for f in files:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\" + output_host + "_WARNING-log-MULTIPLE_FILES.txt", "a")
            fo1.write(f"\n WARNING ERRORS IN  {f}\n \n")
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:  # loop into list crreated
                if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                    if each_line != "":
                        fo1.write(each_line)  # write line on errorlog file
        fo.close()
        fo1.close()
        return None
    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        quit()
    except Exception as e:
        print(e)
        quit()


ErrorLogs()

if __name__ == "__ErrorLogs__":
    ErrorLogs()
