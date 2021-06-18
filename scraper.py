import requests
from bs4 import BeautifulSoup as BS
import re

def getMonth(m):
	return {
		'janúar' : '01',
		'jan.' : '01',
		'febrúar' : '02',
		'feb.' : '02',
		'mars' : '03',
		'mar.' : '03',
		'apríl' : '04',
		'apr.' : '04',
		'maí' : '05',
		'júní' : '06',
		'jún.' : '06',
		'júlí' : '07',
		'júl.' : '07',
		'júlí júní' : '06',
		'ágúst' : '08',
		'ág.' : '08',
		'ágú.' : '08',
		'september' : '09',
		'sep.' : '09',
		'sept.' : '09',
		'október' : '10',
		'okt.' : '10',
		'nóvember' : '11',
		'nóv.' : '11',
		'desember' : '12',
		'des.' : '12',
		'desembre' : '12'
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
	els = soup.select("p")

	if len(soup.select("h1")) > 0: # Þingmaður er á skrá
		res_name = soup.h1.text.strip()
		fulltext = ""
		for elmt in els:
			fulltext += elmt.text + " ::: "
		text = fulltext.replace("(", "").replace(")", "")
		reBirthDeath = re.compile(r".*?(Fædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4})")
		reBirth = re.compile(r".*?(Fædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4})")
		reParty = re.compile(r".*?(?:Alþingismaður|Varaþingmaður) .*? \((.*?flokkur.*?)\)")
		reParents = re.compile(r".*?[Ff]oreldrar:(.*?)([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4}).*? og .*? ([AÁBCDEFGHIÍJKLMNOÓPQRSTUÚVWXYÝZÞÆÖ].*?) ([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4})")
		reParentsFirstAlive = re.compile(r".*?[Ff]oreldrar:(.*?)([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}).*? og.*?([AÁBCDEFGHIÍJKLMNOÓPQRSTUÚVWXYÝZÞÆÖ].*?) ([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4})")
		reParentsSecondAlive = re.compile(r".*?[Ff]oreldrar:(.*?)([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4}).*? og.*?([AÁBCDEFGHIÍJKLMNOÓPQRSTUÚVWXYÝZÞÆÖ].*?) ([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4})")
		reParentsBothAlive = re.compile(r".*?[Ff]oreldrar:(.*?)([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}).*? og.*?([AÁBCDEFGHIÍJKLMNOÓPQRSTUÚVWXYÝZÞÆÖ].*?) ([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4})")

		if reBirthDeath.match(text):
			grps = reBirthDeath.match(text).groups()
		elif reBirth.match(text): # RegEx finnur ekki bæði fæðingar- og dauðadag, leitar að bara fæðingardegi
			grps = reBirth.match(text).groups()
		else:
			return None
		
		res_birth = grps[3] + "-" + getMonth(grps[2]) + "-" + pad(grps[1])
		if len(grps[0]) == 4:
			res_gender = 'f'
		else:
			res_gender = 'm'

		if len(grps) > 4:
			res_death = grps[6] + "-" + getMonth(grps[5]) + "-" + pad(grps[4])
		else:
			res_death = "1000-01-01"

		if reParty.match(fulltext):
			grps = reParty.match(fulltext).groups()
			if grps[0].find("(") > 0:
				res_party = grps[0][grps[0].find("("):]
			else:
				res_party = grps[0]
		else:
			res_party = ""
		if reParents.match(text):
			grps = reParents.match(text).groups()

			if len(grps[1]) == 4:
				res_parent1_gender = "f"
			else:
				res_parent1_gender = "m"

			if len(grps[9]) == 4:
				res_parent2_gender = "f"
			else:
				res_parent2_gender = "m"

			res_parent1_birth = grps[4] + "-" + getMonth(grps[3]) + "-" + pad(grps[2])
			res_parent1_death = grps[7] + "-" + getMonth(grps[6]) + "-" + pad(grps[5])
			res_parent1_name = grps[0].strip()
			res_parent2_birth = grps[12] + "-" + getMonth(grps[11]) + "-" + pad(grps[10])
			res_parent2_death = grps[15] + "-" + getMonth(grps[14]) + "-" + pad(grps[13])
			res_parent2_name = grps[8].strip()

			return ((res_name, res_gender, res_birth, res_death, res_party), (res_parent1_name, res_parent1_gender, res_parent1_birth, res_parent1_death), (res_parent2_name, res_parent2_gender, res_parent2_birth, res_parent2_death))
		elif reParentsFirstAlive.match(text):
			grps = reParentsFirstAlive.match(text).groups()

			if len(grps[1]) == 4:
				res_parent1_gender = "f"
			else:
				res_parent1_gender = "m"

			if len(grps[6]) == 4:
				res_parent2_gender = "f"
			else:
				res_parent2_gender = "m"

			res_parent1_birth = grps[4] + "-" + getMonth(grps[3]) + "-" + pad(grps[2])
			res_parent1_death = "1000-01-01"
			res_parent1_name = grps[0].strip()
			res_parent2_birth = grps[9] + "-" + getMonth(grps[8]) + "-" + pad(grps[7])
			res_parent2_death = grps[12] + "-" + getMonth(grps[11]) + "-" + pad(grps[10])
			res_parent2_name = grps[5].strip()

			return ((res_name, res_gender, res_birth, res_death, res_party), (res_parent1_name, res_parent1_gender, res_parent1_birth, res_parent1_death), (res_parent2_name, res_parent2_gender, res_parent2_birth, res_parent2_death))
		elif reParentsSecondAlive.match(text):
			grps = reParentsSecondAlive.match(text).groups()

			if len(grps[1]) == 4:
				res_parent1_gender = "f"
			else:
				res_parent1_gender = "m"

			if len(grps[9]) == 4:
				res_parent2_gender = "f"
			else:
				res_parent2_gender = "m"

			res_parent1_birth = grps[4] + "-" + getMonth(grps[3]) + "-" + pad(grps[2])
			res_parent1_death = grps[7] + "-" + getMonth(grps[6]) + "-" + pad(grps[5])
			res_parent1_name = grps[0].strip()
			res_parent2_birth = grps[12] + "-" + getMonth(grps[11]) + "-" + pad(grps[10])
			res_parent2_death = "1000-01-01"
			res_parent2_name = grps[8].strip()

			return ((res_name, res_gender, res_birth, res_death, res_party), (res_parent1_name, res_parent1_gender, res_parent1_birth, res_parent1_death), (res_parent2_name, res_parent2_gender, res_parent2_birth, res_parent2_death))
		elif reParentsBothAlive.match(text):
			grps = reParentsBothAlive.match(text).groups()

			if len(grps[1]) == 4:
				res_parent1_gender = "f"
			else:
				res_parent1_gender = "m"

			if len(grps[6]) == 4:
				res_parent2_gender = "f"
			else:
				res_parent2_gender = "m"

			res_parent1_birth = grps[4] + "-" + getMonth(grps[3]) + "-" + pad(grps[2])
			res_parent1_death = "1000-01-01"
			res_parent1_name = grps[0].strip()
			res_parent2_birth = grps[9] + "-" + getMonth(grps[8]) + "-" + pad(grps[7])
			res_parent2_death = "1000-01-01"
			res_parent2_name = grps[5].strip()

			return ((res_name, res_gender, res_birth, res_death, res_party), (res_parent1_name, res_parent1_gender, res_parent1_birth, res_parent1_death), (res_parent2_name, res_parent2_gender, res_parent2_birth, res_parent2_death))
		else:
			return ((res_name, res_gender, res_birth, res_death, res_party), (), ())
	else:
		return None
