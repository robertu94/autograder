%global srcname autograder
%global sum A automatic testing and grading framework in python

Name: python-%{srcname}
Version: 0.0.1
Release: 1%{?dist}
Summary: %{sum}

License: BSD
URL: http://www.cs.clemson.edu/acm
Source0: https://github.com/robertu94/autograder/archive/master.zip

BuildArch: noarch
BuildRequires: python3-devel
Requires: git hg svn docker python3

%description
A automatic testing and grading framework in python

%package -n python3-%{scrname}
Summary: %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%prep
%autosetup -n master.zip

%build
%py3_build

%install
%py3_install

%check
pushd tests
make test
popd

%files -n python3-%{srcname}
%licence LICENCE
%doc README.md
%{python3_sitelab/*
%{_bindir}/autograder

%changelog

* Mon Feb 1 2016 Robert Underwood <rr.underwood94@gmail.com> 0.0.1 Packaged for RPM distributions
