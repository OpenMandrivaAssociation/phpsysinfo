%define rname	phpsysinfo

Summary:	PHPSysInfo displays system status 
Name:		phpSysInfo
Version:	2.5.2
Release:	%mkrel 0.rc2.2
Group:		System/Servers
License:	GPL
URL:		http://phpsysinfo.sourceforge.net/
Source0:	http://belnet.dl.sourceforge.net/sourceforge/phpsysinfo/%{rname}-%{version}-rc2.tar.bz2
Patch0:		phpsysinfo-2.5.2-rc2-mdv_conf.diff
Requires(pre):  apache-mod_php apache-mod_ssl php-xml lm_sensors
Requires:       apache-mod_php apache-mod_ssl php-xml lm_sensors
BuildRequires:	perl
BuildRequires:	ImageMagick
BuildRequires:	apache-base >= 2.0.54
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
PHPSysInfo is a customizable PHP Script that parses /proc, and
formats information nicely. It will display information about
system facts like Uptime, CPU, Memory, PCI devices, SCSI devices,
IDE devices, Network adapters, Disk usage, and more.

Included is also a new lm_sensors module that will present
voltage, temperature, fan speed, etc. if the appropriate
lm_sensors modules are loaded.

%prep

%setup -q -n %{rname}
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

<LocationMatch /%{name}>
    Options FollowSymLinks
    RewriteEngine on
    RewriteCond %{SERVER_PORT} !^443$
    RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
</LocationMatch>

EOF

# install script to call the web interface from the menu.
install -d %{buildroot}%{_libdir}/%{name}/scripts
cat > %{buildroot}%{_libdir}/%{name}/scripts/%{name} <<EOF
#!/bin/sh

url='https://localhost/%{name}'
if ! [ -z "\$BROWSER" ] && ( which \$BROWSER ); then
  browser=\`which \$BROWSER\`
elif [ -x /usr/bin/mozilla-firefox ]; then
  browser=/usr/bin/mozilla-firefox
elif [ -x /usr/bin/konqueror ]; then
  browser=/usr/bin/konqueror
elif [ -x /usr/bin/lynx ]; then
  browser='xterm -bg black -fg white -e lynx'
elif [ -x /usr/bin/links ]; then
  browser='xterm -bg black -fg white -e links'
else
  xmessage "No web browser found, install one or set the BROWSER environment variable!"
  exit 1
fi
\$browser \$url
EOF
chmod 755 %{buildroot}%{_libdir}/%{name}/scripts/%{name}

# Mandriva Icons
#install -d %{buildroot}%{_iconsdir}
#install -d %{buildroot}%{_miconsdir}
#install -d %{buildroot}%{_liconsdir}

#convert themes/original/img/logo_right.png -resize 16x16  %{buildroot}%{_miconsdir}/%{name}.png
#convert themes/original/img/logo_right.png -resize 32x32  %{buildroot}%{_iconsdir}/%{name}.png
#convert themes/original/img/logo_right.png -resize 48x48  %{buildroot}%{_liconsdir}/%{name}.png

# XDG menu entry
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=phpSysInfo
Comment=PHPSysInfo displays system status.  Set the $BROWSER environment variable to choose your preferred browser
Exec=%{_libdir}/%{name}/scripts/%{name} 1>/dev/null 2>/dev/null 
Icon=administration.png
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-System-Monitoring;System;Monitor;
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
%attr(0755,root,root) %{_libdir}/%{name}/scripts/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop 
#%{_iconsdir}/%{name}.png
#%{_miconsdir}/%{name}.png
#%{_liconsdir}/%{name}.png


