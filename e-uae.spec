%define cdrname		cdrtools
%define cdrmainvers	2.01
%define cdrvers 	%{cdrmainvers}a38
%define wiprel		WIP4

# For building with SCSI support
%define build_scsi 1
%{?_with_scsi: %global build_scsi 1}
%{?_without_scsi: %global build_scsi 0}

Summary: A software emulation of the Amiga system
Name: e-uae
Version: 0.8.29
Release: %mkrel 2.%{wiprel}.1
URL: http://sourceforge.net/projects/uaedev/
Source0: e-uae-%{version}-%{wiprel}.tar.bz2
Source1: ftp://ftp.berlios.de/pub/cdrecord/alpha/%{cdrname}-%{cdrvers}.tar.bz2
Patch2: uae-scsi.patch
Patch4: uae-0.8.25-20040302-libscg.patch
Patch5: uae-0.8.22-openscsi.patch
Patch6: e-uae-0.8.27-fucomi.patch
Patch7:	e-uae-0.8.29-WIP4-sdlkeys-wahcade.patch
Patch8:	e-uae-fix-string-format-bug.patch
License: GPL
Group: Emulators
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: X11-devel
BuildRequires: gtk+-devel
BuildRequires: gtk+2-devel
BuildRequires: glib-devel
BuildRequires: SDL-devel x11-data-xkbdata
BuildRequires: attr-devel
Conflicts: uae
Obsoletes: uaedev
Provides: uaedev

%description
UAE is a software emulation of the Amiga system hardware, which
enables you to run most available Amiga software.  Since it is a
software emulation, no extra or special hardware is needed.  The Amiga
hardware is emulated accurately, so that Amiga software is tricked
into thinking it is running on the real thing.  Your computer's
display, keyboard, hard disk and mouse assume the roles of their
emulated counterparts.

Note that to fully emulate the Amiga you need the Amiga KickStart ROM
images, which are copyrighted and, of course, not included here.

[This is in an unofficial branch of UAE (the Ubiquitous Amiga Emulator)
with the aim of bringing the features of WinUAE to non-Windows platforms
such as Linux, Mac OS X and BeOS.]

%prep
%setup -q -n e-uae-%{version}-%{wiprel} -a1
#%patch2 -p1 -b .scsi
%patch4 -p1 -b .libscg
#%patch5 -p1 -b .openscsi
#%patch6 -p1 -b .fucomi
%patch7
%patch8

aclocal -I m4 && automake --foreign --add-missing && autoconf
cd src/tools
aclocal
autoconf

%build
#(cd prelink
#%configure
#%make)

%if %build_scsi
# build libscg for scsi-device support
(cd %{cdrname}-%{cdrmainvers}
ln -sf i586-linux-cc.rul RULES/ia64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/x86_64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/amd64-linux-cc.rul
ln -sf i686-linux-cc.rul RULES/athlon-linux-cc.rul
pwd

CFLAGS="$RPM_OPT_FLAGS" \
CONFFLAGS="%{_target_platform} --prefix=%{_prefix}" \
        XL_ARCH=%{_target_cpu} ./Gmake)
(cd src
./install_libscg ../%{cdrname}-%{cdrmainvers})
%endif

# build uae
CFLAGS="$RPM_OPT_FLAGS -O3 -pipe -ffast-math -fomit-frame-pointer -Wa,--execstack" \
./configure --prefix=%{_prefix} \
            --with-x \
            --with-sdl \
            --with-sdl-sound \
            --with-sdl-gfx \
            --enable-threads \
            --enable-ui \
	    --enable-jit \
%if %build_scsi
            --enable-scsi-device \
	    --with-libscg-includedir=`pwd`/src/include/ \
	    --with-libscg-libdir=`pwd`/src \
%else
            --disable-scsi-device \
%endif
	    --enable-bsdsock-new
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/bin \
	$RPM_BUILD_ROOT%{_libdir}/uae/amiga/source
%makeinstall
cp -pR amiga/* $RPM_BUILD_ROOT/%{_libdir}/uae/amiga/.

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc docs/*
%{_bindir}/*
%{_libdir}/uae
# %doc docs/*


%changelog
* Fri Jan 27 2012 Zombie Ryushu <ryushu@mandriva.org> 0.8.29-2.WIP4.1mdv2011.0
+ Revision: 769464
- Fix deps
- Add wahcade patch and fix string bugs care of codebase7@yahoo.com
- Fix xkb
- Fix xkb
- Fix Prelink
- Add Prelink

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Olivier Blin <blino@mandriva.org>
    - add XDG menu

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.8.29-1.WIP4.1mdv2009.1
+ Revision: 311430
- fix spec file again...
- spec file cleanup

  + Zombie Ryushu <ryushu@mandriva.org>
    - Disable fucomi patch which is obsolete here
    - Fix Macros
    - Version bump
    - Version bump

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.8.29-1.WIP3.4mdv2009.0
+ Revision: 244983
- rebuild

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 0.8.29-1.WIP3.2mdv2008.1
+ Revision: 136407
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel


* Mon Mar 19 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 0.8.29-1.WIP3.2mdv2007.1
+ Revision: 146623
- Added attr-devel, gtk+2-devel to BuildRequires.
- Rebuilt.
- Import e-uae

* Sun Sep 03 2006 Giuseppe Ghibò <ghibo@mandriva.com> 0.8.29-1.WIP3.1mdv2007.0
- Release 0.8.29-WIP3.

* Sun Feb 19 2006 Giuseppe Ghibò <ghibo@mandriva.com> 0.8.28-2.cvs20060219.1mdk
- cvs 20060219.

* Fri Oct 21 2005 Giuseppe Ghibò <ghibo@mandriva.com> 0.8.28-1mdk
- 0.8.28 final.

* Wed Sep 07 2005 Giuseppe Ghibò <ghibo@mandriva.com> 0.8.28-0.rc2.4mdk
- use -Wa,--execstack instead of execstack -s from prelink (Gwenole).

* Tue Sep 06 2005 Giuseppe Ghibò <ghibo@mandriva.com> 0.8.28-0.rc2.3mdk
- cvs 20050905.
- make binary executable stack, otherwise segfaults on A64.

* Fri Aug 26 2005 Giuseppe Ghibò <ghibo@mandriva.com> 0.8.28-0.rc2.2mdk
- Updated to final 0.8.28-RC2.

* Wed Aug 17 2005 Giuseppe Ghibò <ghibo@mandriva.com> 0.8.28-0.rc2.1mdk
- Relase 0.8.28rc2.

* Sat Jan 08 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 0.8.27-2mdk
- Added Provides.

* Sat Jan 08 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 0.8.27-1mdk
- Release 0.8.27.
- Readapted fucomi patch.

* Mon Dec 06 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 0.8.27-0.20041204.1mdk
- Updated to CVS 20041205.

* Thu Sep 02 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 0.8.27-0.20040831.1mdk
- Initial release based on uae spec file.
- Disabled fucomi patch (needs to be rebuilt for new sources).

