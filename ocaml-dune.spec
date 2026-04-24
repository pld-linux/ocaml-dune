#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	dune
Summary:	A composable build system for OCaml
Summary(pl.UTF-8):	Składalny system budowania dla OCamla
Name:		ocaml-%{module}
Version:	3.11.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ocaml/dune/releases
Source0:	https://github.com/ocaml/dune/releases/download/%{version}/%{module}-%{version}.tbz
# Source0-md5:	0dfab1816e5e64cca8288e66fc6f9ff6
Patch0:		no-lwt.patch
Patch1:		no-werror.patch
URL:		https://github.com/ocaml/dune
BuildRequires:	ocaml >= 1:4.08
BuildRequires:	ocaml-csexp >= 1.3.0
%requires_eq	ocaml-runtime
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dune is a build system designed for OCaml/Reason projects only. It
focuses on providing the user with a consistent experience and takes
care of most of the low-level details of OCaml compilation. All you
have to do is provide a description of your project and dune will do
the rest.

%description -l pl.UTF-8
Dune to system budowania zaprojektowany wyłącznie dla projektów
OCamla/Reasona. Skupia się na zapewnieniu użytkownikowi spójnego
zachowania i dba o większość niskopoziomowych szczegółów kompilacji
OCamla. Wszystko, co trzeba zrobić, to utworzenie opisu projektu, a
dune zrobi resztę.

%package devel
Summary:	Development files for dune
Summary(pl.UTF-8):	Pliki programistyczne dune
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-csexp-devel >= 1.3.0

%description devel
This package contains libraries and signature files for developing
applications that use dune.

%description devel -l pl.UTF-8
Ten pakiet zawiera biblioteki i pliki sygnatur do tworzenia aplikacji
wykorzystujących dune.

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1
%patch -P1 -p1

%{__rm} dune-rpc-lwt.opam
%{__rm} -r otherlibs/dune-rpc-lwt

%build
./configure \
	--etcdir %{_sysconfdir} \
	--bindir %{_bindir} \
	--sbindir %{_sbindir} \
	--docdir %{_docdir} \
	--datadir %{_datadir} \
	--libdir %{_libdir}/ocaml \
	--mandir %{_mandir}

%{__make} release \
	CC="%{__cc} %{rpmcflags} -fPIC"

./dune.exe build @install

%{__make} doc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# "make install" only installs the binary.  We want the libraries, too.
./dune.exe install --destdir $RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md CHANGES.md README.md doc/_build/*
%attr(755,root,root) %{_bindir}/dune
%dir %{_libdir}/ocaml/dune
%dir %{_libdir}/ocaml/dune-action-plugin
%dir %{_libdir}/ocaml/dune-build-info
%dir %{_libdir}/ocaml/dune-configurator
%dir %{_libdir}/ocaml/dune-glob
%dir %{_libdir}/ocaml/dune-private-libs
%dir %{_libdir}/ocaml/dune-private-libs/dune_re
%dir %{_libdir}/ocaml/dune-private-libs/dune-section
%dir %{_libdir}/ocaml/dune-private-libs/meta_parser
%dir %{_libdir}/ocaml/dune-site
%dir %{_libdir}/ocaml/dune-site/dynlink
%dir %{_libdir}/ocaml/dune-site/linker
%dir %{_libdir}/ocaml/dune-site/plugins
%dir %{_libdir}/ocaml/dune-site/private
%dir %{_libdir}/ocaml/dune-rpc
%dir %{_libdir}/ocaml/dune-rpc/private
%dir %{_libdir}/ocaml/stdune
%dir %{_libdir}/ocaml/stdune/csexp
%dir %{_libdir}/ocaml/stdune/filesystem_stubs
%{_libdir}/ocaml/dune*/META
%{_libdir}/ocaml/dune-*/*.cma
%{_libdir}/ocaml/dune-*/*.cmi
%{_libdir}/ocaml/dune-*/*/*.cma
%{_libdir}/ocaml/dune-*/*/*.cmi
%{_libdir}/ocaml/dune-configurator/.private
%{_libdir}/ocaml/stdune/META
%{_libdir}/ocaml/stdune/*.cma
%{_libdir}/ocaml/stdune/*.cmi
%{_libdir}/ocaml/stdune/dune-package
%{_libdir}/ocaml/stdune/opam
%{_libdir}/ocaml/stdune/*/*.cma
%{_libdir}/ocaml/stdune/*/*.cmi
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/dune-*/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/dune-*/*/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/stdune/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/stdune/*/*.cmxs
%endif
%{_libdir}/ocaml/stublibs/dlldune_filesystem_stubs_stubs.so
%{_libdir}/ocaml/stublibs/dllstdune_stubs.so
%{_mandir}/man1/dune*.1*
%{_mandir}/man5/dune-config.5*

