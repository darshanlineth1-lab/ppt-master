#!/bin/bash
set -e
P="$1"; DPI="${2:-110}"; R=/home/user/render
rm -rf $R/work $R/png; mkdir -p $R/work/svg_output $R/png
cp "$P"/svg_output/*.svg $R/work/svg_output/; cp -r "$P/icons" $R/work/ 2>/dev/null || true
/home/user/.venv/bin/python /home/user/ppt-master/skills/ppt-master/scripts/svg_finalize/embed_icons.py $R/work/svg_output/*.svg >/dev/null 2>&1 || echo "WARN embed_icons failed"
node $R/render.js $R/work/svg_output $R/out.pdf
/home/user/.venv/bin/python - <<PY 2>/dev/null
import pymupdf
d=pymupdf.open('$R/out.pdf')
for i,p in enumerate(d): p.get_pixmap(dpi=$DPI).save('$R/png/p%02d.png'%(i+1))
PY
