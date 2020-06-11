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
Version:        1.5.3
Release:        1
License:        GPLv2+
Group:          Monitoring
Url:            https://abf.openmandriva.org
# use version here
Source0:	https://github.com/DuratarskeyK/builder-c/archive/%{version}.tar.gz
Source1:	builder.service
Source2:	builder-environment.conf
Source3:	builder.conf
Requires:	curl

BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libconfig)
%if %{with jemalloc}
BuildRequires:  pkgconfig(jemalloc)
%endif

%description
Builder for ABF.

%prep
%autosetup -p1

%build
%set_build_flags
%if %{with jemalloc}
MALLOC_FLAGS="-L$(jemalloc-config --libdir) -Wl,-rpath,$(jemalloc-config --libdir) -ljemalloc $(jemalloc-config --libs)"
%else
MALLOC_FLAGS=""
%endif
%make_build CC=%{__cc}

%install
mkdir -p %{buildroot}%{_bindir}
install -m755 builder %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m644 builder.conf %{buildroot}%{_sysconfdir}/%{name}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/builder-environment.conf
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/builder.conf

%files
%{_bindir}/builder
%{_sysconfdir}/%{name}/builder.conf
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/builder-environment.conf
