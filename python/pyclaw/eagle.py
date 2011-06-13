
import pyclaw.data, shelve, time, os, re, shutil, glob, string

try:
    import subprocess
except(ImportError):
    print 'Must use a more recent version of Python with module subprocess'
    print 'Python 2.5 is recommended'
    sys.exit(1)  
                
# ============================================================================
#  Class EagleForm containing data for creating an html form for Menu
# ============================================================================
class EagleForm:
    """EagleForm class
    
    EagleForm subclass containing data to create an html form for
    Run Menu or Plot Menu for EagleClaw.

    Generally used in <example-directory>/eagleclaw/forms.py
    to specify how the forms should look and what parameters should be
    set on the forms.

    Members:
        datafiles = List of data files from which this object was created
        attributes = List of the names of the attributes of this class
        form_params = List of parameters that are set on this form.
        value = Dictionary of the values for each member of form_params.
        
    Methods:
        Create one or more lines of html file.
        
                
    """
    # -----------------------
    #  Initialization routine
    # -----------------------
    def __init__(self, *reset):
        """Initialize an EagleForm object
        """
        self.attributes = ['datafiles', 'data','form_params','value']  

        self.datafiles = []   # to hold list of data files *.data


        self.form_params = []   # to hold parameters that must be set
                                # on this form, and read from cgi-script.
                                # This list is built up any time one of the
                                # EagleForm methods is called.

        self.value = {}         # To hold values of parameters read from form
                                # by the cgi script processing the form.

        self.reset = len(reset)>0    # = True if initial_defaults to be used

        self.farbtastic = False      # indicates color picker is used


        # The shelve database eagle.db is used to store the values 
        # when the form is submitted, and these values are used as the
        # initial default values if we are returning to the form.
        # If self.eagledb[P].prev_value is missing for some parameter P, then
        # self.initial_defaults[P] is used instead, or None if that is also
        # missing.

        try:
            self.eagledb = shelve.open('eagle.db')
        except:
            print "*** Error opening eagle.db"
            return 

    # -----------------------
    #  Destructor routine
    # -----------------------
    def __del__(self):

        # close the eagle.db database:
        self.eagledb.close()

        # if Farbtastic is used, need to end the form:
        if self.farbtastic:
            print "</form>"
            pass



    # ------------------------------------------------------
    # Methods that create lines of html file for a cgi-form:
    # ------------------------------------------------------


#   ----------------------------------------------------------------------
    def section(self, title, text = ''):
        print '\n<p><eagle4>%s</eagle4>\n'  % title
        print '<p class = "indent1">'
        print text 
        print '</p>\n'


#   ----------------------------------------------------------------------
    def new_line(self, indent=1):
        print '</p><p class="indent%s">' % indent


#   ----------------------------------------------------------------------
    def hspace(self, spaces=3):
        for i in range(spaces):
            print '&nbsp;'


#   ----------------------------------------------------------------------
    def vspace(self, spaces=1):
        for i in range(spaces):
            print '<p>&nbsp;</p>'


#   ----------------------------------------------------------------------
    def raw_html(self, text=''):
        print text


#   ----------------------------------------------------------------------
    def text_input(self, param, title='', size=8, \
               default_value = None, type='str', min=None, max=None):

        self.form_params.append(param)

        if (default_value is None):
            if self.eagledb.has_key(param) and (not self.reset):
                # use value set last time form was submitted, if it was:
                default_value = self.eagledb[param].prev_value
                #print '<p>in eagle.py....using value from db for %s: %s' \
                #       % (param,default_value)
            elif self.initial_defaults.has_key(param):
                # use initial default set in examples/.../eagleclaw/forms.py:
                default_value = self.initial_defaults[param]
            else:
                default_value = ''

        database_record = EagleDatabase()
        database_record.prev_value = default_value
        database_record.type = type
        database_record.min = min
        database_record.max = max
        # store to the database eagle.db:
        self.eagledb[param] = database_record



        print '<span type="initem">'
        print title, '&nbsp;'
        print '<input type="text" name="%s" size="%s" value="%s">' \
              % (param,size,default_value)
        print '&nbsp;&nbsp;&nbsp;</span>'

        
#   ----------------------------------------------------------------------
    def check_box(self, param, choice='', value='', type='str', \
        checked=False):

        if param not in self.form_params:
            self.form_params.append(param)
            
        if checked is None:
            if self.eagledb.has_key(param) and (not self.reset):
                # use value set last time form was submitted, if it was:
                default_value = self.eagledb[param].prev_value
            elif self.initial_defaults.has_key(param):
                # use initial default set in examples/.../eagleclaw/forms.py:
                default_value = self.initial_defaults[param]
            else:
                default_value = ''

        database_record = EagleDatabase()
        database_record.prev_value = default_value
        database_record.type = type
        # store to the database eagle.db:
        self.eagledb[param] = database_record

	print '<p>eagle.check_box: stored to %s to db' % param
	print '<p>', database_record

        if (checked==True):
            print '<input type="checkbox" checked name="%s", value="%s"> ' \
                  % (param, value)
        else:
            print '<input type="checkbox" name="%s", value="%s"> ' \
                  % (param, value)
        print choice, '  &nbsp; '

        
