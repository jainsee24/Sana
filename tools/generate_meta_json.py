import argparse
import json
import os
from typing import List


def collect_image_basenames(directory: str, extension: str) -> List[str]:
    """Return sorted list of basenames for image files with matching txt files."""
    basenames = []
    for entry in os.listdir(directory):
        if entry.lower().endswith(extension.lower()):
            base = os.path.splitext(entry)[0]
            if os.path.isfile(os.path.join(directory, base + ".txt")):
                basenames.append(base)
    basenames.sort()
    return basenames


def generate_metadata(directory: str, extension: str = ".png", output: str = None) -> None:
    """Generate meta_data.json for SanaImgDataset."""
    if output is None:
        output = os.path.join(directory, "meta_data.json")
    img_names = collect_image_basenames(directory, extension)
    metadata = {
        "name": os.path.basename(os.path.abspath(directory)),
        "__kind__": "Sana-ImgDataset",
        "img_names": img_names,
    }
    with open(output, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    print(f"Saved {len(img_names)} entries to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate meta_data.json for SanaImgDataset")
    parser.add_argument("data_dir", help="Directory containing <image><extension> and <image>.txt pairs")
    parser.add_argument("--ext", default=".png", help="Image file extension (default: .png)")
    parser.add_argument("--out", default=None, help="Output meta_data.json path")
    args = parser.parse_args()

    generate_metadata(args.data_dir, args.ext, args.out)
