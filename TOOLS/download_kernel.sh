#/bin/env bash
set -eu

if [[ $# != 1 ]]; then
    >&2 echo "usage: download_kernel.sh [f40]"
    exit 1
fi

TOPDIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")/..")"
SOURCEDIR="${TOPDIR}/SOURCES"
FEDORA="${1}"

TEMP_DIR=$(mktemp -d)
trap '{ rm -rf -- "$TEMP_DIR"; }' EXIT
pushd $TEMP_DIR

wget https://src.fedoraproject.org/rpms/kernel/raw/${FEDORA}/f/kernel.spec
wget https://src.fedoraproject.org/rpms/kernel/raw/${FEDORA}/f/sources

fedpkg --name kernel sources --force --outdir "${SOURCEDIR}"

popd
