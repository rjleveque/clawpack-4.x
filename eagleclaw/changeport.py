
#
# Fix a set of target files by replacing oldpat with newpat. 
#
# Specialized for changing ports in EagleClaw if for some reason
# port 50005 doesn't work, try a different number.
#
# Execute from $CLAW directory
#

import os,sys,glob

oldpat = 'localhost:50005'
newpat = 'localhost:50005'

def changepat(targetfiles):
    currentdir = os.path.abspath(os.getcwd())
    for file in targetfiles:
        infile = open(file,'r')
        lines = infile.read()
        infile.close()

        if lines.find(oldpat) > -1:
            lines = lines.replace(oldpat, newpat)
            print "Fixed file   ",currentdir+"/"+file
        else:
            print "No change to ",currentdir+"/"+file

        outfile = open(file,'w')
        outfile.write(lines)
        outfile.close()


clawdir = os.getenv('CLAW')
os.chdir(clawdir)

changepat(glob.glob('cgi-bin/*.cgi'))
changepat(glob.glob('doc/load.js'))
changepat(glob.glob('README'))

for (dirpath, subdirs, files) in os.walk(clawdir):
    currentdir = os.path.abspath(os.getcwd())
    os.chdir(os.path.abspath(dirpath))
    targetfiles = glob.glob('*.html')+glob.glob('*.py') 
    changepat(targetfiles)
    os.chdir(currentdir)

