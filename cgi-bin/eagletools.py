#!/usr/bin/env python
# set environment variables needed by EagleClaw

def setenv():
    import os,sys
    try:
        new_enough = os.walk
        import subprocess
    except:
        print '<p><h3>Error! -- Must use a more recent version of Python with subprocess and os.walk.</h3>'
        print '<p>Python 2.5 is recommended'
        sys.exit(1)  

    debug = False

    if os.getenv('SERVER_NAME')=='kingkong.amath.washington.edu':
        # set environment variables when run on web server
        # (should be set already if run locally)

        # These may need to be changed for a server other than kingkong:
        homedir = '/var/www/html/'
        os.environ['HOME'] = homedir
        os.environ['HOST'] = 'kingkong.amath.washington.edu'
        clawdir = os.path.join(homedir,'claw')


        clawpythonpath = os.path.join(clawdir,'python')
        os.environ['CLAW'] = clawdir
        os.environ['FC'] = 'gfortran'
        os.environ['PYTHONPATH'] = clawpythonpath
        sys.path.insert(0,clawpythonpath)

    else:
        try: clawdir = os.getenv('CLAW')
        except:
           print 'Error -- environment variable CLAW not set'
           if not debug: sys.exit(1)

    if debug:
        print "<p>Currrent dir = ",os.getcwd()
        print "<br>clawdir = ",clawdir
        print "<p>os.environ: <br>"
        for (k,d) in os.environ.iteritems():
            print k,' = ',d,'<br>'


def read_description(xdir):
    import os, string

    file = xdir + '/eagleclaw/index.html'
    try:
        index = open(file, 'r')
    except:
        print "<p>Error: xdir = ",xdir
        print "<p>Error opening html file ",file, "<p>"

    indescr = False
    description = ""
    for line in index:
        if string.find(line,'eagle_description') > -1:
	    indescr = True
	if string.find(line,r'</div>') > -1:
	    indescr = False
	if indescr:
	    description = description + line
    if description != "":
        description = description + '</div>\n'

    #print "description = ",description, "<p>"
    return description
