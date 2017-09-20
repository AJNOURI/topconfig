#!/usr/bin/env python

from netmiko import ConnectHandler


cisco1562T = {
    'device_type':'cisco_ios',
    'ip':'192.168.111.1',
    'username':'admin',
    'password':'cisco'
}

with open('device_file') as f:
    devices_list = f.read().splitlines()

for devices in devices_list:
    print 'Connection to device ' + devices
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': 'admin',
        'password': 'cisco'
    }

net_connect = ConnectHandler(**cisco1562T)
net_connect.find_prompt()
output = net_connect.send_command("show ip int brief")

