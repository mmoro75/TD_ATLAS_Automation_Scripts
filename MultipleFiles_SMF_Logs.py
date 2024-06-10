import paramiko
import datetime
import re
import socket
from paramiko.ssh_exception import AuthenticationException

def ErrorLogs():
    global filename
    global today
    global date
    today=datetime.datetime.now().strftime("%Y%m%d")
    path = input("Please provide a path where you want your logs to be stored: ")
    hostname = input("please provide hostname-ip_address: ")
    psw = input("please provide server password: ")
    options=input("do you want to download today SMF log? Y or N: ").upper()
    if options == "Y":
        filename = "smf-log-files." + today + ".txt"
        todaysmf = FileDownload(hostname, path,psw)
        Find_Critical(path,today)
        Find_Warning(path,today)
    else:
        dates=input("please enter Year and Month fo SMF files you want to analyze format 'yyyymm' - i.e '202104: ")
        fileList = daysRange(dates)
        FilesDownload(hostname,path,fileList,psw)
        Find_Critical_Files(path,fileList)
        Find_Warning_Files(path, fileList)
    print("Completed find your files at: ",path)
    return None

def daysRange(dates):
    d1, d2 = [int(d1) for d1 in input("Enter smf day from - to you want to analyze 'i.e 10 20': ").split()]
    if (d1 == d2):
        smf=str(dates)+str(d1).zfill(2)
        filename = "smf-log-files." + smf + "_235959.txt"
        fileList = [filename]
        return fileList
    else:
        res = []
        while (d1 < d2 + 1):
            res.append(d1)
            d1 += 1
    days = []
    for day in res:
        if day < 10:
            days.append(str(day).zfill(2))
        else:
            days.append(str(day))
    fileList = []
    for day in days:
        smf=str(dates)+str(day)
        filename = "smf-log-files." + smf + "_235959.txt"
        fileList.append(filename)
    return fileList

def FileDownload(hostname,path,psw):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password=psw,port=22)
        ftp=ssh.open_sftp()
        print("ftp connection established executing:")
        todaysmf=ftp.get("/ThomsonReuters/smf/log/"+filename,path+"\\smf-log-files."+today+".txt")
        ftp.close()
        ssh.close() # close connection
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

def FilesDownload(hostname,path,fileList,psw):
    try:
        fileList
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        print(f"ftp connection established executing\n")
        ftp = ssh.open_sftp()
        for file in fileList:
            ftp.get("/ThomsonReuters/smf/log/" + file, path +"\\" + file )
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
        print("SMF file not found make sure the server ip and local path provided are correct\n double check dates and days range provided are also in the correct format")
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
        fo = open(path + "\\smf-log-files." + today + ".txt", "r")  # open host file in read mode
        fo2 = open(path + "\\Critical_log-" + today + ".txt", "w")  # open file in write mode
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
        fo = open(path + "\\smf-log-files." + today + ".txt", "r")  # open host file in read mode
        fo2 = open(path + "\\Warning_log-" + today + ".txt", "w")  # open file in write mode
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

def Find_Critical_Files(path,fileList):
    try:
        my_dir = path
        patt = r"\bCritical\b"
        for f in fileList:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\Critical-logs-MultipleFiles.txt", "a")
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

def Find_Warning_Files(path,fileList):
    try:
        my_dir = path
        patt = r"\bWarning\b"
        for f in fileList:
            fo = open(my_dir + "\\" + f, "r")  # open host file in read mode
            fo1 = open(my_dir + "\\Warning-log-multipleFiles.txt", "a")
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

if __name__=="__ErrorLogs__":
    ErrorLogs()
