import requests
from bs4 import BeautifulSoup
import sys

pages = 1
search_term = "" 
place = "Mumbai"
file_dest = "./data.txt"

try:
	pages = int(sys.argv[3])
except:
	pages = int(1)
try:
	search_term = sys.argv[1]
	search_term = "-".join(search_term.split())
except:
	print("Enter The Search Term")
	sys.exit(0)
try:
	place = sys.argv[2]
except:
	print("Enter The Location")
	sys.exit(0)
try:
	file_dest = sys.argv[4]
except:
	file_dest="./data.txt"

print(pages,search_term,place,file_dest)

f = open(file_dest,"a+")
ind = 1
for r in xrange(1,pages+1):
	url = "https://www.justdial.com/"+place+"/"+search_term+"/page-"+str(r)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	response = requests.get(url, headers=headers)

	bs = BeautifulSoup(response.content,"html.parser")

	x = bs.findAll("a",{"class":"nlogo lazy srtbyPic"})

	links = [i['href'] for i  in x]
	res = ""

	for l in links:
		res = requests.get(l,headers=headers)
		soup = BeautifulSoup(res.content,"html.parser")
		title = soup.find("span",{"class":"fn"})
		print(title.text+"\n")
		f.write(str(ind)+". "+title.text+"\n")
		ind = ind+1

		address = soup.findAll("span",{"class":"lng_add"})
		print(address[-1].text)
		f.write("Address: "+address[-1].text+"\n")
		s = soup.findAll("a",{"class":"tel"})
		q = soup.findAll("style")

		style = []

		for p in q:
			p = p.text.split("}")
			for e in p:
				for z in e.split("{"):
					style.append(z)
		c = ''
		phone = set()
		for e in s:
		 	n = e.findAll("span")
		 	c=''
		 	for num in n:
		 		try:
		 			matching = [s for s in style if (num['class'][1]+":before") in s]
					i = style.index(matching[0])
					final = int(style[i+1][-3:-1])
					if(final==11):
						c = c+"+"
					else:
						c= c+str(final-1)
		 		except:
		 			print("Icon Style not found")
		 	phone.add(c)
		print(phone)
		f.write("Contact: \n")
		for w in phone:
			f.write(w)
			f.write("\n")
		f.write("\n")

