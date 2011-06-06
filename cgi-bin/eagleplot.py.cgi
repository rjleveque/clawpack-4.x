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
  
  <eagle1>EagleClaw</eagle1>
  <eagle2>Easy Access Graphical Laboratory for Exploring Conservation
          Laws</eagle2>
    """


import cgi,os,sys,time,shelve
import traceback
import cgitb
cgitb.enable()


try:
    import subprocess
except:
    print '<p>Must use a more recent version of Python with module subprocess'
    print 'Python 2.5 is recommended'
    sys.exit(1)


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
    <p> <h2> Error importing pyclaw.eagle" </h2> <p> <pre>
    """
    traceback.print_exc()
    sys.exit(1)

try:
    
    form = cgi.FieldStorage()
    
    rundir = form.getvalue('rundir')
    xdir = form.getvalue('xdir')
    exdir = form.getvalue('exdir')
    plotdir = form.getvalue('plotdir')
    plotdiroption = form.getvalue('plotdiroption')

    fullrundir = os.path.join(clawdir,rundir)
    outdir = os.path.join(rundir,'output')
    fulloutdir = os.path.join(clawdir,outdir)
    fullxdir = os.path.join(clawdir,xdir)
    plotdir = os.path.join(rundir,'eagleplots')
    fullplotdir = os.path.join(clawdir,plotdir)
except:
    print "Error reading form"


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



from pyclaw import data, eagle
exec('datafiles = ' + form.getvalue('datafiles'))

try:
    os.chdir(fullrundir)
except:
    print "Error -- can't move to ", fullrundir
    sys.exit(1)
    
formdata = data.Data(datafiles) 
    
try:
    exec('form_params = ' + form.getvalue('params'))
    for param in form_params:
        exec("value = form.getvalue('%s')" % param)
        exec("formdata.%s = value" % param)
        #print "<p>Read value from form: formdata.%s = %s" % (param,value)

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
    sys.path.append(os.getcwd())
    import eagleforms
except:
    print '<p> *** Error importing eagleforms.py in directory %s<p>' \
           % os.getcwd()
    traceback.print_exc()
    sys.exit(1)


# Save the parameter values in the shelve database eagle.db for use
# as default values the next time eaglerunmenu is executed.

os.chdir(fullrundir)

try:
    eagledb = shelve.open('eagle.db')
except:
    print '<p>Error opening eagle.db'

try:
    #for (param,value) in formdata.params.iteritems():
    for param in form_params:
        if eagledb.has_key(param):
            value = eagledb[param]
            #print '<p>eaglerun.py.cgi: param = %s, value = %s'  % (param,value)
            pass
        else:
            print '<p>eaglerun.py.cgi: param = %s is missing from db' % param
            print 'in directory ',os.getcwd()
except:
    print '<p>Error with eagle.db'


try:
    # Check for valid input:
    #print '<p>formdata.plotline is int: ',isinstance(formdata.plotline,int)
    (formdata,errors) = eagle.check_input(formdata, form_params, eagledb)
    #print '<p>formdata.plotline is int: ',isinstance(formdata.plotline,int)
except:
    print '<p>Problem with eagle.check_input'

try:

    # save values of parameters to eagle.db:
    if not errors:
        for param in form_params:
            value = getattr(formdata, param, None)
            eagledb_obj = eagledb[param]
            eagledb_obj.prev_value = value
            eagledb[param] = eagledb_obj
            #print '<p>eagleplot: saved %s to db: <p>%s' % (param,eagledb_obj)
    eagledb.close()
