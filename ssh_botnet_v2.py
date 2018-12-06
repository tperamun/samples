import optparse
from pexpect import pxssh

class Bot:
	def __init__(self, host, user, password):
		self.host = host
		self.user = user
		self.password = password #password or key.
		self.session  = self.connect() #create SSH session

	def connect(self):
		try:
			s = pxssh.pxssh()
			s.login(self.host, self.user, self.password)

			return s

		except Exception as e:
			print (e)
			print('[-] Error connecting')
			exit(0)

	def send_command(self, cmd):
		self.session.sendline(cmd) #send command
		self.session.prompt() # match one of many possible prompts. Eg $, >, #, etc.
		return self.session.before #print everything before the prompt


botnet = [] #The botnet. Will contain all the bots



def botnet_command(command):
	for bot in botnet:
		output = bot.send_command(command)
		print('[*] Output from ' + bot.host)
		print('[+] '+output.decode('ascii')+'\n')





def add_bot(host, user, password):
	bot = Bot(host, user, password) #Create bot instance.
	botnet.append(bot)




if __name__ == '__main__':
	add_bot('192.168.0.17', 'timal', 'yerr')
	botnet_command("uname -v")













