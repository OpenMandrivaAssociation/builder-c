%ifarch aarch64
# As of cooker 4.0-20180505, jemalloc 5.0.1, builder-c crashes on startup
# on Snapdragon 820 based boards (works fine on other aarch64 boards
# though) if built with jemalloc. Works fine on any board with
# glibc malloc.
%bcond_with jemalloc
%else
%bcond_without jemalloc
%endif

Summary:        ABF builder in pure C
Name:           builder-c
Version:        1.1.3
Release:        1
License:        GPLv2+
Group:          Monitoring
Url:            https://abf.openmandriva.org
# use version here
Source0:	https://github.com/DuratarskeyK/builder-c/archive/%{version}.tar.gz
Source1:	builder.service
Source2:	builder-environment.conf

BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libconfig)
%if %{with jemalloc}
BuildRequires:  pkgconfig(jemalloc)
%endif

%description
Builder for ABF.

%prep
%setup -q

%build
%setup_compile_flags
%if %{with jemalloc}
MALLOC_FLAGS="-L`jemalloc-config --libdir` -ljemalloc `jemalloc-config --libs`"
%else
MALLOC_FLAGS=""
%endif
%{__cc} %{optflags} %{ldflags} $MALLOC_FLAGS -lconfig -lcurl -pthread jsmn.c statistics.c live_inspector.c live_logger.c exec_build.c api.c main.c -o builder

%install
mkdir -p %{buildroot}%{_bindir}
install -m755 builder %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m755 filestore_upload.sh %{buildroot}%{_sysconfdir}/%{name}
install -m644 builder.conf %{buildroot}%{_sysconfdir}/%{name}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/builder-environment.conf

%files
%{_bindir}/builder
%{_sysconfdir}/%{name}/builder.conf
%{_sysconfdir}/%{name}/filestore_upload.sh
%{_unitdir}/%{name}.service
%{_sysconfdir}/sysconfig/builder-environment.conf
