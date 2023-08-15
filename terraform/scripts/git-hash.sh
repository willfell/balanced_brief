#!/bin/bash
set -euo pipefail
if [ -z ${CODEBUILD_RESOLVED_SOURCE_VERSION+x} ]; then
    echo '{"hash": "'"$(git rev-parse --short HEAD)"'"}'
else
    echo '{"hash": "'"${CODEBUILD_RESOLVED_SOURCE_VERSION:0:7}"'"}'
fi
