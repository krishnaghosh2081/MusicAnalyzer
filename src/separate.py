# separate.py — simplified core
import subprocess
from pathlib import Path


def separate(input_path: str, output_dir: str = "./output",
             vocals_only: bool = False, model: str = "htdemucs_6s"):
    """Separate audio into stems using Demucs."""
    
    cmd = ["python", "-m", "demucs",
           "--out", output_dir,
           "-n", model,
           input_path]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Demucs failed: {result.stderr}")
    
    # Flatten output: move from nested path to flat structure
    stem_dir = Path(output_dir) / model / Path(input_path).stem
    for stem_file in stem_dir.glob("*"):
            stem_file.rename(Path(output_dir) / stem_file.name)
            #print("===FileName===",stem_file.name)
            #print("===File===",stem_file)
        
    return {"guitar": str(Path(output_dir) / "guitar.wav")}


