%if 0%{?fedora}
%global with_python3 1
%else
%global with_python3 0
%endif
%global srcname scikit-image

Name: python-scikit-image
Version: 0.14.0
Release: 1%{?dist}
Summary: Image processing in Python
# The following files are BSD 2 clauses, the rest BSD 3 clauses
# skimage/graph/_mcp.pyx
# skimage/graph/heap.pyx
License: BSD

URL: http://scikit-image.org/
Source0: https://pypi.python.org/packages/source/s/scikit-image/scikit-image-%{version}.tar.gz


BuildRequires: xorg-x11-server-Xvfb

%description
The scikit-image SciKit (toolkit for SciPy) extends scipy.ndimage to provide a 
versatile set of image processing routines.

%package -n python2-%{srcname}
Summary: Image processing in Python 2
BuildRequires: python2-devel python2-setuptools python2-numpy
BuildRequires: python2-scipy python2-matplotlib python2-nose
%if 0%{?rhel}
BuildRequires: python-matplotlib-qt4
%endif
BuildRequires: python2-six >= 1.3
BuildRequires: python2-networkx-core
BuildRequires: python2-pillow
BuildRequires: python2-pywt python-Cython
Requires: python2-scipy 
Requires: python2-six >= 1.3
Requires: python2-networkx-core
Requires: python2-pillow
Requires: python2-pywt >= 0.4.0
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
The scikit-image SciKit (toolkit for SciPy) extends scipy.ndimage to provide a 
versatile set of image processing routines.

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary: Image processing in Python 3
BuildRequires: python3-devel python3-setuptools python3-numpy
BuildRequires: python3-scipy python3-matplotlib python3-nose
BuildRequires: python3-six >= 1.3
BuildRequires: python3-networkx-core
BuildRequires: python3-pillow
BuildRequires: python3-pywt python3-Cython
Requires: python3-scipy
Requires: python3-six >= 1.3
Requires: python3-networkx-core
Requires: python3-pillow
Requires: python3-pywt >= 0.4.0
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

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
#%patch0 -p1 -b .Cython
# Remove some shebangs
pushd skimage
for i in $(grep -l -r "/usr/bin/env"); do
   sed -i -e '1d' $i;
done
popd

%build
%py2_build
# Requires plot2rst
#%{__python2} setup.py build_sphinx

%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
%py2_install

%if 0%{?with_python3}
%py3_install
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
 
%files -n python2-%{srcname}
%doc CONTRIBUTORS.txt RELEASE.txt
%license LICENSE.txt
%{python2_sitearch}/skimage
%{python2_sitearch}/scikit_image-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{srcname}
%doc CONTRIBUTORS.txt RELEASE.txt
%license LICENSE.txt
%{python3_sitearch}/skimage
%{python3_sitearch}/scikit_image-*.egg-info
%endif # with_python3

%files -n %{srcname}-tools
%{_bindir}/skivi

%changelog
* Mon Jun 11 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.14.0-1
- New upstream version (0.14.0)

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.0-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Sergio Pascual <sergiopr@fedoraproject.org> - 0.13.0-2
- Add dependency on pywt (PyWavelets)

* Mon May 15 2017 Sergio Pascual <sergiopr@fedoraproject.org> - 0.13.0-1
- New upstream version (0.13.0)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.12.3-6
- Rebuild for Python 3.6

* Tue Aug 16 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.3-5
- Remove Cython build requirement
- Only build python3 for Fedora

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 6 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.3-3
- Run tests, but do not abort build on failure
- Drop py3dir, use new python macros

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

