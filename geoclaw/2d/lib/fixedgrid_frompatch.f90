

subroutine fixedgrid_frompatch(mx,my,meqn,mbc,maux,q,aux,dx,dy, &
           xlower,ylower,level,time,time_afterstep)

    ! Do the new fixed grid stuff on all fgrids, updating 
    ! based on the patch passed in.

    use fixedgrid_module

    implicit none
    integer, intent(in) :: mx,my,meqn,mbc,maux,level
    real(kind=8), intent(in) :: q(1-mbc:mx+mbc, 1-mbc:my+mbc, meqn)
    real(kind=8), intent(in) :: aux(1-mbc:mx+mbc, 1-mbc:my+mbc, maux)
    real(kind=8), intent(in) :: dx,dy,xlower,ylower,time,time_afterstep

    real(kind=8), allocatable, dimension(:,:) :: fg_values
    logical, allocatable, dimension(:) :: mask_fgrid
    type(fgrid), pointer :: fg
    integer :: ifg,k,mv

    if (FG_num_fgrids == 0) then
        return
        endif 

    !write(61,*) '++++ In frompatch, level,mx,my,xlower,ylower'
    !write(61,*) level,mx,my,xlower,ylower
    do ifg=1,FG_num_fgrids
        fg => FG_fgrids(ifg)
        !write(61,*) '++++ frompatch xNbb', fg%x1bb, fg%x2bb

        if (FG_DEBUG) then
            write(61,61) ifg,level,time
 61         format('---------- In fixedgrid_frompatch ----------',/, &
               'ifg = ',i2,' level = ',i1,' time = ',d16.6)
            endif
        if (time_afterstep <= minval(fg%t_last_updated)+fg%dt_for_max) then
            write(61,68) time, minval(fg%t_last_updated)
 68         format('++++ Skipping update at t = ', e20.11,' min t_last = ', &
                   e20.11)
        else
            write(61,67) time, minval(fg%t_last_updated)
 67         format('++++ Doing update at t = ', e20.11,' min t_last = ', &
                   e20.11)
            endif
        if ((time >= fg%tstart_max) .and. (time <= fg%tend_max) .and. &
                (level >= fg%min_level_for_max) .and. &
                (level >= minval(fg%levelmax)) .and. &
                (time_afterstep > minval(fg%t_last_updated)+fg%dt_for_max)) &
                then
            ! Otherwise this level won't update any fg%valuemax elements.
            !write(61,*) '+++ Setting fg_values'

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
                    fg%t_last_updated(k) = time
                    do mv=1,FG_NUM_VAL
                        !print *,'+++ updating fg%valuemax(mv,k),fg_values(mv,k):',&
                        !       fg%valuemax(mv,k),fg_values(mv,k)
                        if ((level > fg%levelmax(k)) .or. &
                              (fg_values(mv,k) > fg%valuemax(mv,k))) then
                            fg%valuemax(mv,k) = fg_values(mv,k)
                            ! also keep track of time maximum happened:
                            fg%tmax(mv,k) = time  
                            endif
                        enddo
                    fg%levelmax(k) = level
                    endif
                enddo
            endif
        enddo

end subroutine fixedgrid_frompatch
