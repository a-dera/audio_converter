# Exemple : Conversion basique MP4 → MP3

## 🎯 Objectif

Convertir tous vos fichiers MP4 en MP3 haute qualité (320 kbps).

## 📋 Prérequis

- FFmpeg installé
- Fichiers MP4 dans un dossier

## 🚀 Steps

### 1. Préparer vos fichiers

Organisez vos MP4 dans un dossier :

```
D:/Videos/
├── video1.mp4
├── video2.mp4
├── video3.mp4
└── ...
```

### 2. Lancer la conversion

**Commande simple :**
```bash
python audio_converter.py D:/Videos
```

**Sortie :**
```
==================================================
🎬 MP4 to MP3 Converter - Haute Qualité
==================================================
✅ FFmpeg détecté

📂 Dossier source: D:\Videos
📁 Dossier sortie: D:\Videos\mp3_output
🎵 Fichiers à convertir: 3
🎚️  Qualité: 320k @ 44100Hz
⚡ Mode parallèle
--------------------------------------------------
✅ video1.mp4 → video1.mp3
✅ video2.mp4 → video2.mp3
✅ video3.mp4 → video3.mp3

==================================================
📊 RÉSUMÉ
==================================================
   Total:    3 fichier(s)
   Réussis:  3 ✅
   Échoués:  0 ❌

✨ Conversion terminée avec succès!
```

### 3. Vérifier les résultats

Les MP3 sont créés dans :
```
D:/Videos/mp3_output/
├── video1.mp3
├── video2.mp3
└── video3.mp3
```

## ⚙️ Options avancées

### Dossier de sortie personnalisé

```bash
python audio_converter.py D:/Videos -o D:/Music
```

### Qualité moyenne (fichiers plus légers)

```bash
# 192 kbps au lieu de 320 kbps
python audio_converter.py D:/Videos -b 192k
```

### Sample rate professionnel (48kHz)

```bash
python audio_converter.py D:/Videos -r 48000
```

### Mode séquentiel (si problèmes de mémoire)

```bash
python audio_converter.py D:/Videos --sequential
```

## 🔍 Vérification qualité

Vérifier le bitrate d'un MP3 généré :

**Windows (PowerShell) :**
```powershell
ffprobe D:\Videos\mp3_output\video1.mp3 2>&1 | Select-String "bitrate"
```

**Linux/macOS :**
```bash
ffprobe D:/Videos/mp3_output/video1.mp3 2>&1 | grep bitrate
```

Vous devriez voir : `bitrate: 320 kb/s`

## 💡 Astuces

### Conversion récursive (sous-dossiers)

Actuellement pas supporté. Workaround :

```bash
# Trouver tous les MP4 et les copier dans un seul dossier
# Puis lancer la conversion
```

### Batch de gros fichiers (>1GB)

Le mode parallèle gère automatiquement. Si problèmes de RAM :

```bash
python audio_converter.py D:/Videos --sequential
```

### Noms de fichiers avec espaces/accents

Aucun problème, le script gère l'UTF-8 nativement :

```
✅ "Livre audio - À la recherche du temps perdu.mp4"
✅ "🎵 Ma chanson préférée.mp4"
```

## 🐛 Dépannage

### Erreur : "FFmpeg n'est pas installé"

Installer FFmpeg (voir README principal).

### Conversion très lente

- Vérifier que le mode parallèle est actif (pas de `--sequential`)
- Vérifier espace disque disponible
- Vérifier que le CPU n'est pas surchargé par d'autres apps

### Fichiers MP3 vides ou corrompus

Vérifier que les MP4 sources ne sont pas corrompus :

```bash
ffmpeg -v error -i video.mp4 -f null -
```

Si erreurs affichées, le MP4 source est corrompu.

---

**🎉 Félicitations !** Vous savez maintenant convertir vos MP4 en MP3 !

**Next steps :**
- [Workflow complet YouTube](batch_workflow.md)
- [Utilisation avancée](advanced_usage.md)
