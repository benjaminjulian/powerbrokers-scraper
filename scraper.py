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
		reParents = re.compile(r".*?[Ff]oreldrar:(.*?)([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4}).*? og.*?(([AÁBCDEFGHIÍJKLMNOÓPQRSTUÚVXYÝZÞÆÖ].*? ){1,4}).*?([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4})")
		reParentsFirstAlive = re.compile(r".*?[Ff]oreldrar:(.*?)([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}).*? og.*?(([AÁBCDEFGHIÍJKLMNOÓPQRSTUÚVXYÝZÞÆÖ].*? ){1,4}).*?([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4})")
		reParentsSecondAlive = re.compile(r".*?[Ff]oreldrar:(.*?)([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}), dáin[n]? ([0-9]{1,2}). (.*?) ([0-9]{4}).*? og.*?(([AÁBCDEFGHIÍJKLMNOÓPQRSTUÚVXYÝZÞÆÖ].*? ){1,4}).*?([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4})")
		reParentsBothAlive = re.compile(r".*?[Ff]oreldrar:(.*?)([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4}).*? og.*?(([AÁBCDEFGHIÍJKLMNOÓPQRSTUÚVXYÝZÞÆÖ].*? ){1,4}).*?([Ff]ædd[u]?).{0,40}? ([0-9]{1,2})\. (.{1,10}) ([0-9]{4})")

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
		else:
			res_death = "0000-00-00"
		
		if reParents.match(text):
			grps = reParents.match(text).groups()

			if len(grps[1]) == 4:
				res_parent1_gender = "kvk"
			else:
				res_parent1_gender = "kk"

			if len(grps[10]) == 4:
				res_parent2_gender = "kvk"
			else:
				res_parent2_gender = "kk"

			res_parent1_birth = grps[4] + "-" + getMonth(grps[3]) + "-" + pad(grps[2])
			res_parent1_death = grps[7] + "-" + getMonth(grps[6]) + "-" + pad(grps[5])
			res_parent1_name = grps[0].strip()
			res_parent2_birth = grps[13] + "-" + getMonth(grps[12]) + "-" + pad(grps[11])
			res_parent2_death = grps[16] + "-" + getMonth(grps[15]) + "-" + pad(grps[14])
			res_parent2_name = grps[8].strip()

			return ((res_name, res_gender, res_birth, res_death), (res_parent1_name, res_parent1_gender, res_parent1_birth, res_parent1_death), (res_parent2_name, res_parent2_gender, res_parent2_birth, res_parent2_death))
		elif reParentsFirstAlive.match(text):
			grps = reParentsFirstAlive.match(text).groups()

			if len(grps[1]) == 4:
				res_parent1_gender = "kvk"
			else:
				res_parent1_gender = "kk"

			if len(grps[10]) == 4:
				res_parent2_gender = "kvk"
			else:
				res_parent2_gender = "kk"

			res_parent1_birth = grps[4] + "-" + getMonth(grps[3]) + "-" + pad(grps[2])
			res_parent1_death = "0000-00-00"
			res_parent1_name = grps[0].strip()
			res_parent2_birth = grps[10] + "-" + getMonth(grps[9]) + "-" + pad(grps[8])
			res_parent2_death = grps[13] + "-" + getMonth(grps[12]) + "-" + pad(grps[11])
			res_parent2_name = grps[5].strip()

			return ((res_name, res_gender, res_birth, res_death), (res_parent1_name, res_parent1_gender, res_parent1_birth, res_parent1_death), (res_parent2_name, res_parent2_gender, res_parent2_birth, res_parent2_death))
		elif reParentsSecondAlive.match(text):
			grps = reParentsSecondAlive.match(text).groups()

			if len(grps[1]) == 4:
				res_parent1_gender = "kvk"
			else:
				res_parent1_gender = "kk"

			if len(grps[10]) == 4:
				res_parent2_gender = "kvk"
			else:
				res_parent2_gender = "kk"

			res_parent1_birth = grps[4] + "-" + getMonth(grps[3]) + "-" + pad(grps[2])
			res_parent1_death = grps[7] + "-" + getMonth(grps[6]) + "-" + pad(grps[5])
			res_parent1_name = grps[0].strip()
			res_parent2_birth = grps[13] + "-" + getMonth(grps[12]) + "-" + pad(grps[11])
			res_parent2_death = "0000-00-00"
			res_parent2_name = grps[8].strip()

			return ((res_name, res_gender, res_birth, res_death), (res_parent1_name, res_parent1_gender, res_parent1_birth, res_parent1_death), (res_parent2_name, res_parent2_gender, res_parent2_birth, res_parent2_death))
		elif reParentsBothAlive.match(text):
			grps = reParentsBothAlive.match(text).groups()

			if len(grps[1]) == 4:
				res_parent1_gender = "kvk"
			else:
				res_parent1_gender = "kk"

			if len(grps[10]) == 4:
				res_parent2_gender = "kvk"
			else:
				res_parent2_gender = "kk"

			res_parent1_birth = grps[4] + "-" + getMonth(grps[3]) + "-" + pad(grps[2])
			res_parent1_death = "0000-00-00"
			res_parent1_name = grps[0].strip()
			res_parent2_birth = grps[10] + "-" + getMonth(grps[9]) + "-" + pad(grps[8])
			res_parent2_death = "0000-00-00"
			res_parent2_name = grps[5].strip()

			return ((res_name, res_gender, res_birth, res_death), (res_parent1_name, res_parent1_gender, res_parent1_birth, res_parent1_death), (res_parent2_name, res_parent2_gender, res_parent2_birth, res_parent2_death))
		else:
			print("failure")
			return (res_name, res_gender, res_birth, res_death)
	else:
		return None

for i in range(1, 100):
	print(i)
	res = fetchMOP(i)
	if res != None:
		if len(res) == 3:
			print(res[0])
			print("-->", res[1])
			print("-->", res[2])
		else:
			print(res)