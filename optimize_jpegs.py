#!/usr/bin/env python3
import sys
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    from PIL import Image, ImageEnhance
    print("PIL trouvé!")
    
    import os
    assets_dir = "/mnt/c/Users/asseman/Documents/web/chantier/renovation-site/assets"
    
    print("🖼️  Optimisation des images JPEG...\n")
    
    for i in range(16, 30):
        img_path = f"{assets_dir}/image{i}.jpeg"
        if os.path.exists(img_path):
            img = Image.open(img_path)
            
            # Améliorer contraste
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            # Augmenter saturation
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.15)
            
            # Légère augmentation de luminosité
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.05)
            
            # Augmenter la netteté
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.2)
            
            # Sauvegarder
            img.save(img_path, quality=92, optimize=True)
            print(f"✓ image{i}.jpeg")
    
    print("\n✅ Optimisation terminée!")
    
except ImportError:
    print("PIL non disponible, images gardées en l'état")
