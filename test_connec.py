import pexpect, time
import os
import time

child = pexpect.spawn('ssh hsekhon@login.hpc.caltech.edu')
child.logfile = open("mylog", "wb")
child.expect("assword", timeout=120)
child.sendline('ILikethebeatles2022')

child.expect('(1-1)', timeout=120)
child.sendline('1')

child.expect("~]", timeout=10)
child.sendline('squeue -u hsekhon')
child.expect("~]", timeout=10)

print(
    child.before
)
