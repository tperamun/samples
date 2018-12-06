import optparse
import socket
from socket import * 
from threading import * 

import nmap

screen_lock = Semaphore(value=1)
def connScan(tgtHost, tgtPort):
	
	try:
		connSkt = socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tgtHost, tgtPort))
		connSkt.send('aha hii :3\r\n')
		results.connSkt.recv(100)
		screen_lock.acquire()
		print('[+]%d/tcp open' %tgtPort)
		print('[+] ' + str(results))
	except:
		screen_lock.acquire()
		print('[-]%d/tcp closed' % tgtPort)
	finally:
		screen_lock.release()
		connSkt.close()
	
def portScan(tgtHost, tgtPorts):
	
	try:
		tgtIP = gethostbyname(tgtHost)
	except:
		print('[-] Cannot resolve %s: Unknown host' % tgtHost)
		return

	try:
		tgtName = gethostbyaddr(tgtIP)
		print('\n[+] Scan Results for: ' + tgtName[0])

	except:
		print('\n[+] Scan Results for: '+ tgtIP)

	clear
setdefaulttimeout(1)

	for tgtPort in tgtPorts:
		#print('Scanning port '+ tgtPort)
		#connScan(tgtHost, int(tgtPort))
		t = Thread(target = connScan, args=(tgtHost, int(tgtPort)))
		t.start()



def main():
	
	parser = optparse.OptionParser('usage%prog -H' + ' <target host> -p <target port>')
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
	parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] seperated by comma')
 
	(options, args) = parser.parse_args()

	tgtHost = options.tgtHost
	tgtPorts = str(options.tgtPort).split(', ')
	print(tgtPorts)	

	if (tgtHost == None) | (tgtPorts[0] == None):
		print ('[-] You must specify a target host and port[s]')
		exit(0)
	
	portScan(tgtHost, tgtPorts)
	
	for tgtPort in tgtPorts:
		nmapScan(tgtHost, tgtPort)


if __name__== '__main__':
	main()