# Extra libs build with dune, keep the separate
%dir %{_libdir}/ocaml/chrome-trace
%{_libdir}/ocaml/chrome-trace/META
%{_libdir}/ocaml/chrome-trace/*.cma
%{_libdir}/ocaml/chrome-trace/*.cmi
%{_libdir}/ocaml/chrome-trace/dune-package
%{_libdir}/ocaml/chrome-trace/opam
%dir %{_libdir}/ocaml/dyn
%{_libdir}/ocaml/dyn/META
%{_libdir}/ocaml/dyn/dune-package
%{_libdir}/ocaml/dyn/*.cma
%{_libdir}/ocaml/dyn/*.cmi
%{_libdir}/ocaml/dyn/opam
%dir %{_libdir}/ocaml/dyn/pp
%{_libdir}/ocaml/dyn/pp/*.cma
%{_libdir}/ocaml/dyn/pp/*.cmi
%dir %{_libdir}/ocaml/ocamlc-loc
%{_libdir}/ocaml/ocamlc-loc/META
%{_libdir}/ocaml/ocamlc-loc/dune-package
%{_libdir}/ocaml/ocamlc-loc/*.cma
%{_libdir}/ocaml/ocamlc-loc/*.cmi
%{_libdir}/ocaml/ocamlc-loc/opam
%dir %{_libdir}/ocaml/ordering
%{_libdir}/ocaml/ordering/META
%{_libdir}/ocaml/ordering/dune-package
%{_libdir}/ocaml/ordering/opam
%{_libdir}/ocaml/ordering/*.cma
%{_libdir}/ocaml/ordering/*.cmi
%dir %{_libdir}/ocaml/xdg
%{_libdir}/ocaml/xdg/META
%{_libdir}/ocaml/xdg/dune-package
%{_libdir}/ocaml/xdg/opam
%{_libdir}/ocaml/xdg/*.cma
%{_libdir}/ocaml/xdg/*.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/chrome-trace/*.cmxs
%{_libdir}/ocaml/dyn/*.cmxs
%{_libdir}/ocaml/dyn/pp/*.cmxs
%{_libdir}/ocaml/ocamlc-loc/*.cmxs
%{_libdir}/ocaml/ordering/*.cmxs
%{_libdir}/ocaml/xdg/*.cmxs
%endif
%{_libdir}/ocaml/stublibs/dllxdg_stubs.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/dune*/dune-package
%{_libdir}/ocaml/dune*/opam
%{_libdir}/ocaml/dune-*/*.cmt
%{_libdir}/ocaml/dune-*/*.cmti
%{_libdir}/ocaml/dune-*/*.ml
%{_libdir}/ocaml/dune-*/*.mli
%{_libdir}/ocaml/dune-*/*/*.cmo
%{_libdir}/ocaml/dune-*/*/*.cmt
%{_libdir}/ocaml/dune-*/*/*.cmti
%{_libdir}/ocaml/dune-*/*/*.ml
%{_libdir}/ocaml/dune-*/*/*.mli
%{_libdir}/ocaml/stdune/*.cmt
%{_libdir}/ocaml/stdune/*.cmti
%{_libdir}/ocaml/stdune/*.ml
%{_libdir}/ocaml/stdune/*.mli
%{_libdir}/ocaml/stdune/*/*.cmt
%{_libdir}/ocaml/stdune/*/*.cmti
%{_libdir}/ocaml/stdune/*/*.ml
%{_libdir}/ocaml/stdune/*/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/dune-*/*.a
%{_libdir}/ocaml/dune-*/*.cmx
%{_libdir}/ocaml/dune-*/*.cmxa
%{_libdir}/ocaml/dune-*/*/*.a
%{_libdir}/ocaml/dune-*/*/*.cmx
%{_libdir}/ocaml/dune-*/*/*.cmxa
%{_libdir}/ocaml/dune-*/*/*.o
%{_libdir}/ocaml/stdune/*.a
%{_libdir}/ocaml/stdune/*.cmx
%{_libdir}/ocaml/stdune/*.cmxa
%{_libdir}/ocaml/stdune/*/*.a
%{_libdir}/ocaml/stdune/*/*.cmx
%{_libdir}/ocaml/stdune/*/*.cmxa
%else
%{_libdir}/ocaml/stdune/libstdune_stubs.a
%{_libdir}/ocaml/stdune/filesystem_stubs/libdune_filesystem_stubs_stubs.a
%endif

