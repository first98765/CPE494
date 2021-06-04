###########################################################
# This code using for study in network searching devices 
# in your local network and showing IP address and 
# the name of the device.
###########################################################
# Create by: Mr.Supakij Buasod (61070503438)
# Update: 04/06/2021

#!/usr/bin/env python3

import os
import socket    
import multiprocessing
import subprocess
import os
import sys

#Find my IP address
def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def map_network():
	# Define variable for keeping the IP that we found
    ip_list = list()
    # get my IP and split it with dot.
    ip_parts = get_my_ip().split('.')
    # From this we use only first three number of our IP address.
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(255)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list

def pinger(job_q, results_q):
    DEVNULL = open(os.devnull, 'w')
    while True:
        ip = job_q.get()
        if ip is None:
            break
        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

program_val = 0

# def main():
if __name__ == '__main__':

    while 1:
    	print('Hello, ' + os.getlogin() + '!')
    	print (" WELCOME ".center(40, '-'))
    	print ("|-- Please select the program")
    	print ("|-- 1. Get my IP address")
    	print ("|-- 2. IP Scanner")
    	print ("|-- 3. Exit")
    	print ("".center(40, '-'))

    	try:
    	    program_val = int(input('|--> Select: '))
    	except:
    	    print("That's not a valid option!")
    	    program_val = 0

        if program_val == 0:
            program_val = 0

        if program_val == 1:
            print (" Get my IP address ".center(40, '='))
            print('>> My IP address is : '+ get_my_ip())
            print ("".center(40, '=')+"\n")
            program_val = 0

        if program_val == 2:
            print('|- Mapping...')
            lst = map_network()
            # print('\n'.join(map(str, lst)))
            
            length = len(lst)
            
            for i in range(length):
                    try:
                        host = socket.gethostbyaddr(lst[i])[0]   
                        print("|- IP Address: {0:<15}| Name: {1:<20}".format(lst[i], host)) 
                        # print("|- IP Address: " + lst[i] + " | Name: '".rjust(30) + host + "'")

                    except socket.herror:
                        pass
            print("\n")
            program_val = 0

        if program_val == 3:
            print (" ~Have a good day~ ".center(40, '*') + "\n")
            break