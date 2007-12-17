%define _requires_exceptions pear(/etc

Summary:	PHPSysInfo displays system status 
Name:		phpsysinfo
Version:	2.5.3
Release:	%mkrel 1
Group:		System/Servers
License:	GPL
URL:		http://phpsysinfo.sourceforge.net/
Source0:	http://belnet.dl.sourceforge.net/sourceforge/phpsysinfo/%{name}-%{version}.tar.gz
Patch0:		phpsysinfo-2.5.2-rc2-mdv_conf.diff
Requires(pre):  apache-mod_php php-xml lm_sensors
Requires:       apache-mod_php php-xml lm_sensors
BuildRequires:	perl
BuildRequires:	apache-base >= 2.0.54
BuildArch:	noarch
Provides:	phpSysInfo = %{version}
Obsoletes:	phpSysInfo

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/var/www/%{name}

cp -aRf * %{buildroot}/var/www/%{name}/

mv %{buildroot}/var/www/%{name}/config.php.new %{buildroot}%{_sysconfdir}/%{name}/config.php

# cleanup
rm -f %{buildroot}/var/www/%{name}/COPYING
rm -f %{buildroot}/var/www/%{name}/ChangeLog
rm -f %{buildroot}/var/www/%{name}/README

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    Order deny,allow
    Deny from all
    Allow from 127.0.0.1
</Directory>

#<LocationMatch /%{name}>
#    Options FollowSymLinks
#    RewriteEngine on
#    RewriteCond %{SERVER_PORT} !^443$
#    RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
#</LocationMatch>

EOF

%post
ccp --delete --ifexists --set "NoOrphans" --ignoreopt config_version --oldfile %{_sysconfdir}/%{name}/config.php --newfile %{_sysconfdir}/%{name}/config.php.rpmnew
%_post_webapp

%postun
%_postun_webapp

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING ChangeLog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/config.php
/var/www/%{name}
