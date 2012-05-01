

subroutine fixedgrid_frompatch(mx,my,meqn,mbc,maux,q,aux,dx,dy, &
           xlower,ylower,level,time)

    ! Do the new fixed grid stuff on all fgrids, updating 
    ! based on the patch passed in.

    use fixedgrid_module

    implicit none
    integer, intent(in) :: mx,my,meqn,mbc,maux,level
    real(kind=8), intent(in) :: q(1-mbc:mx+mbc, 1-mbc:my+mbc, meqn)
    real(kind=8), intent(in) :: aux(1-mbc:mx+mbc, 1-mbc:my+mbc, maux)
    real(kind=8), intent(in) :: dx,dy,xlower,ylower,time

    real(kind=8), allocatable, dimension(:,:) :: fg_values
    logical, allocatable, dimension(:) :: mask_fgrid
    type(fgrid), pointer :: fg
    integer :: ifg,k,mv

    if (FG_num_fgrids == 0) then
        return
        endif 

    do ifg=1,FG_num_fgrids
        fg => FG_fgrids(ifg)

        write(61,61) ifg,level,time
 61     format('---------- In fixedgrid_frompatch ----------',/, &
               '+++ ifg = ',i2,' level = ',i1,' time = ',d16.6)
        if ((time >= fg%tstart) .and. (time <= fg%tend) .and. &
                (level >= fg%min_level_for_max) .and. &
                (level >= minval(fg%levelmax))) then
            ! Otherwise this level won't update any fg%valuemax elements.
            write(61,*) '+++ Setting fg_values'

            allocate(mask_fgrid(1:fg%npts))
            allocate(fg_values(FG_NUM_VAL, 1:fg%npts))
        
            ! Interpolate from q on patch to desired values fg_values on fgrid.
            call fixedgrid_interpolate(mx,my,meqn,mbc,maux,q,aux, &
                 dx,dy,xlower,ylower,ifg,level,fg_values,mask_fgrid,fg%npts)
        
            do k=1,fg%npts
                ! fg_values is set only at points k where the fgrid intersects the
                ! patch, indicated by mask_fgrid(k) == .true.
                ! Also: only update valuemax if the current patch is at least
                ! as high a level as the patch last used to update:
                if (mask_fgrid(k) .and. (level >= fg%levelmax(k))) then
                    do mv=1,FG_NUM_VAL
                        !print *,'+++ updating fg%valuemax(mv,k),fg_values(mv,k):',&
                        !       fg%valuemax(mv,k),fg_values(mv,k)
                        if ((level > fg%levelmax(k)) .or. &
                              (fg_values(mv,k) > fg%valuemax(mv,k))) then
                            fg%valuemax(mv,k) = fg_values(mv,k)
                            endif
                        enddo
                    fg%levelmax(k) = level
                    endif
                enddo
            endif
        enddo

end subroutine fixedgrid_frompatch
