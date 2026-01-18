# AAR - Les Artisans Associés de la Rénovation

Site web professionnel pour présenter les services et réalisations de rénovation.

## 🔒 Sécurité

Ce site est configuré avec les meilleures pratiques de sécurité:

- ✅ Headers HTTP de sécurité (CSP, X-Frame-Options, etc.)
- ✅ HTTPS forcé
- ✅ Protection contre XSS et CSRF
- ✅ Validation serveur des formulaires
- ✅ Rate limiting
- ✅ Compression GZIP
- ✅ Cache Control
- ✅ Fichiers sensibles protégés

## 📋 Déploiement

### Prérequis
- Serveur Apache avec mod_rewrite activé
- PHP 7.4+ avec mail() configuré
- Certificat SSL/TLS (HTTPS)

### Installation

1. **Télécharger les fichiers**
   ```bash
   git clone https://github.com/aarenovation/site.git
   cd renovation-site
   ```

2. **Configuration .env**
   ```bash
   cp .env.example .env
   # Éditer .env avec les bonnes valeurs
   ```

3. **Permissions des fichiers**
   ```bash
   chmod 644 .htaccess
   chmod 755 ./
   chmod 755 ./css
   chmod 755 ./js
   chmod 755 ./assets
   ```

4. **Configurer Apache**
   - Activer mod_rewrite: `a2enmod rewrite`
   - Activer mod_expires: `a2enmod expires`
   - Activer mod_headers: `a2enmod headers`
   - Redémarrer: `systemctl restart apache2`

5. **Vérifier l'installation**
   - Visiter https://votre-domaine.fr
   - Vérifier les headers de sécurité sur https://securityheaders.com
   - Tester les performances sur https://pagespeed.web.dev

## 📁 Structure

```
renovation-site/
├── index.html              # Page principale
├── css/
│   └── styles.css         # Styles
├── js/
│   └── app.js             # Scripts
├── assets/
│   └── [images & vidéo]   # Médias
├── .htaccess              # Configuration Apache
├── robots.txt             # SEO
├── sitemap.xml            # SEO
├── 404.html               # Page d'erreur
├── process_contact.php    # Traitement contact
└── .env                   # Variables sensibles (git ignored)
```

## 📞 Formulaire de Contact

Le formulaire envoie les messages via email avec:
- ✅ Validation côté serveur
- ✅ Sanitisation des inputs
- ✅ Protection anti-spam (rate limiting)
- ✅ Email de confirmation envoyé au client
- ✅ Email d'alerte envoyé à l'admin

### Utiliser SMTP (recommandé)

La configuration par défaut utilise `mail()` de PHP. Pour plus de fiabilité, installez PHPMailer via Composer et configurez les variables SMTP.

1. Installer Composer si nécessaire.
2. Dans le répertoire du projet :

```bash
composer require phpmailer/phpmailer
```

3. Mettre à jour `process_contact.php` pour définir les constantes SMTP (exemple) :

```php
define('SMTP_HOST', 'smtp.example.com');
define('SMTP_PORT', 587);
define('SMTP_USER', 'user@example.com');
define('SMTP_PASS', 'secret');
```

PHPMailer sera utilisé automatiquement si la dépendance est installée.

### Générer WebP pour les images

Le dépôt inclut des scripts d'optimisation (`optimize_jpegs.py`, `optimize_images.sh`). Pour générer des versions WebP :

```bash
# Linux / WSL
./optimize_images.sh
# ou
python3 optimize_jpegs.py --webp assets/
```

Après génération, je peux mettre à jour les balises `<picture>` dans `index.html` pour utiliser WebP en priorité tout en gardant les originaux.

### Conversion automatique WebP + patch HTML

J'ai ajouté un script pratique `scripts/create_webp_and_patch.sh` qui :
- Convertit les images `assets/*.(png|jpg|jpeg)` en WebP (utilise `magick` ou `cwebp` si installés).
- Patch automatiquement `index.html` et `avant-apres.html` pour insérer des balises `<picture>` pointant vers les WebP lorsque disponibles.

Exécution (depuis la racine du projet, WSL ou Linux recommandé) :

```bash
chmod +x scripts/create_webp_and_patch.sh
./scripts/create_webp_and_patch.sh
```

Remarques :
- Installe `ImageMagick` (commande `magick`) ou `libwebp` (`cwebp`) si nécessaire.
- Si tu préfères, je peux exécuter ces commandes sur ta machine (fournis accès), ou tu les lances en local.

## 🔑 Variables d'Environnement

```
CONTACT_EMAIL=aarenovation37@gmail.com
RATE_LIMIT=5              # Tentatives par fenêtre
RATE_LIMIT_WINDOW=3600    # En secondes (1 heure)
ENVIRONMENT=production    # ou development
LOG_ERRORS=false          # À false en prod
```

## 📊 SEO

- ✅ Meta tags OpenGraph
- ✅ Meta robots
- ✅ robots.txt (Google, Bing, etc.)
- ✅ sitemap.xml
- ✅ Structure sémantique HTML5

### Soumettre à Google Search Console
1. Aller sur https://search.google.com/search-console
2. Ajouter la propriété
3. Vérifier le domaine
4. Soumettre le sitemap.xml

## 🔐 Checklist avant mise en ligne

- [ ] Certificat SSL/TLS installé
- [ ] HTTPS fonctionne
- [ ] .htaccess en place et chargé
- [ ] Email de contact testé
- [ ] Headers de sécurité vérifiés
- [ ] Images optimisées
- [ ] Cache OK
- [ ] Erreurs console vérifiées (F12)
- [ ] Mobile responsive testé
- [ ] Tous les liens testés

## 📞 Support

Pour toute question de sécurité ou de déploiement, consulter SECURITY_CHECKLIST.md

## 📄 Licences

- Code: Propriétaire
- Médias: Propriétaires

---
Dernière mise à jour: 15 décembre 2025
