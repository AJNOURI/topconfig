# -*- coding: utf-8 -*-
#!/usr/bin/python
# Remotely configure NAT on Vyatta, VyOS and brocade vrouter boxes
# AJN 19/10/2014

from vlib import *


IP = '192.168.0.149'
LOGIN = 'vyatta'
HOSTNAME = 'vr'
TEST_ID = '1'
TEST_RUN = '1'
ITERATION = '1'
SSH_PASS = password = 'vyatta'

cmd = [
    'set nat source rule 10 outbound-interface eth0',
    'set nat source rule 10 source address 192.168.13.0/24',
    'set nat source rule 10 translation address masquerade'
]
cmdname = "nat masquarade"

vy_set_cfg(IP, cmdname, LOGIN, SSH_PASS, TEST_ID, TEST_RUN, ITERATION, HOSTNAME, *cmd)

cmd = [
    'show nat source rule',
    'show nat destination rule',
    'show nat source statistics',
    'show nat source trans'
]
for c in cmd:
    vy_sh_prm(IP, c, LOGIN, SSH_PASS, TEST_ID, TEST_RUN, ITERATION, HOSTNAME)

cmd = 'nat'
vy_sh_cfg(IP, cmd, LOGIN, SSH_PASS, TEST_ID, TEST_RUN, ITERATION, HOSTNAME)
