# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
import os
import re
import paramiko

pwd = os.path.dirname(os.path.abspath(__file__))

def gethostinfo(request,host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host,22,"root","ltech2",timeout=5)
        sin,sout,serr=ssh.exec_command("uname -n")
        hostname = sout.read()
    except:
        hostname = "Not Available"
    ssh.close()
    print host,"done"

    return HttpResponse(hostname)


def myapp(request):
    global pwd
    threads = []
    filename = os.path.join(pwd,"hosts")
    f = open(filename)
    host_list = f.read().splitlines()
    f.close()

    return render_to_response("index.html",{"host_list":host_list})


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
    html = ""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, "root", "ltech2")
    html += "<center><b>DETAILS</b></center>"
    html += "<table frame='hsides' width='700' align='center'>"
    # CURRENT
    html += "<tr class='detail1'><td><b>CURRENT</b></td><td>"
    sin,sout,serr=ssh.exec_command("uname -n")
    cur = sout.read()
    if cur :
        html += cur + "</td></tr>"
    else :
        html += "none</td></tr>"
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
    ssh.close()

    return HttpResponse(html)
