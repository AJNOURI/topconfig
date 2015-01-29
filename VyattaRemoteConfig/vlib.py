# -*- coding: utf-8 -*-
#!/usr/bin/python
# Vyatta, VyOS and brocade vrouter library
# AJN 19/10/2014

import pexpect
import paramiko


def mkfilename(cmd, testid, testrun, iteration, hostname):

    ucmd = cmd.replace(':', '_')
    ucmd = ucmd.replace('.', '_')
    ucmd = ucmd.replace('/', '_')
    filename = 'C' + testid + '_TR' + testrun + '_IT' + iteration + '_' + hostname + '_' + ucmd
    filename = filename.replace(' ', '_')
    return filename


def para_ssh(ip, command, login, hostname, testid, testrun, iteration, sshpass):

    sshobj = paramiko.SSHClient()
    sshobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshobj.connect(ip, username=login, password=sshpass, allow_agent=False, look_for_keys=False)
    stdin, stdout, stderr = sshobj.exec_command(command)
    filen = mkfilename(command, testid, testrun, iteration, hostname)
    f = open(filen, "w")
    for line in stdout.readlines():
        f.write(line.strip('\r\n')+'\r\n')
    f.close()
    sshobj.close()
    print 'parassh: ', command, ' DONE'
    return filen, command


def lx_cmd(ip, command, login, hostname, testid, testrun, iteration, sshpass, tout):

    ssh_newkey = 'Are you sure you want to continue connecting'
    pcmd = "ssh " + login + "@" + ip + " " + command + " "
    child = pexpect.spawn(pcmd, timeout=tout)
    i = child.expect([ssh_newkey, 'password:', pexpect.EOF])
    if i == 0:
        #print "I say yes"
        child.sendline('yes')
        i = child.expect([ssh_newkey, 'password:', pexpect.EOF])
    if i == 1:
        #print "I give password",
        child.sendline(sshpass)
        filename = mkfilename(command, testid, testrun, iteration, hostname)
        f = file(filename, 'w')
        child.logfile = f
    child.expect(pexpect.EOF)
    child.close()
    # Return filename to the main program
    return filename, command


def paramiko_mod(ip, cmd, wrap, login, sshpass, testid, testrun, iteration, hostname):
    sshobj = paramiko.SSHClient()
    sshobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshobj.connect(ip, username=login, password=sshpass)
    stdin, stdout, stderr = sshobj.exec_command(wrap)
    out = ''.join(stdout)
    filename = mkfilename(cmd, testid, testrun, iteration, hostname)
    f = open(filename, 'w')
    for line in out:
        f.write(line)
    f.close()
    sshobj.close()
    return filename, cmd


def vy_set_cfg(ip, cmdname, login, sshpass, testid, testrun, iteration, hostname, *cmd):
    wrap_head = "/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper begin" + "\n"
    wrap_tail = "/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper commit" + "\n" + \
               "/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper save"
    wrap_body = ""
    for c in cmd:
        wrap_body = wrap_body + '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper ' + c + "\n"
    wrap = wrap_head + wrap_body + wrap_tail
    return paramiko_mod(ip, cmdname, wrap, login, sshpass, testid, testrun, iteration, hostname)


def vy_get_cfg(ip, cmd, login, sshpass, testid, testrun, iteration, hostname):
    wrap = """
        /opt/vyatta/sbin/vyatta-cfg-cmd-wrapper begin
        /opt/vyatta/sbin/vyatta-cfg-cmd-wrapper """ + cmd + """
        """
    return paramiko_mod(ip, cmd, wrap, login, sshpass, testid, testrun, iteration, hostname)


def vy_sh_cfg(ip, cmd, login, sshpass, testid, testrun, iteration, hostname):
    wrap = """
        cli-shell-api showCfg """ + cmd + """
        """
    return paramiko_mod(ip, cmd, wrap, login, sshpass, testid, testrun, iteration, hostname)



def vy_sh_prm(ip, cmd, login, sshpass, testid, testrun, iteration, hostname):

    ########################################vyos_param_show
    ### vyatta show system operational parameters

    child = pexpect.spawn('ssh '+login+'@'+ip)
    child.expect('password:')
    child.sendline(sshpass)
    child.expect('\$')
    child.sendline(cmd)
    child.expect('\$')
    filename = mkfilename(cmd, testid, testrun, iteration, hostname)
    fout = file(filename, 'w')
    for line in child.before:
        fout.write(line)
    fout.close()
    child.close()
    return filename, cmd
