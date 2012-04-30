"""
Create fixed grid output file in new style.
"""

from numpy import linspace

def makefgrid1():
    mx = 11
    my = 11
    xlower = 0.
    xupper = 20.
    ylower = 0.
    yupper = 20.
    x = linspace(xlower, xupper, mx)
    y = linspace(ylower, yupper, my)
    npts = mx*my

    fname = 'setfixedgrids2.data'
    fid = open(fname,'w')
    fid.write("""
        1          # num_fgrids
        1          # fgno for first fgrid
        1., 2.     # tstart,tend
        1          # min_level_for_max
        0          # num_output
        %s          # npts
        \n""" % npts)

    for j in range(my):
        for i in range(mx):
            fid.write("%20.10e %20.10e\n" % (x[i],y[j]))

    print "Created file ", fname
    fid.close()

if __name__ == "__main__":
    makefgrid1()


