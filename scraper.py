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

def fetchMOP(id):
	page = requests.get("https://www.althingi.is/altext/cv/?nfaerslunr=" + str(id))
	soup = BS(page.text, "html.parser")
	els = soup.select("td p")

	if len(els) > 0:
		res_name = soup.h1.text
		text = els[0].text
		reBirthDeath = re.compile(r"(Fædd[u]?).*? ([0-9]{1,2}). (.*?) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4})")
		reBirth = re.compile(r"(Fædd[u]?).*? ([0-9]{1,2}). (.*?) ([0-9]{4})")

		grps = reBirthDeath.match(text).groups()
		
		if len(grps) == 0:
			grps = reBirth.match(text).groups()

			if len(grps) == 0:
				return None
		
		res_birth = grps[3] + "-" + getMonth(grps[2]) + "-" + pad(grps[1])
		if len(grps[0]) == 4:
			res_gender = 'kvk'
		else:
			res_gender = 'kk'

		return (res_name, res_gender, res_birth)
	else:
		return None

print(fetchMOP(61))