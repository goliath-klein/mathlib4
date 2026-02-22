#!/bin/bash

BENCH_DIR=~/benches

if [[ ! -d "$BENCH_DIR" ]]; then
    echo "Error: Directory $BENCH_DIR does not exist."
    exit 1
fi

SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "nosha")

N=1
while true; do
    CANDIDATE="${BENCH_DIR}/measurements-${SHA}-${N}.jsonl"
    if [[ ! -e "$CANDIDATE" ]]; then
        OUTFILE="$CANDIDATE"
        break
    fi
    ((N++))
done

if [[ -f "measurements.jsonl" ]]; then
    mv "measurements.jsonl" "$OUTFILE"
    if [[ $? -eq 0 ]]; then
        echo "Successfully moved log to: $OUTFILE"
    else
        echo "Failed to rename logfile"
        exit 1
    fi
else
    echo "Error: measurements.jsonl not found in current directory."
    exit 1
fi