#   ----------------------------------------------------------------------
    def radio_button(self, param, choice='', value='', type='str', \
        checked=None):

        if param not in self.form_params:
            self.form_params.append(param)
            
        if checked is None:
            if self.eagledb.has_key(param) and (not self.reset):
                # use value set last time form was submitted, if it was:
                default_value = self.eagledb[param].prev_value
            elif self.initial_defaults.has_key(param):
                # use initial default set in examples/.../eagleclaw/forms.py:
                default_value = self.initial_defaults[param]
            else:
                default_value = ''

        database_record = EagleDatabase()
        database_record.prev_value = default_value
        database_record.type = type
        # store to the database eagle.db:
        self.eagledb[param] = database_record

	#print '<p>eagle.radio_button: stored to %s to db' % param
	#print '<p>', database_record

        default_choice = (str(default_value) == str(value))
        if (checked==True) or ((checked==None) and default_choice):
            print '<input type="radio" checked name="%s", value="%s"> ' \
                  % (param, value)
        else:
            print '<input type="radio" name="%s", value="%s"> ' \
                  % (param, value)
        print choice, '  &nbsp; '

#   ----------------------------------------------------------------------
    def farbtastic_picker(self):
        if not self.farbtastic:
            self.farbtastic = True
            # Add a farbtastic color picker to form:
            print """
               <p class="indent1">To use Farbtastic color picker, first
               click a color box below and then pick hue and saturation</p>
               <a href="http://www.acko.net/dev/farbtastic" 
                  style="float: right;"> Farbtastic &nbsp;&nbsp;&nbsp;</a>
               <form action="" style="width: 500px;">
               <div id="picker" style="float: right;"></div>
               <p>
             """
            
#   ----------------------------------------------------------------------
    def farbtastic_input(self, param, title='', size='500px', \
               default_value = None):

        self.form_params.append(param)

        if (default_value is None):
            if self.eagledb.has_key(param) and (not self.reset):
                # use value set last time form was submitted, if it was:
                default_value = self.eagledb[param].prev_value
            elif self.initial_defaults.has_key(param):
                # use initial default set in examples/.../eagleclaw/forms.py:
                default_value = self.initial_defaults[param]
            else:
                default_value = ''

        database_record = EagleDatabase()
        database_record.prev_value = default_value
        # store to the database eagle.db:
        self.eagledb[param] = database_record


        print """%s &nbsp; <input type="text" id="%s" name="%s" 
         class="colorwell" value="%s" >""" \
         % (title, param, param, default_value)


# =========================================================

class EagleDatabase(object):
    def __init__(self):
        self.prev_value = None
        self.type = None
        self.min = None
        self.max = None
    def __repr__(self):
        s = ' prev_value=%s, type=%s, min=%s, max=%s<p>\n' \
	    % (self.prev_value, self.type, self.min, self.max)
	return s

# =========================================================


#--------------------------------
def check_input(data, params, eagledb):
#--------------------------------
    """
    Check input from form, stored in dictionary params, to make sure
    it is valid input.  Requirements are stored in eagledb.
    """
     
    #print '<p>In check_input, eagledb = ',eagledb
    errors = False
    #for (param, value) in params.iteritems():
    for param in params:
	value = getattr(data, param, None)
        error_in_param = False
	if not eagledb.has_key(param):
	    print """<p>*** eagle.check_input error: parameter %s is missing from
	          eagle.db"""  % param
	    error_in_param = True
	    value1 = None
        elif eagledb[param].type:
            try:
                exec("value1 = %s(value)" % eagledb[param].type)
            except:
                error_in_param = True
		value1 = value
                print """<p>*** eagle.check_input error in type of parameter %s: 
                      %s required</p>""" \
                      % (param, eagledb[param].type)
                print "*** Value = ",value,"....  type = ",type(value)

            if ((not error_in_param) and eagledb[param].type in ['int', 'float']):
                if ((eagledb[param].min is not None) and \
                  (value1 < eagledb[param].min)):
                    error_in_param = True
		    value1 = eagledb[param].min
                    print """<p>*** eagle.check_input error in value of parameter %s, 
                         must lie between min = %s and max = %s </p>""" \
                      % (param, eagledb[param].min, eagledb[param].max)
                if ((eagledb[param].max is not None) and \
                  (value1 > eagledb[param].max)):
                    error_in_param = True
		    value1 = eagledb[param].max
                    print """<p>*** eagle.check_input error in value of parameter %s, 
                         must lie between min = %s and max = %s </p>""" \
                      % (param, eagledb[param].min, eagledb[param].max)
 
	else:
	    #print '<p> in else clause, eagledb[param] = ', eagledb[param]
	    value1 = value

	#print '<p> in eagle.py: %s is int: ' % param, isinstance(value1,int)
        exec('data.%s = value1' % param)
        errors = errors or error_in_param

    #data.errors = errors
    return (data, errors)


#----------------------------------------------------------------------
def copytreefilter(oldroot,newroot,omitdirs='[.]svn',omitfiles='[.]', 
                   verbose=1):
