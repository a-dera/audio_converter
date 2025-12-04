#!/usr/bin/env python3
"""
Script pour télécharger les vidéos YouTube en MP3 à partir d'un fichier de liens.
"""

import os
import sys
import subprocess
from pathlib import Path


def download_mp3(url: str, output_folder: Path) -> tuple[bool, str]:
    """Télécharge une vidéo YouTube en MP3."""
    
    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",  # Meilleure qualité
        "-o", str(output_folder / "%(title)s.%(ext)s"),
        "--no-playlist",  # Ignorer les playlists
        url
    ]
    
    try:
        result = subprocess. run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            return True, "OK"
        else:
            error = result.stderr.strip()[:100] if result.stderr else "Erreur inconnue"
            return False, error
    except FileNotFoundError:
        return False, "yt-dlp non trouvé.  Installe-le avec: pip install yt-dlp"
    except Exception as e:
        return False, str(e)


def read_links(file_path: str) -> list[str]:
    """Lit les liens YouTube depuis un fichier texte."""
    links = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Ignorer les commentaires et lignes vides
            if line and not line.startswith('#'):
                # Vérifier que c'est bien un lien YouTube
                if 'youtube.com/watch' in line or 'youtu. be/' in line:
                    links.append(line)
    
    return links


def main():
    # Configuration
    if len(sys.argv) < 2:
        print("Usage: python download_mp3.py <fichier_liens.txt> [dossier_sortie]")
        print("Exemple: python download_mp3.py youtube_links.txt D:/Downloads/mp3")
        sys.exit(1)
    
    links_file = sys. argv[1]
    output_folder = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./mp3_downloads")
    
    if not os.path.exists(links_file):
        print(f"❌ Le fichier '{links_file}' n'existe pas.")
        sys.exit(1)
    
    # Créer le dossier de sortie
    output_folder. mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🎵 Téléchargement YouTube → MP3")
    print("=" * 60)
    
    # Lire les liens
    links = read_links(links_file)
    
    if not links:
        print(f"⚠️ Aucun lien YouTube valide trouvé dans '{links_file}'")
        sys. exit(1)
    
    print(f"\n📄 Fichier source: {links_file}")
    print(f"📁 Dossier sortie: {output_folder. absolute()}")
    print(f"🔗 Liens à télécharger: {len(links)}")
    print("-" * 60)
    
    success = 0
    failed = 0
    failed_urls = []
    
    for i, url in enumerate(links, 1):
        print(f"\n[{i}/{len(links)}] ⬇️  Téléchargement...")
        print(f"    URL: {url}")
        
        ok, message = download_mp3(url, output_folder)
        
        if ok:
            success += 1
            print(f"    ✅ Succès!")
        else:
            failed += 1
            failed_urls.append(url)
            print(f"    ❌ Échec: {message}")
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    print(f"   Total:    {len(links)}")
    print(f"   Réussis:  {success} ✅")
    print(f"   Échoués:  {failed} ❌")
    print(f"\n📁 Fichiers MP3 dans: {output_folder. absolute()}")
    
    if failed_urls:
        print("\n⚠️ Liens échoués:")
        for url in failed_urls:
            print(f"   - {url}")
        
        # Sauvegarder les liens échoués
        failed_file = "failed_downloads.txt"
        with open(failed_file, 'w', encoding='utf-8') as f:
            for url in failed_urls:
                f.write(f"{url}\n")
        print(f"\n💾 Liens échoués sauvegardés dans: {failed_file}")
    
    print("\n✨ Téléchargement terminé!")


if __name__ == "__main__":
    main()