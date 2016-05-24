'''
Miguel Angel Alvarez Cabrerizo (n40lab) - ArtemIT 2016

Description: A script for random password and hashes generation to be used as sudo passwords. 
Ansible Vault is used to encrypt the files containing sensitive information.

Password generator:
http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python

Discussion about Ansible sudo password:
http://stackoverflow.com/questions/21870083/specify-sudo-password-for-ansible

Calling external command:
http://stackoverflow.com/questions/89228/calling-an-external-command-in-python
'''


import string
import random
import os
import sys
from passlib.hash import sha512_crypt
from subprocess import call
import getpass

hosts = ['atlas.artemit.mgmt', 'titan.artemit.mgmt', 'prometeo.artemit.mgmt']
home = os.path.expanduser("~")
cwd = os.getcwd()
host_inventory = cwd + '/inventory.ini'
host_vars_path = cwd + '/host_vars'
vault_command = ['ansible-vault','encrypt']

chars = string.letters + string.digits 

pwdSize = 30

if (not os.path.exists(host_inventory)):
    name = host_inventory
    file = open(name,'w')  

    for host in hosts:
      file.write(host+'\n')

    file.close()


if (not os.path.exists(host_vars_path)):
    os.makedirs(host_vars_path)

for host in hosts:
    password = ''.join(random.SystemRandom().choice(chars) for _ in range(pwdSize))
    sha512_hash = sha512_crypt.encrypt(password)

    name = host_vars_path + '/' + host + '.yml'
    file = open(name,'w')
    file.write('ansible_become_pass: "' + password + '"\n')
    file.write('sudo_sha512_pass: "' + sha512_hash + '"\n')
    file.close()

    vault_command.append(name)

''' encrypt files '''

call(vault_command)

print "All files have been generated.\n"

