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
Version:	2.8.4
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/ocaml/dune/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	68fbc294aeed510425d20498225d416b
URL:		https://github.com/ocaml/dune
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
Dune is a build system designed for OCaml/Reason projects only. It
focuses on providing the user with a consistent experience and takes
care of most of the low-level details of OCaml compilation. All you
have to do is provide a description of your project and dune will do
the rest.

%prep
%setup -q -n %{module}-%{version}

%build
./configure \
	--libdir %{_libdir}/ocaml \
	--mandir %{_mandir}

%{__make} release \
	CC="%{__cc} %{rpmcflags} -fPIC"

%{__make} doc

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
%{_libdir}/ocaml/dune
%{_mandir}/man1/dune*.1*
%{_mandir}/man5/dune*.5*
