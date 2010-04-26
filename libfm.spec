%define major 0
%define libname %mklibname fm %major
%define develname %mklibname -d fm

%define prerel beta2
%define git git20100426

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Version:	0.1.10
Release:	%mkrel -c %prerel 2
License:	GPLv2
Group:		File tools
Source0:	%{name}-%{version}-%git.tar.gz
Patch0:		libfm-0.1.9-string-format.patch
Patch1:		libfm-0.1.5-set-cutomization.patch
Url:		http://pcmanfm.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libmenu-cache-devel >= 0.3.2
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	gtk+2-devel

%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
filesystems supported by gvfs.

%package -n %libname
Group:		File tools
Summary:	%{name} library package
Requires:	%{name} >= %{version}

%description -n %libname
%summary.

%package -n %develname
Group:		File tools
Summary:	%{name} developement files
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description -n %develname
This package contains header files needed when building applications based on
%{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .format
%patch1 -p0 -b .customization

%build
./autogen.sh
%configure2_5x --disable-static
# remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# don't ship .la
find %{buildroot} -name '*.la' | xargs rm -f

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%if %_lib != lib
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif

%postun
if [ "$1" = "0" ]; then
%if %_lib != lib
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif
fi

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%config(noreplace) %{_sysconfdir}/xdg/libfm/pref-apps.conf
%{_bindir}/libfm-pref-apps
%{_libdir}/gio/modules/libgiofm.so
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/gnome-terminal
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/archivers.list
%{_datadir}/%{name}/ui/*
%{_datadir}/applications/libfm-pref-apps.desktop
%{_datadir}/mime/packages/%{name}.xml

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libfm-gtk.so.%{major}*
%{_libdir}/libfm.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%dir %{_includedir}/%{name}/%{name}
%{_includedir}/%{name}/%{name}/*.h
%{_libdir}/libfm-gtk.so
%{_libdir}/libfm.so
%{_libdir}/pkgconfig/libfm-gtk.pc
%{_libdir}/pkgconfig/libfm.pc
