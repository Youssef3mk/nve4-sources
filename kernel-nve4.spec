%define debug_package %{nil}

Name: kernel-nve4
Version: 7.1.3
Release: 1%{?dist}
Summary: Custom kernel for NVE4 (GK104) with built-in video firmware
License: GPL-2.0-only
URL: https://www.kernel.org/
Source0: https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-7.1.3.tar.xz
Source1: kernel-nve4-addons-7.1.3.tar.gz

BuildRequires: gcc, make, bison, flex, openssl-devel, elfutils-devel
BuildRequires: bc, kmod, cpio, xz, rsync, findutils
BuildRequires: python3, python3-devel
BuildRequires: dwarves, ncurses-devel
BuildRequires: diffutils, sed, perl

%description
Custom Linux kernel %{version} for GK104 (NVE4) with:
- Built-in MSVLD/MSPDEC/MSPPP video firmware from NVIDIA blob
- All Nouveau video engines firmware compiled-in
No external firmware files needed.

%prep
%setup -q -n linux-7.1.3
%setup -q -T -D -a 1 -n linux-7.1.3
patch -p1 < patches/0001-gk104-add-built-in-video-firmware.patch

%build
make defconfig
./scripts/config --enable DRM_NOUVEAU
./scripts/config --module DRM_NOUVEAU
./scripts/config --enable DRM_NOUVEAU_BACKLIGHT
./scripts/config --set-str CONFIG_LOCALVERSION "-nve4"
make -j$(nproc) olddefconfig
make -j$(nproc) bzImage modules

%install
export INSTALL_MOD_PATH=%{buildroot}
make modules_install
mkdir -p %{buildroot}/boot
cp arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{version}-nve4
cp System.map %{buildroot}/boot/System.map-%{version}-nve4
cp .config %{buildroot}/boot/config-%{version}-nve4

%files
/boot/*
/lib/modules/%{version}-nve4/*
%exclude /lib/modules/%{version}-nve4/build
%exclude /lib/modules/%{version}-nve4/source

%changelog
* Fri Jul 17 2026 Youssef <youssef@fedora> - 7.1.3-1
- Initial NVE4 kernel with built-in video firmware
