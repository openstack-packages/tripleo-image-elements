# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:		openstack-tripleo-image-elements
Summary:	OpenStack TripleO Image Elements for diskimage-builder
Version:	0.6.5
Release:	1%{?dist}
License:	ASL 2.0
Group:		System Environment/Base
URL:		https://wiki.openstack.org/wiki/TripleO
Source0:	http://tarballs.openstack.org/tripleo-image-elements/tripleo-image-elements-%{version}.tar.gz

# https://review.openstack.org/#/c/81368/
Patch0001:	Remove-mostly-empty-directories.patch

# https://review.openstack.org/#/c/81804/
Patch0002:	Fix-tgt-target-in-cinder-element.patch

# No review for this upstream yet, but we need this to have a working horizon
# from packages install.
Patch0003:	Fix-horizon-local_settings.py.patch

# We can't run neutron-db-manage....upgrade head in reset-db from boot-stack
# due to this bug:
# https://bugs.launchpad.net/neutron/+bug/1254246
# The fix is merged: https://review.openstack.org/#/c/61663/
# However that fix is not in openstack-neutron from rdo icehouse. It will only
# be in the icehouse-3 package which is not yet available.
Patch0004:	No-neutron-db-manage-upgrade-head.patch

# https://review.openstack.org/82529
# git format-patch -1 2e37cf5ba9499ae99d86f017ecb9cf72a206a022
Patch0005:	Create-and-use-libvirtd-group-for-package-install.patch

# No service for swift-container-sync exists in rdo, temporarily patch the
# enable and restart for this service out until we figure out the right fix.
# https://review.openstack.org/#/c/82625/
Patch0006:	No-swift-continer-sync-service.patch

# openstack-cinder no longer requires scsi-target-utils, so we must install the
# package manually.
# Once upstream is refactored into cinder-tgt and cinder-lio support, we can
# just build images with the element we need:
# https://review.openstack.org/#/c/78462/
Patch0007:	cinder-install-tgt.patch

# Patch cinder.conf to set lock_path, volumes_dir, iscsi_helper.
# Needs to be submitted upstream.
Patch0008:	Cinder-conf-patch.patch

# Next 5 patches are fixes for SELinux support.
# https://review.openstack.org/#/c/82981/
Patch0009:	Update-keystone-s-selinux-policies.patch
# https://review.openstack.org/#/c/82980/
Patch0010:	Update-neutron-s-selinux-policies.patch
# https://review.openstack.org/#/c/82978/
Patch0011:	Update-glance-s-selinux-policies.patch
# https://review.openstack.org/#/c/82976/
Patch0012:	Update-nova-s-selinux-policies.patch
# https://review.openstack.org/#/c/85539/
Patch0013:	Update-swift-s-selinux-policies.patch

# https://review.openstack.org/#/c/87295/
Patch0014:	Allow-install-mariadb-from-RDO-repository.patch

BuildArch:	noarch
BuildRequires:	python
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	python-d2to1
BuildRequires:	python-pbr

Requires:	diskimage-builder

%description
OpenStack TripleO Image Elements is a collection of elements for
diskimage-builder that can be used to build OpenStack images for the TripleO
program.

%prep
%setup -q -n tripleo-image-elements-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

# remove .git-keep-empty files that get installed
find %{buildroot} -name .git-keep-empty | xargs rm -f

# These are the scripts created by our patches, but the patches don't bring +x
# along with them, so to avoid some rpmlint errors, +x them here. Once patches
# are marged upstream, these lines can be removed.
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/nova-baremetal/os-refresh-config/configure.d/82-nova-baremetal-selinux
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/keystone/os-refresh-config/configure.d/10-keystone-state
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/keystone/os-refresh-config/configure.d/20-keystone-selinux
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/neutron/os-refresh-config/configure.d/10-neutron-state
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/neutron/os-refresh-config/configure.d/20-neutron-selinux
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/glance/os-refresh-config/configure.d/10-glance-state
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/glance/os-refresh-config/configure.d/20-glance-selinux
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/nova/os-refresh-config/configure.d/20-nova-selinux
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/mariadb-rdo/install.d/10-mariadb
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/mariadb-rdo/os-refresh-config/pre-configure.d/50-mariadb-socket
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/mariadb-rdo/os-refresh-config/post-configure.d/40-mariadb
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/mariadb-dev-rdo/pre-install.d/05-mysql-mariadb-repo
chmod +x %{buildroot}/%{_datarootdir}/tripleo-image-elements/mariadb-dev-rdo/install.d/03-mariadb-dev

%files
%doc LICENSE
%doc README.md
%doc AUTHORS
%doc ChangeLog
%{python_sitelib}/tripleo_image_elements*
%{_datadir}/tripleo-image-elements

%changelog
* Mon Apr 14 2014 James Slagle <jslagle@redhat.com> - 0.6.5-1
- Bump to 0.6.5 release, update patches

* Thu Apr 10 2014 James Slagle <jslagle@redhat.com> - 0.6.3-8
- Add patch for swift SELinux policies
- Add patch for mariadb-galera installs

* Thu Apr 03 2014 James Slagle <jslagle@redhat.com> - 0.6.3-7
- Add +x to newly added files from patches

* Thu Apr 03 2014 James Slagle <jslagle@redhat.com> - 0.6.3-6
- Add patches for improved SELinux support.

* Thu Mar 27 2014 James Slagle <jslagle@redhat.com> - 0.6.3-5
- Add patch for cinder.conf

* Wed Mar 26 2014 James Slagle <jslagle@redhat.com> - 0.6.3-4
- Fix 0002-Fix-tgt-target-in-cinder-element.patch, which was misgenerated
  before

* Tue Mar 25 2014 James Slagle <jslagle@redhat.com> - 0.6.3-3
- Add additional patches for some needed workarounds.

* Sun Mar 23 2014 James Slagle <jslagle@redhat.com> - 0.6.3-2
- Add Patch 0008-Add-missing-x.patch
- Add Patch 0009-Create-and-use-libvirtd-group-for-package-install.patch

* Fri Mar 21 2014 James Slagle <jslagle@redhat.com> - 0.6.3-1
- Rebase onto 0.6.3

* Tue Mar 18 2014 James Slagle <jslagle@redhat.com> - 0.6.0-4
- Add patch 0018-Remove-mostly-empty-directories.patch

* Tue Mar 11 2014 James Slagle <jslagle@redhat.com> - 0.6.0-3
- Update based on review feedback
- Added patch 0017-Add-missing-x.patch

* Mon Feb 24 2014 James Slagle <jslagle@redhat.com> - 0.6.0-2
- Add patches for swift package support.

* Thu Feb 20 2014 James Slagle <jslagle@redhat.com> - 0.6.0-1
- Update to 0.6.0 upstream release.

* Mon Feb 17 2014 James Slagle <jslagle@redhat.com> - 0.5.1-1
- Initial rpm build.
