from setuptools import setup
import sys

if sys.version_info < (2,7) and sys.version_info >= (3,0):
    sys.exit('Sorry, Python < 2.7 and Python > 3.0 is not supported')

setup(name="Autosubmission",
	version="0.0.1",
	description="Auto submit to Codechef or Codeforces",
	author="Bihan Sen",
	author_email="senbihan@gmail.com",
	#packages=['codechef'],
	install_requires=[
		'robobrowser',
		'BeautifulSoup'
		]
	)