# Extra libs build with dune, keep the separate
%{_libdir}/ocaml/chrome-trace/*.cmt
%{_libdir}/ocaml/chrome-trace/*.cmti
%{_libdir}/ocaml/chrome-trace/*.ml
%{_libdir}/ocaml/chrome-trace/*.mli
%{_libdir}/ocaml/dyn/*.cmt
%{_libdir}/ocaml/dyn/*.cmti
%{_libdir}/ocaml/dyn/*.ml
%{_libdir}/ocaml/dyn/*.mli
%{_libdir}/ocaml/dyn/pp/*.cmt
%{_libdir}/ocaml/dyn/pp/*.cmti
%{_libdir}/ocaml/dyn/pp/*.ml
%{_libdir}/ocaml/dyn/pp/*.mli
%{_libdir}/ocaml/ocamlc-loc/*.cmt
%{_libdir}/ocaml/ocamlc-loc/*.cmti
%{_libdir}/ocaml/ocamlc-loc/*.ml
%{_libdir}/ocaml/ocamlc-loc/*.mli
%{_libdir}/ocaml/ordering/*.cmt
%{_libdir}/ocaml/ordering/*.cmti
%{_libdir}/ocaml/ordering/*.ml
%{_libdir}/ocaml/ordering/*.mli
%{_libdir}/ocaml/xdg/*.cmt
%{_libdir}/ocaml/xdg/*.cmti
%{_libdir}/ocaml/xdg/*.ml
%{_libdir}/ocaml/xdg/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/chrome-trace/*.a
%{_libdir}/ocaml/chrome-trace/*.cmx
%{_libdir}/ocaml/chrome-trace/*.cmxa
%{_libdir}/ocaml/dyn/*.a
%{_libdir}/ocaml/dyn/*.cmx
%{_libdir}/ocaml/dyn/*.cmxa
%{_libdir}/ocaml/dyn/pp/*.a
%{_libdir}/ocaml/dyn/pp/*.cmx
%{_libdir}/ocaml/dyn/pp/*.cmxa
%{_libdir}/ocaml/ocamlc-loc/*.a
%{_libdir}/ocaml/ocamlc-loc/*.cmx
%{_libdir}/ocaml/ocamlc-loc/*.cmxa
%{_libdir}/ocaml/ordering/*.a
%{_libdir}/ocaml/ordering/*.cmx
%{_libdir}/ocaml/ordering/*.cmxa
%{_libdir}/ocaml/xdg/*.a
%{_libdir}/ocaml/xdg/*.cmx
%{_libdir}/ocaml/xdg/*.cmxa
%else
%{_libdir}/ocaml/xdg/libxdg_stubs.a
%endif
