%define cdrname cdrtools
%define cdrmainvers 2.01
%define cdrvers %{cdrmainvers}a38
%define wiprel WIP4

# For building with SCSI support
%define build_scsi 0
%{?_with_scsi: %global build_scsi 1}
%{?_without_scsi: %global build_scsi 0}

Summary:	A software emulation of the Amiga system
Name:		e-uae
Version:	0.8.29
Release:	2.%{wiprel}.2
License:	GPLv2+
Group:		Emulators
Url:		http://sourceforge.net/projects/uaedev/
Source0:	e-uae-%{version}-%{wiprel}.tar.bz2
Source1:	ftp://ftp.berlios.de/pub/cdrecord/alpha/%{cdrname}-%{cdrvers}.tar.bz2
Source10:	%{name}.rpmlintrc
Patch4:		uae-0.8.25-20040302-libscg.patch
Patch7:		e-uae-0.8.29-WIP4-sdlkeys-wahcade.patch
Patch8:		e-uae-fix-string-format-bug.patch
BuildRequires:	x11-data-xkbdata
BuildRequires:	attr-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(pangoft2)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(x11)
Conflicts:	uae

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

%files
%doc docs/*
%{_bindir}/*
%{_libdir}/uae

#----------------------------------------------------------------------------

%prep
%setup -q -n e-uae-%{version}-%{wiprel} -a1
%patch4 -p1 -b .libscg
%patch7
%patch8

%build
%if %{build_scsi}
# build libscg for scsi-device support
(cd %{cdrname}-%{cdrmainvers}
ln -sf i586-linux-cc.rul RULES/ia64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/x86_64-linux-cc.rul
ln -sf i586-linux-cc.rul RULES/amd64-linux-cc.rul
ln -sf i686-linux-cc.rul RULES/athlon-linux-cc.rul
pwd

CFLAGS="%{optflags}" \
CONFFLAGS="%{_target_platform} --prefix=%{_prefix}" \
        XL_ARCH=%{_target_cpu} ./Gmake)
(cd src
./install_libscg ../%{cdrname}-%{cdrmainvers})
%endif

# build uae
CFLAGS="%{optflags} -O3 -pipe -ffast-math -fomit-frame-pointer -Wa,--execstack" \
./configure \
	--prefix=%{_prefix} \
	--with-x \
	--with-sdl \
	--with-sdl-sound \
	--with-sdl-gfx \
	--enable-threads \
	--enable-ui \
	--enable-jit \
%if %{build_scsi}
	--enable-scsi-device \
	--with-libscg-includedir=`pwd`/src/include/ \
	--with-libscg-libdir=`pwd`/src \
%else
	--disable-scsi-device \
%endif
	--enable-bsdsock-new
make

%install
mkdir -p %{buildroot}%{_prefix}/bin \
	%{buildroot}%{_libdir}/uae/amiga/source

%makeinstall_std
cp -pR amiga/* %{buildroot}/%{_libdir}/uae/amiga/.

