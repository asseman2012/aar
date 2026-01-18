#!/usr/bin/env python3
"""
Retouche agressif des images - enlever sac poubelle, gens, et coins peinture
Utilise PIL uniquement (pas de dépendances externes)
"""

from PIL import Image, ImageDraw, ImageFilter, ImageOps
import os

def darken_region(img, x1, y1, x2, y2, blur_amount=20):
    """Assombrir et flouter une région (pour les gens/sac)"""
    # Extraire la région
    region = img.crop((x1, y1, x2, y2))
    
    # Flouter fortement
    for _ in range(3):
        region = region.filter(ImageFilter.GaussianBlur(radius=blur_amount))
    
    # Assombrir
    region = ImageOps.posterize(region, 2)
    
    # Repaste
    img.paste(region, (x1, y1))
    return img

def retouch_image(image_path):
    """Retoucher une image de manière agressive"""
    print(f"Retouching {image_path}...")
    
    try:
        # Ouvrir l'image
        img = Image.open(image_path)
        w, h = img.size
        
        print(f"  Image size: {w}x{h}")
        
        # Créer une copie pour ne pas perdre l'original
        result = img.copy()
        
        # 1. FLOUTER LE BAS (sac poubelle) - 15% du bas
        print("  Flouring trash zone (bottom 15%)...")
        trash_y = int(h * 0.85)
        result = darken_region(result, 0, trash_y, w, h, blur_amount=25)
        
        # 2. FLOUTER LES COINS (peinture)
        print("  Flouring corners...")
        corner_size = int(min(w, h) * 0.12)
        
        # Haut gauche
        result = darken_region(result, 0, 0, corner_size, corner_size, blur_amount=20)
        # Haut droit
        result = darken_region(result, w - corner_size, 0, w, corner_size, blur_amount=20)
        # Bas gauche
        result = darken_region(result, 0, h - corner_size, corner_size, h, blur_amount=20)
        # Bas droit
        result = darken_region(result, w - corner_size, h - corner_size, w, h, blur_amount=20)
        
        # 3. FLOUTER LA ZONE GENS (milieu)
        print("  Flouring people zone...")
        people_y1 = int(h * 0.35)
        people_y2 = int(h * 0.75)
        people_x1 = int(w * 0.1)
        people_x2 = int(w * 0.9)
        result = darken_region(result, people_x1, people_y1, people_x2, people_y2, blur_amount=18)
        
        # Sauvegarder
        backup_path = image_path.replace('.jpeg', '_backup.jpeg')
        
        # Garder l'original en backup s'il n'existe pas déjà
        if not os.path.exists(backup_path):
            os.rename(image_path, backup_path)
            print(f"  Backup créé: {backup_path}")
        
        # Sauvegarder la version retouchée
        result.save(image_path, 'JPEG', quality=95)
        print(f"  ✓ Sauvegardé: {image_path}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        return False

# Fichiers à retoucher
images_to_retouch = [
    'image16avant.jpeg',
    'image20apres.jpeg',
    'image28apres.jpeg',
    'image29avant.jpeg'
]

# Aller au répertoire des assets
os.chdir(os.path.expanduser('~/Documents/web/chantier/renovation-site/assets'))

print("="*50)
print("RETOUCHE AGGRESSIVE DES IMAGES")
print("="*50)

success_count = 0
for img in images_to_retouch:
    if os.path.exists(img):
        if retouch_image(img):
            success_count += 1
    else:
        print(f"✗ Fichier non trouvé: {img}")

print("="*50)
print(f"Retouche terminée! ({success_count}/{len(images_to_retouch)} images réussies)")
print("="*50)
