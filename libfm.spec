%define git 0
%define major 1
%define libname %mklibname fm %major
%define develname %mklibname -d fm
%define prerel bcf60a4
%define gitday 20112007
%define ver 0.1.17

Summary:	GIO-based library for file manager-like programs
Name:		libfm
Release:	%mkrel 1
License:	GPLv2
Group:		File tools
%if %git
Version:	%{ver}.git%{gitday}
Source0:	%{name}-%{prerel}.tar.gz
%else
Version:	%{ver}
Source0:	%{name}-%{version}.tar.gz
%endif
Patch0:		libfm-0.1.5-set-cutomization.patch
# patches from upstream:

Url:		http://pcmanfm.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libmenu-cache-devel >= 0.3.2
BuildRequires:	intltool
BuildRequires:	gettext
BuildRequires:	gtk+2-devel
BuildRequires:	gtk-doc
BuildRequires:	dbus-glib-devel

%description
LibFM is a GIO-based library used to develop file manager-like programs. It is
developed as the core of next generation PCManFM and takes care of all file-
related operations such as copy & paste, drag & drop, file associations or 
thumbnails support. By utilizing glib/gio and gvfs, libfm can access remote 
filesystems supported by gvfs.

%package -n %libname
Group:		File tools
Summary:	%{name} library package
Requires:	%{name} = %{version}

%description -n %libname
%summary.

%package -n %develname
Group:		File tools
Summary:	%{name} developement files
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}

%description -n %develname
This package contains header files needed when building applications based on
%{name}.

%prep
%if %git
%setup -q -n %{name}-%{prerel}
%else
%setup -q
%endif
%patch0 -p0 -b .customization

%build
%if %git
./autogen.sh
%endif
%define Werror_cflags %nil
%configure --enable-udisks
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
%if %mdkversion < 201100

	%if %_lib != lib
		%{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules
	%else
		%{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
	%endif
%endif

%postun
%if %mdkversion < 201100
if [ "$1" = "0" ]; then
%if %_lib != lib
 %{_bindir}/gio-querymodules-64 %{_libdir}/gio/modules
%else
 %{_bindir}/gio-querymodules-32 %{_libdir}/gio/modules
%endif
fi
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xdg/libfm/libfm.conf
%config(noreplace) %{_sysconfdir}/xdg/libfm/pref-apps.conf
%{_bindir}/libfm-pref-apps
%if %mdkversion < 201100
%{_libdir}/gio/modules/*
%endif
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/archivers.list
%{_datadir}/%{name}/ui/*
%{_datadir}/applications/libfm-pref-apps.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/gtk-doc/html/*

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
%{_libdir}/libfm-gtk.a
%{_libdir}/libfm.a
%{_libdir}/pkgconfig/libfm-gtk.pc
%{_libdir}/pkgconfig/libfm.pc


%changelog
* Tue Jul 19 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git20112007-2mdv2011.0
+ Revision: 690608
- fix dnd error and update translates

* Thu Jun 16 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git20112006-1
+ Revision: 685697
- update translations and change git date due pcmanfm fix

* Tue Jun 14 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git20111906-3
+ Revision: 685142
- update translate

* Sun Jun 12 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git20111906-2
+ Revision: 684375
- update translations

* Sun Jun 12 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git20111906-1
+ Revision: 684356
- update for new git snapshot

* Sat May 28 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git20111905-1
+ Revision: 681317
- new build from svn. Fix some translate and program issues

* Thu May 05 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git20111904-6
+ Revision: 669541
+ rebuild (emptylog)

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.15.git20111902-5
+ Revision: 662366
- mass rebuild

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 0.1.15.git20111902-4
+ Revision: 640300
- rebuild to obsolete old packages

  + Matthew Dawkins <mattydaw@mandriva.org>
    - fixed ugly BR hack

* Sat Feb 19 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git20111902-3
+ Revision: 638784
+ rebuild (emptylog)

* Thu Feb 17 2011 Александр Казанцев <kazancas@mandriva.org> 0.1.15.git61443ac-2
+ Revision: 638226
- switch to git branch 0.1.15

* Sun Nov 28 2010 Funda Wang <fwang@mandriva.org> 0.1.14-1mdv2011.0
+ Revision: 602272
- new version 0.1.14

* Sat Jul 24 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.12-0.rc1.1mdv2011.0
+ Revision: 557333
- update to 0.1.12 rc1
- drop string format patch, the bug filed upstream was closed as wontfix, so
  compile with Werror_cflags %%nil instead of having to rediff the patch
- add two patches from upstream git

* Tue Apr 27 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.11-0.beta3.1mdv2010.1
+ Revision: 539855
- new release, beta3, 0.1.11
- improve devel package requires

* Mon Apr 26 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.10-0.beta2.2mdv2010.1
+ Revision: 539349
- new git snapshot
- fix post and postun

* Mon Apr 19 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.10-0.beta2.1mdv2010.1
+ Revision: 536542
- update to 1.10 beta2

* Sun Apr 11 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.9-0.beta.4mdv2010.1
+ Revision: 533573
- new git snapshot

* Fri Mar 26 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.9-0.beta.2mdv2010.1
+ Revision: 527615
- improve package dir ownership

* Thu Mar 18 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.9-0.beta.1mdv2010.1
+ Revision: 525010
- new upstream release 0.1.9 beta
- rediff str format patch

* Wed Mar 17 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.5-0.alpha.4mdv2010.1
+ Revision: 523486
- move the gio module to the main package to ease major upgrades
  (spotted by Charles A Edwards)
- more customization to make pcmanfm use xarchiver by default (xarchiver is already present on dual-free iso)

* Tue Mar 16 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.5-0.alpha.3mdv2010.1
+ Revision: 521821
- update to a git snapshot to fix a segfault in nautilus when libfm gio module is
  present
- fix file list
- add post and postun parts for the gio module

* Mon Mar 15 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.5-0.alpha.2mdv2010.1
+ Revision: 519891
- proper libification, (pointed out by fcrozat)

* Wed Mar 10 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.1.5-0.alpha.1mdv2010.1
+ Revision: 517592
- remove uneeded BR's
- improve spec, summary, configure options (thanks Fedora)
- don't ship .la (from Fedora)
- fix package requires so that main package doesn't require -devel packages
- import libfm


