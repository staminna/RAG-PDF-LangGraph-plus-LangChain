#!/bin/bash

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: ./download_pdf.sh <pdf_url> [query]"
    exit 1
fi

# Get the URL and escape it properly
URL="$1"
shift

# Get the query if provided
QUERY="$*"

# Run the Python script with the URL and query
python url_loader.py "$URL" "$QUERY" 