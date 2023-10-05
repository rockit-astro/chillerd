Name:      rockit-chiller
Version:   %{_version}
Release:   1
Summary:   Water chiller
Url:       https://github.com/rockit-astro/chillerd
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/chillerd/
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/chiller %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/chillerd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/chillerd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/completion/chiller %{buildroot}/etc/bash_completion.d

%{__install} %{_sourcedir}/clasp.json %{buildroot}%{_sysconfdir}/chillerd/
%{__install} %{_sourcedir}/10-clasp-chiller.rules %{buildroot}%{_udevrulesdir}

%package server
Summary:  Chiller server
Group:    Unspecified
Requires: python3-rockit-chiller python3-pyserial
%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/chillerd
%defattr(0644,root,root,-)
%{_unitdir}/chillerd@.service

%package client
Summary:  Chiller client
Group:    Unspecified
Requires: python3-rockit-chiller
%description client

%files client
%defattr(0755,root,root,-)
%{_bindir}/chiller
/etc/bash_completion.d/chiller

%package data-clasp
Summary: Chiller data for CLASP
Group:   Unspecified
%description data-clasp

%files data-clasp
%defattr(0644,root,root,-)
%{_udevrulesdir}/10-clasp-chiller.rules
%{_sysconfdir}/chillerd/clasp.json

%changelog
