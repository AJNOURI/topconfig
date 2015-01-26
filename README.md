# cback.py #

### Usage:

           cback [-gh] [ -v | -w ] FILE
           cback --version

Read a list of routers and associated  credentials from FILE (yaml format) and backup
configuration files with optional git version control.

### Arguments:
  FILE   :     mendatory YAML input file for router list

### Options:
*   -h --help :  show this
*   -v            :   verbose mode
*   -w           :   very verbose mode
*   -g            :  use git to contol versions of the configuration files
*   --version :  version inf.

### FILE template:
```
#!yaml

-
 hostname: <hostname>
 IP : <ip>
 LOGIN: <login>
 SSH_PASS: <pass>
-
 hostname: <hostname>
 IP : <ip>
 LOGIN: <login>
 SSH_PASS: <pass>
-
 hostname: <hostname>
 IP : <ip>
 LOGIN: <login>
 SSH_PASS: <pass>
```
