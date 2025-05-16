import os
import shutil
import random
from math import floor

def split_dataset(src_dir, dest_dir, train_ratio=0.7, val_ratio=0.15):
    all_files = []

    for root, _, files in os.walk(src_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, src_dir)
            all_files.append(rel_path)

    random.shuffle(all_files)

    n_total = len(all_files)
    n_train = floor(n_total * train_ratio)
    n_val = floor(n_total * val_ratio)

    train_files = all_files[:n_train]
    val_files = all_files[n_train:n_train + n_val]
    test_files = all_files[n_train + n_val:]

    for split_name, split_files in zip(['train', 'val', 'test'], [train_files, val_files, test_files]):
        for rel_path in split_files:
            src_file = os.path.join(src_dir, rel_path)
            dst_file = os.path.join(dest_dir, split_name, rel_path)
            dst_dir_path = os.path.dirname(dst_file)
            os.makedirs(dst_dir_path, exist_ok=True)
            shutil.copy2(src_file, dst_file)

split_dataset("raw_data", "data/rocks")
