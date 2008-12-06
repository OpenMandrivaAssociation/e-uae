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
Release: %mkrel 1.%{wiprel}.1
URL: http://sourceforge.net/projects/uaedev/
Source0: e-uae-%{version}-%{wiprel}.tar.bz2
Source1: ftp://ftp.berlios.de/pub/cdrecord/alpha/%{cdrname}-%{cdrvers}.tar.bz2
Patch2: uae-scsi.patch
Patch4: uae-0.8.25-20040302-libscg.patch
Patch5: uae-0.8.22-openscsi.patch
Patch6: e-uae-0.8.27-fucomi.patch
License: GPL
Group: Emulators
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: X11-devel
BuildRequires: gtk+-devel
BuildRequires: gtk+2-devel
BuildRequires: glib-devel
BuildRequires: SDL-devel
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
%setup -q -a 1 -n e-uae-%{version}-%{wiprel}
#%patch2 -p1 -b .scsi
%patch4 -p1 -b .libscg
#%patch5 -p1 -b .openscsi
#%patch6 -p1 -b .fucomi

aclocal -I m4 && automake --foreign --add-missing && autoconf
cd src/tools
aclocal
autoconf

%build
(cd prelink
%configure
%make)

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
%doc docs/*


