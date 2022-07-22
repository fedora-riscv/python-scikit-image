%bcond_with check

%global srcname scikit-image

Name: python-scikit-image
Version: 0.19.2
Release: 3%{?dist}
Summary: Image processing in Python
# The following files are BSD 2 clauses, the rest BSD 3 clauses
# skimage/graph/_mcp.pyx
# skimage/graph/heap.pyx
License: BSD

URL: http://scikit-image.org/
Source0: %{pypi_source}

BuildRequires: gcc gcc-c++
BuildRequires: xorg-x11-server-Xvfb

%global _description %{expand:
The scikit-image SciKit (toolkit for SciPy) extends scipy.ndimage to provide a
versatile set of image processing routines.}

%description %_description

%package -n python3-%{srcname}
Summary: %{summary}
BuildRequires: python3-devel
BuildRequires: %{py3_dist setuptools}
BuildRequires: %{py3_dist Cython}
BuildRequires: %{py3_dist numpy}
BuildRequires: pythran
%if %{with check}
BuildRequires: %{py3_dist pytest}
BuildRequires: %{py3_dist scipy}
BuildRequires: %{py3_dist matplotlib}
BuildRequires: %{py3_dist networkx}
BuildRequires: %{py3_dist pillow}
BuildRequires: %{py3_dist imageio}
BuildRequires: %{py3_dist tifffile}
BuildRequires: %{py3_dist PyWavelets}
# Not in fedora:
# pytest-localserver
# Pooch
%endif

%description -n python3-%{srcname} %_description

%package -n %{srcname}-tools
Summary: Scikit-image utility tools
BuildArch: noarch
Requires: python3-%{srcname} = %{version}-%{release}

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
rm -f $(grep -rl '/\* Generated by Cython')

%build
%py3_build

%install
%py3_install
# This is also installed
rm -rf %{buildroot}/%{python3_sitearch}/doc/

%if %{with check}
%check
# Fake matplotlibrc
mkdir -p matplotlib
touch matplotlib/matplotlibrc
export XDG_CONFIG_HOME=`pwd`
export PYTHONDONTWRITEBYTECODE=1
export PYTEST_ADDOPTS='-p no:cacheprovider'
pushd %{buildroot}/%{python3_sitearch}
# We deselect tests that require network
# or packages not in Fedora
# require Pooch 
# require pytest-localserver
 xvfb-run pytest \
  --deselect="data/tests/test_data.py::test_skin"  \
  --deselect "io/tests/test_collection.py::TestImageCollection::test_custom_load_func_w_kwarg" \
  --deselect "restoration/tests/test_rolling_ball.py::test_ndim" \
  --deselect="io/tests/test_io.py::test_imread_http_url"  \
 skimage
popd
%endif

%files -n python3-%{srcname}
%doc CONTRIBUTORS.txt RELEASE.txt
%license LICENSE.txt
%{python3_sitearch}/skimage
%{python3_sitearch}/scikit_image-*.egg-info

%files -n %{srcname}-tools
%{_bindir}/skivi


%changelog
* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Python Maint <python-maint@redhat.com> - 0.19.2-2
- Rebuilt for Python 3.11

* Wed Feb 23 2022 Sergio Pascual <sergiopr@fedoraproject.org> - 0.19.2-1
- New upstream version (0.19.2)
- New BuildReq: pythran

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 07 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.18.3-1
- New upstream version (0.18.3)

* Mon Aug 23 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.18.2-1
- New upstream version (0.18.2)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.18.1-4
- Rebuilt for Python 3.10

* Thu Feb 11 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.18.1-3
- Update testing
- Start using automatic requires

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.18.1-1
- New upstream version (0.18.1)

* Thu Dec 17 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.18.0-1
- New upstream version (0.18.0)

* Thu Aug 27 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.17.2-1
- New upstream version (0.17.2)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.16.2-4
- Rebuilt for Python 3.9

* Thu Feb 13 2020 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.16.2-3
- Update dep on python3-networkx (no longer provides python3-networkx-core in F32+)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 22 2019 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.16.2-1
- Update to 0.16.2 (#1763989)
+
* Tue Oct 15 2019 Orion Poplawski <orion@nwra.com> - 0.16.1-1
- Update to 0.16.1
- Re-generate Cython source

* Thu Sep  5 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.15.0-1
- Rebuilt with fixed python-pywt

* Sat Aug 31 2019 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.0-1
- New upstream version (0.15.0)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May  5 2019 Orion Poplawski <orion@nwra.com> - 0.14.2-1
- Update to 0.14.2 to fix numpy 1.16 compatibility (bugz#1706125)
- Add requires on dask and maplotlib-qt5 (bugz#1691823)

* Mon Mar 04 2019 Christian Dersch <lupinix@mailbox.org> - 0.14.0-7
- Disable automatic dependency generators until we fixed (optional) deps

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14.0-5
- Remove Python 2 subpackage

* Tue Jul 17 2018 Christian Dersch <lupinix@fedoraproject.org> - 0.14.0-4
- BuildRequires: gcc

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14.0-2
- Rebuilt for Python 3.7

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

