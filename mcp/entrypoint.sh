#!/bin/sh
set -eu

: "${BUNDLE_URL:?BUNDLE_URL must not be empty}"
: "${BUNDLE_NAME:?BUNDLE_NAME must not be empty}"
: "${DB_PATH:?DB_PATH must not be empty}"

mkdir -p "$(dirname "${DB_PATH}")"
temporary_db="${DB_PATH}.tmp"
rm -f "${temporary_db}"

cleanup() {
    rm -f "${temporary_db}"
}
trap cleanup EXIT INT TERM

set -- okf ingest "${BUNDLE_URL}" \
    --db "${temporary_db}" \
    --id "${BUNDLE_NAME}" \
    --json

if [ -n "${BUNDLE_REF:-}" ]; then
    set -- "$@" --branch "${BUNDLE_REF}"
fi

if [ -n "${BUNDLE_SUBDIR:-}" ]; then
    set -- "$@" --subdir "${BUNDLE_SUBDIR}"
fi

echo "Fetching and ingesting ${BUNDLE_URL} (${BUNDLE_REF:-default ref}, subdir=${BUNDLE_SUBDIR:-root})" >&2
if "$@"; then
    mv -f "${temporary_db}" "${DB_PATH}"
elif [ -f "${DB_PATH}" ]; then
    echo "Ingestion failed; serving the previous catalog from ${DB_PATH}" >&2
else
    echo "Ingestion failed and no previous catalog is available" >&2
    exit 1
fi

trap - EXIT INT TERM
exec python /app/server.py
