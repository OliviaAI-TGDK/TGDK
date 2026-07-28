#!/bin/bash
# t# by TGDK - TGDK Compiler Compiler (tcc)
# Replaces gcc, wraps TGDK NEETs build
# LICENSE: BFE-TGDK-022ST
# Usage: tcc file.c -o output (same as gcc)

echo "t# by TGDK v022ST - Mobius Compiler"
echo "LICENSE BFE-TGDK-022ST ACTIVE"
echo ""

# If called as tcc with tgdk file, use neets build
if [[ "$*" == *"tgdk"* ]] || [[ "$*" == *"neets"* ]]; then
    echo "[t#] Detected TGDK NEETs build - applying phi/pi lattice flags"
    FLAGS="-lpthread -lm -O2 -DMARA_FACTOR=1.6180339887 -DPHI_LATTICE -DPI_LATTICE -DNEETS_ENABLED"
else
    FLAGS="-lpthread -lm"
fi

# Real compile - replace gcc call
echo "[t#] tcc $* $FLAGS"
gcc $* $FLAGS

STATUS=$?
if [ $STATUS -eq 0 ]; then
    echo ""
    echo "[t#] Build sealed - mobius knot OK"
    echo "[t#] Binary ready - run with ./<output>"
else
    echo "[t#] Build failed - ratio outside 0.8-1.2 clipping"
fi

exit $STATUS
