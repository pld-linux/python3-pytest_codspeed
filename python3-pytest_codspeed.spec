# Conditional build:
%bcond_without	tests	# unit tests

%define		module	pytest_codspeed
Summary:	Pytest plugin to create CodSpeed benchmarks
# Name must match the python module/package name (as on pypi or in 'import' statement)
Name:		python3-%{module}
Version:	3.2.0
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	1af7148ae89f3820b3a3778312ff3b60
URL:		https://pypi.org/project/pytest-codspeed/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
#BuildRequires:	python3-
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Creating benchmarks with pytest-codspeed is compatible with the
standard pytest-benchmark API. So if you already have benchmarks
written with it, you can start using pytest-codspeed right away.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python} -m zipfile -e build-3/*.whl build-3-test
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/py.typed
%{py3_sitedir}/%{module}/__pycache__/*.py*
%{py3_sitedir}/%{module}/instruments/*.py
%{py3_sitedir}/%{module}/instruments/__pycache__/*.py*
%{py3_sitedir}/%{module}/instruments/valgrind/*.py
%{py3_sitedir}/%{module}/instruments/valgrind/__pycache__/*.py*
%dir %{py3_sitedir}/%{module}/instruments/valgrind/_wrapper
%{py3_sitedir}/%{module}/instruments/valgrind/_wrapper/__pycache__/*.py*
%{py3_sitedir}/%{module}/instruments/valgrind/_wrapper/*.py
%{py3_sitedir}/%{module}/instruments/valgrind/_wrapper/*.[chi]
%{py3_sitedir}/%{module}/instruments/valgrind/_wrapper/*.pyi
%attr(755,root,root) %{py3_sitedir}/%{module}/instruments/valgrind/_wrapper/*.so
%{py3_sitedir}/%{module}-%{version}.dist-info
