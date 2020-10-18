import requests
from bs4 import BeautifulSoup as BS
import re

def getMonth(m):
	return {
		'janúar' : '01',
		'febrúar' : '02',
		'mars' : '03',
		'apríl' : '04',
		'maí' : '05',
		'júní' : '06',
		'júlí' : '07',
		'ágúst' : '08',
		'september' : '09',
		'október' : '10',
		'nóvember' : '11',
		'desember' : '12'
	}[m]

def pad(s):
	st = str(s)
	if len(st) == 1:
		return "0" + st
	elif (len(st) == 2):
		return st
	else:
		return "00"

def fetchMOP(id): # Sækja grunngögn um þingmann
	page = requests.get("https://www.althingi.is/altext/cv/?nfaerslunr=" + str(id))
	soup = BS(page.text, "html.parser")
	els = soup.select("td p")

	if len(els) > 0: # Þingmaður er á skrá
		res_name = soup.h1.text.strip()
		text = els[0].text.replace("(", "").replace(")", "")
		reBirthDeath = re.compile(r"(Fædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4})")
		reBirth = re.compile(r"(Fædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4})")

		if reBirthDeath.match(text):
			grps = reBirthDeath.match(text).groups()
		elif reBirth.match(text): # RegEx finnur ekki bæði fæðingar- og dauðadag, leitar að bara fæðingardegi
			grps = reBirth.match(text).groups()
		else:
			return None
		
		res_birth = grps[3] + "-" + getMonth(grps[2]) + "-" + pad(grps[1])
		if len(grps[0]) == 4:
			res_gender = 'kvk'
		else:
			res_gender = 'kk'

		if len(grps) > 4:
			res_death = grps[6] + "-" + getMonth(grps[5]) + "-" + pad(grps[4])
			return (res_name, res_gender, res_birth, res_death)
		else:
			return (res_name, res_gender, res_birth)
	else:
		return None

for i in range(1, 10):
	print(i)
	res = fetchMOP(i)
	if res != None:
		print(res)