# coding: utf-8
#!/usr/bin/python

import paramiko
import pexpect
import re
import sys
import subprocess
import os

class CParam(object):
    def __init__(self, ip, login, hostname, sshpass):
        self.ip = ip
        self.login = login
        self.hostname = hostname
        self.sshpass = sshpass
        try:
            self.sshobj = paramiko.SSHClient()
            self.sshobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.sshobj.connect(self.ip, username=self.login, password=self.sshpass, allow_agent=False,
                                look_for_keys=False)

        except socket.error:
            print "Make sure the device ", self.ip, " is reachable"

    def sendcmd(self, command):
        self.stdin, self.stdout, self.stderr = self.sshobj.exec_command(command)
        out = ''.join(self.stdout)
        #print out
        f = open('fout.tmp', 'w')
        for line in out:
            f.write(line)
        f.close()

### Device information
ip = "192.168.5.202"
login = "admin"
hostname = "SLB"
sshpass = "cisco"
tout = 30
command = 'sh ip slb reals'


while 1:

    # Get inf. from the router
    session = CParam(ip, login, hostname, sshpass)
    session.sendcmd(command)

    # Keep only useful columns
    COMMAND = "cat fout.tmp | awk {'print $1, $3, $5'} > resfile.tmp"
    subprocess.call(COMMAND, shell=True)

    # Remove useless lines
    lines = open('resfile.tmp').readlines()
    open('resfile.csv', 'w').writelines(lines[4:-1])

    #result = subprocess.check_output("cat fout.tmp | awk {'print $1'}")
    #print result
    realsrv = []
    weight = []
    conn = []
    f = open("resfile.csv", "r")
    for line in f:
        sline = line.split()
        realsrv.append(sline[0])
        weight.append(sline[1])
        conn.append(sline[2])

    os.system('clear')
    sign = '#'
    for i in range(len(realsrv)):
        print realsrv[i],' weight: ',weight[i],' conn: ',conn[i],': ','#' * int(conn[i])