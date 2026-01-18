#!/bin/bash
# Optimiser les images JPEG avec ImageMagick

ASSETS="/mnt/c/Users/asseman/Documents/web/chantier/renovation-site/assets"

echo "🖼️  Optimisation des images JPEG..."

for img in $ASSETS/image{16..29}.jpeg; do
  if [ -f "$img" ]; then
    # Améliorer le contraste, la saturation et la luminosité
    convert "$img" \
      -colorspace RGB \
      -modulate 110,120 \
      -contrast-stretch 0 \
      -quality 90 \
      "$img"
    echo "✓ $(basename $img)"
  fi
done

echo "✅ Optimisation terminée!"
