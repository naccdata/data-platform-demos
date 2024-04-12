#!/bin/bash
CENTER=sample-center
PIPELINE=sandbox-form

if [ -z ${FW_API_KEY+x} ]; then 
    echo "ERROR: FW_API_KEY is not set"; 
    exit 1
fi

if [ -z "$(ls -A /wd)" ]; then
   echo "ERROR: No files in working directory";
   exit 1
fi

# 1. Login with FW CLI using environment variable FW_API_KEY
if fw login ${FW_API_KEY}; then
    echo "login successful"
else
    echo "ERROR: failed to login";
    exit 1
fi

# 2. Upload single file
fw upload /wd/form-data-dummyv1.csv fw://${CENTER}/${PIPELINE}