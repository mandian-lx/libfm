%define Werror_cflags %nil

%define api	1.0
%define major	3
%define libname	%mklibname fm %{major}
%define libgtk	%mklibname fm-gtk %{major}
%define devname	%mklibname -d fm
%define git	0
%define prerel	bcf60a4
%define gitday	20112007

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Version:	1.1.4
License:	GPLv2
Group:		File tools
Url:		http://pcmanfm.sourceforge.net/
%if %{git}
Release:	0.%{gitday}.1
Source0:	%{name}-%{prerel}.tar.gz
%else
Release:	11
Source0:	http://dfn.dl.sourceforge.net/sourceforge/pcmanfm/%{name}-%{version}.tar.xz
%endif
Patch0:		libfm-0.1.5-set-cutomization.patch

BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	vala
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libmenu-cache)
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

%package -n %{libgtk}
Summary:	%{name} library package
Group:		File tools
Conflicts:	%{_lib}fm3 < 1.1.0-7

%description -n %{libgtk}
%{summary}.

%package -n %{devname}
Summary:	%{name} developement files
Group:		File tools
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libgtk} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains header files needed when building applications based on
%{name}.

%prep
%if %{git}
%setup -qn %{name}-%{prerel}
%else
%setup -q
%endif
mkdir m4
%apply_patches

%if %{git}
./autogen.sh
%endif
sed -i "s:-Werror::" configure.ac || die
autoreconf -fi

%build
%configure2_5x \
	--disable-static \
	--enable-udisks \
	--with-gtk=2
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

%find_lang %{name}

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%config(noreplace) %{_sysconfdir}/xdg/libfm/pref-apps.conf
%{_bindir}/libfm-pref-apps
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/archivers.list
%{_datadir}/%{name}/ui/*
%{_datadir}/applications/libfm-pref-apps.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man1/libfm-pref-apps.1.*

%files -n %{libname}
%{_libdir}/libfm.so.%{major}*

%files -n %{libgtk}
%{_libdir}/libfm-gtk.so.%{major}*

%files -n %{devname}
#doc #{_datadir}/gtk-doc/html/*
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}-%{api}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}-%{api}/*.h
%{_libdir}/libfm-gtk.so
%{_libdir}/libfm.so
%{_libdir}/pkgconfig/libfm-gtk.pc
%{_libdir}/pkgconfig/libfm-gtk3.pc
%{_libdir}/pkgconfig/libfm.pc

