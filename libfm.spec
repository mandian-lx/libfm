%define Werror_cflags %nil
%define beta beta6

%define api	1.0
%define major	4
%define libname	%mklibname fm %{major}
%define elibname %mklibname fm-extra %{major}
%define devname	%mklibname -d fm
%define git	0
%define prerel	bcf60a4
%define gitday	20112007
%define beta	beta6

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Version:	1.2.0
License:	GPLv2
Group:		File tools
Url:		http://pcmanfm.sourceforge.net/
%if "%{beta}" != ""
Release:	0.%beta.1
Source0:	%{name}-%{version}-%{beta}.tar.xz
%else
%if %{git}
Release:	0.%{gitday}.1
Source0:	%{name}-%{prerel}.tar.gz
%else
Release:	1
Source0:	http://dfn.dl.sourceforge.net/sourceforge/pcmanfm/%{name}-%{version}.tar.xz
%endif
%endif
Patch0:		libfm-0.1.5-set-cutomization.patch

BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	vala
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libmenu-cache)
BuildRequires:	pkgconfig(gio-unix-2.0) >= 2.26.0
BuildRequires:	pkgconfig(glib-2.0) >= 2.26.0
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(pango) >= 1.16.0
Requires:	lxshortcut

%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
filesystems supported by gvfs.

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

%package -n %{devname}
Summary:	%{name} developement files
Group:		File tools
Requires:	%{libname} = %{version}-%{release}
Requires:	%{elibname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains header files needed when building applications based on
%{name}.

%prep
%if "%{beta}" != ""
%setup -qn %{name}-%{version}-%{beta}
%else
%if %{git}
%setup -qn %{name}-%{prerel}
%else
%setup -q
%endif
%endif
%apply_patches

[ -e autogen.sh ] && ./autogen.sh
#sed -i "s:-Werror::" configure.ac || die
#autoreconf -fi

%build
%configure2_5x \
	--disable-static \
	--enable-udisks \
	--without-gtk \
	--disable-demo
# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std

#some hack for avoid upgrade error
#copy all in libfm-1.0 in includedir to libfm instead symlink, rather early it is true
rm -f %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_includedir}/%{name}
cp -f %{buildroot}%{_includedir}/%{name}-%{api}/* %{buildroot}%{_includedir}/%{name}/

# remove gtk artifacts that get installed despite --without-gtk
rm -f %{buildroot}%{_libdir}/pkgconfig/*-gtk*.pc

%find_lang %{name}

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/terminals.list
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/archivers.list
%{_datadir}/%{name}/ui/*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/lxshortcut.desktop
%{_datadir}/applications/libfm-pref-apps.desktop
%{_libdir}/libfm
%{_mandir}/man1/lxshortcut.1*
%{_mandir}/man1/libfm-pref-apps.1*

%files -n %{libname}
%{_libdir}/libfm.so.%{major}*

%files -n %{elibname}
%{_libdir}/libfm-extra.so.%{major}*

%files -n %{devname}
#doc #{_datadir}/gtk-doc/html/*
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}-%{api}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}-%{api}/*.h
%{_libdir}/libfm.so
%{_libdir}/libfm-extra.so
%{_libdir}/pkgconfig/libfm.pc

