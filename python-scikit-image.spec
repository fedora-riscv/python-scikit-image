%global with_python3 1
%global srcname scikit-image

Name: python-scikit-image
Version: 0.12.3
Release: 3%{?dist}
Summary: Image processing in Python
# The following files are BSD 2 clauses, the rest BSD 3 clauses
# skimage/graph/_mcp.pyx
# skimage/graph/heap.pyx
License: BSD

URL: http://scikit-image.org/
Source0: https://pypi.python.org/packages/source/s/scikit-image/scikit-image-%{version}.tar.gz
BuildRequires: python2-devel python-setuptools numpy Cython
BuildRequires: scipy python-matplotlib python-nose
BuildRequires: python-six >= 1.3
BuildRequires: python-networkx-core
BuildRequires: python-pillow
BuildRequires: xorg-x11-server-Xvfb
Requires: scipy 
Requires: python-six >= 1.3
Requires: python-networkx-core
Requires: python-pillow

Provides: python2-scikit-image = %{version}-%{release}

%description
The scikit-image SciKit (toolkit for SciPy) extends scipy.ndimage to provide a 
versatile set of image processing routines.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary: Image processing in Python
BuildRequires: python3-devel python3-setuptools python3-numpy python3-Cython
BuildRequires: python3-scipy python3-matplotlib python3-nose
BuildRequires: python3-six >= 1.3
BuildRequires: python3-networkx-core
BuildRequires: python3-pillow
Requires: python3-scipy
Requires: python3-six >= 1.3
Requires: python3-networkx-core
Requires: python3-pillow

%description -n python3-%{srcname}
The scikit-image SciKit (toolkit for SciPy) extends scipy.ndimage to provide a 
versatile set of image processing routines.

%endif # with_python3

%package -n %{srcname}-tools
Summary: Scikit-image utility tools
BuildArch: noarch
%if 0%{?with_python3}
Requires: python3-%{srcname} = %{version}-%{release}
%else
Requires: python2-%{srcname} = %{version}-%{release}
%endif # with_python3

%description -n %{srcname}-tools
Utilities provided by scikit-image: 'skivi'

%prep
%setup -n %{srcname}-%{version} -q
# Remove some shebangs
pushd skimage
for i in $(grep -l -r "/usr/bin/env"); do
   sed -i -e '1d' $i;
done
popd

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

%build
CFLAGS="%{optflags}" %{__python2} setup.py build
# Requires plot2rst
#%{__python2} setup.py build_sphinx

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif # with_python3

%install

%{__python2} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

find %{buildroot} -name "*.so" | xargs chmod 755

# Checks are not working at the moment
%check
# Fake matplotlibrc
mkdir -p matplotlib
touch matplotlib/matplotlibrc
export XDG_CONFIG_HOME=`pwd`
pushd %{buildroot}/%{python2_sitearch}
xvfb-run nosetests-%{python2_version} skimage || :
popd

%if 0%{?with_python3}
# Fake matplotlibrc
mkdir -p matplotlib
touch matplotlib/matplotlibrc
export XDG_CONFIG_HOME=`pwd`
pushd %{buildroot}/%{python3_sitearch}
xvfb-run nosetests-%{python3_version} skimage || :
popd
%endif # with_python3
 
%files
%doc CONTRIBUTORS.txt DEPENDS.txt RELEASE.txt TASKS.txt
%license LICENSE.txt
%{python2_sitearch}/skimage
%{python2_sitearch}/scikit_image-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc CONTRIBUTORS.txt DEPENDS.txt RELEASE.txt TASKS.txt
%license LICENSE.txt
%{python3_sitearch}/skimage
%{python3_sitearch}/scikit_image-*.egg-info
%endif # with_python3

%files -n %{srcname}-tools
%{_bindir}/skivi

%changelog
* Wed Apr 6 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.3-3
- Run tests, but do not abort build on failure

* Tue Mar 29 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.12.3-2
- New upstream source
- Disable tests for the moment

* Fri Feb 19 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.3-8
- skivi uses python3 (bz #1309240)
- Provides "versioned" python2-scikit-image

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.3-6
- Tarball without problematic copyrigth images (fixes bz #1295193)

* Mon Nov 23 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.3-5
- Provides python2-scikit-image

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.3-2
- Disable tests
- New upstream version (0.11.3)

* Thu Mar 12 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.2-1
- New upstream version (0.11.2)

* Wed Feb 04 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.0-1
- New upstream version

* Tue Jul 29 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.10.1-2
- Remove __provides_exclude_from, is not needed in f20+

* Wed Jul 09 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.10.1-1
- New upstream 0.10.1

* Thu Apr 18 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.9.3-1
- Initial spec file

