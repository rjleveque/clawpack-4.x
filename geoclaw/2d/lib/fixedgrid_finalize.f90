
subroutine fixedgrid_finalize()

    ! Print out the maxval and aux arrays and de-allocate storage.

    use fixedgrid_module

    ! should use mxnest in place of this...
    use dummy_amr_module, only: AMR_MAX_LEVELS  

    implicit none
    character(30) :: fname
    character(1) :: cfg,cma
    integer :: k,ifg,level,mv,ma
    type(fgrid), pointer :: fg

    do ifg=1,FG_num_fgrids

        fg => FG_fgrids(ifg)   

        cfg = char(ichar('0') + ifg)
        fname = 'fort.FG' // cfg // '.valuemax'
        print *, 'Writing to file ', fname
        open(unit=FG_UNIT,file=trim(fname),status='unknown',form='formatted')

        do k=1,fg%npts
            write(FG_UNIT,111) fg%x(k),fg%y(k), fg%levelmax(k), &
                  (fg%valuemax(mv,k), mv=1,FG_NUM_VAL)
 111        format(2d17.8,i4,20d17.8)
            enddo

        close(FG_UNIT)


        do ma=1,FG_NUM_AUX
            cma = char(ichar('0') + ma)
            fname = 'fort.FG' // cfg // '.aux' // cma
            print *, 'Writing to file ', fname
            open(unit=FG_UNIT,file=trim(fname),status='unknown',form='formatted')

            do k=1,fg%npts
                write(FG_UNIT,112) fg%x(k),fg%y(k), &
                      (fg%aux(level,ma,k), level=1,AMR_MAX_LEVELS)
 112            format(2d17.8,20d17.8)
                enddo

            close(FG_UNIT)
            enddo

        ! deallocate(fg%valuemax,fg%levelmax,fg%aux,fg%x,fg%y,fg%t_output)
        enddo

end subroutine fixedgrid_finalize
