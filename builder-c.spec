%ifarch aarch64
# As of cooker 4.0-20180505, jemalloc 5.0.1, builder-c crashes on startup
# on Snapdragon 820 based boards (works fine on other aarch64 boards
# though) if built with jemalloc. Works fine on any board with
# glibc malloc.
%bcond_with jemalloc
%else
%bcond_without jemalloc
%endif

Summary:	ABF client builder in pure C
Name:		builder-c
Version:	1.5.6
Release:	3
License:	GPLv2+
Group:		Monitoring
Url:		https://abf.openmandriva.org
# use version here
Source0:	https://github.com/DuratarskeyK/builder-c/archive/%{version}.tar.gz
# (tpg) these were merged by upstream, so remove when new version is released
Patch0:		0000-try-to-retry-DNS-catch.patch
Patch1:		0001-better-logging-for-DNS-retry.patch
Source1:	builder.service
Source2:	builder-environment.conf
Source3:	builder.conf
Source4:	builder.sysusers
Source5:	builder.tmpfiles
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libconfig)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	systemd-macros
%if %{with jemalloc}
BuildRequires:	pkgconfig(jemalloc)
%endif
# (tpg) keep that list close to https://github.com/OpenMandrivaSoftware/docker-builder/blob/master/Dockerfile.builder
Requires:	python
Requires:	mock
Requires:	git
Requires:	coreutils
Requires:	curl
Requires:	sudo
Requires:	procps-ng
Requires:	gnutar
Requires:	findutils
Requires:	util-linux
Requires:	wget
Requires:	rpmdevtools
Requires:	sed
Requires:	grep
Requires:	xz
Requires:	gnupg
Requires:	hostname
Requires:	python-yaml
Requires:	python-magic

%description
Client builder for abf.openmandriva.org.

How to run builder on your host:
1. Edit /etc/sysconfig/builder-environment.conf
    and provide needed data i.e. BUILD_TOKEN
2. systemctl enable --now builder-c.service

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
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_sysusersdir}/builder.conf
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/builder.conf

%files
%{_bindir}/builder
%{_sysconfdir}/%{name}/builder.conf
%{_unitdir}/%{name}.service
%{_sysusersdir}/builder.conf
%{_tmpfilesdir}/builder.conf
%config(noreplace) %{_sysconfdir}/sysconfig/builder-environment.conf
