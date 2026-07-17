%global debug_package %{nil}

%global with_nvk 1
%global with_va 1
%global with_opencl 1

Name: mesa-nve4
Version: 26.3.1
Release: 0.1.nve4%{?dist}
Summary: Mesa for NVE4 (GK104) with Nouveau + NVK + Rusticl + VA-API
License: MIT AND BSD-3-Clause AND SGI-B-2.0
URL: http://www.mesa3d.org
Source0: https://gitlab.freedesktop.org/mesa/mesa/-/archive/mesa-26.3.1/mesa-mesa-26.3.1.tar.bz2

BuildRequires: meson >= 1.7.0
BuildRequires: gcc, gcc-c++
BuildRequires: gettext
BuildRequires: pkgconfig(libdrm) >= 2.4.97
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(zlib) >= 1.2.3
BuildRequires: pkgconfig(libzstd)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(wayland-protocols) >= 1.8
BuildRequires: pkgconfig(wayland-client) >= 1.11
BuildRequires: pkgconfig(wayland-server) >= 1.11
BuildRequires: pkgconfig(wayland-egl-backend) >= 3
BuildRequires: pkgconfig(x11), pkgconfig(xext)
BuildRequires: pkgconfig(xdamage) >= 1.1
BuildRequires: pkgconfig(xfixes), pkgconfig(xxf86vm)
BuildRequires: pkgconfig(xcb-glx) >= 1.8.1
BuildRequires: pkgconfig(xcb), pkgconfig(x11-xcb)
BuildRequires: pkgconfig(xcb-dri2) >= 1.8
BuildRequires: pkgconfig(xcb-dri3), pkgconfig(xcb-present)
BuildRequires: pkgconfig(xcb-sync), pkgconfig(xshmfence) >= 1.1
BuildRequires: pkgconfig(dri2proto) >= 2.8
BuildRequires: pkgconfig(glproto) >= 1.4.14
BuildRequires: bison, flex
BuildRequires: pkgconfig(libva) >= 0.38.0
BuildRequires: pkgconfig(libelf)
BuildRequires: pkgconfig(libglvnd) >= 1.3.2
BuildRequires: pkgconfig(vulkan)
BuildRequires: llvm-devel >= 7.0.0
BuildRequires: clang-devel
BuildRequires: pkgconfig(libclc)
BuildRequires: pkgconfig(SPIRV-Tools)
BuildRequires: pkgconfig(LLVMSPIRVLib)
BuildRequires: bindgen
BuildRequires: rust-packaging
BuildRequires: rustfmt
BuildRequires: cbindgen
BuildRequires: vulkan-headers
BuildRequires: glslang
BuildRequires: pkgconfig(libpng)
BuildRequires: python3-devel
BuildRequires: python3-mako, python3-pycparser, python3-pyyaml
BuildRequires: cmake

%description
Mesa 3D Graphics Library for NVE4 (GK104 / Kepler) with:
- Nouveau Gallium (nvc0) for OpenGL 4.6
- NVK Vulkan 1.2 driver
- Rusticl OpenCL 3.0
- VA-API video decode (MPEG-2, VC-1, H.264)

%prep
%setup -q -n mesa-mesa-26.3.1

%build
export RUSTFLAGS="%build_rustflags"
export MESON_PACKAGE_CACHE_DIR="%{cargo_registry}/"

meson setup build \
  -Dplatforms=x11,wayland \
  -Dgallium-drivers=nouveau \
  -Dgallium-va=enabled \
  -Dgallium-rusticl=true \
  -Dvulkan-drivers=nouveau \
  -Dvideo-codecs=all \
  -Dbuildtype=release \
  -Dprefix=/usr \
  -Dlibdir=%{_libdir} \
  -Dgles1=enabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=enabled \
  -Dglvnd=enabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dbuild-tests=false \
  -Dxlib-lease=disabled \
  -Dtools=nouveau

ninja -C build -j$(nproc)

%install
DESTDIR=%{buildroot} ninja -C build install

%files
%{_bindir}/nv_mme_dump
%{_bindir}/nv_push_dump
%{_libdir}/libGLX_mesa.so.0*
%{_libdir}/libGLX_system.so.0*
%{_libdir}/libEGL_mesa.so.0*
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*
%{_libdir}/libgallium-*.so
%{_libdir}/gbm/dri_gbm.so
%{_libdir}/dri/nouveau_dri.so
%{_libdir}/dri/nouveau_drv_video.so
%{_libdir}/libvulkan_nouveau.so
%{_datadir}/vulkan/icd.d/nouveau_icd.*.json
%{_libdir}/libRusticlOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/rusticl.icd
%{_datadir}/drirc.d/*
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libclc/*
%{_datadir}/libclc/*
%{_libdir}/libGLESv2.so.2*
%{_libdir}/libEGL.so.1*
%{_libdir}/libglapi.so.*
%{_libdir}/libnouveau_noop_drm_shim.so

%changelog
* Fri Jul 17 2026 Youssef <youssef@fedora> - 26.3.1-0.1.nve4
- Mesa for NVE4: Nouveau + NVK + Rusticl + VA-API
