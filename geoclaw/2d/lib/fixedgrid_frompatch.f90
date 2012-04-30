

subroutine fixedgrid_frompatch(mx,my,meqn,mbc,maux,q,aux,dx,dy, &
           xlower,ylower,level)

    ! Do the new fixed grid stuff on all fgrids, updating 
    ! based on the patch passed in.

    use fixedgrid_module

    implicit none
    integer, intent(in) :: mx,my,meqn,mbc,maux,level
    real(kind=8), intent(in) :: q(1-mbc:mx+mbc, 1-mbc:my+mbc, meqn)
    real(kind=8), intent(in) :: aux(1-mbc:mx+mbc, 1-mbc:my+mbc, maux)
    real(kind=8), intent(in) :: dx,dy,xlower,ylower

    real(kind=8), allocatable, dimension(:,:) :: fg_values
    logical, allocatable, dimension(:) :: mask_fgrid
    type(fgrid), pointer :: fg
    integer :: ifg,k,mv

    do ifg=1,FG_num_fgrids
        fg => FG_fgrids(ifg)

        if (level >= minval(fg%levelmax)) then
            ! Otherwise this level doesn't update any fg%valuemax elements.

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
