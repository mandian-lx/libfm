%define api 1.0
%define major 4
%define libname %mklibname fm %{major}
%define elibname %mklibname fm-extra %{major}
%define glibname %mklibname fm-gtk %{major}
%define devname %mklibname -d fm
%define git 0

%bcond_without gtk

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Version:	1.2.5
%if %{git}
Release:	0.%{git}.1
Source0:	%{name}-%{git}.tar.xz
%else
Release:	1
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.xz
%endif
License:	GPLv2
Group:		File tools
Url:		https://wiki.lxde.org/en/Libfm
Patch0:		libfm-0.1.5-set-cutomization.patch

BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	vala
BuildRequires:	pkgconfig(cairo) >= 1.8.0
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.26.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.26.0
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libmenu-cache) >= 0.3.2
BuildRequires:	pkgconfig(pango) >= 1.16.0
%if %{with gtk}
BuildRequires:	pkgconfig(gtk+-2.0) >= 2.18.0
%endif

%description
Lightweight X11 Desktop Environment project (a.k.a LXDE) aimed to provide a
new desktop environment which is useful enough and keep resource usage lower
at the same time. Useabiliy, speed, and memory usage are our main concern.

Unlike other tightly integrated desktops LXDE strives to be modular, so each
component can be used independently with few dependencies. This makes
porting LXDE to different distributions and platforms easier.

A glib/gio-based library providing some file management utilities and
related-widgets missing in gtk+/glib. This is the core of PCManFM. The
library is desktop independent (not LXDE specific) and has clean API.
Itcan be used to develop other applications requiring file management
functionality.

#---------------------------------------------------------------------------

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/terminals.list
%{_datadir}/%{name}/archivers.list
%{_datadir}/mime/packages/%{name}.xml
%{_libdir}/libfm

#---------------------------------------------------------------------------

%if %{with gtk}
%package gtk
Summary:	gtk related parts of the %{name} library
Group:		File tools

%description gtk
gtk related parts of the %{name} library

%files gtk
%{_bindir}/libfm-pref-apps
%{_mandir}/man1/libfm-pref-apps.1*
%{_datadir}/applications/libfm-pref-apps.desktop
%dir %{_datadir}/%{name}/images
%{_datadir}/%{name}/images/*
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/ui/*
%endif

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	%{name} library package
Group:		File tools
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
%{summary}.

%files -n %{libname}
%{_libdir}/libfm.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{elibname}
Summary:	%{name} extra library package
Group:		File tools
Requires:	%{libname} = %{EVRD}

%description -n %{elibname}
%{summary}

%files -n %{elibname}
%{_libdir}/libfm-extra.so.%{major}*

#---------------------------------------------------------------------------

%if %{with gtk}
%package -n %{glibname}
Summary:	%{name} extra library package
Group:		File tools
Requires:	%{libname} = %{EVRD}

%description -n %{glibname}
%{summary}

%files -n %{glibname}
%{_libdir}/libfm-gtk.so.%{major}*
%endif

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	%{name} developement files
Group:		File tools
Requires:	%{libname} = %{version}-%{release}
Requires:	%{elibname} = %{version}-%{release}
Requires:	%{glibname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains header files needed when building applications based on
%{name}.

%files -n %{devname}
#doc % {_datadir}/gtk-doc/html/*
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}-%{api}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}-%{api}/*.h
%{_libdir}/libfm.so
%{_libdir}/libfm-extra.so
%{_libdir}/pkgconfig/libfm.pc
%{_libdir}/pkgconfig/libfm-extra.pc
%if %{with gtk}
%{_libdir}/libfm-gtk.so
%{_libdir}/pkgconfig/libfm-gtk.pc
%endif

#---------------------------------------------------------------------------

%package -n lxshortcut
Summary:	Edit app shortcuts
Group:		Graphical desktop/Other

%description -n lxshortcut
LXShortcut is a small program used to edit application shortcuts created
with freedesktop.org Desktop Entry spec.

%if %{with gtk}
%files -n lxshortcut
%{_bindir}/lxshortcut
%{_datadir}/applications/lxshortcut.desktop
%{_mandir}/man1/lxshortcut.1*
%endif

#---------------------------------------------------------------------------

%prep

%if %{git}
%setup -q -n %{name}-%{git}
%else
%setup -q
%endif
%apply_patches

[ -e autogen.sh ] && ./autogen.sh

%build
%configure \
	--enable-udisks \
%if %{without gtk}
	--without-gtk \
%endif
	%{nil}
%make

%install
%makeinstall_std

#some hack for avoid upgrade error
#copy all in libfm-1.0 in includedir to libfm instead symlink, rather early it is true
rm -rf %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_includedir}/%{name}
cp -f %{buildroot}%{_includedir}/%{name}-%{api}/* %{buildroot}%{_includedir}/%{name}/

# locales
%find_lang %{name}

