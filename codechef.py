import re
from robobrowser import RoboBrowser
import sys
from bs4 import BeautifulSoup
import requests
import platform
import time

"""
This program takes commandline argument as
	$python codechef.py c|p [path_to_Filename_with_extension]
	
c 	: Contest
p 	: Practice
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

User = {
	'username'		:	'user_name',
	'password'		:	'password'
}

#add your suitable language and code from codechef submit drop down menu
langList = {
	'cpp' 	: 	'44',
	'py'  	:	'4',
	'c'		:	'11',
	'java'	:	'10'
}

delay = 30 # delay to show the verdict once submitted. Adjust as required

def login():
	browser = RoboBrowser(parser="html.parser")
	browser.open("https://www.codechef.com")
	login_form = browser.get_forms()[0]
	if login_form == None:
		print "Some Error Occurred"
		exit(0)
	login_form['name'] = User['username']
	login_form['pass'] = User['password']
	browser.submit_form(login_form)
	#authentication yet to be implemented
	return browser

def login_Until():
	br = login()
	while True:
		#print br
		if br.url == "https://www.codechef.com/node" or br.url == "https://www.codechef.com/":
			print bcolors.OKGREEN +  "Successfully Logged In" + bcolors.ENDC
			break
		elif br.url == "https://www.codechef.com/session/limit":
			sess_form = br.get_form(id='session-limit-page')
			if sess_form == None :
				continue
			opList = sess_form['sid'].options
			sess_form['sid'].value = opList[0]
			br.submit_form(sess_form)
		else:
			#print br.url
			br = login()
	return br
 
def get_Problem_Code(prog):
	"""Gets Problem code if the file name and the problem code is similar,
		for example, if the file name is CHEFCODE.cpp and the problem code is CHEFCODE
	"""
	os = platform.system()
	char =''
	if os == 'Windows':
		char = '\\'
	elif os == 'Linux':
		char ='/'
	s = prog
	while True:
		i = s.find(char) 
		if i == -1:
			break
		s = s[i+1:]

	return s[:s.find('.')]


if __name__ == '__main__':
	
	if len(sys.argv) != 3 :
		print bcolors.FAIL + bcolors.BOLD + "Command Error: $python codechef.py p|c <path_to_source_file>" + bcolors.ENDC
		exit(0)
	
	browser = login_Until()

	prob_type = sys.argv[1]
	prog = sys.argv[2]

	#prob_code = get_Problem_Code(prog) #use this if you submit your source file as problem code 

	prog_lang = prog[prog.find('.')+1:]
	prob_code = raw_input('Problem Code: ')
	if prob_type == 'p':
		sub_url = 'https://www.codechef.com/submit/'+prob_code
		res_url = url = 'https://www.codechef.com/status/'+prob_code+','+User["username"]
	elif prob_type == 'c':
		contest = raw_input('Enter Contest Code: ')
		sub_url = 'https://www.codechef.com/'+contest+'/submit/'+prob_code
		res_url = url = 'https://www.codechef.com/'+contest+'/status/'+prob_code+','+User["username"];
	else:
		print bcolors.FAIL + bcolors.BOLD + "Command Error: $python codechef.py p|c <path_to_source_file>" + bcolors.ENDC
		exit(0)

	browser.open(sub_url)
	subForm = browser.get_form(id='problem-submission')
	if subForm == None:
		print bcolors.FAIL +"Some Error Occured! Retry. [Authentication Problem] " + bcolors.ENDC
		exit(0)

	subForm['files[sourcefile]'].value = open(prog,'r')
	subForm['language'].value = langList[prog_lang]

	browser.submit_form(subForm)
	print bcolors.OKBLUE + "Succesfully Submitted..." + bcolors.ENDC

	print bcolors.OKBLUE + "Waiting for Verdict..."  + bcolors.ENDC
	time.sleep(delay)


	f = requests.get(res_url)
	soup = BeautifulSoup(f.text,"html.parser")
	t = soup.find_all("table",{"class" : "dataTable"})
	area = t[0].tbody.tr
	if area.img == None:
		print bcolors.FAIL + "Error! Please Check Verdict on site : " + res_url + bcolors.ENDC
		exit(0)

	res_img = area.img['src']
	if res_img.endswith('tick-icon.gif'):
		print bcolors.OKGREEN + bcolors.BOLD + "Accepted" + bcolors.ENDC
	elif res_img.endswith('alert-icon.gif'):
		print bcolors.WARNING + bcolors.BOLD + "Compilation Error" + bcolors.ENDC
	elif res_img.endswith('cross-icon.gif'):
		print bcolors.FAIL + bcolors.BOLD + "Wrong Answer" + bcolors.ENDC
	elif res_img.endswith('runtime-error.png'):
		print bcolors.FAIL + bcolors.BOLD + "Runtime Error" + bcolors.ENDC
	elif res_img.endswith('clock_error.png'):
		print bcolors.WARNING + bcolors.BOLD + "Time Limit Exceeded" + bcolors.ENDC