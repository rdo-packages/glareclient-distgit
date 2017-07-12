%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname glareclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:    python-glareclient
Version: XXX
Release: XXX
Summary: Python API and CLI for OpenStack Glare

License: ASL 2.0
URL:     https://launchpad.net/python-glareclient
Source0: https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch: noarch

%description
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.

%package -n python2-%{sname}
Summary: Python API and CLI for OpenStack Glare
%{?python_provide:%python_provide python2-glareclient}
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: git

Requires:       python-cliff >= 2.3.0
Requires:       python-keystoneclient >= 1:3.8.0
Requires:       python-openstackclient >= 1.5.0
Requires:       python-osc-lib >= 1.2.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-utils >= 3.18.0
Requires:       python-osprofiler
Requires:       python-pbr
Requires:       python-requests >= 2.10.0
Requires:       python-six >= 1.9.0

%description -n python2-%{sname}
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary: Python API and CLI for OpenStack Glare
%{?python_provide:%python_provide python3-glareclient}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires:       python3-cliff >= 2.3.0
Requires:       python3-keystoneclient >= 1:3.8.0
Requires:       python3-openstackclient >= 1.5.0
Requires:       python3-osc-lib >= 1.2.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-utils >= 3.18.0
Requires:       python3-osprofiler
Requires:       python3-pbr
Requires:       python3-requests >= 2.10.0
Requires:       python3-six >= 1.9.0

%description -n python3-%{sname}
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.
%endif

%package doc
Summary: Documentation for OpenStack Glare API Client

BuildRequires: python-sphinx

%description doc
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.

This package contains auto-generated documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git

%py_req_cleanup


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
echo "%{version}" > %{buildroot}%{python3_sitelib}/glareclient/versioninfo
mv %{buildroot}%{_bindir}/glare %{buildroot}%{_bindir}/glare-%{python3_version}
ln -s ./glare-%{python3_version} %{buildroot}%{_bindir}/glare-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/glareclient/tests
%endif

%py2_install
echo "%{version}" > %{buildroot}%{python2_sitelib}/glareclient/versioninfo
mv %{buildroot}%{_bindir}/glare %{buildroot}%{_bindir}/glare-%{python2_version}
ln -s ./glare-%{python2_version} %{buildroot}%{_bindir}/glare-2

ln -s ./glare-2 %{buildroot}%{_bindir}/glare

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/glare.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/glare

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/glareclient/tests


%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# generate man page
%{__python2} setup.py build_sphinx -b man
install -p -D -m 644 doc/build/man/glare.1 %{buildroot}%{_mandir}/man1/glare.1

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/glareclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/glare.1.gz
%{_bindir}/glare
%{_bindir}/glare-2
%{_bindir}/glare-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/glare.1.gz
%{_bindir}/glare-3
%{_bindir}/glare-%{python3_version}
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
