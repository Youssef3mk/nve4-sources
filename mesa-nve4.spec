%global debug_package %{nil}

Name: mesa-nve4
Version: 26.3.0
Release: 1%{?dist}
Summary: Mesa 3D with NVE4 (GK104) optimizations - Nouveau + NVK + Rusticl + VA-API
License: MIT
URL: https://www.mesa3d.org/
Source0: mesa-26.3.0.tar.xz

BuildRequires: meson >= 1.7.0
BuildRequires: ninja-build
BuildRequires: gcc, gcc-c++
BuildRequires: python3-devel, python3-setuptools
BuildRequires: pkgconfig(libdrm) >= 2.4.120
BuildRequires: pkgconfig(libdrm_nouveau)
BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(x11), pkgconfig(xcb), pkgconfig(xorg-server)
BuildRequires: pkgconfig(wayland-client), pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-protocols) >= 1.33
BuildRequires: pkgconfig(xdamage), pkgconfig(xfixes), pkgconfig(xcb-dri3)
BuildRequires: pkgconfig(xcb-present), pkgconfig(xcb-sync)
BuildRequires: pkgconfig(xshmfence)
BuildRequires: pkgconfig(libelf)
BuildRequires: pkgconfig(zlib), pkgconfig(zstd)
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(libglvnd)
BuildRequires: pkgconfig(LLVM) >= 18
BuildRequires: pkgconfig(spirv-tools)
BuildRequires: pkgconfig(spirv-llvm-translator)
BuildRequires: pkgconfig(libclc)
BuildRequires: pkgconfig(SPIRV-Tools)
BuildRequires: rust >= 1.82
BuildRequires: cargo
BuildRequires: bindgen >= 0.71.1
BuildRequires: elfutils-libelf-devel

%if 0%{?fedora} >= 40
BuildRequires: rust-std-static
%endif

Provides: mesa(%{version}-%{release})
Provides: mesa-nve4 = %{version}-%{release}
Provides: mesa-libgallium-nouveau
Provides: mesa-vulkan-drivers-nouveau
Provides: mesa-rusticl-nouveau
Provides: mesa-va-drivers-nouveau

%description
Mesa 3D Graphics Library built for NVE4 (GK104 / Kepler) with:
- Nouveau Gallium driver (nvc0) for OpenGL
- NVK Vulkan driver 
- Rusticl OpenCL driver
- VA-API video acceleration
- ALL video codecs enabled (MPEG-2, VC-1, H.264)

%prep
%setup -q -n mesa-26.3.0

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
%{_libdir}/lib*.so
%{_libdir}/dri/nouveau_vieux_dri.so
%{_libdir}/dri/nouveau_dri.so
%{_libdir}/libGL.so.*
%{_libdir}/libEGL.so.*
%{_libdir}/libGLESv*.so.*
%{_libdir}/libgbm.so.*
%{_libdir}/libglapi.so.*
%{_libdir}/libxatracker.so.*
%{_libdir}/pkgconfig/*
%{_libdir}/vulkan/*.json
%{_libdir}/vulkan/lib*.so
%{_libdir}/gallium-pipe/*
%{_datadir}/drirc.d/*
%{_datadir}/glvnd/*
%{_libdir}/libclc/*
%{_datadir}/libclc/*
%{_libdir}/libRusticlOpenCL*.so*
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la

%changelog
* Fri Jul 17 2026 Youssef <youssef@fedora> - 26.3.0-1
- Initial NVE4 Mesa build with Nouveau + NVK + Rusticl + VA-API
