#!/usr/bin/env python3
import argparse
import csv
import json
import sys
from pathlib import Path
from PIL import Image

def image_size(image_path):
    with Image.open(image_path) as img: return img.width, img.height

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--splits", nargs="+", default=["train", "val", "test"])
    args = parser.parse_args()
    if args.out is None: args.out = args.root / "annotations"
    args.out.mkdir(parents=True, exist_ok=True)

    tomatoes_dir = args.root / "tomatoes"
    with open(tomatoes_dir / "labelmap.json", 'r') as f: labelmap = json.load(f)
    
    for split in args.splits:
        print(f"Generating COCO for split: {split}")
        # Simplification: only color variant for now, or could iterate all
        for variant in ['color', 'grayscale', 'without_augmentation', 'with_augmentation']:
            images, anns = [], []
            img_id, ann_id = 1, 1
            for sub_dir in tomatoes_dir.iterdir():
                if not sub_dir.is_dir() or sub_dir.name == 'sets': continue
                var_dir = sub_dir / variant
                if not var_dir.exists(): continue
                split_f = var_dir / "sets" / f"{split}.txt"
                if not split_f.exists(): continue
                with open(split_f, 'r') as f: stems = [line.strip() for line in f if line.strip()]
                for stem in stems:
                    img_path = var_dir / "images" / f"{stem}.JPG"
                    if not img_path.exists(): img_path = var_dir / "images" / f"{stem}.jpg"
                    if not img_path.exists(): continue
                    w, h = image_size(img_path)
                    images.append({"id": img_id, "file_name": f"tomatoes/{sub_dir.name}/{variant}/images/{img_path.name}", "width": w, "height": h})
                    csv_f = var_dir / "csv" / f"{stem}.csv"
                    if csv_f.exists():
                        with open(csv_f, 'r') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                x, y, width, height = int(row['x']), int(row['y']), int(row['width']), int(row['height'])
                                label = int(row['label'])
                                anns.append({"id": ann_id, "image_id": img_id, "category_id": label, "bbox": [x, y, width, height], "area": width*height, "iscrowd": 0})
                                ann_id += 1
                    img_id += 1
            
            if images:
                coco = {
                    "info": {"description": f"PlantVillage Tomato {variant} {split}"},
                    "images": images,
                    "annotations": anns,
                    "categories": [{"id": item['label_id'], "name": item['object_name'], "supercategory": "tomato"} for item in labelmap if item['object_id'] != 0]
                }
                out_f = args.out / f"tomatoes_{variant}_{split}.json"
                with open(out_f, 'w') as f: json.dump(coco, f, indent=2)
                print(f"  Created {out_f.name}")

if __name__ == "__main__": main()
