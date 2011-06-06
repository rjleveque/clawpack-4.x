#!/usr/bin/env python

print 'Content-type: text/html\n'
print """

  <html> 
  <head>
  <link type="text/css" rel="stylesheet"
  href="http://localhost:50005/eagleclaw/eagleclaw.css">
  </head>
  
  
  <SCRIPT SRC= http://localhost:50005/doc/load.js> </SCRIPT>
  
  
  <body>
  
  <eagle1>EagleClaw -- Main Menu</eagle1>
  
  
  <eagle2>Easy Access Graphical Laboratory for
          Exploring Conservation Laws</eagle2>
  
  <p>&nbsp;<p>
"""


import cgi,os,sys,time
import traceback
import shutil
import cgitb
cgitb.enable()

try: 
    import eagletools
except: 
    print '<p>No eagletools found<p>'

eagletools.setenv()
clawdir = os.environ['CLAW']


try:
    
    form = cgi.FieldStorage()
    
    rundir = form.getvalue('rundir').strip()  # strip of whitespace
    rundir = '/eagleclaw/runs/' + rundir
    fullrundir = clawdir + rundir

    try:
        os.chdir(fullrundir)
    except:
        print "Error -- directory does not exist: ", fullrundir
        sys.exit(1)
    
    print "<p><h2>Welcome back to %s <p></h2>" % rundir

    if 0:
        try:
            info = open('info.txt','rb')
	    print info.readlines()
	    info.close()
        except:
            print "<p>No info.txt file found<p>"


    print """
    &nbsp;&nbsp;
    <a href="http://localhost:50005%s/eaglemenu.html">Go to Index</a>
    """ % rundir


except:
    print """
    <p>
    <h2>Error!</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"

