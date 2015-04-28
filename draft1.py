
#!/usr/bin/env python
#from __future__ import print_function
import os, time, csv, re

time_period_for_showing_data = input("In what time period do you want to see the output? ")
time_period_for_IO = input("In what time period do you want to see the output? ")
software = raw_input("Enter the software you want to check:")
time_period = raw_input("How long do you want to test the process? 00:00:00 ")
time_difference = map(int, re.split(r"[:,]",time_period))
time_difference_in_seconds = time_difference[0]*3600+time_difference[1]*60+time_difference[2]
st = os.popen("date +%s")
starting_time = st.read()
ending_time = int(starting_time)+int(time_difference_in_seconds)
output_file = open("test.csv", 'w')
while int(starting_time) < ending_time:
    #mylist = []
    time.sleep(time_period_for_showing_data)
    list_of_two_IO = []
    #Get IO
    for i in range(2):
        IO = os.popen("netstat -s|egrep '(InOctets|OutOctets)'")
        io = IO.read()
        splited_set = io.split()
        list_of_two_IO.append(splited_set[1])
        list_of_two_IO.append(splited_set[3])
        if i: break
        time.sleep(time_period_for_IO)
    Difference_InOctets_rbt = int(list_of_two_IO[3]) - int(list_of_two_IO[1])
    Difference_OutOctets_tbt = int(list_of_two_IO[2]) - int(list_of_two_IO[0])
    #Get Mem|Swap
    memswap = os.popen("egrep 'Mem|Swap' /proc/meminfo",'r')
    ms = memswap.readlines()
    msdict = dict()
    for i in ms:
        sublinelist = i.split()
        if int(sublinelist[1])!=0:
            msdict[sublinelist[0]]=float(sublinelist[1])
    mom_percentage = msdict['MemFree:']/msdict['MemTotal:']
    swap_percentage = msdict['SwapFree:']/msdict['SwapTotal:']
    #Get get timestamp
    timestamp = os.popen("date +%s")
    t = timestamp.read()
    check_time = time.strftime("%m-%d_%H:%M:%S", time.localtime(int(t)))
    #Get load over 1 minute
    loadline = os.popen("uptime")
    la = loadline.read()
    load_over_last_one_minute = la.split()[-3].strip(',')
    #Get CPU
    runningsoftware = os.popen("ps -aux")
    s = runningsoftware.readlines()
    selecting_software = dict()
    CPU_total = 0
    for i in s[1:]:
        if software in i:
            line_info_list = i.split()
            selecting_software[software]=line_info_list[2]
        CPU_total += float(i.split()[2])
    mylist = [check_time, load_over_last_one_minute, Difference_InOctets_rbt, Difference_OutOctets_tbt, mom_percentage, swap_percentage, selecting_software[software], CPU_total]
    ss = os.popen("date +%s")
    starting_time = ss.read()
    print >>output_file, ','.join([str(i) for i in mylist]).encode("utf-8")
output_file.close()
