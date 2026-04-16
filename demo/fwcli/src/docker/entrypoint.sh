#!/bin/bash

# Confirm the API key environment variable is set
if [ -z ${FW_API_KEY+x} ]; then
    echo "ERROR: FW_API_KEY is not set";
    exit 1
fi

# Confirm there are files to transfer
if [ -z "$(ls -A /wd)" ]; then
   echo "ERROR: No files in working directory";
   exit 1
fi

# Use environment variables with defaults for configuration
ADCID=${ADCID:-0}
DATATYPE=${DATATYPE:-form}
PIPELINE=${PIPELINE:-sandbox}
STUDYID=${STUDYID:-adrc}

# 1. Login with FW CLI using environment variable FW_API_KEY
if ! fw login ${FW_API_KEY}; then
    echo "ERROR: failed to login";
    exit 1
fi

# 2. Determine center group
if ! CENTER=$(center_lookup "${ADCID}"); then
    echo "ERROR: center lookup failed"
    exit 1
fi
echo "Using center: ${CENTER}"

# 3. Determine pipeline
if ! PIPELINE_LABEL=$(pipeline_lookup -c "${CENTER}" -d "${DATATYPE}" -p "${PIPELINE}" -s "${STUDYID}"); then
    echo "ERROR: pipeline lookup failed"
    exit 1
fi
echo "Using pipeline: ${PIPELINE_LABEL}"

# 4. Upload single file
fw upload /wd/form-data-dummyv1.csv "fw://${CENTER}/${PIPELINE_LABEL}"
