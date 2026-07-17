%define debug_package %{nil}

Name: mesa-nve4
Version: 26.3.0
Release: 1%{?dist}
Summary: Mesa for NVE4 (GK104) - Nouveau + NVK + Rusticl + VA-API
License: MIT
URL: https://gitlab.freedesktop.org/mesa/mesa
Source0: https://gitlab.freedesktop.org/mesa/mesa/-/archive/mesa-26.3.0/mesa-mesa-26.3.0.tar.bz2

BuildRequires: meson >= 1.7.0
BuildRequires: ninja-build
BuildRequires: gcc, gcc-c++
BuildRequires: python3-devel, python3-setuptools
BuildRequires: pkgconfig(libdrm) >= 2.4.120
BuildRequires: pkgconfig(libdrm_nouveau)
BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(x11), pkgconfig(xcb), pkgconfig(xcb-dri3)
BuildRequires: pkgconfig(wayland-client), pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-protocols) >= 1.33
BuildRequires: pkgconfig(xdamage), pkgconfig(xfixes)
BuildRequires: pkgconfig(xshmfence)
BuildRequires: pkgconfig(libelf)
BuildRequires: pkgconfig(zlib), pkgconfig(zstd)
BuildRequires: pkgconfig(libglvnd)
BuildRequires: pkgconfig(LLVM) >= 18
BuildRequires: pkgconfig(spirv-tools)
BuildRequires: pkgconfig(spirv-llvm-translator)
BuildRequires: pkgconfig(libclc)
BuildRequires: rust >= 1.82, cargo
BuildRequires: bindgen >= 0.71.1
BuildRequires: elfutils-libelf-devel

%description
Mesa for NVE4 (GK104 / Kepler) with:
- Nouveau Gallium (nvc0) for OpenGL
- NVK Vulkan driver
- Rusticl OpenCL
- VA-API video decode (MPEG-2, VC-1, H.264)

%prep
%setup -q -n mesa-mesa-26.3.0

%build
meson setup build \
  -Dgallium-drivers=nouveau \
  -Dvulkan-drivers=nouveau \
  -Dgallium-rusticl=enabled \
  -Dgallium-va=enabled \
  -Dvideo-codecs=all \
  -Dbuildtype=release \
  -Dprefix=/usr \
  -Dlibdir=%{_libdir} \
  -Dgallium-nine=false \
  -Dgallium-omx=disabled \
  -Dgallium-opencl=disabled \
  -Dgallium-vdpau=disabled \
  -Dplatforms=x11,wayland \
  -Dglx=dri \
  -Degl=enabled \
  -Dgbm=enabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled
ninja -C build -j$(nproc)

%install
DESTDIR=%{buildroot} ninja -C build install
%{_ldconfig}

%files
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/dri/nouveau_dri.so
%{_libdir}/vulkan/*.json
%{_libdir}/vulkan/lib*.so
%{_libdir}/gallium-pipe/*
%{_libdir}/libclc/*
%{_datadir}/libclc/*
%{_libdir}/libRusticlOpenCL*.so*
%{_datadir}/drirc.d/*
%{_datadir}/glvnd/*
%exclude %{_libdir}/*.a

%changelog
* Fri Jul 17 2026 Youssef <youssef@fedora> - 26.3.0-1
- Initial NVE4 Mesa build
