# 🌐 Guide d'Hébergement Gratuit

## Options d'hébergement gratuit pour le dashboard

### 🏆 Option 1 : GitHub Pages (Recommandé - Le plus simple)

**Avantages** : Gratuit, facile, domaine .github.io, SSL automatique

```bash
# 1. Créer un repo sur GitHub
# 2. Pousser votre projet
git add .
git commit -m "Add financial analysis dashboard"
git push origin main

# 3. Activer GitHub Pages
# Sur GitHub.com : Settings > Pages
# Source: Deploy from a branch
# Branch: main
# Folder: /docs
# Save

# Votre dashboard sera accessible sur :
# https://[votre-username].github.io/[nom-repo]/
```

**Temps de déploiement** : ~2 minutes

---

### 🚀 Option 2 : Netlify (Drag & Drop)

**Avantages** : Déploiement instantané, domaine personnalisable, SSL automatique

```bash
# 1. Aller sur netlify.com et créer un compte gratuit
# 2. Cliquer sur "Add new site" > "Deploy manually"
# 3. Glisser-déposer le dossier docs/ dans la zone
# 4. Site déployé instantanément !

# URL automatique : https://random-name-12345.netlify.app
# Vous pouvez changer le nom dans Site settings
```

**Temps de déploiement** : ~30 secondes

---

### ⚡ Option 3 : Cloudflare Pages

**Avantages** : Performance mondiale, CDN ultra-rapide, gratuit illimité

#### Méthode A : Via Dashboard (Plus simple)
```bash
# 1. Compte sur pages.cloudflare.com
# 2. "Create a project" > "Connect to Git"
# 3. Sélectionner votre repo GitHub
# 4. Build settings :
#    - Build command: (laisser vide)
#    - Build output directory: docs
# 5. "Save and Deploy"

# URL : https://finance-dashboard.pages.dev
```

#### Méthode B : Via CLI
```bash
# Installer Wrangler
npm install -g wrangler

# Se connecter
wrangler login

# Déployer
cd docs
wrangler pages publish . --project-name=finance-dashboard

# URL : https://finance-dashboard.pages.dev
```

**Temps de déploiement** : ~1 minute

---

### 📦 Option 4 : Render

**Avantages** : Déploiement automatique à chaque commit

```bash
# 1. Compte sur render.com
# 2. "New" > "Static Site"
# 3. Connecter votre repo GitHub
# 4. Settings :
#    - Name: finance-dashboard
#    - Branch: main
#    - Publish directory: docs
# 5. "Create Static Site"

# URL : https://finance-dashboard.onrender.com
# Se met à jour automatiquement à chaque push !
```

**Temps de déploiement** : ~2-3 minutes

---

### 🎯 Option 5 : GitLab Pages

**Avantages** : Alternative à GitHub, même simplicité

```bash
# 1. Créer repo sur gitlab.com
# 2. Créer fichier .gitlab-ci.yml :

pages:
  stage: deploy
  script:
    - echo "Deploying pages"
  artifacts:
    paths:
      - docs
  only:
    - main

# 3. Push
git add .
git commit -m "Add dashboard"
git push

# URL : https://[username].gitlab.io/[repo-name]/
```

---

## 📊 Comparaison

| Service | Vitesse | Facilité | Domaine custom | SSL |
|---------|---------|----------|----------------|-----|
| **GitHub Pages** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ |
| **Netlify** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ |
| **Cloudflare** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ |
| **Render** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ |
| **GitLab** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ |

---

## 💡 Recommandation

Pour votre portfolio :
- **GitHub Pages** : Le plus simple, intégration parfaite avec GitHub
- **Netlify** : Si vous voulez un nom de domaine plus pro
- **Cloudflare** : Si vous voulez la meilleure performance mondiale

**Tous sont 100% gratuits et sans limite de bande passante !**

---

## 🔧 Domaine Personnalisé (Optionnel)

Si vous avez un nom de domaine (ex: acheter sur Namecheap ~10$/an) :

### Pour GitHub Pages :
```bash
# 1. Créer fichier docs/CNAME avec :
dashboard.votredomaine.com

# 2. Dans votre DNS, ajouter :
# Type: CNAME
# Name: dashboard
# Value: username.github.io
```

### Pour Netlify/Cloudflare/Render :
```bash
# Dans les settings du service :
# Custom domain > Add custom domain
# Suivre les instructions DNS
```

---

## ✅ Checklist avant déploiement

- [ ] Dashboard généré dans `docs/index.html`
- [ ] Testé localement (http://localhost:8080)
- [ ] Fichiers inutiles supprimés
- [ ] README.md à jour
- [ ] Git repo initialisé

---

**Prêt à déployer !** 🚀
