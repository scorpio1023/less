# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
import os
import paramiko
import threading

hosts_info = {}

def setuphosts_info(host_list):
    global hosts_info
    length = len(host_list)
    for i in range(length):
        hosts_info[host_list[i]] = ""


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
    threads = []
    lock = threading.RLock()
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"hosts")
    f = open(filename)
    host_list = f.read().splitlines()
    print host_list
    f.close()
    setuphosts_info(host_list)
    print hosts_info
    for host in host_list:
        t = threading.Thread(target=gethostinfo, args=(host,lock))
        threads.append(t)
    for thd in threads:
        thd.start()
    for thd in threads:
        thd.join()
    return render_to_response("index.html",{"hosts_info":hosts_info, "host_list":host_list})


def detail(request, host):
    html = ""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, "root", "ltech2")
    sin,sout,serr=ssh.exec_command("who")
    alist = sout.read().splitlines()
    html += "<p align='center'><strong>who</strong></p>"
    html += "<table frame='hsides' width='700' align='center'>"
    if alist :
        for line in alist:
            html += "<tr>"
            import re
            blist = re.split("\s+", line)
            for item in blist:
                html += "<td>"+item+"</td>"
            html += "</tr>"
    else :
        html += "<tr><td>No one<td></tr>"
    html += "</table>"

    return HttpResponse(html)
