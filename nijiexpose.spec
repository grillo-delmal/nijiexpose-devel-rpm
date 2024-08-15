%define nijiexpose_ver 0.0.0
%define nijiexpose_semver 0.0.0+build.249.07c757e
%define nijiexpose_dist 249
%define nijiexpose_commit 07c757e7149127a968fd6c2508973b68eb56127e
%define nijiexpose_short 07c757e

# Project maintained deps
%define nijilive_semver 0.0.0+build.649.20567d5
%define nijilive_commit 20567d51f25d629c9378745b88a2c30d0f6216e0
%define nijilive_short 20567d5

%define nijiui_semver 0.0.0+build.77.73c9acf
%define nijiui_commit 73c9acf257ca54fbb0a4274db4fd10e5f82a456e
%define nijiui_short 73c9acf

%if 0%{nijiexpose_dist} > 0
%define nijiexpose_suffix ^%{nijiexpose_dist}.git%{nijiexpose_short}
%endif

Name:           nijiexpose
Version:        %{nijiexpose_ver}%{?nijiexpose_suffix:}
Release:        %autorelease
Summary:        Tool to use nijilive puppets

# Bundled lib licenses
##   nijilive licenses: BSD-2-Clause
##   nijiui licenses: BSD-2-Clause
# Static dependencies licenses
##   bindbc-loader licenses: BSL-1.0
##   bindbc-lua licenses: BSL-1.0
##   bindbc-sdl licenses: BSL-1.0
##   ddbus licenses: MIT
##   diet-ng licenses: MIT
##   dportals licenses: BSD-2-Clause
##   dunit licenses: MIT
##   eventcore licenses: MIT
##   facetrack-d licenses: BSD-2-Clause
##   fghj licenses: BSL-1.0
##   i18n-d licenses: BSD-2-Clause
##   i2d-imgui licenses: BSL-1.0 and MIT
##   i2d-opengl licenses: BSL-1.0
##   imagefmt licenses: BSD-2-Clause
##   inmath licenses: BSD-2-Clause
##   lumars licenses: MIT
##   mir-algorithm licenses: Apache-2.0
##   mir-core licenses: Apache-2.0
##   mir-linux-kernel licenses: BSL-1.0
##   openssl licenses: OpenSSL
##   silly licenses: ISC
##   stdx-allocator licenses: BSD-2-Clause
##   taggedalgebraic licenses: BSD-2-Clause
##   tinyfiledialogs licenses: Zlib
##   vibe-container licenses: MIT
##   vibe-core licenses: MIT
##   vibe-d licenses: MIT
##   vmc-d licenses: BSD-2-Clause
License:        BSD-2-Clause and Apache-2.0 and BSL-1.0 and ISC and MIT and OpenSSL and Zlib

URL:            https://github.com/grillo-delmal/nijiexpose-rpm

Source0:        https://github.com/nijigenerate/nijiexpose/archive/%{nijiexpose_commit}/%{name}-%{nijiexpose_short}.tar.gz

# Project maintained deps
Source1:        https://github.com/nijigenerate/nijilive/archive/%{nijilive_commit}/nijilive-%{nijilive_short}.tar.gz
Source2:        https://github.com/nijigenerate/nijiui/archive/%{nijiui_commit}/nijiui-%{nijiui_short}.tar.gz

Patch0:         nijiexpose_0_deps.patch
Patch1:         nijiexpose_1_lua.patch
Patch2:         nijiui_0_deps.patch

# dlang
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  git

BuildRequires:  zdub-dub-settings-hack

BuildRequires:  zdub-bindbc-loader-static
BuildRequires:  zdub-bindbc-lua-static
BuildRequires:  zdub-bindbc-sdl-static
BuildRequires:  zdub-ddbus-static
BuildRequires:  zdub-diet-ng-static
BuildRequires:  zdub-dportals-static
BuildRequires:  zdub-dunit-static
BuildRequires:  zdub-eventcore-static
BuildRequires:  zdub-facetrack-d-static
BuildRequires:  zdub-fghj-static
BuildRequires:  zdub-i18n-d-static
BuildRequires:  zdub-i2d-imgui-static
BuildRequires:  zdub-i2d-opengl-static
BuildRequires:  zdub-imagefmt-static
BuildRequires:  zdub-inmath-static
BuildRequires:  zdub-lumars-static
BuildRequires:  zdub-mir-algorithm-static
BuildRequires:  zdub-mir-core-static
BuildRequires:  zdub-mir-linux-kernel-static
BuildRequires:  zdub-openssl-static
BuildRequires:  zdub-silly-static
BuildRequires:  zdub-stdx-allocator-static
BuildRequires:  zdub-taggedalgebraic-static
BuildRequires:  zdub-tinyfiledialogs-static
BuildRequires:  zdub-vibe-container-static
BuildRequires:  zdub-vibe-core-static
BuildRequires:  zdub-vibe-d-static
BuildRequires:  zdub-vmc-d-static

