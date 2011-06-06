#!/usr/bin/env python

print 'Content-type: text/html\n'
print r"""

  <html> 
  <title>EagleClaw Run Menu</title>
  <head>
  <link type="text/css" rel="stylesheet"
        href="http://localhost:50005/eagleclaw/eagleclaw.css">
  </head>
  
  
  <SCRIPT SRC= http://localhost:50005/doc/load.js> </SCRIPT>
  <!- latex macros: -->
  $\newcommand{\vector}[1]{\left[\begin{array}{c} #1 \end{array}\right]}$ 
  $\newenvironment{matrix}{\left[\begin{array}{cccccccccc}} {\end{array}\right]}$ 
  
  
  <body>
  
  <eagle1>EagleClaw -- Run Menu</eagle1>
  <eagle2>Easy Access Graphical Laboratory for Exploring Conservation
  Laws</eagle2>

"""

import cgi,os,sys,time
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
    <p> <h2> Error importing pyclaw.eagle" </h2> <p> <pre>
    """
    traceback.print_exc()
    sys.exit(1)

try:
    form = cgi.FieldStorage()
    rundir = form.getvalue('rundir')
    xdir = form.getvalue('xdir')
    exdir = form.getvalue('exdir')
    reset = form.getvalue('reset')
except:
    print "<p>Error reading form"


try:
    fullrundir = os.path.join(clawdir,rundir)
    fullxdir = os.path.join(clawdir,xdir)
    fullexdir = os.path.join(clawdir,exdir)
    outdir = os.path.join(rundir,'output')
    fulloutdir = os.path.join(clawdir,outdir)
    thisdir = '$CLAW/' + rundir
except:
    print "<p>Error setting directories"

try:
    os.chdir(fullrundir)
except:
    print "Error -- can't move to ", fullrundir
    
try:
    sys.path.append(os.getcwd())
    import eagleforms
except:
    print '<p> *** Error importing eagleforms.py in directory %s<p>' \
           % os.getcwd()
    traceback.print_exc()
    

print """
  <eagle4>Location:</eagle4>
      <p class="indent1">
      Current run-directory: &nbsp;&nbsp; %s </p>
      <p class="indent1">
      Template directory for this example:     &nbsp;&nbsp;   $CLAW/%s
      </p>
    """   % (rundir, exdir)


print """
  <p>
  <eagle4>Problem description:</eagle4>
  <div class="eagle_description">
  <p>

"""

try:
    print eagleforms.problem_description()
except:
    print "<p>Error setting problem description "
    print "Function problem_description should be defined in "
    print '    ',   fullexdir + '/eagleforms.py'


print """
  <p>
  More about this example and the source code:
  <a href="http://localhost:50005/%s/README.html">README.html</a>
  </p></div>
""" % exdir  # used to be rundir!



os.chdir(fullrundir)

print """
  <form action="http://localhost:50005/cgi-bin/eaglerun.py.cgi"
               method="POST">
  <input readonly type="hidden" name="xdir" value = "%s">
  <input readonly type="hidden" name="exdir" value = "%s">
  <input readonly type="hidden" name="rundir" value = "%s">
  """ % (xdir, exdir, rundir)

try:
    # make the rest of the form
    if reset:
        runform = eagle.EagleForm(reset)
    else:
        runform = eagle.EagleForm()

    runform = eagleforms.make_runform(runform)
except:
    print """<p>*** Error with the function make_runform defined
           in file %s/eagleforms.py""" % fullrundir
    traceback.print_exc()
    sys.exit(1)

datafiles = []
for datafile in runform.datafiles:
    datafiles.append(os.path.join(fullrundir, datafile))
runform.datafiles = datafiles
#print '<p> in eaglerunmenu: datafiles = ', datafiles

try:
    # store the parameter names and data files for use in the cgi-script:
    print """
      <input readonly type="hidden" name="params" value="%s">
      <input readonly type="hidden" name="datafiles" value="%s">
      """ % (str(runform.form_params), str(runform.datafiles))
except:
    print """
      <p>*** Error writing runform.form_params ' %s <br>
          or runform.datafiles = %s<p>
      """ % (str(runform.form_params), str(runform.datafiles))
    traceback.print_exc()
    sys.exit(1)


print """
  <p>
  <eagle4>Run the Clawpack code:</eagle4>
  <p class="indent1">
  <input type="submit" name=request value="Run claw">
  </p>
  </form>
  <p> &nbsp; <p>

  <eagle4>Other options:</eagle4>
  <form action="http://localhost:50005/cgi-bin/eaglerunmenu.py.cgi" method="POST">
  <input readonly type="hidden" name="xdir" value="%s">
  <input readonly type="hidden" name="exdir" value="%s">
  <input readonly type="hidden" name="rundir" value="%s">
  <input readonly type="hidden" name="reset" value="1">
  <p class="indent1">
  <input type="submit" name=request value="Reset form"> using
      runform.initial_defaults from 
      <a href="http://localhost:50005/%s/eagleforms.py">eagleforms.py</a>
      <a href="http://localhost:50005/%s/eagleforms.py.html">[.html]</a>
  </p>
  </form>
    """  % (xdir, exdir, rundir, rundir, rundir)


print """

  <p class="indent1">
      <a href="http://localhost:50005/%s/eaglemenu.html">Return to Main Menu</a>
  </p>

  <p class="indent1">
  <a href="http://localhost:50005/eagleclaw/examples.html">
  Return to EagleClaw Examples Index</a>
  </p>

  </body>
  </html>

""" % rundir


del runform  # cleans up by closing the eagle.db database
