#!/usr/bin/env python

print 'Content-type: text/html\n'
print r"""

  <html> 
  <title>EagleClaw</title>
  <head>
  <link type="text/css" rel="stylesheet"
        href="http://localhost:50005/eagleclaw/eagleclaw.css">
  </head>
  
  <body>
  
  <eagle1>EagleClaw --- Run Results</eagle1>
  <eagle2>Easy Access Graphical Laboratory for Exploring Conservation
  Laws</eagle2>


"""


import cgi,os,sys,time,shelve
import traceback
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
    print """
    <p> <h2> Error importing pyclaw.eagle</h2>
    """
    traceback.print_exc()
    sys.exit(1)


try:
    form = cgi.FieldStorage()
    
    rundir = form.getvalue('rundir')
    xdir = form.getvalue('xdir')
    exdir = form.getvalue('exdir')

    fullrundir = os.path.join(clawdir,rundir)
    outdir = os.path.join(rundir,'output')
    fulloutdir = os.path.join(clawdir,outdir)
    fullxdir = os.path.join(clawdir,xdir)
    plotdir = os.path.join(rundir,'eagleplots')
except:
    print "<p>Error reading dirs from form"
    sys.exit(1)

print """
  <eagle4>Location:</eagle4>
      <p class="indent1">
      Current run-directory: &nbsp;&nbsp; %s </p>
      <p class="indent1">
      Template directory for this example:     &nbsp;&nbsp;   $CLAW/%s
      </p>
  <eagle4>Execution output:</eagle4>
  <div class="indent1">
    """   % (rundir, exdir)


try:
    os.chdir(fullrundir)
except:
    print "<p><h2>Error moving to run-directory %s <p>" % fullrundir
    sys.exit(1)
#try:
#    os.chdir(fullrundir + '/eagleclaw')
#except:
#    print "Error -- can't move to eagleclaw subdirectory of", fullrundir
#    sys.exit(1)

try:
    eagledb = shelve.open('eagle.db')
    #rundir = eagledb['rundir']
    #xdir = eagledb['xdir']
    #exdir = eagledb['exdir']
except:
    print '<p>Error opening eagle.db'

runresults = open('runresults.html','w')
runresults.write(r"""
  <html> 
  <title>EagleClaw</title>
  <head>
  <link type="text/css" rel="stylesheet"
        href="http://localhost:50005/eagleclaw/eagleclaw.css">
  </head>
  
  
  <SCRIPT SRC= http://localhost:50005/doc/load.js> </SCRIPT>
  <!- latex macros: -->
  $\newcommand{\vector}[1]{\left[\begin{array}{c} #1 \end{array}\right]}$ 
  $\newenvironment{matrix}{\left[\begin{array}{cccccccccc}} {\end{array}\right]}$ 
  
  <body>
  
  <eagle1>EagleClaw --- Run Results</eagle1>
  <eagle2>Easy Access Graphical Laboratory for Exploring Conservation
  Laws</eagle2>


  <eagle4>Location:</eagle4>
      <p class="indent1">
      Current run-directory: &nbsp;&nbsp; %s </p>
      <p class="indent1">
      Template directory for this example:     &nbsp;&nbsp;   $CLAW/%s
      </p>

  <eagle4>Execution output:</eagle4>
  <div class="indent1">
    """   % (rundir,exdir))


exec('datafiles = ' + form.getvalue('datafiles'))
#print 'datafiles = xx%sxx' % datafiles

import pyclaw.data

data = pyclaw.data.Data(datafiles) 
#print '<p>data:  ',  str(data.__data)
#print '<p> data.get_owners() = ', data.get_owners()

#data = pyclaw.data.Data() 
#for datafile in datafiles:
#    data.read(datafile)
    
try:
    exec('form_params = ' + form.getvalue('params'))
    for param in form_params:
        exec("value = form.getvalue('%s')" % param)
        #exec("data.%s = %s" % (param, value))
	setattr(data, param, value)
        #data.params[param] = value
        #print "<p>Read value from form: data.%s = %s" % (param,value)

except:
    print """
    <p>
    <h2>Error in reading data from form</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"



try:
    os.chdir(fullrundir)
except:
    print "Error -- can't move to ", fullrundir
    sys.exit(1)
    

try:
    sys.path.append(os.getcwd())
    import eagleforms
except:
    print '<p> *** Error importing eagleforms.py in directory %s<p>' \
           % os.getcwd()
    traceback.print_exc()
    sys.exit(1)

os.chdir(fullrundir)


# Save the parameter values in the shelve database eagle.db for use
# as default values the next time eaglerunmenu is executed.


try:
    for param in form_params:
	if eagledb.has_key(param):
	    value = eagledb[param]
            #print '<p>eaglerun.py.cgi: param = %s, value = %s'  % (param,value)
	else:
            print '<p>eaglerun.py.cgi: param = %s is missing from db' % param
except:
    print '<p>Error with eagle.db'


try:
    # Check for valid input:
    data,errors = eagle.check_input(data, form_params, eagledb)

    # save values of parameters to eagle.db:
    if not errors:
        #for (param, value) in data.params.iteritems():
        for param in form_params:
            value = getattr(data, param, None)
            eagledb_obj = eagledb[param]
            eagledb_obj.prev_value = value
            eagledb[param] = eagledb_obj
    eagledb.close()
except:
    print """
    <p>
    <h2>Error with eagle.db or checking input</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"
    sys.exit(1)

