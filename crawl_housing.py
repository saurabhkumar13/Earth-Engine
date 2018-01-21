import urllib2
import re
import requests

url_base = 'http://www.censusindia.gov.in/2011census/HLO/HL_PCA/'
url_housing = 'Houselisting-housing-HLPCA.html'
cont = urllib2.urlopen(url_base+url_housing).read()
urls = re.findall(r'href =[\'"]?([^\'" >]+)', cont)

for url in urls:
    cont = urllib2.urlopen(url_base+url).read()
    urls_xls = re.findall(r'href =[\'"]?([^\'" >]+)', cont)
    for url in urls_xls:
        resp = requests.get(url_base+url)
        output = open(url[8:], 'wb')
        output.write(resp.content)
        output.close()
        print 'getting ', url
