%define prerel alpha

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Version:	0.1.5
Release:	%mkrel -c %prerel 1
License:	GPLv2
Group:		File tools
Source0:	%{name}-%{version}.tar.gz
Patch0:		libfm-0.1.5-string-format.patch
Patch1:		libfm-0.1.5-set-default-terminal.patch
Url:		http://pcmanfm.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libmenu-cache-devel
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	perl
BuildRequires:	perl-XML-Parser
BuildRequires:	gtk+2-devel
BuildRequires:	libgvfs-devel

%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
filesystems supported by gvfs.


%package -n %{name}-devel
Group:		File tools
Summary:	%{name} developement files
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{name} >= %{version}-%{release}

%description -n %{name}-devel
This package contains header files needed if you wish to build applications
based on %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .format
%patch1 -p0

%build
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

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%config(noreplace) %{_sysconfdir}/xdg/libfm/pref-apps.conf
%{_bindir}/libfm-pref-apps
%{_libdir}/libfm-gtk.so.0*
%{_libdir}/libfm.so.0*
%{_libdir}/gio/modules/libgiofm.so
%{_libdir}/%{name}/gnome-terminal
%{_datadir}/%{name}/ui/*
%{_datadir}/applications/libfm-pref-apps.desktop
%{_datadir}/mime/packages/%{name}.xml

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/%{name}/%{name}/*.h
%{_libdir}/libfm-gtk.so
%{_libdir}/libfm.so
%{_libdir}/pkgconfig/libfm-gtk.pc
%{_libdir}/pkgconfig/libfm.pc
