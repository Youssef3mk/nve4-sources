%define debug_package %{nil}
%define _build_id_links none
%define _disable_source_fetch 0

%define _basekver 7.1
%define _stablekver 3
%define _kver %{version}-%{release}.%{_arch}
%define _kernel_dir /lib/modules/%{_kver}

Name: kernel-nve4
Version: %{_basekver}.%{_stablekver}
Release: 1%{?dist}
Summary: Custom kernel for NVE4 (GK104) with built-in video firmware
License: GPL-2.0-only
URL: https://www.kernel.org/
Source0: https://cdn.kernel.org/pub/linux/kernel/v7.x/linux-%{version}.tar.xz
Source1: kernel-nve4-addons-%{version}.tar.gz

BuildRequires: bc, bison, flex
BuildRequires: dwarves, elfutils-devel
BuildRequires: gcc, make, kmod
BuildRequires: openssl, openssl-devel
BuildRequires: perl-Carp, perl-devel, perl-generators, perl-interpreter
BuildRequires: python3-devel, python3-pyyaml, python-srpm-macros
BuildRequires: cpio, xz, findutils, diffutils, sed

Provides: installonlypkg(kernel)
Provides: kernel = %{version}-%{release}
Provides: kernel-core = %{version}-%{release}
Provides: kernel-modules = %{version}-%{release}
Requires(pre): coreutils, dracut >= 027, systemd >= 203-2
Requires(preun): systemd >= 200

%description
Custom Linux kernel %{version} for GK104 (NVE4) with:
- Built-in MSVLD/MSPDEC/MSPPP video firmware from NVIDIA blob
- All Nouveau video engines firmware compiled-in
No external firmware files needed.

%prep
%setup -q -n linux-%{version}
%setup -q -T -D -a 1 -n linux-%{version}
patch -p1 < patches/0001-gk104-add-built-in-video-firmware.patch

%build
make defconfig
./scripts/config --module DRM_NOUVEAU
./scripts/config --enable DRM_NOUVEAU_BACKLIGHT
./scripts/config --set-str CONFIG_LOCALVERSION "-nve4"
make -j$(nproc) olddefconfig
make -j$(nproc) all

%install
export INSTALL_MOD_PATH=%{buildroot}
make modules_install

# Install kernel
install -Dm644 "$(make -s image_name)" "%{buildroot}%{_kernel_dir}/vmlinuz"
install -Dt %{buildroot}%{_kernel_dir} -m644 System.map

# Install config
cp .config %{buildroot}%{_kernel_dir}/config

# Create stub initramfs
install -dm755 %{buildroot}/boot
dd if=/dev/zero of=%{buildroot}/boot/initramfs-%{_kver}.img bs=1M count=20

%post
if [ ! -e /run/ostree-booted ]; then
    /bin/kernel-install add %{_kver} %{_kernel_dir}/vmlinuz || exit $?
fi

%preun
/bin/kernel-install remove %{_kver} || exit $?

%posttrans
/sbin/depmod -a %{_kver}
if [ ! -e /run/ostree-booted ]; then
    echo "Running: dracut -f --kver %{_kver}"
    dracut -f --kver "%{_kver}" || exit $?
fi

%files
%license COPYING
/boot/initramfs-%{_kver}.img
%{_kernel_dir}/vmlinuz
%{_kernel_dir}/System.map
%{_kernel_dir}/config
%{_kernel_dir}/kernel
%{_kernel_dir}/modules.order
%{_kernel_dir}/modules.builtin
%{_kernel_dir}/modules.builtin.modinfo
%exclude %{_kernel_dir}/build
%exclude %{_kernel_dir}/source

%changelog
* Fri Jul 17 2026 Youssef <youssef@fedora> - 7.1.3-1
- Initial NVE4 kernel with built-in video firmware
