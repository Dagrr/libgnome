Summary:	GNOME base library
Summary(pl):	Podstawowa biblioteka GNOME
Name:		libgnome
Version:	1.114.0
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	ftp://ftp.gnome.org/pub/gnome/pre-gnome2/sources/libgnome/%{name}-%{version}.tar.bz2
Patch0:		%{name}-gconf2.patch
URL:		ftp://www.gnome.org/
PreReq:		GConf2 >= 1.1.8
PreReq:		/sbin/ldconfig
# Added to avoid the warning messages about utmp group, bug #24171
# fixme, just libzvt?
PreReq:		utempter
BuildRequires:	GConf2-devel >= 1.1.8
BuildRequires:	ORBit2-devel >= 2.3.106
BuildRequires:	audiofile-devel
BuildRequires:	esound-devel
BuildRequires:	glib2-devel >= 1.3.15
BuildRequires:	gnome-vfs2-devel >= 1.9.7
BuildRequires:	libbonobo-devel >= 1.112.0
BuildRequires:	libxml2-devel >= 2.4.14
BuildRequires:	libxslt-devel >= 1.0.15
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir	/etc/X11/GNOME2

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
GUI applications and desktop tools to be used in conjunction with a
window manager for the X Window System. The libgnome package includes
non-GUI-related libraries that are needed to run GNOME. The libgnomeui
package contains X11-dependent GNOME library features.

%description -l pl
GNOME (GNU Network Object Model Environment) jest przyjaznym dla
u�ytkownika zbiorem aplikacji i narz�dzi do u�ywania w po��czeniu z
menad�erem okien pod X Window System. Pakiet libgnome zawiera
biblioteki nie zwi�zane z graficznym interfejsem potrzebne do
uruchomienia GNOME. Pakiet libgnomeui zawiera biblioteki GNOME zale�ne
od X11.

%package devel
Summary:	Headers for libgnome
Summary(pl):	Pliki nag��wkowe libgnome
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}

%description devel
GNOME (GNU Network Object Model Environment) is a user-friendly set of
GUI applications and desktop tools to be used in conjunction with a
window manager for the X Window System. The libgnome-devel package
includes the libraries and include files that you will need to use
libgnome.

You should install the libgnome-devel package if you would like to
compile GNOME applications. You do not need to install libgnome-devel
if you just want to use the GNOME desktop environment.

%description devel -l pl
Pliki nag��wkowe potrzebne do kompilowania program�w korzystaj�cych z
libgnome.

%package static
Summary:	Static libgnome libraries
Summary(pl):	Statyczne biblioteki libgnome
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of libgnome libraries.

%description static -l pl
Statyczna wersja bibliotek libgnome.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing acinclude.m4
libtoolize --copy --force
aclocal
autoconf
#automake -a -c -f
%configure \
	--enable-gtk-doc=no

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

gzip -9nf AUTHORS ChangeLog NEWS README

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
export GCONF_CONFIG_SOURCE
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/desktop_gnome_*.schemas > /dev/null

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS.gz ChangeLog.gz NEWS.gz README.gz
%{_sysconfdir}/gconf/schemas/*
%{_sysconfdir}/gnome-vfs-2.0/modules/*
%{_sysconfdir}/sound/events/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/*.??
%attr(755,root,root) %{_libdir}/bonobo/monikers/*.??
%{_libdir}/bonobo/servers/*
# FIXME: where put this?
#%{_datadir}/sgml

%files devel
%defattr(644,root,root,755)
%{_libdir}/lib*.so
%{_pkgconfigdir}/*.pc
%{_includedir}/libgnome-2.0
%{_datadir}/gtk-doc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%{_libdir}/gnome-vfs-2.0/modules/*.a
%{_libdir}/bonobo/monikers/*.a
