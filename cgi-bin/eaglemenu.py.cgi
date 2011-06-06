#!/usr/bin/env python


print 'Content-type: text/html\n'
print r"""

  <html> 
  <head>
  <link type="text/css" rel="stylesheet"
  href="http://localhost:50005/eagleclaw/eagleclaw.css">
  </head>
  
  
  <SCRIPT SRC= http://localhost:50005/doc/load.js> </SCRIPT>
  <!- latex macros: -->
  $\newcommand{\vector}[1]{\left[\begin{array}{c} #1 \end{array}\right]}$ 
  $\newenvironment{matrix}{\left[\begin{array}{cccccccccc}} {\end{array}\right]}$ 
  
  
  <body>
  
  <eagle1>EagleClaw -- Main Menu</eagle1>
  
  
  <eagle2>Easy Access Graphical Laboratory for
          Exploring Conservation Laws</eagle2>
  
  <p>&nbsp;<p>

"""


import cgi,os,sys
import traceback
import cgitb
cgitb.enable()
try: 
    import eagletools
except: 
    print '  <p> Error: No eagletools found<p>'

eagletools.setenv()
clawdir = os.environ['CLAW']

try:
    form = cgi.FieldStorage()
    rundir = form.getvalue('rundir')
    exdir = form.getvalue('exdir')
    fullexdir = os.path.join(clawdir,exdir)
    xdir = exdir  # assume executable is in template directory
    fullxdir = os.path.join(clawdir,xdir)
except:
    print "Error reading form"

if rundir != 'NORUN':
    fullrundir = os.path.join(clawdir,rundir)
    outdir = os.path.join(rundir,'output')
    fulloutdir = os.path.join(clawdir,outdir)
    eagledir = os.path.join(rundir,'eagleclaw')
    plotdir = os.path.join(rundir,'eagleplots')
    readmedir = exdir  # used to be rundir!
    thisdir = '$CLAW/' + rundir
    formsdir = fullrundir + '/eagleclaw'
else:
    readmedir = exdir
    thisdir = '$CLAW/' + exdir
    formsdir = fullexdir + '/eagleclaw'
    

try:
    os.chdir(formsdir)
except:
    print 'Error -- cannot move to directory ',formsdir
    
try:
    sys.path.append(os.getcwd())
    import forms
except:
    print '<p> *** Error importing forms.py in directory %s<p>' \
           % os.getcwd()
    traceback.print_exc()
    

if rundir != 'NORUN':
    print """
      <eagle4>Location:</eagle4>
      <p class="indent1">
      Current run-directory: &nbsp;&nbsp; <a href="http://localhost:50005/%s">%s</a>  &nbsp; ... &nbsp; 
      <a href="http://localhost:50005/%s/eagleclaw/index.html">/eagleclaw/index.html</a>
      </p>
    """   % (rundir, rundir, rundir)
    print """
  <p class="indent1">
  Template directory for this example:     &nbsp;&nbsp;   
  <a href="http://localhost:50005/%s">%s</a>      &nbsp; ... &nbsp; 
  <a href="http://localhost:50005/%s/eagleclaw/index.html">/eagleclaw/index.html</a>
  </p>
    """ % (exdir,exdir,exdir)
else:
    print """
      <eagle4>Location:</eagle4>
      <p class="indent1"> %s </p>
    """ % thisdir





print """
  <p>
  <eagle4>Problem description:</eagle4>
  <div class="eagle_description">
  <p>

"""

try:
    print forms.problem_description()
except:
    print "<p>Error setting problem description "
    print "Function problem_description should be defined in "
    print '    ',   fullexdir + '/eagleclaw/forms.py'


print """
  <p>
  More about this example and the source code:
  <a href="http://localhost:50005/%s/README.html">README.html</a>
  </p></div>
""" % readmedir



#---------------------------------------------------------------------

print """
  <eagle4>Run the code and plot results:</eagle4>
  <p>
  """

nextstep = int(form.getvalue('nextstep'))

#----------------
#---- Step 1 ----
#----------------

if rundir != 'NORUN':
    print """

  <form action="http://localhost:50005/cgi-bin/eaglerunmenu.py.cgi"
        method="POST">
  <input readonly type="hidden" name="rundir" size=80 value=%s>
  <input readonly type="hidden" name="xdir" size=80 value=%s>
  <input readonly type="hidden" name="exdir" size=80 value=%s>
  """ % (rundir,xdir,exdir)

if (nextstep != 1) or (rundir == 'NORUN'):
    print '<p class="indent1"><b>Step 1:&nbsp;</b>'
