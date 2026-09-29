#
# (C) Copyright 2000 - 2009
# Wolfgang Denk, DENX Software Engineering, wd@denx.de.
#
# See file CREDITS for list of people who contributed to this
# project.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307 USA
#

Summary:
========

This directory contains the source code for U-Boot, a boot loader for
Embedded boards based on PowerPC, ARM, MIPS and several other
processors, which can be installed in a boot ROM and used to
initialize and test the hardware or to download and run application
code.

The development of U-Boot is closely related to Linux: some parts of
the source code originate in the Linux source tree, we have some
header files in common, and special provision has been made to
support booting of Linux images.

Some attention has been paid to make this software easily
configurable and extendable. For instance, all monitor commands are
implemented with the same call interface, so that it's very easy to
add new commands. Also, instead of permanently adding rarely used
code (for instance hardware test utilities) to the monitor, you can
load and run it dynamically.


Status:
=======

In general, all boards for which a configuration option exists in the
Makefile have been tested to some extent and can be considered
"working". In fact, many of them are used in production systems.

In case of problems see the CHANGELOG and CREDITS files to find out
who contributed the specific port. The MAINTAINERS file lists board
maintainers.


Where to get help:
==================

In case you have questions about, problems with or contributions for
U-Boot you should send a message to the U-Boot mailing list at
<u-boot@lists.denx.de>. There is also an archive of previous traffic
on the mailing list - please search the archive before asking FAQ's.
Please see http://lists.denx.de/pipermail/u-boot and
http://dir.gmane.org/gmane.comp.boot-loaders.u-boot


Where to get source code:
=========================

The U-Boot source code is maintained in the git repository at
git://www.denx.de/git/u-boot.git ; you can browse it online at
http://www.denx.de/cgi-bin/gitweb.cgi?p=u-boot.git;a=summary

The "snapshot" links on this page allow you to download tarballs of
any version you might be interested in. Official releases are also
available for FTP download from the ftp://ftp.denx.de/pub/u-boot/
directory.

Pre-built (and tested) images are available from
ftp://ftp.denx.de/pub/u-boot/images/


Where we come from:
===================

- start from 8xxrom sources
- create PPCBoot project (http://sourceforge.net/projects/ppcboot)
- clean up code
- make it easier to add custom boards
- make it possible to add other [PowerPC] CPUs
- extend functions, especially:
  * Provide extended interface to Linux boot loader
  * S-Record download
  * network boot
  * PCMCIA / CompactFlash / ATA disk / SCSI ... boot
- create ARMBoot project (http://sourceforge.net/projects/armboot)
- add other CPU families (starting with ARM)
- create U-Boot project (http://sourceforge.net/projects/u-boot)
- current project page: see http://www.denx.de/wiki/U-Boot


Names and Spelling:
===================

The "official" name of this project is "Das U-Boot". The spelling
"U-Boot" shall be used in all written text (documentation, comments
in source files etc.). Example:

	This is the README file for the U-Boot project.

File names etc. shall be 

[...截断...]

based on the string "u-boot". Examples:

	include/asm-ppc/u-boot.h

	#include <asm/u-boot.h>

Variable names, preprocessor constants etc. shall be either based on
the string "u_boot" or on "U_BOOT". Example:

	U_BOOT_VERSION		u_boot_logo
	IH_OS_U_BOOT		u_boot_hush_start


Versioning:
===========

U-Boot uses a 3 level version number containing a version, a
sub-version, and a patchlevel: "U-Boot-2.34.5" means version "2",
sub-version "34", and patchlevel "4".

The patchlevel is used to indicate certain stages of development
between released versions, i. e. officially released versions of
U-Boot will always have a patchlevel of "0".


Directory Hierarchy:
====================

/arch			Architecture specific files
  /arm			Files generic to ARM architecture
    /cpu		CPU specific files
      /arm720t		Files specific to ARM 720 CPUs
      /arm920t		Files specific to ARM 920 CPUs
	/at91rm9200	Files specific to Atmel AT91RM9200 CPU
	/imx		Files specific to Freescale MC9328 i.MX CPUs
	/s3c24x0	Files specific to Samsung S3C24X0 CPUs
      /arm925t		Files specific to ARM 925 CPUs
      /arm926ejs	Files specific to ARM 926 CPUs
      /arm1136		Files specific to ARM 1136 CPUs
      /ixp		Files specific to Intel XScale IXP CPUs
      /pxa		Files specific to Intel XScale PXA CPUs
      /s3c44b0		Files specific to Samsung S3C44B0 CPUs
      /sa1100		Files specific to Intel StrongARM SA1100 CPUs
    /lib		Architecture specific library files
  /avr32		Files generic to AVR32 architecture
    /cpu		CPU specific files
    /lib		Architecture specific library files
  /blackfin		Files generic to Analog Devices Blackfin architecture
    /cpu		CPU specific files
    /lib		Architecture specific library files
  /i386			Files generic to i386 architecture
    /cpu		CPU specific files
    /lib		Architecture specific library files
  /m68k			Files generic to m68k architecture
    /cpu		CPU specific files
      /mcf52x2		Files specific to Freescale ColdFire MCF52x2 CPUs
      /mcf5227x		Files specific to Freescale ColdFire MCF5227x CPUs
      /mcf532x		Files specific to Freescale ColdFire MCF5329 CPUs
      /mcf5445x		Files specific to Freescale ColdFire MCF5445x CPUs
      /mcf547x_8x	Files specific to Freescale ColdFire MCF547x_8x CPUs
    /lib		Architecture specific library files
  /microblaze		Files generic to microblaze architecture
    /cpu		CPU specific files
    /lib		Architecture specific library files
  /mips			Files generic to MIPS architecture
    /cpu		CPU specific files
    /lib		Architecture specific library files
  /nios2		Files generic to Altera NIOS2 architecture
    /cpu		CPU specific files
    /lib		Architecture specific library files
  /powerpc		Files generic to PowerPC architecture
    /cpu		CPU specific files
      /74xx_7xx		Files specific to Freescale MPC74xx and 7xx CPUs
      /mpc5xx		Files specific to Freescale MPC5xx CPUs
      /mpc5xxx		Files specific to Freescale MPC5xxx CPUs
      /mpc8xx		Files specific to Freescale MPC8xx CPUs
      /mpc8220		Files specific to Freescale MPC8220 CPUs
      /mpc824x		Files specific to Freescale MPC824x CPUs
      /mpc8260		Files specific to Freescale MPC8260 CPUs
      /mpc85xx		Files specific to Freescale MPC85xx CPUs
      /ppc4xx		Files specific to AMCC PowerPC 4xx CPUs
    /lib		Architecture specific library files
  /sh			Files generic to SH architecture
    /cpu		CPU specific files
      /sh2		Files specific to sh2 CPUs
      /sh3		Files specific to sh3 CPUs
      /sh4		Files specific to sh4 CPUs
    /lib		Architecture specific library files
  /sparc		Files generic to SPARC architecture
    /cpu		CPU specific files
      /leon2		Files specific to Gaisler LEON2 SPARC CPU
      /leon3		Files specific to Gaisler LEON3 SPARC CPU
    /lib		Architecture specific library files
/api			Machine/arch independent API for external apps
/board			Board dependent files
/common			Misc architecture independent functions
/disk			Code for disk drive partition handling
/doc			Documentation (don't expect too muc