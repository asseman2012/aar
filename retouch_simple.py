#!/usr/bin/env python3
"""
Retouche simple - juste flouter les zones
"""

from PIL import Image, ImageFilter
import os
import shutil

def blur_zone(img, x1, y1, x2, y2, radius=15):
    """Flouter une région spécifique"""
    # Extraire la zone
    zone = img.crop((x1, y1, x2, y2))
    
    # Flouter
    zone_blurred = zone.filter(ImageFilter.GaussianBlur(radius=radius))
    
    # Repaster
    img.paste(zone_blurred, (x1, y1))
    return img

def retouch_simple(image_path):
    """Retouche basique avec flou seulement"""
    print(f"Retouching {image_path}...")
    
    try:
        # Restaurer depuis le backup si disponible
        backup = image_path.replace('.jpeg', '_backup.jpeg')
        if os.path.exists(backup):
            shutil.copy(backup, image_path)
            print(f"  Restored from backup: {backup}")
        
        img = Image.open(image_path)
        w, h = img.size
        print(f"  Image size: {w}x{h}")
        
        result = img.copy()
        
        # Flouter le bas (sac) - flou très fort
        print("  Blurring bottom (trash zone)...")
        result = blur_zone(result, 0, int(h * 0.85), w, h, radius=30)
        
        # Flouter les 4 coins (peinture) - flou moyen
        print("  Blurring corners...")
        corner = int(min(w, h) * 0.1)
        result = blur_zone(result, 0, 0, corner, corner, radius=20)  # top-left
        result = blur_zone(result, w - corner, 0, w, corner, radius=20)  # top-right
        result = blur_zone(result, 0, h - corner, corner, h, radius=20)  # bottom-left
        result = blur_zone(result, w - corner, h - corner, w, h, radius=20)  # bottom-right
        
        # Flouter la zone gens (milieu) - flou doux
        print("  Blurring people zone...")
        result = blur_zone(
            result,
            int(w * 0.15), int(h * 0.35),
            int(w * 0.85), int(h * 0.75),
            radius=15
        )
        
        # Sauvegarder
        result.save(image_path, 'JPEG', quality=95)
        print(f"  ✓ Done: {image_path}")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Images à retoucher
images = [
    'image16avant.jpeg',
    'image20apres.jpeg',
    'image28apres.jpeg',
    'image29avant.jpeg'
]

os.chdir(os.path.expanduser('~/Documents/web/chantier/renovation-site/assets'))

print("\n" + "="*50)
print("RETOUCHE SIMPLE (flou seulement)")
print("="*50 + "\n")

for img in images:
    if os.path.exists(img):
        retouch_simple(img)
    else:
        print(f"✗ Not found: {img}")

print("\n" + "="*50)
print("Done!")
print("="*50 + "\n")
