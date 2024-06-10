import paramiko
import datetime
import re
import tkinter
import socket

from paramiko.ssh_exception import AuthenticationException


def ErrorLogs():
    global filename
    global today
    global date
    today=datetime.datetime.now().strftime("%Y%m%d")
    path = path_var.get()
    hostname = hostname_var.get()
    psw = psw_var.get()
    options=Multiple_var.get()
    if options == "N":
        filename = "smf-log-files." + today + ".txt"
        todaysmf = FileDownload(hostname, path,psw)
        Find_Critical(path,today)
        Find_Warning(path,today)
    else:
        dates=Dates_var.get()
        fileList = daysRange(dates)
        FilesDownload(hostname,path,fileList,psw)
        Find_Critical_Files(path,fileList)
        Find_Warning_Files(path, fileList)
    return None


def daysRange(dates):
    d1=int(d1_var.get())
    d2=int(d2_var.get())
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
        con = tkinter.Label(window, text="ftp connection established executing")
        con.pack()
        todaysmf=ftp.get("/ThomsonReuters/smf/log/"+filename,path+"\\smf-log-files."+today+".txt")
        ftp.close()
        ssh.close() # close connection
        return todaysmf
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
        err = tkinter.Label(window, text=f"SMF file not found make sure the server ip and local path provided are correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except ConnectionError:
        err = tkinter.Label(window, text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except ConnectionRefusedError:
        err = tkinter.Label(window, text=f"connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
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

def FilesDownload(hostname,path,fileList,psw):
    try:
        fileList
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password=psw, port=22)
        ftp = ssh.open_sftp()
        con = tkinter.Label(window, text="ftp connection established executing")
        con.pack()
        ftp = ssh.open_sftp()
        for file in fileList:
            ftp.get("/ThomsonReuters/smf/log/" + file, path +"\\" + file )
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
                            text=f"SMF file not found make sure the server ip and local path provided are correct\n \n double check dates and days range provided are also in the correct format\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except ConnectionError:
        err = tkinter.Label(window,
                            text=f"Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except ConnectionRefusedError:
        err = tkinter.Label(window,
                            text=f"Connection is refused make sure password for the server is correct\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise


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
        err = tkinter.Label(window, text=f"SMF file not found make sure SMF file to analyze is downloaded at {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise


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
        output = tkinter.Label(window,
                               text=f"Completed find your files at: {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        output.pack()
        return None
    except FileNotFoundError:
        err = tkinter.Label(window, text=f"SMF file not found make sure SMF file to analyze is downloaded at {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise


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
        err = tkinter.Label(window, text=f"SMF file not found make sure SMF file to analyze is downloaded at {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise

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
        output = tkinter.Label(window,
                               text=f"Completed find your files at: {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        output.pack()
        fo.close()
        fo1.close()
        return None

    except FileNotFoundError:
        err = tkinter.Label(window, text=f"SMF file not found make sure SMF file to analyze is downloaded at {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
        err.pack()
        raise




def update_window():
    global getDateLabel
    global getD1Label
    global getD2Label
    global getDateEntry
    global getD1Entry
    global getD2Entry
    global executeButton
    global executeButton1
    if  Multiple_var.get() == "Y":

        executeButton.destroy()

        getDateLabel=tkinter.Label(window,text="Enter Year and Month fo SMF files you want to analyze format 'yyyymm' - i.e '202104: ",font=('calibre', 10, 'normal'))
        getDateLabel.pack()
        getDateEntry=tkinter.Entry(window, textvariable=Dates_var,width=10,font=('calibre', 10, 'normal'))
        getDateEntry.pack()

        getD1Label=tkinter.Label(window,text="Enter day from: ",font=('calibre', 10, 'normal'))
        getD1Label.pack()
        getD1Entry=tkinter.Entry(window, textvariable=d1_var,width=5,font=('calibre', 10, 'normal'))
        getD1Entry.pack()

        getD2Label=tkinter.Label(window,text="Enter day to: ",font=('calibre', 10, 'normal'))
        getD2Label.pack()
        getD2Entry=tkinter.Entry(window, textvariable=d2_var,width=5,font=('calibre', 10, 'normal'))
        getD2Entry.pack()

        executeButton1 = tkinter.Button(window, text="Execute", command=ErrorLogs)
        executeButton1.pack()

    else:
        getDateLabel.destroy()
        getDateEntry.destroy()
        getD1Label.destroy()
        getD1Entry.destroy()
        getD2Label.destroy()
        getD2Entry.destroy()
        executeButton1.destroy()
        executeButton1 = tkinter.Button(window, text="Execute", command=ErrorLogs)
        executeButton1.pack()


window=tkinter.Tk()
window.geometry("700x500")
path_var=tkinter.StringVar()
hostname_var=tkinter.StringVar()
psw_var=tkinter.StringVar()
Multiple_var=tkinter.StringVar()
Dates_var=tkinter.StringVar()
d1_var=tkinter.StringVar()
d2_var=tkinter.StringVar()


window.title("SMF LOGs")
label=tkinter.Label(window,text="Warning & Errors Logs")
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

getMultipleLabel=tkinter.Checkbutton(window, variable=Multiple_var,onvalue="Y", offvalue="N",text="Multiple files:", command=update_window)
getMultipleLabel.deselect()
getMultipleLabel.pack()

executeButton=tkinter.Button(window,text="Execute",command=ErrorLogs)
executeButton.pack()

window.mainloop()