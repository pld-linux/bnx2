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
Version:	1.9.20b
Release:	0.1
License:	GPL
Group:		Base
# from http://www-947.ibm.com/systems/support/supportsite.wss/docdisplay?lndocid=MIGR-5081938&brandind=5000020
# download: brcm_dd_nic_netxtreme2-1.9.20b_1.50.13_sles11_32-64.tgz
Source0:	netxtreme2-5.0.17.tar.gz
# Source0-md5:	ef4561b8fac71126da0bfa12255c34c2
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.27}
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
%setup -q -c
mv netxtreme2-*/* .
mv bnx2/{README.TXT,RELEASE.TXT} .

%build
%build_kernel_modules -m bnx2 -C bnx2/src \
	EXTRA_CFLAGS="-DHAVE_IP_HDR -DHAVE_LE32 -DNEW_SKB"

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
%doc README.TXT RELEASE.TXT INSTALL.TXT
/lib/modules/%{_kernel_ver}/kernel/net/*.ko*
