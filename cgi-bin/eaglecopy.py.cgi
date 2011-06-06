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
  
  <eagle1>EagleClaw</eagle1>
  
  
  <eagle2>Easy Access Graphical Laboratory for
          Exploring Conservation Laws</eagle2>
  
  <p>&nbsp;<p>

"""


import cgi,os,sys,time, string
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
    from pyclaw import eagle
except:
    print '*** Error importing pyclaw.eagle --- '
    print '    $CLAW/python may not be on PYTHONPATH'
    sys.exit(1)
    

try:
    form = cgi.FieldStorage()
    
    exdir = form.getvalue('exdir')
    newrundescr = form.getvalue('newrundescr')
except:
    print "Error reading form"
    sys.exit(1)
    
if newrundescr is None:
    newrundescr = ''

#print "<p>clawdir = ",clawdir
#print "<p>exdir = ",exdir
#print "<p>newrundescr = ",newrundescr

try:
    fullexdir = os.path.join(clawdir,exdir)
    runsdir = os.path.join(clawdir,'eagleclaw/runs')



    try:
        os.chdir(runsdir)
    except:
        print "Error -- can't move to directory", runsdir
        sys.exit(1)
    

    # Create new directory name from current time

    creationtime = eagle.current_time(addtz=True)
    t = time.localtime(time.time())
    s="%2i%2i%2i.%2i%2i%2i"% (t[0]-2000,t[1],t[2],t[3],t[4],t[5])
    DST = t[8]
    newrun =  s.replace(' ','0')
    fullnewrun = os.path.abspath(newrun)


    if os.path.isdir(fullnewrun):
        # in the unlikely event that two users try to create new directories
	# in the same second, having the same name:
	print """
	<p><h2>Error!  Directory already exists.<p>
	Please use the back button to go back and try again.
	"""
	sys.exit(1)


    try:
        eagle.copytreefilter(fullexdir,fullnewrun,\
                omitdirs='[.]svn|eagleplots', \
                omitfiles='fort[.]|[.]png|xclaw|xamr',verbose=0)
        #print "Copied %s  to  %s" %(fullexdir,fullnewrun)
    except:
        print "Error -- can't copy %s  to  %s" %(fullexdir,fullnewrun)
        sys.exit(1)

except:
    print " <p> <h2>Error creating directory!</h2> <p> <pre>"
    traceback.print_exc()
    print "</pre><p>"
    sys.exit(1)

try:
    #os.chdir(fullnewrun + '/eagleclaw')
    os.chdir(fullnewrun)
    #print "<p>directory: ",os.getcwd()
except:
    pass

try:
    from pyclaw import make_eaglemenu as M
    M.make_menu(exdir,'eagleclaw/runs/' + newrun)

except:
    print " <p> <h2>Error creating menu file!</h2> <p> <pre>"
    traceback.print_exc()
    print "</pre><p>"
    sys.exit(1)

try:
	    
    # prepend to index in eagleclaw/runs/index.html
    os.chdir(runsdir)
    newindex = open('newindex.html','wb')
    if os.path.isfile('index.html'):
        # index.html already exists:
        index = open('index.html','r')
        line = ''
	while string.find(line,'<hr>') == -1:
            line = index.readline()
	    newindex.write(line)
    else:
        # index.html doesn't exist, so first write header:
        newindex.write("""
           <head>
           <link type="text/css" rel="stylesheet"
           href="http://localhost:50005/eagleclaw/eagleclaw.css">
           </head>
           <body>
           <eagle1>EagleClaw -- Index of past runs</eagle1> 
           <eagle2>Easy Access Graphical Laboratory for  
                   Exploring Conservation Laws</eagle2>
	   <p><center>
           (Directory name is creation time in format  yymmdd.hhmmss )
	   </center><p><hr><p>
           """)

    newindex.write("""
	  <p><a href="%s/eaglemenu.html">%s</a> 
	  &nbsp;&nbsp; copied from 
	  &nbsp;&nbsp; %s 
	  &nbsp;&nbsp; on 
	  &nbsp;&nbsp; %s
	  """ % (newrun,newrun,exdir,creationtime))

    if newrundescr != '':
        newindex.write("""
            <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            Description: &nbsp; <font color="brown">%s</font></p>
            """ % newrundescr)

    if os.path.isfile('index.html'):
	# copy over the remaining previous contents 
	while line != '':
            line = index.readline()
	    newindex.write(line)
        index.close()
        os.remove('index.html')
    else:
        newindex.write("</html>")

    newindex.close()
    os.rename('newindex.html','index.html')

except:
    print """
    <p>
    <h2>Error modifying runs/index.html file!</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"
    sys.exit(1)

try:
	    
    # append to eagleclaw log in eagleclaw/runs/logfile.txt
    os.chdir(runsdir)
    if os.path.isfile('logfile.txt'):
        # logfile.txt already exists and we want to append to end:
        logfile = open('logfile.txt','a+')
    else:
        logfile = open('logfile.txt','w')

    addr = os.environ['REMOTE_ADDR']
    logfile.write("%s on %s, addr = %s, \n           copied from %s \n\n" \
             % (newrun,creationtime,addr,exdir))
    if newrundescr != '':
        logfile.write('    Description:   '+newrundescr+'</p>')

    logfile.close()
except:
    print """
    <p>
    <h2>Error modifying runs/logfile.txt file!</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"
    sys.exit(1)

print """
<p>
<h3>Executable copy created in directory %s    
&nbsp;&nbsp;&nbsp;
""" % newrun

#print """
#<a href="http://localhost:50005/eagleclaw/runs/%s/eagleclaw/index.html">
#Go to Index</a>
#""" % newrun
print '</h3>'

print"""
<p>
Save this number for future reference if you want to return to it later.
<p>
&nbsp;&nbsp;&nbsp;
(Directory name is creation time (%s) in format  yymmdd.hhmmss )
<p>
""" % time.tzname[DST]


print """
<p>
&nbsp;&nbsp;&nbsp;
<a href="http://localhost:50005/%s/eaglemenu.html">Go to Main Menu</a> 
&nbsp;&nbsp;
To set parameters, run code, and plot results</p>

""" % ('eagleclaw/runs/'+newrun)

print "</html>"
