%bcond_without jemalloc

Summary:	ABF client builder in pure C
Name:		builder-c
Version:	1.5.9
Release:	2
License:	GPLv2+
Group:		Monitoring
Url:		https://abf.openmandriva.org
# use version here
Source0:	https://github.com/DuratarskeyK/builder-c/archive/%{version}.tar.gz?/%{name}-%{version}.tar.gz
Source1:	builder.service
Source2:	builder-environment.conf
Source3:	builder.conf
Source4:	builder.sysusers
Source5:	builder.tmpfiles
Source6:	https://raw.githubusercontent.com/OpenMandrivaSoftware/docker-builder/refs/heads/master/logchecker.go

Patch0:		builder-c-1.5.7-fixes-for-newer-toolchains.patch
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libconfig)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	systemd-rpm-macros
BuildRequires:	golang
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
Requires(pre):	systemd
%systemd_requires

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
go build -x -o %{buildroot}%{_bindir}/logchecker logchecker.go
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m644 builder.conf %{buildroot}%{_sysconfdir}/%{name}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/builder-environment.conf
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/builder.conf
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%pre
%sysusers_create_package %{name} %{SOURCE4}

%post
if ! grep -qE "mock.*NOPASSWD.*" /etc/sudoers; then
    printf "%s\n"  "%mock ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
fi

%transfiletriggerin -- /etc/mock
chown -R omv:mock /etc/mock

%transfiletriggerpostun -- /etc/mock
chown -R omv:mock /etc/mock

%files
%dir %{_sysconfdir}/%{name}
%{_bindir}/builder
%{_sysconfdir}/%{name}/builder.conf
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/builder-environment.conf
