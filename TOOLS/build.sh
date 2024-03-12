#/bin/env bash

set -eux

# make sure we check our own directories
TOPDIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")/..")"
SOURCEDIR="${TOPDIR}/SOURCES"
SPECDIR="${TOPDIR}/SPECS"

rpmbuild \
    --define "_sourcedir ${SOURCEDIR}" \
    --define "_specdir ${SPECDIR}" \
    $@
