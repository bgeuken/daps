#
# spec file for package suse-xsl-stylesheets
#
# Copyright (c) 2011, 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
#

Name:           suse-xsl-stylesheets
Version:        1.9.20

###############################################################
# 
# ATTENTION: Do NOT edit this file outside of
#            https://svn.code.sf.net/p/daps/svn/trunk/daps/\
#            suse/packaging/suse-xsl-stylesheets.spec
#
#  Your changes will be lost on the next update
#  If you do not have access to the SVN repository, notify
#  <fsundermeyer@opensuse.org> and <toms@opensuse.org>
#  or send a patch
#
################################################################

%define dtdversion      1.0
%define dtdname         novdoc
%define regcat          %{_bindir}/sgml-register-catalog
%define dbstyles        %{_datadir}/xml/docbook/stylesheet/nwalsh/current
%define novdoc_catalog  for-catalog-%{dtdname}-%{dtdversion}.xml
%define susexsl_catalog for-catalog-%{name}.xml

Release:        1
Summary:        SUSE-branded Docbook stylesheets for XSLT 1.0
License:        GPL-2.0 or GPL-3.0
Group:          Productivity/Publishing/XML
URL:            http://sourceforge.net/p/daps/suse-xslt
Source0:        http://downloads.sourceforge.net/project/daps/suse-xsl-stylesheets/%{name}-%{version}.tar.bz2
Source1:        susexsl-fetch-source
Source2:        %{name}.rpmlintrc
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

BuildRequires:  docbook-xsl-stylesheets >= 1.77
BuildRequires:  fdupes
BuildRequires:  libxslt
BuildRequires:  make
# Only needed to fix the "have choice" error between xerces-j2 and crimson
%if 0%{?suse_version} == 1210
BuildRequires:  xerces-j2
%endif
BuildRequires:  trang

Requires:       docbook
Requires:       docbook-xsl-stylesheets >= 1.77
Requires:       libxslt

Recommends:     daps
Recommends:     docbook5
Recommends:     docbook5-xsl-stylesheets
Recommends:     google-opensans-fonts
Recommends:     sil-charis-fonts
Recommends:     dejavu-fonts

%if 0%{?sles_version}
Recommends:     ttf-founder-simplified
%else
Recommends:    wqy-microhei-fonts
%endif

Obsoletes:      susedoc <= 4.3.33
Provides:       susedoc = 4.3.34

%description
SUSE-branded DocBook stylesheets for XSLT 1.0

Extensions for the DocBook XSLT 1.0 stylesheets that provide SUSE branding 
for PDF, HTML, and ePUB. This package also provides the NovDoc DTD, a subset of
the DocBook 4 DTD.

#--------------------------------------------------------------------------
%prep
%setup -q -n %{name}

#--------------------------------------------------------------------------
%build
%__make  %{?_smp_mflags}

#--------------------------------------------------------------------------
%install
make install DESTDIR=$RPM_BUILD_ROOT

# create symlinks:
%fdupes -s $RPM_BUILD_ROOT/%{_datadir}

#----------------------
%post
# register catalogs
#
# SGML CATALOG
#
if [ -x %{regcat} ]; then
  %{regcat} -a %{_datadir}/sgml/CATALOG.%{dtdname}-%{dtdversion} >/dev/null 2>&1 || true
fi
# XML Catalogs
#
# remove existing entries first - needed for
# zypper in, since it does not call postun
# delete ...
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --del %{dtdname}-%{dtdversion}
# ... and add it again
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --add /etc/xml/%{novdoc_catalog}
# delete ...
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --del %{name}
# ... and add it again
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --add /etc/xml/%{susexsl_catalog}

exit 0

#----------------------
%postun
#
# Remove catalog entries
#
# delete catalog entries
# only run if package is really uninstalled ($1 = 0) and not
# in case of an update
#
if [ 0 = $1 ]; then 
  if [ ! -f %{_sysconfdir}/xml/%{novdoc_catalog} -a -x /usr/bin/edit-xml-catalog ] ; then
    # SGML: novdoc dtd entry
        echo "######################## deleting catalog in postun"
    %{regcat} -r %{_datadir}/sgml/CATALOG.%{dtdname}-%{dtdversion} >/dev/null 2>&1 || true
    # XML
    # novdoc dtd entry
    edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
        --del %{dtdname}-%{dtdversion}
    # susexsl entry
    edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
        --del %{name}
  fi
fi

exit 0


#----------------------
%files
%defattr(-,root,root)

# Directories
%dir %{_datadir}/xml/docbook/stylesheet/suse
%dir %{_datadir}/xml/docbook/stylesheet/suse_beta

%dir %{_datadir}/xml/%{dtdname}
%dir %{_datadir}/xml/%{dtdname}/schema
%dir %{_datadir}/xml/%{dtdname}/schema/*
%dir %{_datadir}/xml/%{dtdname}/schema/*/%{dtdversion}

%dir %{_defaultdocdir}/%{name}

# stylesheets
%{_datadir}/xml/docbook/stylesheet/suse/*
%{_datadir}/xml/docbook/stylesheet/suse_beta

# NovDoc Schemas
%{_datadir}/xml/%{dtdname}/schema/dtd/%{dtdversion}/*
%{_datadir}/xml/%{dtdname}/schema/rng/%{dtdversion}/*

# Catalogs
%config /var/lib/sgml/CATALOG.*
%{_datadir}/sgml/CATALOG.*
%config %{_sysconfdir}/xml/*.xml

# Documentation
%doc %{_defaultdocdir}/%{name}/*

#----------------------
%changelog
