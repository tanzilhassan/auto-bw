print('    ___   __  ____________  ____ _       __')
print('   /   | / / / /_  __/ __ \/ __ ) |     / /')
print('  / /| |/ / / / / / / / / / __  | | /| / / ')
print(' / ___ / /_/ / / / / /_/ / /_/ /| |/ |/ /  ')
print('/_/  |_\____/ /_/  \____/_____/ |__/|__/   ')
print('                                           ')

print('v 1.1')
#print('by Nafiz Imtiaz')

import requests
import sys
import xml.etree.cElementTree as ET
import re
from time import gmtime, strftime, localtime

#url's
prtgurl = 'http://ipsla.equitel.com.bd'
xmlurl = 'http://ipsla.equitel.com.bd/api/table.xml?&content=values&sortby=-datetime&display=extendedheaders&varexpand=tabletitle&tabletitle=Sensor%20Data&graphid=0&columns=datetime%2Cvalue_%2Ccoverage%2Cobjid%2Cbaselink&id='
urlid = [
{'id':'5357', 'name': 'IIG Total (CR/Po1)'},
{'id':'5358', 'name': 'F@H Primary'},
{'id':'5585', 'name': 'F@H Secondary'},
{'id':'5348', 'name': 'Summit'},
{'id':'5353', 'name': 'Summit secondary'},
{'id':'3176', 'name': 'BSCCL'},
{'id':'2116', 'name': 'IDS'},
{'id':'5033', 'name': 'Sadia Tech'},
{'id':'5032', 'name': 'Info-Link'},
{'id':'2136', 'name': 'BTC'},
{'id':'3463', 'name': 'BDIX(Primary)'},
{'id':'4707', 'name': 'BDIX(Secondary)'},
{'id':'4813', 'name': 'NOVO Nix'},
{'id':'4403', 'name': 'Novo GGC'},
{'id':'5447', 'name': 'Info-Link GGC'},
{'id':'5241', 'name': 'Sadia Tech GGC'},
{'id':'4328', 'name': 'BT ISP GGC'},
{'id':'3467', 'name': 'BT-MGMT'},
{'id':'5274', 'name': 'Ranks-IT'},
{'id':'5556', 'name': 'Ranks-GGC'}]
login_data = dict(username='', password='')
session = requests.session()
session.post(prtgurl, data=login_data)
#print('Login Successful')
print('\n')

#get time
datetime = strftime('%d-%m-%y : %I:%M %p',localtime())
dT = strftime('%d_%m_%y_%I_%M_%p', localtime())
dT = dT +'.txt'
def showTraffic (urlid):
 #Fetch the raw xml data
 #out_file = open(dT,'a+')
 #print >> out_file, datetime, '\n' 
 #out_file.write(datetime+'\n')
 datetime = strftime('%d-%m-%y : %I:%M %p',localtime())
 dT = strftime('%d_%m_%y_%I_%M_%p', localtime())
 dT = dT +'.txt'
 out_file = open(dT,'a+')
 print >> out_file, datetime, '\n'
 out_file.close()

 for i in urlid:
  xmldata = session.get(xmlurl + i['id'])
  f = open('table.xml','w')
  f.write(xmldata.text)
  #print('Acquired raw xml data')
  f.close();
  session.close()
  out_file = open('adad.txt','a')

  #XML Manipulation
 
  tree = ET.parse('table.xml')
  root = tree.getroot()
  inelements = []
  outelements = []

  for elemin in root.iter('value'): 
	if elemin.attrib['channel']=='Traffic In (speed)':
		str1=elemin.text.replace(',','')
		if str1 == 'Error':
		 numin=[0]
		else:	
		 if str1.find('.')==-1:
		  numin = re.findall("\d+", str1)
		  numin = map(int,numin)
		 else:
		  numin = re.findall("\d+\.\d+", str1)
		  numin = map(float,numin)
		#print numin
		inelements.append(numin)


  for elemout in root.iter('value'):
	if elemout.attrib['channel']=='Traffic Out (speed)':
		str2=elemout.text.replace(',','')
		if str2 == 'Error':
		 numout = [0]
		else: 	
		 if str2.find('.')==-1:
		  numout = re.findall("\d+", str2)
		  numout = map(int,numout)
		 else:
		  numout = re.findall("\d+\.\d+", str2)
		  numout = map(float,numout)
		#print numout
		outelements.append(numout)

  maxin =  max(inelements[:60])
  maxout = max(outelements[:60])
  #minin =  min(inelements[:60])
  #minout = min(outelements[:60])
  #avin = (maxin[0] + minin[0])/2;
  #avout = (maxout[0] + minout[0])/2;
  #print inelements
  #print outelements
  avin = maxin[0]; 
  avout = maxout[0] ;
  out_file = open(dT,'a+') ; 
  #print >> out_file, datetime+'\n'
  print >> out_file, i['name'],':',avin,'/',avout,'Mbps'



  print i['name'],':',avin,'/',avout,'Mbps','\n'
 print >> out_file,'\nBR/\n'  
print datetime, '\n'
showTraffic(urlid)
#print '\nBR/\n',sys.argv[1],'\n\n'
session.close()