#----------------------------------------------------------------------
    """
      Recursively copy directory oldroot to new directory newroot.
      omitdir is a regular expression indicating directories to omit
      omitfiles is a regular expression indicating files to omit
      verbose=1 will print after successful completion.
      verbose=2 will print after each file copy.
    """

    oldroot = os.path.abspath(oldroot)
    newroot = os.path.abspath(newroot)

    try:
        omitdirs = re.compile(omitdirs)
    except:
        print "Problem compiling regular expression omitdirs"
        return
    try:
        omitfiles = re.compile(omitfiles)
    except:
        print "Problem compiling regular expression omitfiles"
        return

    if not os.path.isdir(oldroot):
        print "First argument must be an existing directory"
        return

    if os.path.exists(newroot):
        print "%s already exists - exiting" % newroot
        return

    for (dpath, dnames, fnames) in os.walk(oldroot):

        # filter out subdirectories that should be omitted:
        dnames[:] = [d for d in dnames if not omitdirs.search(d)]

        newdir = dpath.replace(oldroot,newroot)
        try: 
            os.mkdir(newdir)
        except: 
            print "aborting -- cannot make newdir = ", newdir
            return
        for file in fnames:
            # filter out files that should be omitted:
            if not omitfiles.search(file):
                shutil.copy2(os.path.join(dpath,file), \
                             os.path.join(newdir,file))
                if verbose > 1:
                    print "copied %s to %s   " \
                          % (file, os.path.join(newdir,file))

    if verbose > 0:
        print "Successfully copied %s to %s" % (oldroot,newroot)
        

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


#------------------------------------------------------------
def runclaw(xdir='.', rundir='.', outdir='.', overwrite=False, \
             xclawcmd = 'xclaw', xclawout=None, xclawerr=None, \
             savecode=False, runmake=False, verbose=True):
#------------------------------------------------------------
    '''
    Run the command xdir/xclawcmd, directing the output fort.*
    files to outdir, writing unit 6 timestepping info to file xclawout.
    Runtime error messages are written to file xclawerr.
    If xclawout(xclawerr) is None, then output to stdout(stderr).

    If savecode==True, archive a copy of the code into directory outdir.

    This function returns the returncode from the process running xclawcmd,
    which will be nonzero if a runtime error occurs.
    '''

    debug = False
    if debug:
        print "<p>In runclaw... xdir = ",xdir
        print "<p>outdir = ",outdir
        print "<p>xclawout = ",xclawout
        print "<p>"
    
    startdir = os.getcwd()
    xdir = os.path.abspath(xdir)
    xclawcmd = os.path.join(xdir,xclawcmd)

    try:
	os.chdir(xdir)
    except:
        print "Cannot change to directory xdir = ",xdir
	return 999


    if runmake:
	if os.path.isfile('Makefile'):
            try:
                os.system('make')
            except:
                print 'Warning: make failed in directory xdir = ',xdir
        else:
            print 'Warning: no make file in directory xdir = ',xdir

    
    if outdir != '.':
        if os.path.isfile(outdir):
            print "Error: outdir specified is a file"
            return 999
        elif (os.path.isdir(outdir) & overwrite):
            if verbose:
                print "Directory ", outdir, " already exists, "
                print "   will be removed and recreated..."
            try:
                shutil.rmtree(outdir)
            except:
                print "Cannot remove directory ",outdir
                return 999
        elif (os.path.isdir(outdir) & (not overwrite)):
            print "Directory ", outdir, " already exists."
            print "Remove directory with 'rm -r ",outdir,"' and try again,"
            print "  or use overwrite=True in call to runclaw"
            return 999

        try:
            os.mkdir(outdir)
        except:
            print "Cannot make directory ",outdir
            return 999
        if verbose:
            print "Created output directory ",outdir

    
    try:
        os.chdir(rundir)
    except:
        print "Cannot change to directory ",rundir
        return 999

    datafiles = glob.glob('*.data')
    if datafiles == ():
        print "Warning: no data files found in directory ",rundir
    else:
        if rundir != outdir:
            for file in datafiles:
                shutil.copy(file,os.path.join(outdir,file))
            if os.path.isfile('mapc2p.py'):
                file = 'mapc2p.py'
                shutil.copy(file,os.path.join(outdir,file))

    if xclawout:
	xclawout = open(xclawout,'wb')
    if xclawerr:
	xclawerr = open(xclawerr,'wb')

    os.chdir(outdir)

    #print "\nIn directory outdir = ",outdir,"\n"

    # execute command to run fortran program:

    try:
        #print "\nExecuting ",xclawcmd, "  ...  "
        pclaw = subprocess.Popen(xclawcmd,stdout=xclawout,stderr=xclawerr)
        pclaw.wait()   # wait for code to run

        if pclaw.returncode == 0:
            print "\nFinished executing\n"
        else:
            print "\n *** Runtime error: return code = %s\n " % pclaw.returncode
    except:
        print "\nError: could not execute command\n"
        return 999

    os.chdir(startdir)
    return pclaw.returncode
