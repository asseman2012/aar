#!/usr/bin/env python3
"""
Script pour retoucher les images : enlever sac poubelle, gens, et corners avec peinture
Utilise la technique du clone stamp / blur
"""

from PIL import Image, ImageDraw, ImageFilter
import os

# Chemins des images
images_to_retouch = [
    'assets/image16avant.jpeg',
    'assets/image20apres.jpeg',
    'assets/image28apres.jpeg',
    'assets/image29avant.jpeg'
]

def smart_inpaint(img, mask_region):
    """
    Faire une retouche simple : flouter les zones à enlever
    et faire une transition douce
    """
    # Créer une copie
    result = img.copy()
    
    # Pour chaque zone du mask, appliquer un flou progressif
    for _ in range(3):
        result = result.filter(ImageFilter.GaussianBlur(radius=2))
    
    return result

def retouch_image(image_path):
    """Retoucher une image"""
    print(f"Retouching {image_path}...")
    
    # Ouvrir l'image
    img = Image.open(image_path)
    w, h = img.size
    
    # Créer une copie pour la retouche
    result = img.copy()
    draw = ImageDraw.Draw(result, 'RGBA')
    
    # Zones à retoucher
    # 1. Bas de l'image (sac poubelle) - flouter fortement
    trash_zone = (0, int(h * 0.85), w, h)
    trash_img = img.crop(trash_zone)
    for _ in range(5):
        trash_img = trash_img.filter(ImageFilter.GaussianBlur(radius=15))
    result.paste(trash_img, (trash_zone[0], trash_zone[1]))
    
    # 2. Coins (peinture)
    corner_size = int(min(h, w) * 0.1)
    corners = [
        (0, 0, corner_size, corner_size),  # Haut gauche
        (w - corner_size, 0, w, corner_size),  # Haut droit
        (0, h - corner_size, corner_size, h),  # Bas gauche
        (w - corner_size, h - corner_size, w, h)  # Bas droit
    ]
    
    for corner in corners:
        corner_img = img.crop(corner)
        for _ in range(4):
            corner_img = corner_img.filter(ImageFilter.GaussianBlur(radius=10))
        result.paste(corner_img, (corner[0], corner[1]))
    
    # 3. Zone milieu (gens) - application sélective
    people_zone = (int(w * 0.15), int(h * 0.4), int(w * 0.85), int(h * 0.8))
    people_img = img.crop(people_zone)
    for _ in range(3):
        people_img = people_img.filter(ImageFilter.GaussianBlur(radius=8))
    result.paste(people_img, (people_zone[0], people_zone[1]))
    
    # Sauvegarder
    backup_path = image_path.replace('.jpeg', '_backup.jpeg')
    if not os.path.exists(backup_path):
        os.rename(image_path, backup_path)
    
    result.save(image_path, quality=95)
    
    print(f"  Saved to {image_path}")
    print(f"  Backup: {backup_path}")

# Traiter toutes les images
for img_path in images_to_retouch:
    if os.path.exists(img_path):
        try:
            retouch_image(img_path)
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    else:
        print(f"File not found: {img_path}")

print("Done!")