if errors:
    print "<p>***Errors in data --- aborting</p></html>"
    sys.exit(1)

# ------------------------------------------------
# Valid data on the form, massage it if necessary:

try:
    data = eagleforms.massage_runform_data(data)
except:
    print '<p> *** Error executing massage_runform_data<p>'
    print '<p> this should be defined in eagleforms.py... in directory<br>'
    print '    %s<p>' % os.getcwd()
    traceback.print_exc()
    sys.exit(1)

# At this point data should contain any modified data values for any of the
# data files.  Write these values to the datafiles:

try:
    #exec('datafiles = ' + form.getvalue('datafiles'))
    for file in datafiles:
        print "<p>  Writing parameters to file ",file
    #    data.write(file)
    data.write()
except:
    print """
    <p>
    <h2>Error in reading datafiles from form or writing to files</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"
    sys.exit(1)


# ===========================================================================
# Run the Clawpack code:
# ----------------------

try:
    starttime = eagle.current_time()
    print " <p>\n Job started: %s \n<p>"  % starttime
    runresults.write( " <p>\n Job started: %s \n<p>"  % starttime)

    if os.path.isfile('claw.data'):
        xclawcmd = 'xclaw'
    elif os.path.isfile('amr2ez.data'):
        xclawcmd = 'xamr'
    else:
        print 'Warning: did not find expected data file'
        xclawcmd = 'xclaw'

    returncode = eagle.runclaw(xdir=fullxdir,rundir=fullrundir, \
                 outdir=fulloutdir, xclawcmd=xclawcmd, \
                 xclawout='xclawout.txt', xclawerr='xclawerr.txt', \
                 runmake = True, overwrite=True, verbose=False)
    if returncode != 0:
        print "<p><h2>*** Error occurred running xclaw,"
        print "   returncode = %4i *** </h2><p>" % returncode
	print "<a href='http://localhost:50005/%s/xclawerr.txt'>" % rundir
        print "View error statments</a><p>" 
    
    endtime = eagle.current_time()
    print " <p>\n Job completed: %s \n"  % endtime
    runresults.write( " <p>\n Job completed: %s \n"  % endtime)
    
    runresults.write( """
    <p>
    <a href="http://localhost:50005/%s/xclawout.txt">View claw timestepping output</a>
    <p>
    """ % rundir)
    
    
except:
    print """
    <p>
    <h2>Error in running code!</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    sys.exit(1)


# ====================================================================




runresults.write( """</div>
  <eagle4>Next step:</eagle4>
  <p>
  <form action="http://localhost:50005/cgi-bin/eagleplotmenu.py.cgi" method="POST">
  <input readonly type="hidden" name="xdir" value="%s">
  <input readonly type="hidden" name="exdir" value="%s">
  <input readonly type="hidden" name="rundir" value="%s">
  <input readonly type="hidden" name="nextstep" value="2">
  <p class="indent1">
  <input type="submit" name=request value="Go to Plot Menu"> 
  </p>
  </form>
    """  % (xdir, exdir, rundir))


runresults.write( """
  <eagle4>Other options:</eagle4>
  <p>
  <form action="http://localhost:50005/cgi-bin/eaglerunmenu.py.cgi" method="POST">
  <input readonly type="hidden" name="xdir" value="%s">
  <input readonly type="hidden" name="exdir" value="%s">
  <input readonly type="hidden" name="rundir" value="%s">
  <p class="indent1">
  <input type="submit" name=request value="Return to Run Menu"> 
  </form>
    """  % (xdir, exdir, rundir))

runresults.write( """
  
  <p class="indent1">
  Return to <a href="http://localhost:50005/%s/eaglemenu.html">
  Main Menu</a> 
  </p>

  <p class="indent1">
  Return to <a href="http://localhost:50005/eagleclaw/examples.html">
  EagleClaw Examples Index</a>
  </p>

  </body>
  </html>

"""  % rundir)

runresults.close()


if returncode == 0:
    print '<meta http-equiv="REFRESH" ',\
      'content="3;url=http://localhost:50005/%s/runresults.html">' % rundir

    print """
      <p>
      Successful completion... Will redirect in 3 seconds to <p>
      &nbsp;&nbsp;&nbsp;<a href="http://localhost:50005/%s/runresults.html">
      %s/runresults.html</a> ... """ % (rundir,rundir)
