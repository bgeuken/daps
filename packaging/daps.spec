#
# spec file for package daps
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
#
###############################################################
# 
# ATTENTION: Do NOT edit this file outside of
#            https://svn.code.sf.net/p/daps/svn/trunk/daps/packaging/daps.spec
#
#  Your changes will be lost on the next update
#  If you do not have access to the SVN repository, notify
#  <fsundermeyer@opensuse.org> and <toms@opensuse.org>
#  or send a patch
#
################################################################
#
# Please submit bugfixes or comments via https://sourceforge.net/p/daps/tickets
#
Name:           daps
Version:        1.0.2.1
Release:        0

%define docbuilddir    %{_datadir}/daps
%define regcat         %{_bindir}/sgml-register-catalog
%define fontdir        %{_datadir}/fonts/truetype
%define dbstyles       %{_datadir}/xml/docbook/stylesheet/nwalsh/current
%define daps_catalog   for-catalog-%{name}.xml

Summary:        DocBook Authoring and Publishing Suite
License:        GPL-2.0 or GPL-3.0
Group:          Productivity/Publishing/XML
Url:            http://sourceforge.net/p/daps
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}.rpmlintrc
Source2:        %{name}-fetch-source
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

BuildRequires:  bash >= 4.0
BuildRequires:  dia
BuildRequires:  docbook-xsl-stylesheets >= 1.75
BuildRequires:  docbook_4
%if 0%{?suse_version} > 1140
BuildRequires:  perl-Image-ExifTool
%else
BuildRequires:  exiftool
%endif
%if 0%{?suse_version} >= 1220
BuildRequires:  libxml2-tools
%endif
BuildRequires:  fam
BuildRequires:  fdupes
BuildRequires:  ImageMagick
BuildRequires:  inkscape
BuildRequires:  libxslt
BuildRequires:  openSUSE-release
BuildRequires:  optipng
BuildRequires:  python-xml
BuildRequires:  sgml-skel
BuildRequires:  suse-xsl-stylesheets
BuildRequires:  svg-dtd
BuildRequires:  transfig

# the following requirements are not really needed for building, but we add
# them nevertheless in order to see if the build target is able to fullfill
# the requirements for installation
BuildRequires:  dejavu
BuildRequires:  freefont
BuildRequires:  ghostscript-library
BuildRequires:  liberation-fonts
BuildRequires:  LinuxLibertine
BuildRequires:  mplus-fonts
BuildRequires:  poppler-tools
BuildRequires:  xmlformat

%if 0%{?suse_version} >= 1140
BuildRequires:  perl-checkbot
BuildRequires:  xmlgraphics-fop >= 0.94
%else
BuildRequires:  fop >= 0.94
%if %{undefined sles_version}
BuildRequires:  checkbot
%endif
%endif

PreReq:         libxml2
PreReq:         sgml-skel

Requires:       bash >= 4.0
Requires:       dejavu
Requires:       dia
Requires:       docbook_4
Requires:       docbook-xsl-stylesheets >= 1.75
Requires:       exiftool
Requires:       fam
Requires:       freefont
Requires:       ghostscript-library
Requires:       ImageMagick
Requires:       inkscape
Requires:       libxslt
Requires:       liberation-fonts
Requires:       LinuxLibertine
Requires:       make
Requires:       mplus-fonts
Requires:       optipng
Requires:       poppler-tools
Requires:       sgml-skel
Requires:       svg-dtd
Requires:       transfig
%if 0%{?suse_version} >= 1140
Requires:       perl-checkbot
Requires:       xmlgraphics-fop >= 0.94
%else
Requires:       fop >= 0.94
%if %{undefined sles_version}
Requires:       checkbot
%else
Recommends:     checkbot
%endif
%endif
Requires:       python-xml

Recommends:     agfa-fonts
Recommends:     aspell aspell-en
# Only works only for openSUSE 11.4 and below
%if 0%{?suse_version} < 1210
Recommends:     aspell-en-huge
%endif
Recommends:     daps-docmanager
Recommends:     docbook_5
Recommends:     emacs psgml
Recommends:     epubcheck
# Split of ttf-founder-simplified and ttf-founder-traditional
Recommends:     FZFangSong FZHeiTi FZSongTi
Recommends:     fifth-leg-font
Recommends:     jing
Recommends:     remake
# needed to create ePUBs
Recommends:     ruby
# Japanese Fonts:
Recommends:     sazanami-fonts
Recommends:     suse-xsl-stylesheets
# Chinese
Recommends:     ttf-arphic
# Korean Fonts:
Recommends:     unfonts
# Internal XEP package:
Recommends:     xep

#Obsoletes:      susedoc <= 4.3.27
Provides:       susedoc < 4.4

%description
DocBook Authoring and Publishing Suite (DAPS)

DAPS contains a set of stylesheets, scripts and makefiles that enable
you to create HTML, PDF, EPUB and other formats from DocBook XML with a
single command. It also contains tools to generate profiled source
tarballs for distributing your XML sources for translation or review.

DAPS also includes tools that assist you when writing DocBook XML:
linkchecker, validator, spellchecker, editor macros and stylesheets for
converting DocBook XML.

DAPS is the successor of susedoc. See
/usr/share/doc/packages/daps/README.upgrade_from_susedoc_4.x
for upgrade instructions.


#--------------------------------------------------------------------------
%prep
%setup -q -n %{name}
#%%patch1 -p1

#--------------------------------------------------------------------------
%build
%configure --docdir=%{_defaultdocdir}/%{name} --disable-edit-rootcatalog
%__make  %{?_smp_mflags}

#--------------------------------------------------------------------------
%install
make install DESTDIR=$RPM_BUILD_ROOT

# create symlinks:
%fdupes -s $RPM_BUILD_ROOT/%{_datadir}

#----------------------
%post
#
# XML Catalog entries for daps profiling
#
# remove existing entries first (if existing) - needed for
# zypper in, since it does not call postun
#
# delete ...
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --del %{name}
# ... and add it again
edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --add /etc/xml/%{daps_catalog}

%run_suseconfig_fonts
exit 0

#----------------------
%postun
#
# delete catalog entry for daps profiling
# only run if package is really uninstalled ($1 = 0) and not
# in case of an update
#
if [ 0 = $1 ]; then 
if [ -x /usr/bin/edit-xml-catalog ] ; then
  edit-xml-catalog --group --catalog /etc/xml/suse-catalog.xml \
  --del %{name}
fi

%run_suseconfig_fonts
fi
exit 0

#----------------------
%files
%defattr(-,root,root)

%dir %{fontdir}
%dir %{_sysconfdir}/%{name}
%dir %{_defaultdocdir}/%{name}

%config %{_sysconfdir}/xml/*.xml
%config %{_sysconfdir}/%{name}/*

%doc %{_mandir}/man1/*.1%{ext_man}
%doc %{_defaultdocdir}/%{name}/*

%{_bindir}/*
%{_datadir}/emacs/site-lisp/docbook_macros.el
%{fontdir}/*
%{docbuilddir}

%exclude %{_defaultdocdir}/%{name}/INSTALL

#----------------------

%changelog
