%global with_python3 1
%global upname scikit-image

Name: python-scikit-image
Version: 0.10.1
Release: 2%{?dist}
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
Requires: scipy 
Requires: python-six >= 1.3

%description
The scikit-image SciKit (toolkit for SciPy) extends scipy.ndimage to provide a 
versatile set of image processing routines.

%if 0%{?with_python3}
%package -n python3-%{upname}
Summary: Image processing in Python
BuildRequires: python3-devel python3-setuptools python3-numpy python3-Cython
BuildRequires: python3-scipy python3-matplotlib python3-nose
BuildRequires: python3-six >= 1.3
Requires: python3-scipy
Requires: python3-six >= 1.3

%description -n python3-%{upname}
The scikit-image SciKit (toolkit for SciPy) extends scipy.ndimage to provide a 
versatile set of image processing routines.

%endif # with_python3

%package -n %{upname}-tools
Summary: Scikit-image utility tools
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description -n %{upname}-tools
Utilities provided by scikit-image: 'skivi'

%prep
%setup -n %{upname}-%{version} -q
# Remove some shebangs
pushd skimage
for i in $(grep -l -r "/usr/bin/env"); do
   sed -i -e '1d' $i;
done
popd

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

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
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install --skip-build --root  %{buildroot}

find %{buildroot} -name "*.so" | xargs chmod 755

# Checks are not working at the moment
#%check
#pushd %{buildroot}/%{python2_sitearch}
#nosetests-%{python2_version} skimage
#popd

#%if 0%{?with_python3}
#pushd %{buildroot}/%{python3_sitearch}
#nosetests-%{python3_version} skimage
#popd
#%endif # with_python3
 
%files
%doc CONTRIBUTORS.txt DEPENDS.txt LICENSE.txt RELEASE.txt TASKS.txt
%{python2_sitearch}/skimage
%{python2_sitearch}/scikit_image-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{upname}
%doc CONTRIBUTORS.txt DEPENDS.txt LICENSE.txt RELEASE.txt TASKS.txt
%{python3_sitearch}/skimage
%{python3_sitearch}/scikit_image-*.egg-info
%endif # with_python3

%files -n %{upname}-tools
%{_bindir}/skivi

%changelog
* Tue Jul 29 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.10.1-2
- Remove __provides_exclude_from, is not needed in f20+

* Wed Jul 09 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.10.1-1
- New upstream 0.10.1

* Thu Apr 18 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.9.3-1
- Initial spec file

