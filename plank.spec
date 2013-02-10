%define		rel		1
%define		subver	734
Summary:	Plank is meant to be the simplest dock on the planet
Name:		plank
Version:	0.2.0
Release:	0.%{subver}.%{rel}
License:	GPL v3+
Group:		X11/Applications
URL:		http://wiki.go-docky.com/index.php?title=Plank:Introduction
# bzr branch lp:plank; cd plank; bzr up -r734
# ./autogen.sh; make dist
Source0:	%{name}-%{version}.%{subver}.tar.xz
# Source0-md5:	2f57cd8444c3c6eab3534739c5814440
BuildRequires:	bamf3-devel
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel
BuildRequires:	gnome-common
BuildRequires:	gtk+3-devel
BuildRequires:	intltool
BuildRequires:	libgee0.6-devel
BuildRequires:	libwnck-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
Requires:	bamf-daemon
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Requires(post,postun):	/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A very simple dock written in Vala.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for %{name}

%prep
%setup -q -n %{name}-%{version}.%{subver}

%build
%configure
%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libplank.la

# no apport
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/apport/crashdb.conf.d/%{name}-crashdb.conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/apport/package-hooks/source_%{name}.py

desktop-file-validate $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

%{__rm} $RPM_BUILD_ROOT%{_localedir}/sma

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_libdir}/libplank.so.*.*.*
%ghost %{_libdir}/libplank.so.0
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.svg

%files devel
%defattr(644,root,root,755)
%{_libdir}/libplank.so
%{_pkgconfigdir}/%{name}.pc
%{_includedir}/%{name}
%{_datadir}/vala/vapi/%{name}.vapi
%{_datadir}/vala/vapi/%{name}.deps
