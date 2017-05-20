#!/bin/env
import sys
import time
import re
from robobrowser import RoboBrowser
import time
import random
import hashlib
import httplib	
import requests
import json
import platform

"""
This program takes commandline argument as
	$python codeforces.py c|C|p|P [Filename_with_extension]
	
c 	: Contest
p 	: Practice
pc 	: past contest
Filename must be same of problem code
File may not reside in the same directory
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#Add these fields as required
User = {
	'handle' 	: '',
	'password' 	: '',
	'key' 		: '',
	'secret' 	: ''
}
base_url = 'http://www.codeforces.com/enter'
browser = RoboBrowser(parser="lxml")
delay = 15

def get_Problem_Code(prog,char):
	"""Gets Problem code if the file name and the problem code is similar,
		for example, if the file name is CHEFCODE.cpp the problem code will be like CHEFCODE
	"""
	s = prog
	while True:
		i = s.find(char) 
		if i == -1:
			break
		s = s[i+1:]

	return s[:s.find('.')]

def get_char():
	os = platform.system()
	char =''
	if os == 'Windows':
		char = '\\'
	elif os == 'Linux':
		char ='/'
	return char


if len(sys.argv) != 3 :
	print bcolors.FAIL + bcolors.BOLD + "Command Error: $python codeforces.py pc|p|c <source_file>" + bcolors.ENDC
	print bcolors.WARNING + "Source file Name : PROBLEMNAME.extension " + bcolors.ENDC
	exit(0)

p_type = str(sys.argv[1]) 
prog = str(sys.argv[2]) # file name
problem_code = get_Problem_Code(prog,get_char())
problem_index = problem_code[-1]
contest_code = ''

"""
Check validity of Problem_code
"""
p = re.compile('\d{3}[A-G]{1}')
m = p.match(problem_code)
if m is None:
	print bcolors.FAIL + "Problem Code/Contest Code Invalid" + bcolors.ENDC
	exit(0)


"""
Set Language according to Extension
"""
lang_code = 0
#add your suitable language
if prog.endswith('.cpp'):
	lang_code = 42 # GNU G++11 5.1.0
elif prog.endswith('.py'):
	lang_code = 7 # Python 2.7.12
elif prog.endswith('.java'):
	lang_code = 36
else:
	print "Enter Valid Program"
	exit(0)

print bcolors.OKBLUE +  "Connecting to the Server" + bcolors.ENDC

"""
Login to Codeforces.com
"""
browser.open(base_url)
form = browser.get_form(id='enterForm')
if form == None:
	print bcolors.FAIL + "Server Busy. Retry Later" + bcolors.ENDC
	exit(0)
form['handle'] = User['handle']
form['password'] = User['password']
browser.submit_form(form)

#go to a problem
print bcolors.OKBLUE +  "Logged In to Codeforces for : " + User['handle'] + bcolors.ENDC

if p_type == "C" or p_type == "c" or p_type == "pc": #contest or past contest
	contest_code = problem_code[:-1]
	problem_url = 'http://codeforces.com/contest/'+contest_code+'/submit'
elif p_type == "P" or p_type == "p":
	problem_url = 'http://codeforces.com/problemset/submit'

browser.open(problem_url)

if p_type == "C" or p_type == "c": #Running Contest
	form = browser.get_forms()[1]
	form['submittedProblemIndex'].value = str(problem_index)
elif p_type == "pc": #Past Contest
	form = browser.get_forms()[1]
	form['submittedProblemIndex'].value = str(problem_index)
elif p_type == "P" or p_type == "p":
	form = browser.get_forms()[1]
	form['submittedProblemCode'] = str(problem_code)
	#exit(0)

form['programTypeId'].value = str(lang_code)
form['sourceFile'].value = open(prog,'r')
browser.submit_form(form)
print bcolors.OKBLUE +  "Submitted. Waiting for Verdict" + bcolors.ENDC
# give time to submit
time.sleep(delay)	#wait for 15s

#verdict
apikey = User['key']
#print apikey
utime = str(int(time.time()))
apiSig = str(random.randint(000000,999999))
method = 'user.status'
handle = User['handle']
string_1 = method+'?handle='+User['handle']+'&from=1&count=1&apiKey='+apikey+'&time='+utime
hash_string = apiSig+'/'+method+'?apiKey='+apikey+'&count=1&from=1&handle='+User['handle']+'&time='+utime+'#'+User['secret']
m = hashlib.sha512()
m.update(hash_string)
url_string = 'http://codeforces.com/api/'+string_1 +'&apiSig='+apiSig+m.hexdigest()

r = requests.get(url_string)
data = r.json()
js_data = json.dumps(data,indent=4)
#print js_data
#info = json.loads(str(data))
status = data["status"]
if status == "FAILED":
	print data["comment"]
	exit(0)
res = data["result"][0]
#print res
info = json.dumps(res,indent = 4)
#print info
verdict =  res["verdict"]
mem_taken = res["memoryConsumedBytes"]
time_taken = res["timeConsumedMillis"]


print "\nYOUR RESULT:"
print "Verdict:",
if verdict == "OK":
	print bcolors.OKGREEN + bcolors.BOLD + "Accepted" + bcolors.ENDC
elif verdict == "WRONG_ANSWER":
	print bcolors.FAIL + bcolors.BOLD + "Wrong Answer" + bcolors.ENDC
elif verdict == "TIME_LIMIT_EXCEEDED":
	print bcolors.WARNING + bcolors.BOLD + "Time Limit Exceeded" + bcolors.ENDC
else:
	print verdict
print "Time Taken:",time_taken,"ms"
print "Memory Used:",mem_taken, "bytes"
