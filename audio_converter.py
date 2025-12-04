#!/usr/bin/env python3
"""
MP4 to MP3 Converter - Script autonome
Convertit tous les fichiers MP4 d'un dossier en MP3 haute qualité (320 kbps)

Auteur: Amédée / ELYA DATA INTELLIGENCE
Prérequis: FFmpeg doit être installé sur le système
    - Ubuntu/Debian: sudo apt install ffmpeg
    - macOS: brew install ffmpeg
    - Windows: télécharger depuis https://ffmpeg.org/download.html
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil


# Configuration par défaut
DEFAULT_BITRATE = "320k"
DEFAULT_SAMPLE_RATE = 44100
MAX_WORKERS = 50


def check_ffmpeg():
    """Vérifie si FFmpeg est installé sur le système."""
    if shutil.which("ffmpeg") is None:
        print("❌ ERREUR: FFmpeg n'est pas installé ou n'est pas dans le PATH.")
        print("\nInstallation:")
        print("  - Ubuntu/Debian: sudo apt install ffmpeg")
        print("  - macOS: brew install ffmpeg")
        print("  - Windows: télécharger depuis https://ffmpeg.org/download.html")
        sys.exit(1)
    print("✅ FFmpeg détecté")


def get_mp4_files(input_folder: Path) -> list[Path]:
    """Récupère tous les fichiers MP4 du dossier."""
    mp4_files = list(input_folder.glob("*.mp4")) + list(input_folder.glob("*.MP4"))
    return mp4_files


def convert_mp4_to_mp3(
    input_file: Path,
    output_folder: Path,
    bitrate: str = DEFAULT_BITRATE,
    sample_rate: int = DEFAULT_SAMPLE_RATE
) -> tuple[bool, str, str]:
    """
    Convertit un fichier MP4 en MP3.
    
    Args:
        input_file: Chemin du fichier MP4 source
        output_folder: Dossier de destination
        bitrate: Débit audio (ex: "320k")
        sample_rate: Fréquence d'échantillonnage (ex: 44100)
    
    Returns:
        tuple: (succès, nom_fichier, message)
    """
    output_file = output_folder / f"{input_file.stem}.mp3"
    
    cmd = [
        "ffmpeg",
        "-i", str(input_file),
        "-vn",                      # Pas de vidéo
        "-acodec", "libmp3lame",    # Codec MP3
        "-ab", bitrate,             # Bitrate audio
        "-ar", str(sample_rate),    # Sample rate
        "-ac", "2",                 # Stéréo
        "-q:a", "0",                # Meilleure qualité VBR
        "-y",                       # Écraser si existe
        str(output_file)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, input_file.name, f"→ {output_file.name}"
    except subprocess.CalledProcessError as e:
        return False, input_file.name, f"Erreur: {e.stderr[:100]}"


def convert_batch(
    input_folder: str,
    output_folder: str = None,
    bitrate: str = DEFAULT_BITRATE,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    parallel: bool = True
) -> dict:
    """
    Convertit tous les fichiers MP4 d'un dossier en MP3.
    
    Args:
        input_folder: Dossier source contenant les MP4
        output_folder: Dossier de destination (par défaut: input_folder/mp3_output)
        bitrate: Débit audio
        sample_rate: Fréquence d'échantillonnage
        parallel: Exécution parallèle
    
    Returns:
        dict: Statistiques de conversion
    """
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"❌ ERREUR: Le dossier '{input_folder}' n'existe pas.")
        sys.exit(1)
    
    if not input_path.is_dir():
        print(f"❌ ERREUR: '{input_folder}' n'est pas un dossier.")
        sys.exit(1)
    
    # Dossier de sortie
    if output_folder:
        output_path = Path(output_folder)
    else:
        output_path = input_path / "mp3_output"
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Récupérer les fichiers MP4
    mp4_files = get_mp4_files(input_path)
    
    if not mp4_files:
        print(f"⚠️  Aucun fichier MP4 trouvé dans '{input_folder}'")
        return {"total": 0, "success": 0, "failed": 0}
    
    print(f"\n📂 Dossier source: {input_path.absolute()}")
    print(f"📁 Dossier sortie: {output_path.absolute()}")
    print(f"🎵 Fichiers à convertir: {len(mp4_files)}")
    print(f"🎚️  Qualité: {bitrate} @ {sample_rate}Hz")
    print(f"{'⚡ Mode parallèle' if parallel else '🔄 Mode séquentiel'}")
    print("-" * 50)
    
    stats = {"total": len(mp4_files), "success": 0, "failed": 0}
    
    if parallel and len(mp4_files) > 1:
        # Conversion parallèle
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(
                    convert_mp4_to_mp3, 
                    f, 
                    output_path, 
                    bitrate, 
                    sample_rate
                ): f for f in mp4_files
            }
            
            for future in as_completed(futures):
                success, filename, message = future.result()
                if success:
                    stats["success"] += 1
                    print(f"✅ {filename} {message}")
                else:
                    stats["failed"] += 1
                    print(f"❌ {filename} {message}")
    else:
        # Conversion séquentielle
        for i, mp4_file in enumerate(mp4_files, 1):
            print(f"[{i}/{len(mp4_files)}] Conversion de {mp4_file.name}...", end=" ")
            success, filename, message = convert_mp4_to_mp3(
                mp4_file, 
                output_path, 
                bitrate, 
                sample_rate
            )
            if success:
                stats["success"] += 1
                print(f"✅ {message}")
            else:
                stats["failed"] += 1
                print(f"❌ {message}")
    
    return stats


def main():
    """Point d'entrée principal du script."""
    parser = argparse.ArgumentParser(
        description="Convertit tous les fichiers MP4 d'un dossier en MP3 haute qualité",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python mp4_to_mp3_converter.py /chemin/vers/videos
  python mp4_to_mp3_converter.py /videos -o /music -b 256k
  python mp4_to_mp3_converter.py ./mes_videos --sequential
        """
    )
    
    parser.add_argument(
        "input_folder",
        help="Dossier contenant les fichiers MP4 à convertir"
    )
    
    parser.add_argument(
        "-o", "--output",
        dest="output_folder",
        help="Dossier de destination (par défaut: input_folder/mp3_output)"
    )
    
    parser.add_argument(
        "-b", "--bitrate",
        default=DEFAULT_BITRATE,
        help=f"Débit audio (par défaut: {DEFAULT_BITRATE})"
    )
    
    parser.add_argument(
        "-r", "--sample-rate",
        type=int,
        default=DEFAULT_SAMPLE_RATE,
        help=f"Fréquence d'échantillonnage (par défaut: {DEFAULT_SAMPLE_RATE})"
    )
    
    parser.add_argument(
        "-s", "--sequential",
        action="store_true",
        help="Désactive le traitement parallèle"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🎬 MP4 to MP3 Converter - Haute Qualité")
    print("=" * 50)
    
    # Vérifier FFmpeg
    check_ffmpeg()
    
    # Lancer la conversion
    stats = convert_batch(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        bitrate=args.bitrate,
        sample_rate=args.sample_rate,
        parallel=not args.sequential
    )
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ")
    print("=" * 50)
    print(f"   Total:    {stats['total']} fichier(s)")
    print(f"   Réussis:  {stats['success']} ✅")
    print(f"   Échoués:  {stats['failed']} ❌")
    
    if stats["failed"] > 0:
        sys.exit(1)
    
    print("\n✨ Conversion terminée avec succès!")


if __name__ == "__main__":
    main()