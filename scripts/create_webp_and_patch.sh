#!/usr/bin/env bash
# Script to convert images to WebP (if cwebp or magick available) and patch HTML to use <picture>
# Run this from the project root on your machine (WSL or Linux/macOS).

set -euo pipefail
cd "$(dirname "$0")/.."
ASSETS="assets"
FILES=(1 2 3 4 5 6)

# Conversion: try magick, then cwebp
if command -v magick >/dev/null 2>&1; then
  CONVERTER=magick
elif command -v cwebp >/dev/null 2>&1; then
  CONVERTER=cwebp
else
  echo "No converter found. Install ImageMagick (magick) or libwebp (cwebp)." >&2
  exit 1
fi

echo "Using converter: $CONVERTER"

for n in "${FILES[@]}"; do
  for ext in png jpg jpeg; do
    src="$ASSETS/${n}avant.$ext"
    if [ -f "$src" ]; then
      dst="${src%.*}.webp"
      if [ "$CONVERTER" = "magick" ]; then
        magick "$src" -quality 80 "$dst" && echo "Converted $src -> $dst"
      else
        cwebp -q 80 "$src" -o "$dst" && echo "Converted $src -> $dst"
      fi
      break
    fi
  done
  for ext in png jpg jpeg; do
    src="$ASSETS/${n}apres.$ext"
    if [ -f "$src" ]; then
      dst="${src%.*}.webp"
      if [ "$CONVERTER" = "magick" ]; then
        magick "$src" -quality 80 "$dst" && echo "Converted $src -> $dst"
      else
        cwebp -q 80 "$src" -o "$dst" && echo "Converted $src -> $dst"
      fi
      break
    fi
  done
done

# Patch HTML files (index and avant-apres)
HTML_FILES=(index.html avant-apres.html)
for hf in "${HTML_FILES[@]}"; do
  [ -f "$hf" ] || continue
  tmp="$hf.tmp"
  cp "$hf" "$tmp"
  for n in "${FILES[@]}"; do
    # Build patterns
    before_img_pattern="<img src=\"assets/${n}avant.*?>"
    after_img_pattern="<img src=\"assets/${n}apres.*?>"
    # Build replacement
    before_webp="$ASSETS/${n}avant.webp"
    after_webp="$ASSETS/${n}apres.webp"
    if [ -f "$before_webp" ]; then
      # Replace the single <img ...before...> with <picture> block keeping the original img line
      perl -0777 -pe "s|(<img src=\"assets/${n}avant[^>]*>)|<picture>\\n  <source srcset=\"assets/${n}avant.webp\" type=\"image/webp\" />\\n  \1\\n</picture>|s" -i "$tmp" || true
    fi
    if [ -f "$after_webp" ]; then
      perl -0777 -pe "s|(<img src=\"assets/${n}apres[^>]*>)|<picture>\\n  <source srcset=\"assets/${n}apres.webp\" type=\"image/webp\" />\\n  \1\\n</picture>|s" -i "$tmp" || true
    fi
  done
  mv "$tmp" "$hf"
  echo "Patched $hf"
done

echo "Done. Remember to review the updated HTML files and commit changes."