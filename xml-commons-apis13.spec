Name:		xml-commons-apis13
Version:	1.3.05
Epoch:		1
Release:	2
Summary:	APIs for DOM, SAX, and JAXP
Group:		Development/Java
License:	ASL 2.0 and W3C and Public Domain
URL:		http://xml.apache.org/commons/

# From source control because the published tarball doesn't include some docs:
#   svn export http://svn.apache.org/repos/asf/xml/commons/tags/xml-commons-external-1_3_05/java/external/
#   tar czf xml-commons-external-1.3.05-src.tar.gz external
Source0:	xml-commons-external-%{version}-src.tar.xz
Source1:	%{name}-MANIFEST.MF
Source2:	%{name}-ext-MANIFEST.MF
Source3:	http://repo1.maven.org/maven2/xml-apis/xml-apis/2.0.2/xml-apis-2.0.2.pom
Source4:	http://repo1.maven.org/maven2/xml-apis/xml-apis-ext/1.3.04/xml-apis-ext-1.3.04.pom

BuildArch:	noarch

BuildRequires:	java-devel >= 0:1.6.0
BuildRequires:	jpackage-utils
BuildRequires:	ant
BuildRequires:	zip
Requires:	java
Requires:	jpackage-utils
Requires(post):	jpackage-utils
Requires(postun):	jpackage-utils

Obsoletes:	xml-commons-jaxp-1.3-apis < %EVRD
Provides:	xml-commons-jaxp-1.3-apis = %EVRD

%description
xml-commons-apis is designed to organize and have common packaging for
the various externally-defined standard interfaces for XML. This
includes the DOM, SAX, and JAXP. 

%package manual
Summary:	Manual for %{name}
Group:		Development/Java
Obsoletes:	xml-commons-jaxp-1.3-apis-manual < %EVRD
Provides:	xml-commons-jaxp-1.3-apis-manual = %EVRD

%description manual
%{summary}.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
Obsoletes:	xml-commons-jaxp-1.3-apis-javadoc < %EVRD
Provides:	xml-commons-jaxp-1.3-apis-javadoc = %EVRD

%description javadoc
%{summary}.

%prep
%setup -q -n xml-commons-external-%(echo %version |sed -e 's,\.,_,g')/java/external

# Make sure upstream hasn't sneaked in any jars we don't know about
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# Fix file encodings
iconv -f iso8859-1 -t utf-8 LICENSE.dom-documentation.txt > \
  LICENSE.dom-doc.temp && mv -f LICENSE.dom-doc.temp LICENSE.dom-documentation.txt
iconv -f iso8859-1 -t utf-8 LICENSE.dom-software.txt > \
  LICENSE.dom-sof.temp && mv -f LICENSE.dom-sof.temp LICENSE.dom-software.txt

# remove bogus section from poms
cp %{SOURCE3} %{SOURCE4} .
sed -i '/distributionManagement/,/\/distributionManagement/ {d}' *.pom

%build
ant -Dant.build.javac.source=1.5 -Dant.build.javac.target=1.5 jar javadoc

%install

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/xml-apis.jar META-INF/MANIFEST.MF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/xml-apis-ext.jar META-INF/MANIFEST.MF

# Jars
install -pD -T build/xml-apis.jar %{buildroot}%{_javadir}/%{name}.jar
install -pDm 644 xml-apis-[0-9]*.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom
%add_to_maven_depmap xml-apis xml-apis %{version} JPP %{name}
%add_maven_depmap -a xerces:dom3-xml-apis

install -pD -T build/xml-apis-ext.jar %{buildroot}%{_javadir}/%{name}-ext.jar
install -pDm 644 xml-apis-ext*.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}-ext.pom
%add_to_maven_depmap xml-apis xml-apis-ext %{version} JPP %{name}-ext

# for better interoperability with the jpp apis packages
ln -sf %{name}.jar %{buildroot}%{_javadir}/jaxp13.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/xml-commons-jaxp-1.3-apis.jar

# Javadocs
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/docs/javadoc/* %{buildroot}%{_javadocdir}/%{name}
 
# prevent apis javadoc from being included in doc
rm -rf build/docs/javadoc

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc LICENSE NOTICE 
%doc LICENSE.dom-documentation.txt README.dom.txt
%doc LICENSE.dom-software.txt LICENSE.sac.html
%doc LICENSE.sax.txt README-sax  README.sax.txt
%{_javadir}/*
%{_mavendepmapfragdir}/%{name}
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavenpomdir}/JPP-%{name}-ext.pom

%files manual
%doc build/docs/*

%files javadoc
%{_javadocdir}/*
