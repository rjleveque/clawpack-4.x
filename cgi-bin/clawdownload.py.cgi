#!/usr/bin/env python

print 'Content-type: text/html\n'
print """

<html> 
<font color="brown">
<center> <h1>CLAWPACK Download page</h1>
</center>
</font>
"""


import cgi,os,sys,time
import traceback
import shutil


# This may need to be changed for a server other than kingkong:
rootdir = '/var/www/html/claw/www/clawdownload'


#-----------------------------
def current_time(addtz=False):
#-----------------------------
    # determine current time and reformat:
    time1 = time.asctime()
    year = time1[-5:]
    day = time1[:-14]
    hour = time1[-13:-5]
    current_time = day + year + ' at ' + hour
    if addtz:
        current_time = current_time + ' ' + time.tzname[time.daylight]
    return current_time



try:
    form = cgi.FieldStorage()
    
    lastname = form.getvalue('lastname')
    firstname = form.getvalue('firstname')
    institution = form.getvalue('institution')
    email = form.getvalue('email')
    sendemail = form.getvalue('sendemail')
    sendemail = (sendemail == 'True')

    logfname = os.path.join(rootdir,'download_log.txt')
    emailfname = os.path.join(rootdir,'email_list.txt')

except:
    print """
    <p>
    <h2>Error reading form</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"

try:
    file = open(logfname,"a+")
    file.write('Time = %s' % current_time())
    file.write('\nName = %s, %s' % (lastname,firstname))
    file.write('\nInstitution = %s' % institution)
    file.write('\nemail = %s' % email)
    file.write('     Send = %s' % sendemail)
    file.write('\naddress = %s' % os.environ['REMOTE_ADDR'])
    file.write('\n-----------------------------------\n')
    file.close()

    if sendemail:
        file = open(emailfname,"a+")
        file.write('%s\n' % email)
        file.close()
	    
except:
    print """
    <p>
    <h2>Error writing log files</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"

print """
<p>
<h2>Thank you for registering</h2>
<p>
<h3><a href="http://kingkong.amath.washington.edu/claw/www/clawdownload/downloadmenu.html">Proceed to download menu</a>
</html>
"""
