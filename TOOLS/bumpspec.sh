#!/usr/bin/env bash
set -eu

if [[ $# != 2 ]]; then
    >&2 echo "error: bumpspec requires 2 arguments"
    exit 1
fi

COMMENT="${1}"
SPEC="${2}"

SPECRELEASE="$(grep "%define specrelease " ${SPEC})"
# assumes the release number is 3 digits
SPECRELEASE_NUMBER="$(echo ${SPECRELEASE} | cut -b 21-23)"

NEW_SPECRELEASE_NUMBER="$(( ${SPECRELEASE_NUMBER} + 1))"
NEW_SPECRELEASE="${SPECRELEASE/${SPECRELEASE_NUMBER}/${NEW_SPECRELEASE_NUMBER}}"

echo ${NEW_SPECRELEASE}

sed -i "s|${SPECRELEASE}|${NEW_SPECRELEASE}|g" ${SPEC}

rpmdev-bumpspec --comment="${COMMENT}" ${SPEC}

sed -i "s|%{pkg_release}.1|%{pkg_release}|g" ${SPEC}