else:
    print '<p class="indent1"><font color="red"><b>Step 1:&nbsp;</b></font>'

if rundir != 'NORUN':
    print """
  <input type="submit" name=request value="Go to Run Menu">  &nbsp;
  Set parameters and run Clawpack code in current run-directory

  </p>
  </form>
  </p>
    """  
else:
    print """
  [Set parameters and run Clawpack code]  -- You must first create a copy
     (see below).
  </p>
  """


#----------------
#---- Step 2 ----
#----------------

fortfiles = (rundir != 'NORUN')

if fortfiles:
    fortfiles = os.path.isfile(fullrundir + '/output/fort.t0000')

if not fortfiles:
    print """
  <p class="indent1"><b>Step 2:&nbsp;</b>
  [Set plot parameters and plot results]  -- You must first run the code.
  </p>
    """

else:
    print """

  <p class="indent2">

  <form action="http://localhost:50005/cgi-bin/eagleplotmenu.py.cgi"
        method="POST">
  <input readonly type="hidden" name="rundir" value=%s>
  <input readonly type="hidden" name="xdir" value=%s>
  <input readonly type="hidden" name="exdir" value=%s>
    """  % (rundir, xdir, exdir)

    if nextstep==2:
        print """
          <p class="indent1"><font color="red"><b>Step 2:&nbsp;</b></font>
          """
    else:
        print """
          <p class="indent1"><b>Step 2:&nbsp;</b>
          """

    print """
  <input type="submit" name=request 
        value="Go to Plot Menu">&nbsp;
  Set plot parameters and plot results 
  </p>
  </form>
  </p>
    """



#----------------
#---- Step 3 ----
#----------------

if nextstep == 3:
    print '    <p class="indent1"><font color="red"><b>Step 3:&nbsp;</b></font>'
else:
    print '    <p class="indent1"><b>Step 3:&nbsp;</b>'


plotindex = (rundir != 'NORUN')
if plotindex:
    plotindex =  os.path.isfile(fullrundir + '/eagleplots/_PlotIndex.html')

if plotindex:
    print """
       View plots:  &nbsp;&nbsp;
       <a href="http://localhost:50005/%s/eagleplots/_PlotIndex.html">
            From default eagleplots directory</a>
       </p>
    """  % rundir
else:
    print '[View plots]  -- You must first plot results </p>'


if rundir != 'NORUN' and os.path.isfile(fullrundir + '/plotindex.html'):
    print """
  <p class="indent3">
  <a href="%s/plotindex.html">
  From other plot directories in this run-directory
  </a>
  </p>
    """  % rundir

#--------------------------------------------------------------------

print "<p>&nbsp;<p>"

if rundir == 'NORUN':
    print "  <eagle4>Create an executable copy:</eagle4>"
else:
    print "  <eagle4>Create a new run-directory:</eagle4>"




print """

  <p class="indent1">
  <form action="http://localhost:50005/cgi-bin/eaglecopy.py.cgi"
        method="POST">
  <input readonly type="hidden" name="exdir" size=80
         value=%s>
  <p class="indent1">
  <input type="submit" name=request value=
         "Create a fresh copy"> &nbsp; of this example in a new run-directory 
         &nbsp;&nbsp;(first fill in line below if desired)
  </p>
  <p class="indent2">
  Description (optional):  &nbsp;&nbsp;
     <input type="text" name="newrundescr" size=80 value="">
  </p>
  <p class="indent2">
  The new run-directory name will be created dynamically.
  </p>
  </form>
  </p>
  <p>
  <eagle4>Other options:</eagle4>
  <p class="indent1">
  Return to a <a href="http://localhost:50005/eagleclaw/returning.html">
  previous run-directory</a>
  </p>

"""  % exdir


if 0:
    print """


  <p class="indent1">
  <form action="http://localhost:50005/cgi-bin/eaglechdir.py.cgi"
        method="POST">
  <p class="indent1">
  <input type="submit" name=request 
         value="Return to a previous run-directory"> 
         &nbsp;&nbsp; (first fill in line below) 
  </p>
  <p class="indent2">
  Previous run-directory: 
     <input type="text" name="rundir" size=80 value="%s">
  </p>
  <p class="indent1">
  Choose from 
  <a href="http://localhost:50005/eagleclaw/runs/index.html">
     Index of previous runs</a>
  </form>
  </p>
    """  % rundir

print """
  <p class=indent1>Return to 
  <a href="http://localhost:50005/eagleclaw/examples.html">
          EagleClaw Examples Index</a>
  to select a different example.</p>
  """

print "  </html>"
