Summary:	PHPSysInfo displays system status 
Name:		phpsysinfo
Version:	2.5.4
Release:	9
Group:		System/Servers
License:	GPLv2+
URL:		http://phpsysinfo.sourceforge.net/
Source0:	http://ovh.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Patch0:		phpsysinfo-2.5.2-rc2-mdv_conf.diff
Requires:       apache-mod_php php-xml lm_sensors
Requires(post):   ccp
BuildArch:	noarch

%description
PHPSysInfo is a customizable PHP Script that parses /proc, and formats
information nicely. It will display information about system facts like Uptime,
CPU, Memory, PCI devices, SCSI devices, IDE devices, Network adapters, Disk
usage, and more.

Included is also a new lm_sensors module that will present voltage,
temperature, fan speed, etc. if the appropriate lm_sensors modules are loaded.

%prep

%setup -q -n %{name}
%patch0 -p1

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/var/www/%{name}

cp -aRf * %{buildroot}/var/www/%{name}/

mv %{buildroot}/var/www/%{name}/config.php.new %{buildroot}%{_sysconfdir}/%{name}/config.php

# cleanup
rm -f %{buildroot}/var/www/%{name}/COPYING
rm -f %{buildroot}/var/www/%{name}/ChangeLog
rm -f %{buildroot}/var/www/%{name}/README

cat > %{buildroot}%{webappconfdir}/%{name}.conf << EOF
Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    Order allow,deny
    Allow from all
</Directory>
EOF

%post
ccp --delete --ifexists --set "NoOrphans" --ignoreopt config_version \
    --oldfile %{_sysconfdir}/%{name}/config.php \
    --newfile %{_sysconfdir}/%{name}/config.php.rpmnew


%clean

%files
%defattr(-,root,root)
%doc COPYING ChangeLog README
%config(noreplace) %{webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}
/var/www/%{name}


%changelog
* Tue Dec 07 2010 Oden Eriksson <oeriksson@mandriva.com> 2.5.4-7mdv2011.0
+ Revision: 614541
- the mass rebuild of 2010.1 packages

* Sun Feb 07 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.5.4-6mdv2010.1
+ Revision: 501754
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 2.5.4-5mdv2010.0
+ Revision: 430708
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Fri Aug 01 2008 Thierry Vignaud <tv@mandriva.org> 2.5.4-4mdv2009.0
+ Revision: 259000
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 2.5.4-3mdv2009.0
+ Revision: 246886
- rebuild

* Sat Feb 02 2008 Funda Wang <fwang@mandriva.org> 2.5.4-1mdv2008.1
+ Revision: 161426
- New version 2.5.4

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Aug 19 2007 Oden Eriksson <oeriksson@mandriva.com> 2.5.3-1mdv2008.0
+ Revision: 66589
- 2.5.3
- lowercase the package name


* Fri Mar 16 2007 Nicolas Lécureuil <neoclust@mandriva.org> 2.5.2-0.rc2.2mdv2007.1
+ Revision: 145029
- Add XDG menu entry
- Import phpSysInfo

* Mon May 15 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-0.rc2.1mdk
- 2.5.2rc2
- use the webapps policy
- fix a menuentry
- add mod_rewrite rules to enforce ssl connections
- fix deps

* Mon Jun 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.3-2mdk
- fix deps

* Tue Aug 24 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.3-1mdk
- 2.3 (works with php5-*)

