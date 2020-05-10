#!/usr/bin/python

import threading
import queue
import sys
import argparse
from passlib.hash import argon2

helptext="""
  
     _    ____   ____  ___  _   _ ____      ____ ____      _    ____ _  __  
    / \  |  _ \ / ___|/ _ \| \ | |___ \    / ___|  _ \    / \  / ___| |/ /  
   / _ \ | |_) | |  _| | | |  \| | __) |  | |   | |_) |  / _ \| |   | ' /   
  / ___ \|  _ <| |_| | |_| | |\  |/ __/   | |___|  _ <  / ___ \ |___| . \   
 /_/   \_\_| \_\\____|\___/|_| \_|_____|   \____|_| \_\/_/   \_\____|_|\_\  
  
A quick and dirty password cracker script to crack argon2 hashes based on python passlib.  
Note: install argon2-cffi or argon2pure for the script to work  
  
Author - DotDotSlash https://github.com/DotDotSlashRepo 
Version 1.0
  
"""

print(helptext)

parser = argparse.ArgumentParser(description='Script to crack argon2 hashes.')
parser.add_argument('--threads', default=30,nargs='?', const=30, type=int, help='number of threads for execution, by default up-to 30 threads are used')
parser.add_argument('--passwordlist',default='10k-most-common.txt', type=str, help='wordlist file for password cracking, uses 10k-most-common.txt by default',nargs='?',const='10k-most-common.txt')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('--hashlist', type=str, help='file containing argon2 hashes, in the format username:password_hash', required=True)
args = parser.parse_args()
argv=vars(args)
hashFile=argv['hashlist']
passwordFile=argv['passwordlist']
Threadcount=argv['threads']
 
if(Threadcount<1):
    Threadcount=30
hashList = open(hashFile,'r').read().splitlines()
passwordList = open(passwordFile,'r').read().splitlines()
 
class WorkerThread(threading.Thread) :
 
    def __init__(self, queue, tid) :
        threading.Thread.__init__(self)
        self.queue = queue
        self.tid = tid
 
    def run(self) :
        while True :
            passwordHash = None 
            try :
                passwordHash = self.queue.get(block=True,timeout=1)
                if (passwordHash.count(':') != 1):
                    print("[x]ERROR! Invalid hash format: "+passwordHash)
                    return
                username= passwordHash.split(':')[0]
                encryptedPassword= passwordHash.split(':')[1]
            except :
                return
 
            try :
                cracked=0
                for password in passwordList:
                                    passwordCheck = argon2.verify(password, encryptedPassword)
                                    if(passwordCheck==True):
                                            print("[+] Successful Login! Username: " + username + " Password: " + password + "(" + passwordHash + ")")
                                            cracked=1
                                            break
                if(cracked==0):
                    print("[!] Unable to crack: " + username + " Password: " + encryptedPassword)
            except :
                raise 
 
            self.queue.task_done()
 
queue = queue.Queue()
 
threads = []
for i in range(1, Threadcount) : 
    worker = WorkerThread(queue, i) 
    worker.setDaemon(True)
    worker.start()
    threads.append(worker)
 
for passwordHash in hashList :
    queue.put(passwordHash)
 
queue.join()
 
 
for item in threads :
    item.join()
 
print("Cracking Complete!")