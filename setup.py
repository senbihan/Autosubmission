from setuptools import setup

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