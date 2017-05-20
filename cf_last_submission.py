# codeforces api

import time
import random
import hashlib
import httplib	
import requests
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

User = {
	'handle' 	: 'your handle',
	'key' 		: 'your key',
	'secret' 	: 'your secret'
}

apikey = User['key']
#print apikey
utime = str(int(time.time()))
apiSig = str(random.randint(000000,999999))
method = 'user.status'
handle = User['handle']
#Don't change these
string_1 = method+'?handle='+User['handle']+'&from=1&count=1&apiKey='+apikey+'&time='+utime
hash_string = apiSig+'/'+method+'?apiKey='+apikey+'&count=1&from=1&handle='+User['handle']+'&time='+utime+'#'+User['secret']
m = hashlib.sha512()
m.update(hash_string)
url_string = 'http://codeforces.com/api/'+string_1 +'&apiSig='+apiSig+m.hexdigest()
r = requests.get(url_string)
data = r.json()
js_data = json.dumps(data,indent=4)

status = data["status"]
if status == "FAILED":
	print data["comment"]
	exit(0)
res = data["result"][0]

info = json.dumps(res,indent = 4)

verdict =  res["verdict"]
mem_taken = res["memoryConsumedBytes"]
time_taken = res["timeConsumedMillis"]



print "\nYOUR RESULT: "
print "Verdict: ",
if verdict == "OK":
	print bcolors.OKGREEN + "Accepted" + bcolors.ENDC
elif verdict == "WRONG_ANSWER":
	print bcolors.WARNING + "Wrong Answer" + bcolors.ENDC
else:
	print verdict
print "Time Taken: ",time_taken," ms"
print "Memory Used: ",mem_taken, "bytes"
