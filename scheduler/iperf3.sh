iperf3 -c 192.168.3.131 -b 512K -t 100 -p 5201 > /dev/null 2>&1 &
iperf3 -c 192.168.3.131 -b 512K -R -t 100 -p 5202 > /dev/null 2>&1 &