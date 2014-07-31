# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Name:		openstack-tripleo-image-elements
Summary:	OpenStack TripleO Image Elements for diskimage-builder
Version:	0.6.5
Release:	7%{?dist}
License:	ASL 2.0
Group:		System Environment/Base
URL:		https://wiki.openstack.org/wiki/TripleO
Source0:	http://tarballs.openstack.org/tripleo-image-elements/tripleo-image-elements-%{version}.tar.gz

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
%setup -q -n tripleo-image-elements-%{upstream_version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

# remove .git-keep-empty files that get installed
find %{buildroot} -name .git-keep-empty | xargs rm -f

%files
%doc LICENSE
%doc README.md
%doc AUTHORS
%doc ChangeLog
%{python_sitelib}/tripleo_image_elements*
%{_datadir}/tripleo-image-elements

%changelog
* Tue Jul 1 2014 James Slagle <jslagle@redhat.com> - 0.6.5-7
- Bump release

* Tue Jul 1 2014 James Slagle <jslagle@redhat.com> - 0.6.5-6
- Add patch Move-rabbitmq-server-cluster-port.patch

* Thu Jun 26 2014 James Slagle <jslagle@redhat.com> - 0.6.5-5
- Add 3 new SELinux patches

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 James Slagle <jslagle@redhat.com> - 0.6.5-3
- Update patch Allow-install-mariadb-from-RDO-repository.patch
  since mariadb-galera-devel is no longer available, it's just plain
  mariadb-devel
- Make files from swift selinux patch +x

* Wed Apr 23 2014 James Slagle <jslagle@redhat.com> - 0.6.5-2
- Add patch Make-innodb-pool-size-configurable.patch

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