except:
    print """
    <p>
    <h2>Error with eagle.db</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"
    sys.exit(1)

if errors:
    print "<p>*** Errors in data --- aborting</p></html>"
    sys.exit(1)
  

# ------------------------------------------------
# Valid data on the form, massage it if necessary:

try:
    formdata = eagleforms.massage_plotform_data(formdata)
except:
    print '<p> *** Error executing massage_plotform_data<p>'
    print '<p> this should be defined in eagleforms.py... in directory<br>'
    print '    %s<p>' % os.getcwd()
    traceback.print_exc()
    sys.exit(1)

# At this point formdata should contain any modified data values for any of the
# data files.  Write these values to the datafiles:

try:
    #exec('datafiles = ' + form.getvalue('datafiles'))
    #formdata.write()
    for file in datafiles:
        print "<p>  Writing parameters to file ",file
        formdata.write(file)
except:
    print """
    <p>
    <h2>Error in writing formdata to files</h2>
    <p>
    <pre>
    """
    traceback.print_exc()
    print "</pre><p>"
    sys.exit(1)

#print '<p> got this far'
#sys.exit(0)

# add a line to the logfile each time plotting is done:

try:
    runsdir = os.path.join(clawdir,'eagleclaw/runs')
    os.chdir(runsdir)
    logfile = open('logfile.txt','a+')
    addr = os.environ['REMOTE_ADDR']
    currenttime = eagle.current_time()
    thisrun = os.path.split(rundir)[1]
    logfile.write("%s on %s, addr = %s, plotting\n\n" \
             % (thisrun,currenttime,addr))
    logfile.close()
except:
    print "<p>Error writing logfile<p>"


os.chdir(fullrundir)
    
#-----------------------------------------------------------------
# Start making the html file to redirect to on completion:

plotresults = open('plotresults.html','w')
plotresults.write(r"""
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
  
  <eagle1>EagleClaw --- Plot Results</eagle1>
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
    """   % (rundir, exdir))




# ===========================================================================
# Do the plotting:
# ----------------

pydir = os.getenv('CLAW') + '/python'


starttime = eagle.current_time()
print " <p>\n Plotting started: %s \n<p>"  % starttime
print " <p>\n Plotting in progress ....."

plotresults.write( " <p>\n Plotting started: %s \n"  % starttime)

try:

    if sys.platform == 'cygwin':
        try:
            syscmd = " C:/Python25/python.exe C:/cygwin%s/pyclaw/ploteagleclaw.py "\
                       % pydir \
                    + """ 'C:\cygwin%s' %i """ % (fullrundir, eagleforms.ndim())
            plotcmd = open('plotcmd.exe','w')
            plotcmd.write(syscmd)
            plotcmd.close()
            syscmd = os.path.join(os.getcwd(),'plotcmd.exe')
            pclaw = subprocess.Popen(syscmd) 
            pclaw.wait()   # wait for code to run
            returncode = pclaw.returncode
            #returncode = subprocess.call(syscmd)
        except:
            print "<p> Problem using Popen -- aborting"
            print  '<p>%s<p>' % syscmd
            returncode = 1
            print """ <p>\n <a href="http://localhost:50005/%s/plotmsg.txt">
                           View plotter messages</a>\n"""  % rundir
            sys.exit(1)
    else:
        try:
            from pyclaw import plotting, data
            pd = data.ClawPlotData()
            pd.rundir = fullrundir
            pd.outdir = fullrundir + '/output'
            pd.plotdir = fullrundir + '/eagleplots'
            pd.setplot = True
            pd.framenos = 'all'
            pd.fignos = 'all'
            pd.overwrite = True
            pd.msgfile = 'plotmsg.txt'
            pd.html_eagle = True
    
            plotting.printframes(pd)
            print "\nFinished executing\n"
            returncode = 0
        except:
            print "\n *** Plotting error ***"
            print """ <p>\n <a href="http://localhost:50005/%s/plotmsg.txt">
                           View plotter messages</a>\n"""  % rundir
            returncode = 1
            sys.exit(1)

    endtime = eagle.current_time()
    print " <p>\n Plotting completed: %s \n"  % endtime
    plotresults.write( " <p>\n Plotting completed: %s \n"  % endtime)
    plotresults.write( """ <p>\n <a href="http://localhost:50005/%s/plotmsg.txt">
                       View plotter messages</a>\n"""  % rundir)
    
    
except:
    print """
    <p>
    <h2>Error in plotting!</h2>
    <p>
    <pre>
    """
    returncode = 1
    plotresults.write( """ <p>\n <a href="http://localhost:50005/%s/plotmsg.txt">
                       View plotter messages</a>\n"""  % rundir)
    traceback.print_exc()
    sys.exit(1)


# ====================================================================

plotresults.write("""</div>
  <eagle4>Next step:</eagle4>
  <p class="indent1">
  <a href="http://localhost:50005/%s/eagleplots/_PlotIndex.html">View the plots</a>
  </p>
  """ % rundir)



plotresults.write( """
  <eagle4>Other options:</eagle4>

  <p>
  <form action="http://localhost:50005/cgi-bin/eagleplotmenu.py.cgi" method="POST">
  <input readonly type="hidden" name="xdir" value="%s">
  <input readonly type="hidden" name="exdir" value="%s">
  <input readonly type="hidden" name="rundir" value="%s">
  <input readonly type="hidden" name="nextstep" value="2">
  <p class="indent1">
  <input type="submit" name=request value="Return to Plot Menu"> 
  </form>
    """  % (xdir, exdir, rundir))

plotresults.write( """
  <p>
  <form action="http://localhost:50005/cgi-bin/eaglerunmenu.py.cgi" method="POST">
  <input readonly type="hidden" name="xdir" value="%s">
  <input readonly type="hidden" name="exdir" value="%s">
  <input readonly type="hidden" name="rundir" value="%s">
  <p class="indent1">
  <input type="submit" name=request value="Return to Run Menu"> 
  </form>
    """  % (xdir, exdir, rundir))

plotresults.write( """
  
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


plotresults.close()

if returncode == 0:
    print '<meta http-equiv="REFRESH" ',\
      'content="3;url=http://localhost:50005/%s/plotresults.html">' % rundir

    print """
      <p>
      Successful completion... Will redirect in 3 seconds to <p>
      &nbsp;&nbsp;&nbsp;<a href="http://localhost:50005/%s/plotresults.html">
      %s/plotresults.html</a> ... """ % (rundir,rundir)
