%define	module	mimp

Name:		horde-%{module}
Version:	1.1.4
Release:	5
Summary:	The Horde Mobile Internet Messaging Program
License:	GPL
Group:		System/Servers
URL:		https://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org:21/pub/mimp/mimp-h3-%{version}.tar.gz
Requires(post):	rpm-helper
Requires:	horde >= 3.0
Requires:	php-imap
Requires:	php-ldap
BuildArch:	noarch

%description
MIMP is the Mobile IMP, one of the Horde applications.
It provides webmail access to IMAP and POP3 accounts via
a cut down UI suitable for mobile phones and PDAs

%prep
%setup -q -n %{module}-h3-%{version}

%build

%install
# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Require all denied
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Require all denied
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Mimp Horde configuration file
//
 
$this->applications['mimp'] = array(
    'fileroot' => $this->applications['horde']['fileroot'] . '/mimp',
    'webroot'  => $this->applications['horde']['webroot'] . '/mimp',
    'name'     => _("Mobile Mail"),
    'status'   => 'notoolbar'
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

# fix script shellbang
for file in `find %{buildroot}%{_datadir}/horde/%{module}/scripts`; do
	perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|' $file
done

%clean

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi


%files
%doc README COPYING docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}


%changelog
* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 1.1.3-3mdv2011.0
+ Revision: 565270
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.3-2mdv2010.1
+ Revision: 493349
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Sat Dec 26 2009 Funda Wang <fwang@mandriva.org> 1.1.3-1mdv2010.1
+ Revision: 482414
- new version 1.1.3

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - restrict default access permissions to localhost only, as per new policy

* Wed Sep 16 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.2-1mdv2010.0
+ Revision: 443652
- new version
- new files setup

* Wed Aug 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.1-3mdv2010.0
+ Revision: 418310
- fix registry file (fix #52696)

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.1-2mdv2009.1
+ Revision: 295318
- cosmetics

* Sun Oct 19 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.1-1mdv2009.1
+ Revision: 295295
- update to new version 1.1.1

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.1-2mdv2009.0
+ Revision: 267076
- rebuild early 2009.0 package (before pixel changes)

* Fri May 30 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1-1mdv2009.0
+ Revision: 213378
- new version

  + Colin Guthrie <cguthrie@mandriva.org>
    - Better defaults as used in horde registry.

* Fri Mar 07 2008 Colin Guthrie <cguthrie@mandriva.org> 1.0.2-1mdv2008.1
+ Revision: 181171
- import horde-mimp



