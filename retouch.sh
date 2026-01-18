#!/bin/bash
# Script pour retoucher les images avec ImageMagick (convert)

cd /mnt/c/Users/asseman/Documents/web/chantier/renovation-site/assets

echo "Retouching image16avant.jpeg..."
# Créer une copie de backup
cp image16avant.jpeg image16avant_backup.jpeg

# Flouter le bas (sac poubelle) et les coins
convert image16avant_backup.jpeg \
  \( +clone -crop 100%x15%+0+85% -blur 0x15 \) -gravity South -composite \
  \( +clone -crop 10%x10%+0+0 -blur 0x10 \) -gravity NorthWest -composite \
  \( +clone -crop 10%x10%+0+0 -blur 0x10 \) -gravity NorthEast -composite \
  image16avant.jpeg

echo "Retouching image20apres.jpeg..."
cp image20apres.jpeg image20apres_backup.jpeg
convert image20apres_backup.jpeg \
  \( +clone -crop 100%x15%+0+85% -blur 0x15 \) -gravity South -composite \
  \( +clone -crop 10%x10%+0+0 -blur 0x10 \) -gravity NorthWest -composite \
  \( +clone -crop 10%x10%+0+0 -blur 0x10 \) -gravity NorthEast -composite \
  image20apres.jpeg

echo "Retouching image28apres.jpeg..."
cp image28apres.jpeg image28apres_backup.jpeg
convert image28apres_backup.jpeg \
  \( +clone -crop 100%x15%+0+85% -blur 0x15 \) -gravity South -composite \
  \( +clone -crop 10%x10%+0+0 -blur 0x10 \) -gravity NorthWest -composite \
  \( +clone -crop 10%x10%+0+0 -blur 0x10 \) -gravity NorthEast -composite \
  image28apres.jpeg

echo "Retouching image29avant.jpeg..."
cp image29avant.jpeg image29avant_backup.jpeg
convert image29avant_backup.jpeg \
  \( +clone -crop 100%x15%+0+85% -blur 0x15 \) -gravity South -composite \
  \( +clone -crop 10%x10%+0+0 -blur 0x10 \) -gravity NorthWest -composite \
  \( +clone -crop 10%x10%+0+0 -blur 0x10 \) -gravity NorthEast -composite \
  image29avant.jpeg

echo "Done!"
