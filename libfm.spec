%define prerel alpha

Summary:	Basic file management library for PCManFM
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
BuildRequires:	gettext
BuildRequires:	perl
BuildRequires:	perl-XML-Parser
BuildRequires:	gtk+2-devel

%description
%summary.

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
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%config(noreplace) %{_sysconfdir}/xdg/libfm/pref-apps.conf
%{_bindir}/libfm-pref-apps
%{_libdir}/libfm.so*
%{_libdir}/libfm-gtk.so*
%{_libdir}/gio/modules/libgiofm.so
%{_libdir}/%{name}/gnome-terminal
%{_datadir}/%{name}/ui/*
%{_datadir}/applications/libfm-pref-apps.desktop
%{_datadir}/mime/packages/%{name}.xml

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/%{name}/%{name}/*.h
%{_libdir}/libfm-gtk.a 
%{_libdir}/libfm-gtk.la
%{_libdir}/libfm.a
%{_libdir}/libfm.la
%{_libdir}/gio/modules/libgiofm.a
%{_libdir}/gio/modules/libgiofm.la
%{_libdir}/pkgconfig/libfm-gtk.pc
%{_libdir}/pkgconfig/libfm.pc
