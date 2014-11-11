%define api	1.0
%define major	4
%define libname %mklibname fm %{major}
%define elibname %mklibname fm-extra %{major}
%define	glibname %mklibname fm-gtk %{major}
%define devname %mklibname -d fm
%define git 0
%bcond_without gtk

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Version:	1.2.3
%if %{git}
Release:	0.%{git}.1
Source0:	%{name}-%{git}.tar.xz
%else
Release:	1
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.xz
%endif
License:	GPLv2
Group:		File tools
Url:		http://pcmanfm.sourceforge.net/
Patch0:		libfm-0.1.5-set-cutomization.patch
#Patch1:		libfm-1.2.0-conditioned-pkgconfig-files.patch
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
%if %{without gtk}
Obsoletes:	lxshortcut
%endif

%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
filesystems supported by gvfs.

%package gtk
Summary:	gtk related parts of the %{name} library
Group:		File tools
Requires:	lxshortcut = %{EVRD}

%description gtk
gtk related parts of the %{name} library

%package -n %{libname}
Summary:	%{name} library package
Group:		File tools
Suggests:	%{name} = %{version}-%{release}

%description -n %{libname}
%{summary}.

%package -n %{elibname}
Summary:	%{name} extra library package
Group:		File tools
Requires:	%{libname} = %{EVRD}

%description -n %{elibname}
%{summary}

%package -n %{glibname}
Summary:	%{name} extra library package
Group:		File tools
Requires:	%{libname} = %{EVRD}

%description -n %{glibname}
%{summary}

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

%package -n lxshortcut
Summary:	Edit app shortcuts
Group:		Graphical desktop/Other

%description -n lxshortcut
LXShortcut is a small program used to edit application shortcuts created
with freedesktop.org Desktop Entry spec.

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
	--without-gtk
%endif

%make

%install
%makeinstall_std

#some hack for avoid upgrade error
#copy all in libfm-1.0 in includedir to libfm instead symlink, rather early it is true
rm -rf %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_includedir}/%{name}
cp -f %{buildroot}%{_includedir}/%{name}-%{api}/* %{buildroot}%{_includedir}/%{name}/

%find_lang %{name}

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/terminals.list
%{_datadir}/%{name}/archivers.list
%{_datadir}/mime/packages/%{name}.xml
%{_libdir}/libfm

%if %{with gtk}
%files gtk
%{_bindir}/libfm-pref-apps
%{_mandir}/man1/libfm-pref-apps.1*
%{_datadir}/applications/libfm-pref-apps.desktop
%dir %{_datadir}/%{name}/images
%{_datadir}/%{name}/images/*
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/ui/*
%endif

%files -n %{libname}
%{_libdir}/libfm.so.%{major}*

%files -n %{elibname}
%{_libdir}/libfm-extra.so.%{major}*

%if %{with gtk}
%files -n %{glibname}
%{_libdir}/libfm-gtk.so.%{major}*
%endif

%files -n %{devname}
#doc #{_datadir}/gtk-doc/html/*
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

%if %{with gtk}
%files -n lxshortcut
%{_bindir}/lxshortcut
%{_datadir}/applications/lxshortcut.desktop
%{_mandir}/man1/lxshortcut.1*
%endif
