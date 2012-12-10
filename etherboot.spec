%define docver  5.2.2

Summary:	Software package for booting x86 PCs over a network
Name:		etherboot
Version: 	5.4.4
Release: 	%mkrel 5
License:	GPL
Group:		Development/Kernel
Source0:	http://prdownloads.sourceforge.net/etherboot/%{name}-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/etherboot/%{name}-doc-%{docver}.tar.bz2
Patch0:		etherboot-5.4.4-no-inline.patch
URL:		http://etherboot.sourceforge.net/
ExclusiveArch:	%{ix86} ia64 x86_64
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
%patch0 -p0 -b .no_inline

%build
# we don't use custom optimizations here because it can cause problems
# parallel make dies on cluster
make allzdsks allzpxes allzlilos -C src \
%ifarch x86_64
ARCH="i386" EXTRA_CFLAGS="-m32" EXTRA_ASFLAGS="--32" EXTRA_LDFLAGS="-m elf_i386"
# (x86_64 flags from main Makefile)
# x86_64 systems can run 32-bit code so there is no sense in porting etherboot
# to x86_64 native, also this way the boot images have the ability to work on
# both 32-bit and 64-bit systems
%endif

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



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 5.4.4-5mdv2011.0
+ Revision: 618245
- the mass rebuild of 2010.0 packages

* Fri May 22 2009 Eugeni Dodonov <eugeni@mandriva.com> 5.4.4-4mdv2010.0
+ Revision: 378611
- Updated to 5.4.4.
  Dropped Patch0 (no longer required).
  Added patch to handle inlined functions correctly.

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 5.4.3-2mdv2008.1
+ Revision: 136405
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Aug 07 2007 Anssi Hannula <anssi@mandriva.org> 5.4.3-2mdv2008.0
+ Revision: 59573
- build on ia64 and x86_64 as well

* Sat Jul 07 2007 Funda Wang <fwang@mandriva.org> 5.4.3-1mdv2008.0
+ Revision: 49368
- New version


* Fri Jun 09 2006 Stew Benedict <sbenedict@mandriva.com> 5.4.2-1mdv2007.0
- 5.4.2

* Mon Nov 28 2005 Stew Benedict <sbenedict@mandriva.com> 5.4.1-1mdk
- New release 5.4.1

* Tue Aug 30 2005 Stew Benedict <sbenedict@mandriva.com> 5.4.0-2mdk
- fix build (P0)

* Wed May 04 2005 Stew Benedict <sbenedict@mandriva.com> 5.4.0-1mdk
- New release 5.4.0, drop P0, rpmlint cleanups
- README.MDK doesn't apply anymore, back to pre-built images

* Wed Dec 01 2004 Pixel <pixel@mandrakesoft.com> 5.2.5-2mdk
- fix and enhance a little README.MDK

* Mon Nov 08 2004 Stew Benedict <sbenedict@mandrakesoft.com> 5.2.5-1mdk
- 5.2.5, drop p0 - merged upstream
- add new patch0 for gcc-3.4.1

* Fri May 07 2004 Stew Benedict <sbenedict@mandrakesoft.com> 5.2.4-2mdk
- examples from description -> README.MDK for Thierry

* Thu May 06 2004 Stew Benedict <sbenedict@mandrakesoft.com> 5.2.4-1mdk
- 5.2.4

* Tue Dec 23 2003 Stew Benedict <sbenedict@mandrakesoft.com> 5.2.2-2mdk
- build additional files for creating other types of images

* Fri Dec 19 2003 Stew Benedict <sbenedict@mandrakesoft.com> 5.2.2-1mdk
- 5.2.2, add patch0 - build in memcmp

* Thu Aug 07 2003 Stew Benedict <sbenedict@mandrakesoft.com> 5.0.11-1mdk
- 5.0.11

