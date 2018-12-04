import pexpect

PROMPT =['# ', '>>> ', '> ', '\$ ', '[sudo] password for timal: ']

def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before.decode('ascii'))
    
    
def connect(user, host, password):
    ssh_newkey = "Are you sure you want to continue connecting"
    conn_str   = 'ssh ' + user + "@" + host
    child = pexpect.spawn(conn_str)
    
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    
    
    if ret == 0:
        print('[-] Error connecting'); return
    
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    
        if ret == 0:
            print('[-] Error Connecting')
            return
        
    child.sendline(password)
    child.expect(PROMPT)
    return child
    
    


def main():
    host = '192.168.0.17'
    user = 'timal'
    password = ''
    child = connect(user, host, password)
    send_command(child, 'ls -al')
    send_command(child, 'cd Desktop')
    send_command(child, 'pwd')
    send_command(child, 'ls')


if __name__ == '__main__':
    main()
