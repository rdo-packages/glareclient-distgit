%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch: noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.

%package -n python3-%{sname}
Summary: Python API and CLI for OpenStack Glare
%{?python_provide:%python_provide python3-%{sname}}
Obsoletes: python2-%{sname} < %{version}-%{release}
BuildRequires:       python3-devel
BuildRequires:       python3-setuptools
BuildRequires:       python3-pbr
BuildRequires:       git-core
BuildRequires:       python3-cliff >= 2.3.0
BuildRequires:       python3-keystoneclient >= 1:3.8.0
BuildRequires:       python3-openstackclient >= 1.5.0
BuildRequires:       python3-oslo-i18n >= 3.15.3
BuildRequires:       python3-oslo-utils >= 3.33.0
BuildRequires:       python3-osprofiler
BuildRequires:       python3-requests >= 2.14.2
BuildRequires:       python3-six >= 1.10.0

# Required for tests
BuildRequires:       python3-os-testr
BuildRequires:       python3-oslotest
BuildRequires:       python3-osc-lib-tests
BuildRequires:       python3-testrepository
BuildRequires:       python3-testscenarios
BuildRequires:       python3-testtools
BuildRequires:       python3-mock

BuildRequires:       python3-requests-mock

Requires:       python3-cliff >= 2.3.0
Requires:       python3-keystoneauth1 >= 3.4.0
Requires:       python3-osc-lib >= 1.7.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-osprofiler
Requires:       python3-pbr
Requires:       python3-requests >= 2.14.2
Requires:       python3-six >= 1.10.0
Requires:       python3-prettytable

%description -n python3-%{sname}
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.

%if 0%{?with_doc}
%package doc
Summary: Documentation for OpenStack Glare API Client

BuildRequires: python3-sphinx
BuildRequires: python3-oslo-sphinx

%description doc
Python client for Glare REST API. Includes python library for Glare API,
Command Line Interface (CLI) library and openstackclient plugin.

This package contains auto-generated documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

rm -rf *requirements.txt

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%{py3_build}

%install
%{py3_install}
echo "%{version}" > %{buildroot}%{python3_sitelib}/%{sname}/versioninfo
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s glare %{buildroot}%{_bindir}/glare-3

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/glare.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/glare

%if 0%{?with_doc}
%{__python3} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# generate man page
%{__python3} setup.py build_sphinx -b man
install -p -D -m 644 doc/build/man/glare.1 %{buildroot}%{_mandir}/man1/glare.1
%endif

%check
export PYTHON=%{__python3}
# (TODO) Ignore unit tests results until https://bugs.launchpad.net/python-glareclient/+bug/1711469.
# is fixed
%{__python3} setup.py testr || true

%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%if 0%{?with_doc}
%{_mandir}/man1/glare.1.gz
%endif
%{_bindir}/glare
%{_bindir}/glare-3

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
