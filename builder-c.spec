Summary:        ABF builder in pure C
Name:           builder-c
Version:        1.0
Release:        7
License:        GPLv2+
Group:          Monitoring
Url:            https://abf.openmandriva.org
# use version here
Source0:	https://github.com/DuratarskeyK/builder-c/archive/master.tar.gz

BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libconfig)
BuildRequires:  pkgconfig(jemalloc)

%description
Builder for ABF

%prep
%setup -qn %{name}-master

%build
%setup_compile_flags
%{__cc} %{optflags} %{_ldflags} -lconfig -lcurl -pthread -ljemalloc jsmn.c statistics.c live_inspector.c live_logger.c exec_build.c api.c main.c -o builder


%install
mkdir -p %{buildroot}%{_bindir}
install -m755 builder %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m755 filestore_upload.sh %{buildroot}%{_sysconfdir}/%{name}
install -m644 builder.conf %{buildroot}%{_sysconfdir}/%{name}

%files
%{_bindir}/builder
%{_sysconfdir}/%{name}/builder.conf
%{_sysconfdir}/%{name}/filestore_upload.sh
