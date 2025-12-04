# 🎵 Audio Converter

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FFmpeg Required](https://img.shields.io/badge/FFmpeg-required-red.svg)](https://ffmpeg.org/)

**Suite d'outils Python pour la conversion et le téléchargement audio/vidéo**

Collection de scripts CLI professionnels pour :
- 🎬 Convertir des MP4 en MP3 haute qualité (parallèle)
- 🔍 Rechercher des vidéos YouTube depuis des noms de fichiers
- ⬇️ Télécharger des MP3 depuis YouTube en batch

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
  - [Convertir MP4 → MP3](#1-convertir-mp4--mp3)
  - [Rechercher sur YouTube](#2-rechercher-sur-youtube)
  - [Télécharger depuis YouTube](#3-télécharger-depuis-youtube)
- [Workflow complet](#-workflow-complet)
- [Configuration avancée](#-configuration-avancée)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Fonctionnalités

### 🎬 **audio_converter.py** - Conversion MP4 → MP3
- ✅ Conversion batch haute qualité (320 kbps par défaut)
- ✅ Traitement parallèle ultra-rapide (jusqu'à 50 threads)
- ✅ Préservation des métadonnées
- ✅ Gestion intelligente des erreurs
- ✅ Interface CLI intuitive

### 🔍 **youtube_search.py** - Recherche YouTube
- ✅ Recherche automatique depuis noms de fichiers MP4
- ✅ Nettoyage intelligent des noms (emojis, caractères spéciaux)
- ✅ Génération de fichiers de liens
- ✅ Rapport détaillé (trouvés/non trouvés)
- ✅ Rate limiting intégré

### ⬇️ **download_mp3.py** - Téléchargement YouTube
- ✅ Téléchargement batch depuis fichier de liens
- ✅ Meilleure qualité audio disponible
- ✅ Gestion automatique des échecs
- ✅ Sauvegarde des liens échoués
- ✅ Support multi-formats YouTube

---

## 🔧 Prérequis

### Systèmes supportés
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+, Debian, Fedora, Arch)

### Dépendances système

#### **FFmpeg** (obligatoire pour audio_converter.py)

**Ubuntu/Debian :**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS :**
```bash
brew install ffmpeg
```

**Windows :**
1. Télécharger depuis [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extraire et ajouter au PATH système
3. Vérifier : `ffmpeg -version`

**Fedora :**
```bash
sudo dnf install ffmpeg
```

**Arch Linux :**
```bash
sudo pacman -S ffmpeg
```

#### **Python 3.8+** (obligatoire)
Vérifier votre version :
```bash
python --version
# ou
python3 --version
```

---

## 📦 Installation

### Installation rapide

```bash
# Cloner le repo
git clone https://github.com/a-dera/audio_converter.git
cd audio-converter

# Installer les dépendances Python
pip install -r requirements.txt

# Vérifier FFmpeg
ffmpeg -version
```

### Installation des dépendances Python uniquement

```bash
pip install yt-dlp
```

---

## 🚀 Utilisation

### 1. Convertir MP4 → MP3

**Conversion simple :**
```bash
python audio_converter.py /chemin/vers/videos
```

**Conversion avec options :**
```bash
# Dossier de sortie personnalisé
python audio_converter.py /videos -o /music

# Bitrate personnalisé (256 kbps)
python audio_converter.py /videos -b 256k

# Sample rate 48kHz
python audio_converter.py /videos -r 48000

# Mode séquentiel (désactive parallèle)
python audio_converter.py /videos --sequential
```

**Paramètres :**
- `input_folder` : Dossier contenant les MP4 (obligatoire)
- `-o, --output` : Dossier de sortie (défaut : `input_folder/mp3_output`)
- `-b, --bitrate` : Débit audio (défaut : `320k`)
- `-r, --sample-rate` : Fréquence d'échantillonnage (défaut : `44100`)
- `-s, --sequential` : Désactive le traitement parallèle

**Exemple de sortie :**
```
==================================================
🎬 MP4 to MP3 Converter - Haute Qualité
==================================================
✅ FFmpeg détecté

📂 Dossier source: D:\Videos
📁 Dossier sortie: D:\Videos\mp3_output
🎵 Fichiers à convertir: 25
🎚️  Qualité: 320k @ 44100Hz
⚡ Mode parallèle
--------------------------------------------------
✅ video1.mp4 → video1.mp3
✅ video2.mp4 → video2.mp3
...

==================================================
📊 RÉSUMÉ
==================================================
   Total:    25 fichier(s)
   Réussis:  25 ✅
   Échoués:  0 ❌

✨ Conversion terminée avec succès!
```

---

### 2. Rechercher sur YouTube

**Recherche depuis noms de fichiers MP4 :**
```bash
python youtube_search.py /chemin/vers/videos
```

**Avec fichier de sortie personnalisé :**
```bash
python youtube_search.py /chemin/vers/videos mes_liens.txt
```

**Paramètres :**
- `dossier_mp4` : Dossier contenant les MP4 (obligatoire)
- `fichier_sortie.txt` : Nom du fichier de sortie (défaut : `youtube_links.txt`)

**Exemple de sortie :**
```
============================================================
🔍 Recherche YouTube à partir des noms de fichiers MP4
============================================================

📂 Dossier: D:\Downloads\videos\leger
🎵 Fichiers trouvés: 15
📄 Fichier de sortie: youtube_links.txt
------------------------------------------------------------

[1/15] 🔎 Recherche: Livre audio - Le Petit Prince.mp4...
    Query: Livre audio Le Petit Prince...
    ✅ Trouvé: https://www.youtube.com/watch?v=xxxxx

[2/15] 🔎 Recherche: Audio - Les Misérables.mp4...
    Query: Audio Les Misérables...
    ✅ Trouvé: https://www.youtube.com/watch?v=yyyyy

...

============================================================
📊 RÉSUMÉ
============================================================
   Total fichiers:  15
   Liens trouvés:   13 ✅
   Non trouvés:     2 ❌

✅ Fichier complet: youtube_links.txt
✅ Liens uniquement: youtube_links_links_only.txt
```

**Fichiers générés :**
- `youtube_links.txt` : Tous les résultats (avec commentaires pour non trouvés)
- `youtube_links_links_only.txt` : Uniquement les liens valides

---

### 3. Télécharger depuis YouTube

**Téléchargement depuis fichier de liens :**
```bash
python download_mp3.py youtube_links.txt
```

**Avec dossier de sortie personnalisé :**
```bash
python download_mp3.py youtube_links.txt D:/Downloads/mp3
```

**Paramètres :**
- `fichier_liens.txt` : Fichier contenant les liens YouTube (obligatoire)
- `dossier_sortie` : Dossier de destination (défaut : `./mp3_downloads`)

**Format du fichier de liens :**
```txt
# Mes vidéos YouTube
https://www.youtube.com/watch?v=xxxxx
https://www.youtube.com/watch?v=yyyyy
# Commentaires ignorés
https://www.youtube.com/watch?v=zzzzz
```

**Exemple de sortie :**
```
============================================================
🎵 Téléchargement YouTube → MP3
============================================================

📄 Fichier source: youtube_links.txt
📁 Dossier sortie: D:\Downloads\mp3
🔗 Liens à télécharger: 10
------------------------------------------------------------

[1/10] ⬇️  Téléchargement...
    URL: https://www.youtube.com/watch?v=xxxxx
    ✅ Succès!

[2/10] ⬇️  Téléchargement...
    URL: https://www.youtube.com/watch?v=yyyyy
    ✅ Succès!

...

============================================================
📊 RÉSUMÉ
============================================================
   Total:    10
   Réussis:  9 ✅
   Échoués:  1 ❌

📁 Fichiers MP3 dans: D:\Downloads\mp3

💾 Liens échoués sauvegardés dans: failed_downloads.txt

✨ Téléchargement terminé!
```

---

## 🔄 Workflow complet

**Cas d'usage : Vous avez des MP4 locaux et voulez retrouver les sources YouTube pour re-télécharger en meilleure qualité**

```bash
# 1. Rechercher les vidéos YouTube correspondantes
python youtube_search.py D:/Videos/livres_audio youtube_links.txt

# 2. Télécharger les MP3 depuis YouTube (meilleure qualité)
python download_mp3.py youtube_links_links_only.txt D:/Music/audiobooks

# 3. (Optionnel) Convertir d'autres MP4 locaux
python audio_converter.py D:/Videos/autres -o D:/Music/converted
```

**Cas d'usage : Conversion batch simple**

```bash
# Convertir tous vos MP4 en MP3 320kbps
python audio_converter.py D:/Downloads/videos
```

---

## ⚙️ Configuration avancée

### Parallélisation

Par défaut, `audio_converter.py` utilise **50 workers** en parallèle.

**Modifier dans le code :**
```python
# audio_converter.py, ligne 19
MAX_WORKERS = 20  # Réduire pour machines moins puissantes
```

**Ou désactiver :**
```bash
python audio_converter.py /videos --sequential
```

### Qualité audio

**Bitrates recommandés :**
- `128k` : Qualité acceptable, fichiers légers
- `192k` : Bonne qualité
- `256k` : Très bonne qualité
- `320k` : Qualité maximale MP3 (par défaut)

**Sample rates courants :**
- `44100` : Standard CD (par défaut)
- `48000` : Standard professionnel
- `96000` : Hi-Res audio (fichiers volumineux)

### Rate limiting YouTube

`youtube_search.py` inclut une pause de **1 seconde** entre requêtes pour éviter les blocages.

**Modifier dans le code :**
```python
# youtube_search.py, ligne 134
time.sleep(1)  # Augmenter si nécessaire
```

---

## 🐛 Dépannage

### Erreur : "FFmpeg n'est pas installé"
**Solution :** Installer FFmpeg (voir [Prérequis](#-prérequis))

### Erreur : "yt-dlp n'est pas installé"
**Solution :**
```bash
pip install yt-dlp
```

### Erreur : "Cannot read property of undefined" ou caractères bizarres
**Solution :** Le script gère déjà l'UTF-8, mais sur Windows :
```bash
chcp 65001  # Active UTF-8 dans PowerShell
python download_mp3.py ...
```

### Téléchargement YouTube échoue (429 Too Many Requests)
**Solution :** Attendre quelques minutes, puis relancer avec le fichier `failed_downloads.txt`

### Conversion très lente
**Solution :** 
- Vérifier que le mode parallèle est actif (pas de `--sequential`)
- Réduire `MAX_WORKERS` si CPU surchargé
- Vérifier espace disque disponible

---

## 🤝 Contributing

Les contributions sont les bienvenues ! 

**Processus :**
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push sur la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

**Guidelines :**
- Code Python 3.8+ avec type hints
- Docstrings pour toutes les fonctions publiques
- Tests unitaires pour nouvelles fonctionnalités
- Suivre PEP 8 (formatage avec `black`)

---

## 📄 License

Distribué sous licence **MIT**. Voir [LICENSE](LICENSE) pour plus d'informations.

---

## 👨‍💻 Auteur

**[A. DERA](https://github.com/a-dera)**

---

## 🙏 Remerciements

- [FFmpeg](https://ffmpeg.org/) - Le couteau suisse du multimedia
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Fork amélioré de youtube-dl
- Communauté Python open-source

---

## 📊 Statistiques

![GitHub stars](https://img.shields.io/github/stars/a-dera/audio_converter?style=social)
![GitHub forks](https://img.shields.io/github/forks/a-dera/audio_converter?style=social)
![GitHub issues](https://img.shields.io/github/issues/a-dera/audio_converter)

---

**⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !**
