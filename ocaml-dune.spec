#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	dune
Summary:	A composable build system for OCaml
Name:		ocaml-%{module}
Version:	1.5.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/ocaml/dune/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	3f14fccc36dd6b852390831a3f2b4137
Patch0:		mandir.patch
URL:		https://github.com/ocaml/dune
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}
%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
A composable build system for OCaml.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
ocaml configure.ml

%{__make} -j1 release \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md CHANGES.md README.md
%attr(755,root,root) %{_bindir}/dune
%attr(755,root,root) %{_bindir}/jbuilder
%{_libdir}/ocaml/site-lib/%{module}
%{_mandir}/man1/dune*.1*
%{_mandir}/man5/dune*.5*
