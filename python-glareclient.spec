# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname glareclient
# oslosphinx do not work with sphinx > 2
%global with_doc 0

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

%package -n python%{pyver}-%{sname}
Summary: Python API and CLI for OpenStack Glare
%{?python_provide:%python_provide python%{pyver}-%{sname}}
Obsoletes: python2-%{sname} < %{version}-%{release}
BuildRequires:       python%{pyver}-devel
BuildRequires:       python%{pyver}-setuptools
BuildRequires:       python%{pyver}-pbr
BuildRequires:       git
BuildRequires:       python%{pyver}-cliff >= 2.3.0
BuildRequires:       python%{pyver}-keystoneclient >= 1:3.8.0
BuildRequires:       python%{pyver}-openstackclient >= 1.5.0
BuildRequires:       python%{pyver}-oslo-i18n >= 3.15.3
BuildRequires:       python%{pyver}-oslo-utils >= 3.33.0
BuildRequires:       python%{pyver}-osprofiler
BuildRequires:       python%{pyver}-requests >= 2.14.2
BuildRequires:       python%{pyver}-six >= 1.10.0

# Required for tests
BuildRequires:       python%{pyver}-os-testr
BuildRequires:       python%{pyver}-oslotest
BuildRequires:       python%{pyver}-osc-lib-tests
BuildRequires:       python%{pyver}-testrepository
BuildRequires:       python%{pyver}-testscenarios
BuildRequires:       python%{pyver}-testtools
BuildRequires:       python%{pyver}-mock

BuildRequires:       python%{pyver}-requests-mock

Requires:       python%{pyver}-cliff >= 2.3.0
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-osc-lib >= 1.7.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-osprofiler
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-requests >= 2.14.2
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-prettytable

%description -n python%{pyver}-%{sname}
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.

%if 0%{?with_doc}
%package doc
Summary: Documentation for OpenStack Glare API Client

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-oslo-sphinx

%description doc
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.

This package contains auto-generated documentation.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

rm -rf *requirements.txt

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%{pyver_build}

%install
%{pyver_install}
echo "%{version}" > %{buildroot}%{pyver_sitelib}/%{sname}/versioninfo
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s glare %{buildroot}%{_bindir}/glare-%{pyver}

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/glare.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/glare

%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# generate man page
%{pyver_bin} setup.py build_sphinx -b man
install -p -D -m 644 doc/build/man/glare.1 %{buildroot}%{_mandir}/man1/glare.1
%endif

%check
export PYTHON=%{pyver_bin}
# (TODO) Ignore unit tests results until https://bugs.launchpad.net/python-glareclient/+bug/1711469.
# is fixed
%{pyver_bin} setup.py testr || true

%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%if 0%{?with_doc}
%{_mandir}/man1/glare.1.gz
%endif
%{_bindir}/glare
%{_bindir}/glare-%{pyver}

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
