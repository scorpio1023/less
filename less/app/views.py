# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
import os
import re
import paramiko
import threading

hosts_info = {}
pwd = os.path.dirname(os.path.abspath(__file__))

def gethostinfo(host,lock):
    global hosts_info
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host,22,"root","ltech2",timeout=5)
        sin,sout,serr=ssh.exec_command("uname -n")
        hostname = sout.read()
    except:
        hostname = "Not Available"
    lock.acquire()
    hosts_info[host] = hostname
    lock.release()
    ssh.close()
    print host,"done"
    

def myapp(request):
    global hosts_info
    global pwd
    threads = []
    lock = threading.RLock()
    filename = os.path.join(pwd,"hosts")
    f = open(filename)
    host_list = f.read().splitlines()
    f.close()
    for host in host_list:
        t = threading.Thread(target=gethostinfo, args=(host,lock))
        threads.append(t)
    for thd in threads:
        thd.start()
    for thd in threads:
        thd.join()
    return render_to_response("index.html",{"hosts_info":hosts_info, "host_list":host_list})


def dealgrub(buf, flag):
    if flag == "grub" :
        keywd = "kernel"
    else :
        keywd = "linux"
    kernel = []
    klist = re.findall("^\s+|\t+%s.*?\n"%keywd, buf)
    for line in klist :
        alist = re.split("\s+|\t+", line)
        kernel.append(alist[2].lstrip("/"))
    kernel = list(set(kernel))
    return kernel


def anawho(w_list):
    global pwd
    result = {}
    m_dict = {}
    filename = os.path.join(pwd,"members")
    f = open(filename)
    m_list = f.read().splitlines()
    f.close()
    for line in m_list :
        alist = re.split("\s+",line)
        m_dict[alist[1]] = alist[0]
    w_list = list(set(w_list))
    for line in w_list :
        m = re.search("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",line);
        if m :
            if m.group(1) in m_dict.keys() :
                result[m.group(1)] = m_dict[m.group(1)]
            else :
                result[m.group(1)] = "Unknown"
    return result


def detail(request, host):
    global hosts_info
    html = ""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, "root", "ltech2")
    html += "<center><b>DETAILS</b></center>"
    html += "<table frame='hsides' width='700' align='center'>"
    # CURRENT
    html += "<tr class='detail1'><td><b>CURRENT</b></td><td>" + hosts_info[host] + "</td></tr>"
    # BOOT
    html += "<tr class='detail2'><td><b>BOOT</b></td><td>"
    sin,sout,serr=ssh.exec_command("df | grep /boot | awk '{print $1}'")
    boot = sout.read()
    if boot :
        html += boot + "</td></tr>"
    else :
        html += "none</td></tr>"
    # OSes
    com = """DEVFILE=$(mktemp);MNTDIR=$(mktemp -d);HF=$MNTDIR/etc/sysconfig/network;fdisk -l | grep "Linux$" | awk '{print $1}'>$DEVFILE;while read line;do echo -n "$line:";if mount $line $MNTDIR 2>/dev/null;then if [ -f $HF ];then echo `cat $HF | grep HOSTNAME | awk -F'=' '{print $2}'`;else echo;fi;umount $MNTDIR;else echo;fi; done < $DEVFILE;rm -f $DEVFILE;rmdir $MNTDIR>/dev/null"""
    html += "<tr class='detail1'><td><b>OSes</b></td><td>"
    sin,sout,serr=ssh.exec_command(com)
    oses = sout.read().splitlines()
    print oses
    for line in oses :
        alist = re.split(":",line)
        if alist[1] == "" :
            continue
        html += alist[0] + ":&nbsp;&nbsp;" + alist[1] + "<br>"
    html += "</td></tr>"
    # LOGIN
    html += "<tr class='detail2'><td><b>LOGIN</b></td><td>"
    sin,sout,serr=ssh.exec_command("who | awk '{print $5}'")
    alist = sout.read().splitlines()
    if alist :
        who_dict = anawho(alist)
        if who_dict :
            for k in who_dict.keys() :
                html += who_dict[k] + "&nbsp;&nbsp;From&nbsp;&nbsp;" + k + "<br>"
            html += "</td></tr>"
        else :
            html += "No one</td></tr>"
    else :
        html += "No one</td></tr>"
    html += "</table>"

    return HttpResponse(html)
