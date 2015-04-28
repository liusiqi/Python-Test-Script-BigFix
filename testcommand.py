#!/usr/bin/env python
from __future__ import print_function
import os,time

print('start testing\n')
print('#1command for Mem|Swap')
memswap = os.popen("egrep 'Mem|Swap' /proc/meminfo",'r')
ms = memswap.readlines()
msdict = dict()
for i in ms:
    sublinelist = i.split()
    if int(sublinelist[1]) != 0:
        msdict[sublinelist[0]] = float(sublinelist[1])
mom = msdict['MemFree:']/msdict['MemTotal:']
swap = msdict['SwapFree:']/msdict['SwapTotal:']
print(mom,swap)
print()
print('#2command for timestamp')
timestamp = os.popen("date +%s")
t = timestamp.read()
print(t, end = '')
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t))))
print()
print('#3command for load')
loadaverage = os.popen("uptime")
la = loadaverage.read()
print(la.split(),end='')
print()
print('#4command for CPU')
#softwarename = input("Enter the software you want to check: ").strip()
runningsoftware = os.popen("ps -aux")
s = runningsoftware.readlines()
for i in s[1:]:
    if float(i.split()[2])>0:
        print(i.split()[0],i.split()[1],i.split()[2])
print()
print('5command for I/O')
l = []
for i in range(2):
    IO = os.popen("netstat -s|egrep '(InOctets|OutOctets)'")
    io = IO.read()
    print(io.split())
    l.append(io.split()[1])
    l.append(io.split()[3])
    time.sleep(3)
print(l)
InP = (int(l[3])-int(l[1]))
OutP = (int(l[2])-int(l[0]))
print(InP,OutP)

