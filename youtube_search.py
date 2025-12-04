#!/usr/bin/env python3
"""
Script pour rechercher les vidéos YouTube à partir des noms de fichiers MP4
et sauvegarder les liens dans un fichier texte.
"""

import os
import sys
import re
import time
from pathlib import Path

try:
    from yt_dlp import YoutubeDL
except ImportError:
    print("❌ yt-dlp n'est pas installé. Installe-le avec: pip install yt-dlp")
    sys.exit(1)


def clean_filename_for_search(filename: str) -> str:
    """Nettoie le nom de fichier pour la recherche YouTube."""
    # Enlever l'extension
    name = Path(filename).stem
    
    # Enlever les emojis et caractères spéciaux
    name = name.encode('ascii', 'ignore').decode('ascii')
    
    # Enlever les caractères problématiques
    name = re.sub(r'[_\-\.\(\)\[\]]+', ' ', name)
    
    # Enlever "Livre audio", "Audio", etc.  pour une meilleure recherche
    # (on les garde car ça aide à trouver la bonne vidéo)
    
    # Nettoyer les espaces multiples
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name


def search_youtube(query: str, max_results: int = 1) -> str | None:
    """Recherche une vidéo sur YouTube et retourne le lien."""
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'default_search': 'ytsearch',
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Rechercher sur YouTube
            result = ydl. extract_info(f"ytsearch{max_results}:{query}", download=False)
            
            if result and 'entries' in result and result['entries']:
                first_result = result['entries'][0]
                video_id = first_result. get('id')
                if video_id:
                    return f"https://www.youtube.com/watch? v={video_id}"
    except Exception as e:
        print(f"   ⚠️ Erreur de recherche: {e}")
    
    return None


def get_mp4_files(folder: Path) -> list[Path]:
    """Récupère tous les fichiers MP4 du dossier."""
    mp4_files = list(folder.glob("*.mp4")) + list(folder. glob("*.MP4"))
    return sorted(mp4_files)


def main():
    # Configuration
    if len(sys.argv) < 2:
        print("Usage: python youtube_search.py <dossier_mp4> [fichier_sortie.txt]")
        print("Exemple: python youtube_search.py D:/Downloads/videos/leger")
        sys.exit(1)
    
    input_folder = Path(sys. argv[1])
    output_file = sys.argv[2] if len(sys.argv) > 2 else "youtube_links.txt"
    
    if not input_folder. exists():
        print(f"❌ Le dossier '{input_folder}' n'existe pas.")
        sys.exit(1)
    
    print("=" * 60)
    print("🔍 Recherche YouTube à partir des noms de fichiers MP4")
    print("=" * 60)
    
    mp4_files = get_mp4_files(input_folder)
    
    if not mp4_files:
        print(f"⚠️ Aucun fichier MP4 trouvé dans '{input_folder}'")
        sys.exit(1)
    
    print(f"\n📂 Dossier: {input_folder. absolute()}")
    print(f"🎵 Fichiers trouvés: {len(mp4_files)}")
    print(f"📄 Fichier de sortie: {output_file}")
    print("-" * 60)
    
    results = []
    found = 0
    not_found = 0
    
    for i, mp4_file in enumerate(mp4_files, 1):
        filename = mp4_file.name
        search_query = clean_filename_for_search(filename)
        
        print(f"\n[{i}/{len(mp4_files)}] 🔎 Recherche: {filename[:50]}...")
        print(f"    Query: {search_query[:60]}...")
        
        # Rechercher sur YouTube
        link = search_youtube(search_query)
        
        if link:
            found += 1
            print(f"    ✅ Trouvé: {link}")
            results.append({
                'filename': filename,
                'query': search_query,
                'link': link
            })
        else:
            not_found += 1
            print(f"    ❌ Non trouvé")
            results.append({
                'filename': filename,
                'query': search_query,
                'link': None
            })
        
        # Pause pour éviter d'être bloqué par YouTube
        time.sleep(1)
    
    # Sauvegarder les résultats
    print("\n" + "=" * 60)
    print("💾 Sauvegarde des résultats...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f. write("# Liens YouTube trouvés\n")
        f.write(f"# Généré à partir de: {input_folder.absolute()}\n")
        f.write(f"# Total: {found} trouvés / {len(mp4_files)} fichiers\n")
        f.write("#" + "=" * 58 + "\n\n")
        
        for r in results:
            if r['link']:
                f.write(f"{r['link']}\n")
            else:
                f.write(f"# NON TROUVÉ: {r['filename']}\n")
    
    # Créer aussi un fichier avec seulement les liens valides
    links_only_file = output_file.replace('.txt', '_links_only.txt')
    with open(links_only_file, 'w', encoding='utf-8') as f:
        for r in results:
            if r['link']:
                f. write(f"{r['link']}\n")
    
    print(f"\n✅ Fichier complet: {output_file}")
    print(f"✅ Liens uniquement: {links_only_file}")
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    print(f"   Total fichiers:  {len(mp4_files)}")
    print(f"   Liens trouvés:   {found} ✅")
    print(f"   Non trouvés:     {not_found} ❌")
    
    if not_found > 0:
        print("\n⚠️ Fichiers non trouvés:")
        for r in results:
            if not r['link']:
                print(f"   - {r['filename'][:50]}...")


if __name__ == "__main__":
    main()