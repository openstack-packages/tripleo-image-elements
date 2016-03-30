# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:		openstack-tripleo-image-elements
Summary:	OpenStack TripleO Image Elements for diskimage-builder
Version:    0.9.9
Release:    1%{?dist}
License:	ASL 2.0
Group:		System Environment/Base
URL:		https://wiki.openstack.org/wiki/TripleO
Source0:	http://tarballs.openstack.org/tripleo-image-elements/tripleo-image-elements-%{version}%{?milestone}.tar.gz

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

%post
manifest_file=/etc/dib-manifests/dib-element-manifest

if [ -f $manifest_file ]; then
    source /usr/share/diskimage-builder/lib/common-functions
    TMP_HOOKS_PATH=$(mktemp -d)
    IMAGE_ELEMENT=$(cat $manifest_file)
    ELEMENTS_PATH=/usr/share/instack-undercloud/:/usr/share/tripleo-image-elements/:/usr/share/diskimage-builder/elements/
    generate_hooks

    # os-apply-config templates
    TEMPLATE_ROOT=/usr/libexec/os-apply-config/templates
    if [ -d $TEMPLATE_ROOT ]; then
	TEMPLATE_SOURCE=$TMP_HOOKS_PATH/os-apply-config
	rsync --delete --exclude='.*.swp' -Cr $TEMPLATE_SOURCE/ $TEMPLATE_ROOT/
    fi

    # os-refresh-config scripts
    SCRIPT_BASE=/usr/libexec/os-refresh-config
    if [ -d $SCRIPT_BASE ]; then
	SCRIPT_SOURCE=$TMP_HOOKS_PATH/os-refresh-config
	rsync --delete -r $SCRIPT_SOURCE/ $SCRIPT_BASE/
    fi

    # bin files
    if [ -d /usr/local/bin ]; then
        install -m 0755 -o root -g root $TMP_HOOKS_PATH/bin/* /usr/local/bin
    fi
fi

# be sure to always exit true
true

%files
%doc LICENSE
%doc README.md
%doc AUTHORS
%doc ChangeLog
%{python_sitelib}/tripleo_image_elements*
%{_datadir}/tripleo-image-elements

%changelog
* Wed Mar 30 2016 RDO <rdo-list@redhat.com> 0.9.9-1
- RC1 Rebuild for Mitaka RC1 0.9.9
