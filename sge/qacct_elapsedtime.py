#~/usr/bin/python

import os, sys, time
from datetime import datetime
from datetime import timedelta

args = sys.argv

try:
    jstart = args[1]
    jend = args[2]
except:
    print "python qacct_elapstedtime.py start_job_id end_job_id"
    sys.exit(0)

sum_h = 0
sum_m = 0
sum_s = 0
sum_c = 0

for i in range( int(jstart), int(jend)+1 ):
    times = os.popen( "qacct -j "+str(i)+" | egrep '^[s|e]' | grep time" ).read()
    times = times.strip()
    start,end = times.split('\n')
    start_y,start_m,start_d = start.split()[5], start.split()[2], start.split()[3]
    start_time = start.split()[4]
    end_y,end_m,end_d = end.split()[5], end.split()[2], end.split()[3]
    end_time = end.split()[4]


    FMT = '%Y:%b:%d:%H:%M:%S'
    tdelta = datetime.strptime( end_y+':'+end_m+':'+end_d+':'+end_time,FMT ) - \
            datetime.strptime( start_y+':'+start_m+':'+start_d+':'+start_time,FMT )

    d = int(tdelta.days)
    h,m,s = str(timedelta(seconds=tdelta.seconds)).split(':')

    sum_h += int(h)+(d*24)
    sum_m += int(m)
    sum_s += int(s)

    sum_c += 1

tot_s = 60*60*sum_h + 60*sum_m + sum_s
avg_s = int( tot_s / sum_c )

print 'jid: ', jstart+'-'+jend
print 'sum: ', tot_s
print 'cnt: ', sum_c
d,h,m,s = str(time.strftime("%d:%H:%M:%S", time.gmtime(avg_s))).split(':')
h = (int(d)-1)*24+int(h)
print 'avg: ', ':'.join([str(h),str(m),str(s)])
