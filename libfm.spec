%define git 0
%define major 3
%define libname %mklibname fm %{major}
%define develname %mklibname -d fm
%define prerel bcf60a4
%define gitday 20112007
%define ver 1.1.0
%define devel_rel 1.0

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Release:	5
License:	GPLv2
Group:		File tools
Url:		http://pcmanfm.sourceforge.net/
%if %{git}
Version:	%{ver}.git%{gitday}
Source0:	%{name}-%{prerel}.tar.gz
%else
Version:	%{ver}
Source0:	http://dfn.dl.sourceforge.net/sourceforge/pcmanfm/%name-%version.tar.gz
%endif
Patch0:		libfm-0.1.5-set-cutomization.patch
#Patch1:		libfm-0.1.17-automake1.12.patch
# patches from upstream:
Patch100:	libfm-1.1.0-smb-symlink.patch

BuildRequires:	libmenu-cache-devel >= 0.3.2
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	vala
Requires:	lxshortcut

%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
filesystems supported by gvfs.

%package -n %{libname}
Group:		File tools
Summary:	%{name} library package
Requires:	%{name} = %{version}

%description -n %{libname}
%{summary}.

%package -n %{develname}
Group:		File tools
Summary:	%{name} developement files
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-%{develname} < %{version}

%description -n %{develname}
This package contains header files needed when building applications based on
%{name}.

%prep
%if %{git}
%setup -q -n %{name}-%{prerel}
%else
%setup -q
%endif

%apply_patches

%build
%if %{git}
./autogen.sh
%endif
sed -i "s:-Werror::" configure.ac || die
autoreconf -fi
%define Werror_cflags %nil
%configure --enable-udisks  --with-gtk=2
# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
rm -rf %{buildroot}
%makeinstall_std

#some hack for avoid upgrade error
#copy all in libfm-1.0 in includedir to libfm instead symlink, rather early it is true
rm -f %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_includedir}/%{name}
cp -f %{buildroot}%{_includedir}/%{name}-%{devel_rel}/* %{buildroot}%{_includedir}/%{name}/


# don't ship .la
find %{buildroot} -name '*.la' | xargs rm -f

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
#{_datadir}/gtk-doc/html/*
%{_mandir}/man1/libfm-pref-apps.1.*

%files -n %{libname}
%{_libdir}/libfm-gtk.so.%{major}*
%{_libdir}/libfm.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}-%{devel_rel}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}-%{devel_rel}/*.h
%{_libdir}/libfm-gtk.so
%{_libdir}/libfm.so
%{_libdir}/libfm-gtk.a
%{_libdir}/libfm.a
%{_libdir}/pkgconfig/libfm-gtk.pc
%{_libdir}/pkgconfig/libfm-gtk3.pc
%{_libdir}/pkgconfig/libfm.pc
