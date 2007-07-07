%define docver  5.2.2

Summary:	Software package for booting x86 PCs over a network
Name:		etherboot
Version: 	5.4.3
Release: 	%mkrel 1
License:	GPL
Group:		Development/Kernel
Source0:	http://prdownloads.sourceforge.net/etherboot/%{name}-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/etherboot/%{name}-doc-%{docver}.tar.bz2
Patch0:		etherboot-5.4.0-gcc4.patch
URL:		http://etherboot.sourceforge.net/
ExclusiveArch:	%{ix86}
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	dos2unix

%description
Etherboot is a free software package for booting x86 PCs over a
network. In principle this could be any network technology that TCP/IP
runs on that supports broadcasting. In practice, the bandwidth
required means it's only practical over LANs and some WANs. Etherboot
is useful for booting PCs diskless. This is desirable in various
situations, for example:
  - Maintaining software for a cluster of equally configured
    workstations centrally.`
  - A low-cost X-terminal.
  - A low cost user platform where remote partitions are mounted by NFS
    and you are willing to accept the slowness of data transfers that
    results from NFS, compared to a local disk.
  - Various kinds of remote servers, e.g. a tape drive server that can
    be accessed with the RMT protocol.
  - Routers.
  - Machines doing tasks in environments unfriendly to disks.

See %{_docdir}/%{name}-%{version}/README.MDK for examples of usage.

%prep
%setup -q -a1
#%patch0 -p1 -b .gcc4

%build
# we don't use custom optimizations here because it can cause problems
# parallel make dies on cluster
make allzdsks allzpxes allzlilos -C src

# clean up cvs files, remove .exe files
find . -name '.cvs*' | xargs rm -f
find . -name '*.exe' | xargs rm -f
find . -name '.keepme' | xargs rm -f
find . -name '.DS_Store' | xargs rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name}/{zdsk,zpxe,zlilo},%{_bindir}}

install src/bin/*.zdsk $RPM_BUILD_ROOT%{_datadir}/%{name}/zdsk
install src/bin/*.zpxe $RPM_BUILD_ROOT%{_datadir}/%{name}/zpxe
install src/bin/*.zlilo $RPM_BUILD_ROOT%{_datadir}/%{name}/zlilo
install src/util/makerom.pl $RPM_BUILD_ROOT%{_bindir}/makerom

# (sb) rpmlint
#find contrib/wakeonlan -type f | xargs dos2unix
dos2unix contrib/wakeonlan/readme.txt
dos2unix contrib/wakeonlan/wakeup.pl
dos2unix contrib/wakeonlan/mp-form.pl
dos2unix contrib/romid/pktdrv.bat
dos2unix contrib/hdload/hdload.S
dos2unix contrib/romid/readme
dos2unix contrib/wakeonlan/mp-form.txt
dos2unix contrib/wakeonlan/mp-form1.pl
sed -i 's|perl/bin/perl|usr/bin/perl|' contrib/wakeonlan/mp-form.pl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL RELNOTES index.html doc contrib
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%attr(755,root,root) %{_bindir}/*

