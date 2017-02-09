import requests
from bs4 import BeautifulSoup
import pickle 
import csv
import string
import sys

#builds csv file of all US and Canada cities in place, link
def buildplacesdic():
    with open('placesdic.csv', 'w') as csvfile:
        fieldnames = ['place', 'link']
        write = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
        write.writeheader()
        search_url = "https://www.craigslist.org/about/sites#US"
        source_code = requests.get(search_url)
        html_doc = source_code.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        index = 0
        limit = 425
        #cuts off so we only have US
        for x in soup.find_all('a'):
            link = str(x)
            linkstart = link.find("//") + 2
            linkend = link.find('/"')
            placestart = linkend + 3
            placeend = link.find('</a')
            if index == limit:
                break
            index = index + 1
            
            if (not link.find('#') == 9) and (link.find('name') == -1):
                print(link[linkstart:linkend])
                print(link[placestart:placeend])
                linkadd = link[linkstart:linkend]
                placeadd = link[placestart:placeend]
                write.writerow({'place':placeadd, 'link':linkadd})

#gets the number of results. Remember I need to divide by 100 to get pages
def getnumresults(city):
    search_url = 'http://' + city + '/search/rea'
    #search_url = 'http://auburn.craigslist.org/search/rea'
    source_code = requests.get(search_url)
    html_doc = source_code.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    #gets total pages for the city
    for x in soup.find_all('span'):
        span = str(x)
        if span.find('totalcount')  > 1:
            resultsstart = span.find('count') + 7 
            resultsend = span.find('/span></span><a class="button') - 8
            return span[resultsstart:resultsend]

#appends a citydic.csv file that makes a table of title, link, price
def appendsearchcity(city):
    with open('citydic.csv', 'a') as newFile:
        writer = csv.writer(newFile)
        #entries = float(getnumresults(city))
        #pages = int(entries)/100 
        #changing the range from pages to 25
        for x in range(0 ,25):
            search_url = 'http://' + city + '/search/rea?s=' + str(x * 100)
            source_code = requests.get(search_url)
            html_doc = source_code.text
            soup = BeautifulSoup(html_doc, 'html.parser')

            title = ''
            link = ''
            price = ''
            for l in soup.find_all('a'):
                link = str(l)
                if (not link.find('result-price') == -1):
                    starttitle = link.find('price">$') + 8
                    endtitle = link.find('</span>')
                    price = link[starttitle:endtitle]
                if (not link.find('result-title') == -1):
                    starttitle = link.find('html">') + 6
                    endtitle = link.find('</a>')
                    title = link[starttitle:endtitle]
                    title = title.encode(sys.stdout.encoding, errors='replace')
                    startlink = link.find('href=') + 6
                    endlink = link.find('.html">')
                    link = city + link[startlink:endlink] + '.html'
                    print(title)
                    writer.writerow([title, link, price])
                    price = 0

#buils a citydic.csv file that makes a table of title, link, price
def beginsearchcity():
    city = 'auburn.craigslist.org'
    with open('citydic.csv', 'w') as csvfile:
        fieldnames = ['title', 'link', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', lineterminator='\n')
        writer.writeheader()
        entries = (getnumresults(city))
        entries = int(entries)
        pages = entries/100
        pages = int(pages)
        for x in range(0 ,pages):
            search_url = 'http://' + city + '/search/rea?s=' + str(x * 100)
            source_code = requests.get(search_url)
            html_doc = source_code.text
            soup = BeautifulSoup(html_doc, 'html.parser')
            title = ''
            link = ''
            price = 0
            for l in soup.find_all('a'):
                link = str(l)
                if (not link.find('result-price') == -1):
                    starttitle = link.find('price">$') + 8
                    endtitle = link.find('</span>')
                    price = link[starttitle:endtitle]
                if (not link.find('result-title') == -1):
                    starttitle = link.find('html">') + 6
                    endtitle = link.find('</a>')
                    title = link[starttitle:endtitle]
                    title = title.encode(sys.stdout.encoding, errors='replace')
                    startlink = link.find('href=') + 6
                    endlink = link.find('.html">')
                    link = city + link[startlink:endlink] +'.html'
                    print(title + link + str(price))
                    writer.writerow({'title':title, 'link':link, 'price':price})
                    price = 0

def allcsvs():
    with open('placesdic.csv', 'r') as f:
        reader = csv.reader(f)
        index = 0
        for row in reader:
            if(row[0] != 'place'):
                print(index)
                index = index + 1
                print(row[0])
                appendsearchcity(row[1])

#buildplacesdic()
beginsearchcity()
allcsvs()





