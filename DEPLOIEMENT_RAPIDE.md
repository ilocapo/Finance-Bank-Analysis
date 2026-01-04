# 🚀 Déploiement Rapide - 3 Minutes

## Option la plus simple : GitHub Pages

### Étape 1 : Créer le repo GitHub (1 min)
```bash
# Sur github.com :
# 1. Cliquer "New repository"
# 2. Nom : finance-banks-analysis
# 3. Public
# 4. Create repository
```

### Étape 2 : Pousser le code (1 min)
```bash
cd /home/ilona/Documents/Portofolio/finance-banks-analysis

# Initialiser si nécessaire
git init
git add .
git commit -m "Dashboard financier banques françaises"

# Lier au repo GitHub
git remote add origin https://github.com/[USERNAME]/finance-banks-analysis.git
git branch -M main
git push -u origin main
```

### Étape 3 : Activer GitHub Pages (1 min)
```bash
# Sur GitHub.com, dans votre repo :
# 1. Settings (onglet en haut)
# 2. Pages (menu gauche)
# 3. Source : Deploy from a branch
# 4. Branch : main
# 5. Folder : /docs
# 6. Save

# ✅ Attendre 1-2 minutes
# Votre site sera sur : https://[USERNAME].github.io/finance-banks-analysis/
```

## ✨ C'est tout !

Votre dashboard est maintenant en ligne, accessible 24/7, gratuitement !

---

## Alternative ultra-rapide : Netlify (30 secondes)

```bash
# 1. netlify.com > Sign up (gratuit)
# 2. "Add new site" > "Deploy manually"  
# 3. Glisser-déposer le dossier docs/
# 4. ✅ Site en ligne !

# URL : https://[random-name].netlify.app
# Renommer dans Site settings
```

---

Pour plus d'options, voir HEBERGEMENT.md
