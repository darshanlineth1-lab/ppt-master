#!/bin/bash
# usage: mk.sh <file.svg> <icon> "<Title>" <page-no>   (body on stdin; optional $DEFS extra defs)
set -e
D=/home/user/ppt-master/projects/optics_wave_nature_of_light_a4_20261113/svg_output
T=/home/user/render/template_04.svg
{
  awk 'NF==0{exit} {print}' "$T" | sed "s/wave-sine\" x=\"118\"/$2\" x=\"118\"/; s|>Wave Theory of Light<|>$3<|" | awk -v defs="$DEFS" '/<\/defs>/ && defs!="" {print defs} {print}'
  echo
  cat
  echo
  awk '/<g id="page-footer"/{f=1} f{print}' "$T" | sed "s|fill=\"#C2527C\">4</text>|fill=\"#C2527C\">$4</text>|"
} > "$D/$1"
/home/user/.venv/bin/python -c "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1]); print('xml ok')" "$D/$1"
