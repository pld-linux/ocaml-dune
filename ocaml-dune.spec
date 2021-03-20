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
Release:	3
License:	MIT
Group:		Libraries
Source0:	https://github.com/ocaml/dune/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	68fbc294aeed510425d20498225d416b
URL:		https://github.com/ocaml/dune
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-csexp
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dune is a build system designed for OCaml/Reason projects only. It
focuses on providing the user with a consistent experience and takes
care of most of the low-level details of OCaml compilation. All you
have to do is provide a description of your project and dune will do
the rest.

%package        devel
Summary:	Development files for dune
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-csexp-devel

%description    devel
This package contains libraries and signature files for developing
applications that use dune.

%prep
%setup -q -n %{module}-%{version}

%build
./configure \
	--libdir %{_libdir}/ocaml \
	--mandir %{_mandir}

%{__make} release \
	CC="%{__cc} %{rpmcflags} -fPIC"

./dune.exe build @install

%{__make} doc

# Relink the stublibs.  See https://github.com/ocaml/dune/issues/2977.
cd _build/default/src/stdune
ocamlmklib -g -ldopt "%{rpmldflags}" -o stdune_stubs fcntl_stubs.o
cd -
cd _build/default/src/dune_filesystem_stubs
ocamlmklib -g -ldopt "%{rpmldflags}" -o dune_filesystem_stubs_stubs \
	$(ar t libdune_filesystem_stubs_stubs.a)

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# "make install" only installs the binary.  We want the libraries, too.
./dune.exe install --destdir $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md CHANGES.md README.md MIGRATION.md doc/_build/*
%attr(755,root,root) %{_bindir}/dune
%dir %{_libdir}/ocaml/dune
%dir %{_libdir}/ocaml/dune-action-plugin
%dir %{_libdir}/ocaml/dune-build-info
%dir %{_libdir}/ocaml/dune-configurator
%dir %{_libdir}/ocaml/dune-glob
%dir %{_libdir}/ocaml/dune-private-libs
%dir %{_libdir}/ocaml/dune-private-libs/dune-lang
%dir %{_libdir}/ocaml/dune-private-libs/dune_re
%dir %{_libdir}/ocaml/dune-private-libs/ocaml-config
%dir %{_libdir}/ocaml/dune-private-libs/stdune
%dir %{_libdir}/ocaml/dune-site
%dir %{_libdir}/ocaml/dune-site/plugins
%{_libdir}/ocaml/dune*/META
%{_libdir}/ocaml/dune*/*.cma
%{_libdir}/ocaml/dune*/*.cmi
%{_libdir}/ocaml/dune-configurator/.private
%{_libdir}/ocaml/dune-private-libs/*/*.cma
%{_libdir}/ocaml/dune-private-libs/*/*.cmi
%{_libdir}/ocaml/dune-site/*/*.cma
%{_libdir}/ocaml/dune-site/*/*.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/dune*/*.cmxs
%{_libdir}/ocaml/dune-private-libs/*/*.cmxs
%{_libdir}/ocaml/dune-site/*/*.cmxs
%endif
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllstdune_stubs.so
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dlldune_filesystem_stubs_stubs.so
%{_mandir}/man1/dune*.1*
%{_mandir}/man5/dune*.5*

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/dune*/dune-package
%{_libdir}/ocaml/dune*/opam
%{_libdir}/ocaml/dune*/*.cmt
%{_libdir}/ocaml/dune*/*.cmti
%{_libdir}/ocaml/dune*/*.ml
%{_libdir}/ocaml/dune*/*.mli
%{_libdir}/ocaml/dune-private-libs/*/*.cmt
%{_libdir}/ocaml/dune-private-libs/*/*.cmti
%{_libdir}/ocaml/dune-private-libs/*/*.ml
%{_libdir}/ocaml/dune-private-libs/*/*.mli
%{_libdir}/ocaml/dune-site/*/*.cmt
%{_libdir}/ocaml/dune-site/*/*.cmti
%{_libdir}/ocaml/dune-site/*/*.ml
%{_libdir}/ocaml/dune-site/*/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/dune*/*.a
%{_libdir}/ocaml/dune*/*.cmx
%{_libdir}/ocaml/dune*/*.cmxa
%{_libdir}/ocaml/dune-private-libs/*/*.a
%{_libdir}/ocaml/dune-private-libs/*/*.cmx
%{_libdir}/ocaml/dune-private-libs/*/*.cmxa
%{_libdir}/ocaml/dune-site/*/*.a
%{_libdir}/ocaml/dune-site/*/*.cmx
%{_libdir}/ocaml/dune-site/*/*.cmxa
%else
%{_libdir}/ocaml/dune-private-libs/filesystem_stubs/libdune_filesystem_stubs_stubs.a
%{_libdir}/ocaml/dune-private-libs/stdune/libstdune_stubs.a
%endif
