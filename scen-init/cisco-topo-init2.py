#!/usr/bin/env python

# Copyright 2014 by AJ NOURI <ajn.bin@gmail.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

"""Usage:
  cback [-gh] [ -v | -w ] FILE
  cback --version

           Process router list and parameters from FILE, backup
           configuration files with optional git version control.

Arguments:
  FILE        mendatory YAML input file for router list

Options:
  -h --help   show this
  -v          verbose mode
  -w          very verbose mode
  -g          use git to contol versions of the configuration files
  --version   version inf.

FILE template:
-
 HOSTNAME: <hostname>
 IP : <ip>
 LOGIN: <login>
 SSH_PASS: <pass>
-
 HOSTNAME: <hostname>
 IP : <ip>
 LOGIN: <login>
 SSH_PASS: <pass>
-
 HOSTNAME: <hostname>
 IP : <ip>
 LOGIN: <login>
 SSH_PASS: <pass>
"""

import paramiko
import socket
import os
import sh
import sys
from datetime import datetime
import logging
import yaml
import multiprocessing
from docopt import docopt


def main(docopt_args):

    def git_fn(filename, comment):
            try:
                sh.sudo.git("init")
                sh.sudo.git("add", filename)
                sh.sudo.git("commit", comment, "--allow-empty")
            except sh.ErrorReturnCode:
                print(sys.exc_info()[1])

    def paramiko_mod(ip, cmd, login, sshpass, hostname):

        try:
            sshobj = paramiko.SSHClient()
            sshobj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            sshobj.connect(ip, username=login, password=sshpass, allow_agent=False,look_for_keys=False)
            stdin, stdout, stderr = sshobj.exec_command(cmd)
            out = ''.join(stdout)

            filename = hostname + ".cfg"
            now = str(datetime.now())
            comment = "-m " + "\" " + now + "\""

            f = open(filename, 'w')
            for line in out:
                f.write(line)
            f.close()
            if docopt_args['-g']:
                git_fn(filename, comment)
            sshobj.close()
            logging.info('==> Backup of Router' + hostname + ' : IP ' + ip + ' done.')
            return filename, cmd
        except socket.error, v:
            errorcode = v[0]
            print(os.strerror(errorcode))


    if docopt_args['--version']:
        print ' cback.py : version ' + __version__ + '   by AJ NOURI, ajn.bin@gmail.com'
    else:
        if docopt_args['-w']:
            logging.basicConfig(level=logging.DEBUG)
        elif docopt_args['-v']:
            logging.basicConfig(level=logging.INFO)

        # Reading the router list and connection parameters
        stream = open(docopt_args['FILE'], 'r')
        rdata = yaml.load(stream)


        CMD = 'sh run'
        task_list = []

        for router in rdata:
            task = multiprocessing.Process(target=paramiko_mod, args=(router['IP'], CMD, router['LOGIN'], router['SSH_PASS'], router['HOSTNAME']))
            task_list.append(task)
            task.start()

        for task in task_list:
            task.join()

if __name__ == '__main__':
    # parse arguments based on docstring
    args = docopt(__doc__)
    # Run the program with the validated args
    main(args)
