#!/usr/bin/env python

print 'Content-type: text/html\n'
print r"""

  <html> 
  <title>EagleClaw Plot Menu</title>
  <head>
  <link type="text/css" rel="stylesheet"
        href="http://localhost:50005/eagleclaw/eagleclaw.css">
  
  
  <SCRIPT SRC= http://localhost:50005/doc/load.js> </SCRIPT>
  <!- latex macros: -->
  $\newcommand{\vector}[1]{\left[\begin{array}{c} #1 \end{array}\right]}$ 
  $\newenvironment{matrix}{\left[\begin{array}{cccccccccc}} {\end{array}\right]}$ 
  
 <!-- ========== Farbtastic color picker script ========== -->
 <script type="text/javascript" src="http://localhost:50005/eagleclaw/farbtastic/jquery.js"></script>
<script type="text/javascript" src="http://localhost:50005/eagleclaw/farbtastic/farbtastic.js"></script>

 <link rel="stylesheet" href="http://localhost:50005/eagleclaw/farbtastic/farbtastic.css" type="text/css" />

 <style type="text/css" media="screen">
   .colorwell {
     border: 2px solid #aaa;
     width: 12em;
     text-align: center;
     cursor: pointer;
   }
   body .colorwell-selected {
     border: 2px solid #000;
     font-weight: bold;
   }
 </style>

 <script type="text/javascript" charset="utf-8">
  $(document).ready(function() {
    $('#demo').hide();
    var f = $.farbtastic('#picker');
    var p = $('#picker').css('opacity', 0.25);
    var selected;
    $('.colorwell')
      .each(function () { f.linkTo(this); $(this).css('opacity', 0.75); })
      .focus(function() {
        if (selected) {
          $(selected).css('opacity',
0.75).removeClass('colorwell-selected');
        }
        f.linkTo(this);
        p.css('opacity', 1);
        $(selected = this).css('opacity', 1).addClass('colorwell-selected');
      });
  });
 </script>
 <!-- ========== end Farbtastic color picker script ========== -->
  </head>

  
  <body>
  
  <eagle1>EagleClaw -- Plot Menu</eagle1>
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
    traceback.print_exc()
    sys.exit(1)

try:
    fullrundir = os.path.join(clawdir,rundir)
    fullxdir = os.path.join(clawdir,xdir)
    fullexdir = os.path.join(clawdir,exdir)
    outdir = os.path.join(rundir,'output')
    fulloutdir = os.path.join(clawdir,outdir)
    thisdir = '$CLAW/' + rundir
except:
    print "<p>Error setting directories"
    print "<p>rundir:",rundir
    print "<p>xdir:",xdir
    print "<p>exdir:",exdir
    traceback.print_exc()
    sys.exit(1)
    

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
  <form action="http://localhost:50005/cgi-bin/eagleplot.py.cgi"
               method="POST">
  <input readonly type="hidden" name="xdir" value = "%s">
  <input readonly type="hidden" name="exdir" value = "%s">
  <input readonly type="hidden" name="rundir" value = "%s">
  """ % (xdir, exdir, rundir)

try:
    if reset:
        plotform = eagle.EagleForm(reset)
    else:
        plotform = eagle.EagleForm()
    # make the rest of the form
    plotform = eagleforms.make_plotform(plotform)
except:
    print """<p>*** Error with the function make_plotform defined
           in file %s/eagleforms.py""" % fullrundir
    traceback.print_exc()
    sys.exit(1)

try:
    # store the parameter names and data files for use in the cgi-script:
    print """
      <input readonly type="hidden" name="params" value="%s">
      <input readonly type="hidden" name="datafiles" value="%s">
      """ % (str(plotform.form_params), str(plotform.datafiles))
except:
    print """
      <p>*** Error writing plotform.form_params ' %s <br>
          or plotform.datafiles = %s<p>
      """ % (str(plotform.form_params), str(plotform.datafiles))
    traceback.print_exc()
    sys.exit(1)

del plotform  # cleans up by closing the eagle.db database

print """
  <p>
  <eagle4>Create the plots:</eagle4>
  <p class="indent1">
  <input type="submit" name=request value="Create plots">
  </p>
  </form>
  <p> &nbsp; <p>
"""

if 0:
    print """
  <p>
  <eagle4>Create the plots:</eagle4>
  <p class="indent1">
  <input type="radio" checked name="plotdiroption", value="0"> 
        In default directory <font color="blue">eagleplots</font> 
  </p>
  <p class="indent1">
  <input type="radio" name="plotdiroption", value="1">
        In a different plot directory named &nbsp;
  <input type="text" name="plotdir" size="30" value="Doesn't work yet">
  </p>
  <p class="indent1">
  <input type="submit" name=request value="Create plots">
  </p>
  </form>
"""
 

print """
  <eagle4>Other options:</eagle4>
  <form action="http://localhost:50005/cgi-bin/eagleplotmenu.py.cgi" method="POST">
  <input readonly type="hidden" name="xdir" value="%s">
  <input readonly type="hidden" name="exdir" value="%s">
  <input readonly type="hidden" name="rundir" value="%s">
  <input readonly type="hidden" name="reset" value="1">
  <p class="indent1">
  <input type="submit" name=request value="Reset form"> using
      plotform.initial_defaults from 
      <a href="http://localhost:50005/%s/eagleforms.py">eagleforms.py</a>
      <a href="http://localhost:50005/%s/eagleforms.py.html">[.html]</a>
  </p>
  </form>
    """  % (xdir, exdir, rundir, rundir, rundir)


plotindex = "%s/eagleplots/_PlotIndex.html" % fullrundir
if os.path.isfile(plotindex):
    print """
      <p class="indent1">
      <a href="http://localhost:50005/%s/eagleplots/_PlotIndex.html">View plots</a> from previous
    plot creation
      </p>
    """ % rundir


print """
  <form action="http://localhost:50005/cgi-bin/eaglerunmenu.py.cgi" method="POST">
  <input readonly type="hidden" name="xdir" value="%s">
  <input readonly type="hidden" name="exdir" value="%s">
  <input readonly type="hidden" name="rundir" value="%s">
  <p class="indent1">
  <input type="submit" name=request value="Return to Run Menu"> 
  </p>
  </form>
    """  % (xdir, exdir, rundir)

print """

  <p class="indent1">
      <a href="http://localhost:50005/%s/eaglemenu.html">Return to Main Menu</a>
  </p>
""" % rundir

#print """
#  <p class="indent1">
#  <a href="PlotsIndex.html">
#  Plots Index for this run-directory</a>
#  </p>
#"""

print """
  <p class="indent1">
  <a href="http://localhost:50005/eagleclaw/examples.html">
  Return to EagleClaw Examples Index</a>
  </p>

  </body>
  </html>

"""



