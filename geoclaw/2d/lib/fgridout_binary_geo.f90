
! Binary output version !
!======================================================================
      subroutine fgridout(fgrid1,fgrid2,fgrid3,xlowfg,xhifg,ylowfg, &
                 yhifg,mxfg,myfg,mvarsfg,mvarsfg2,toutfg,ioutfg,ng, &
                 ioutarrival,ioutflag)
!======================================================================

      implicit double precision (a-h,o-z)

      dimension fgrid1(1:mxfg,1:myfg,mvarsfg)
      dimension fgrid2(1:mxfg,1:myfg,mvarsfg)
      dimension fgrid3(1:mxfg,1:myfg,mvarsfg2)

      real(kind=4), allocatable, dimension(:,:,:) :: fgrid1b,fgrid2b,fgrid3b
      real(kind=4) :: tau

      character*15 fgoutname

!=====================FGRIDOUT==========================================
!         # This routine interpolates in time and then outputs a grid at
!         # time=toutfg

!     # Binary output version, outputting only h, hu, hv
!=======================================================================

      allocate(fgrid1b(1:mxfg,1:myfg,1:mvarsfg))
      allocate(fgrid2b(1:mxfg,1:myfg,1:mvarsfg))
      allocate(fgrid3b(1:mxfg,1:myfg,1:mvarsfg2))

!     # convert to 4-byte versions:
      fgrid1b = fgrid1
      fgrid2b = fgrid2
      fgrid3b = fgrid3

!     ASCII file for times and grid data:
      fgoutname = 'fort.fgnnt_xxxx'
      ngridnumber= ng
      do ipos = 9, 8, -1
          idigit= mod(ngridnumber,10)
          fgoutname(ipos:ipos) = char(ichar('0') + idigit)
          ngridnumber = ngridnumber/ 10
      enddo

      noutnumber=ioutfg
      do ipos = 15, 12, -1
          idigit = mod(noutnumber,10)
          fgoutname(ipos:ipos) = char(ichar('0') + idigit)
          noutnumber = noutnumber / 10
      enddo

      open(unit=90,file=fgoutname,status='unknown', &
             form='formatted')
      write(90,"(e18.8)") toutfg
      write(90,"(i6)") mxfg
      write(90,"(i6)") myfg
      write(90,"(e18.8)") xlowfg
      write(90,"(e18.8)") ylowfg
      write(90,"(e18.8)") xhifg
      write(90,"(e18.8)") yhifg
      close(90)


!     Binary file for data:
      fgoutname = 'fort.fgnnb_xxxx'
      ngridnumber= ng
      do ipos = 9, 8, -1
          idigit= mod(ngridnumber,10)
          fgoutname(ipos:ipos) = char(ichar('0') + idigit)
          ngridnumber = ngridnumber/ 10
      enddo

      noutnumber=ioutfg
      do ipos = 15, 12, -1
          idigit = mod(noutnumber,10)
          fgoutname(ipos:ipos) = char(ichar('0') + idigit)
          noutnumber = noutnumber / 10
      enddo


      open(unit=90,file=fgoutname,status='unknown', &
             form='unformatted',access='direct',recl=4*mxfg*myfg)



      indhmin = ioutarrival+2
      indhmax = ioutarrival+3
        
!     # interpolate the grid in time, to the output time, using 
!     # the solution in fgrid1 and fgrid2, which represent the 
!     # solution on the fixed grid at the two nearest computational times

      write(90,rec=1) (1.e0 - tau)*fgrid1b(:,:,1) + tau*fgrid2b(:,:,1)
      write(90,rec=2) (1.e0 - tau)*fgrid1b(:,:,2) + tau*fgrid2b(:,:,2)
      write(90,rec=3) (1.e0 - tau)*fgrid1b(:,:,3) + tau*fgrid2b(:,:,3)
!     # output eta = h+B rather than the eta with nan's:
      write(90,rec=4) (1.e0 - tau)*(fgrid1b(:,:,1)+fgrid1b(:,:,4)) &
                       + tau*(fgrid2b(:,:,1) + fgrid2b(:,:,4))
      write(90,rec=5) fgrid3b(:,:,indetamax)

      close(unit=90)

      write(*,*) 'FGRIDOUT binary output at frame ',ioutfg
      end subroutine
