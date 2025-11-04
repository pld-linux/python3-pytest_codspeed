#
# Conditional build:
%bcond_with	tests	# unit tests

%define		module	pytest_codspeed
Summary:	Pytest plugin to create CodSpeed benchmarks
Summary(pl.UTF-8):	Wtyczka pytesta do tworzenia benchmarków CodSpeed
Name:		python3-%{module}
Version:	4.2.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pytest-codspeed/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest_codspeed/%{module}-%{version}.tar.gz
# Source0-md5:	6b0fc18c07596207513a4447e8a35199
Patch0:		noarchlimit.patch
URL:		https://pypi.org/project/pytest-codspeed/
BuildRequires:	python3-build
BuildRequires:	python3-cffi >= 1.17.1
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:61
%if %{with tests}
%if "%{_ver_lt %{py3_ver} 3.10}" == "1"
BuildRequires:	python3-importlib_metadata >= 8.5.0
%endif
BuildRequires:	python3-pytest >= 3.8
BuildRequires:	python3-rich >= 13.8.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
BuildRequires:	valgrind
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pytest plugin to create CodSpeed benchmarks.

%description -l pl.UTF-8
Wtyczka pytesta do tworzenia benchmarków CodSpeed.

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1

%build
export PYTEST_CODSPEED_FORCE_EXTENSION_BUILD=1

%py3_build_pyproject

%if %{with tests}
%{__python} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

# module sources
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/pytest_codspeed/instruments/hooks/instrument-hooks

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%dir %{py3_sitedir}/%{module}
%{py3_sitedir}/%{module}/*.py
%{py3_sitedir}/%{module}/py.typed
%{py3_sitedir}/%{module}/__pycache__
%dir %{py3_sitedir}/%{module}/instruments
%{py3_sitedir}/%{module}/instruments/*.py
%{py3_sitedir}/%{module}/instruments/__pycache__
%dir %{py3_sitedir}/%{module}/instruments/hooks
%attr(755,root,root) %{py3_sitedir}/%{module}/instruments/hooks/dist_instrument_hooks.cpython-*.so
%{py3_sitedir}/%{module}/instruments/hooks/dist_instrument_hooks.pyi
%{py3_sitedir}/%{module}/instruments/hooks/*.py
%{py3_sitedir}/%{module}/instruments/hooks/__pycache__
%{py3_sitedir}/%{module}-%{version}.dist-info
