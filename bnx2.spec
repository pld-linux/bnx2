# TODO
# - also from same source possible to build: bnx2x, cnic
#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	0.1
%define		pname	bnx2
Summary:	Broadcom NetXtreme II Gigabit ethernet driver
Name:		%{pname}%{_alt_kernel}
Version:	2.0.8e
Release:	0.1
License:	GPL
Group:		Base
# from https://www-947.ibm.com/support/entry/portal/docdisplay?brand=5000020&lndocid=MIGR-5081938
# download: brcm_dd_nic_netxtreme2-*.tgz
Source0:	ftp://download2.boulder.ibm.com/ecc/sar/CMA/XSA/brcm_dd_nic_netxtreme2-%{version}_1.52.16_sles11_32-64.tgz
# Source0-md5:	29b93ae8c6ba423687b1268285a7befb
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.27}
BuildRequires:	rpm-utils
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Broadcom NetXtreme II Gigabit ethernet
driver for the Broadcom NetXtreme II BCM5706/BCM5708/5709/5716
10/100/1000/2500/10000 Mbps PCIX/PCIE Ethernet Network Controller.

%package -n kernel%{_alt_kernel}-net-bnx2
Summary:	Linux driver for bnx2
Summary(pl.UTF-8):	Sterownik dla Linuksa do bnx2
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-bnx2
This package contains the Broadcom NetXtreme II Gigabit ethernet
driver for the Broadcom NetXtreme II BCM5706/BCM5708/5709/5716
10/100/1000/2500/10000 Mbps PCIX/PCIE Ethernet Network Controller.

%prep
%setup -qc
rpm2cpio sles11/noarch/update/SUSE-SLES/11/sources/brcm-netxtreme2-sles11-*.src.rpm | cpio -dimu
%{__tar} -zxf netxtreme2-*.tar.gz
mv netxtreme2-*/* .

%build
%build_kernel_modules -m bnx2 -C bnx2/src \
	EXTRA_CFLAGS="-DHAVE_IP_HDR -DHAVE_LE32 -DNEW_SKB -DHAVE_BOOL"

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m bnx2/src/bnx2 -d kernel/net

%post	-n kernel%{_alt_kernel}-net-bnx2
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-bnx2
%depmod %{_kernel_ver}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n kernel%{_alt_kernel}-net-bnx2
%defattr(644,root,root,755)
%doc bnx2/{README.TXT,RELEASE.TXT,ChangeLog}
/lib/modules/%{_kernel_ver}/kernel/net/*.ko*