Requires:       hicolor-icon-theme

#bindbc-lua deps
Requires:       luajit

#dportals deps
Requires:       dbus

#i2d-imgui deps
Requires:       libstdc++
Requires:       freetype
Requires:       SDL2

#openssl deps
Requires:       openssl-devel


%description
nijilive is a framework for realtime 2D puppet animation which can be used for VTubing, 
game development and digital animation. 
nijiexpose is a tool that lets you use nijilive puppets as tracked avatars.


%prep
%setup -n %{name}-%{nijiexpose_commit}

cat > source/nijiexpose/ver.d <<EOF
module nijiexpose.ver;

enum INS_VERSION = "%{nijiexpose_semver}";
EOF

# FIX: Add fake dependency
mkdir -p deps/bindbc-spout2
cat > deps/bindbc-spout2/dub.sdl <<EOF
name "bindbc-spout2"
EOF
dub add-local deps/bindbc-spout2 "0.1.1"


%patch -P 0 -p1 -b .nijiexpose-deps
%patch -P 1 -p1 -b .nijiexpose-lua
mkdir -p deps

# Project maintained deps
tar -xzf %{SOURCE1}
mv nijilive-%{nijilive_commit} deps/nijilive
dub add-local deps/nijilive/ "%{nijilive_semver}"

pushd deps; pushd nijilive

# FIX: nijilive version dependent on git
cat > source/nijilive/ver.d <<EOF
module nijilive.ver;

enum IN_VERSION = "%{nijilive_semver}";
EOF

[ -f dub.sdl ] && dub convert -f json
mv -f dub.json dub.json.base
jq 'walk(if type == "object" then with_entries(select(.key | test("preBuildCommands*") | not)) else . end)' dub.json.base > dub.json

popd; popd

tar -xzf %{SOURCE2}
mv nijiui-%{nijiui_commit} deps/nijiui
dub add-local deps/nijiui/ "%{nijiui_semver}"

pushd deps; pushd nijiui

%patch -P 2 -p1 -b .nijiui-deps

[ -f dub.sdl ] && dub convert -f json
mv -f dub.json dub.json.base
jq 'walk(if type == "object" then with_entries(select(.key | test("preBuildCommands*") | not)) else . end)' dub.json.base > dub.json

popd; popd


%build
export DFLAGS="%{_d_optflags} -L-rpath=%{_libdir}/nijiexpose/"
dub build \
    --cache=local \
    --config=linux-full \
    --skip-registry=all \
    --non-interactive \
    --temp-build \
    --compiler=ldc2
mkdir ./out/
cp /tmp/.dub/build/nijiexpose*/linux-full*/* ./out/


%install
install -d ${RPM_BUILD_ROOT}%{_libdir}/nijiexpose
install -p ./out/cimgui.so ${RPM_BUILD_ROOT}%{_libdir}/nijiexpose/cimgui.so

install -d ${RPM_BUILD_ROOT}%{_bindir}
install -p ./out/nijiexpose ${RPM_BUILD_ROOT}%{_bindir}/nijiexpose

install -d ${RPM_BUILD_ROOT}%{_datadir}/applications/
install -p -m 644 ./build-aux/linux/nijiexpose.desktop ${RPM_BUILD_ROOT}%{_datadir}/applications/nijiexpose.desktop
desktop-file-validate \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/nijiexpose.desktop

install -d ${RPM_BUILD_ROOT}%{_metainfodir}/
install -p -m 644 ./build-aux/linux/nijiexpose.appdata.xml ${RPM_BUILD_ROOT}%{_metainfodir}/nijiexpose.appdata.xml
appstream-util validate-relax --nonet \
    ${RPM_BUILD_ROOT}%{_metainfodir}/nijiexpose.appdata.xml

install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/
install -p -m 644 ./res/logo_256.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/nijiexpose.png

# Dependency licenses
install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/deps/
find ./deps/ -mindepth 1 -maxdepth 1 -exec \
    install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/{} ';'

find ./deps/ -mindepth 2 -maxdepth 2 -iname '*LICENSE*' -exec \
    install -p -m 644 "{}" "${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/{}" ';'

install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/res/
find ./res/ -mindepth 1 -maxdepth 1 -iname '*LICENSE*' -exec \
    install -p -m 644 {} ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/{} ';'


%files
%license LICENSE
%{_datadir}/licenses/%{name}/*
%{_bindir}/nijiexpose
%{_libdir}/nijiexpose/*
%{_metainfodir}/nijiexpose.appdata.xml
%{_datadir}/applications/nijiexpose.desktop
%{_datadir}/icons/hicolor/256x256/apps/nijiexpose.png


%changelog
%autochangelog