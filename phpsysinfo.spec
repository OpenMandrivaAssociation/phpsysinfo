%define _requires_exceptions pear(/etc

Summary:	PHPSysInfo displays system status 
Name:		phpsysinfo
Version:	2.5.4
Release:	%mkrel 6
Group:		System/Servers
License:	GPLv2+
URL:		http://phpsysinfo.sourceforge.net/
Source0:	http://ovh.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Patch0:		phpsysinfo-2.5.2-rc2-mdv_conf.diff
Requires:       apache-mod_php php-xml lm_sensors
Requires(post):   ccp
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING ChangeLog README
%config(noreplace) %{webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}
/var/www/%{name}
