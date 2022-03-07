#
# Conditional build:
%bcond_without	apidocs		# Doxygen based API docs

%define		qtver	5.4.0
Summary:	Icecream GUI Monitor
Name:		icemon
Version:	3.3
Release:	4
License:	GPL v2+
Group:		Applications/System
#Source0Download: https://github.com/icecc/icemon/releases
Source0:	https://github.com/icecc/icemon/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	e7356476ca0f489057723ad9c781679b
URL:		https://kfunk.org/tag/icemon/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.1.0
BuildRequires:	docbook2X
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	icecream-devel >= 1.3
BuildRequires:	kf5-extra-cmake-modules
BuildRequires:	libstdc++-devel >= 6:4.8.1
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	gtk-update-icon-cache
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}
Requires:	hicolor-icon-theme
Requires:	icecream-libs >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Icecream GUI Monitor.

%package apidocs
Summary:	icemon API documentation
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for icemon.

%prep
%setup -q

%build
%cmake -B build \
	-DDOCBOOK_TO_MAN_EXECUTABLE=/usr/bin/docbook2X2man

%{__make} -C build
%{?with_apidocs:%{__make} -C build doc}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database

%postun
%update_icon_cache hicolor
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/icemon
%{_desktopdir}/icemon.desktop
%{_iconsdir}/hicolor/*/apps/icemon.png
%{_mandir}/man1/icemon.1*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/html/*
%endif
