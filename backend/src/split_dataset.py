import os
import shutil
import random
from math import floor


def split_dataset(src_dir, dest_dir, train_ratio=0.7, val_ratio=0.15):
    classes = os.listdir(src_dir)

    for cls in classes:
        files = os.listdir(os.path.join(src_dir, cls))
        random.shuffle(files)

        n_total = len(files)
        n_train = floor(n_total * train_ratio)
        n_val = floor(n_total * val_ratio)

        train_files = files[:n_train]
        val_files = files[n_train : n_train + n_val]
        test_files = files[n_train + n_val :]

        for split_name, split_files in zip(
            ["train", "val", "test"], [train_files, val_files, test_files]
        ):
            dest_class_dir = os.path.join(dest_dir, split_name, cls)
            os.makedirs(dest_class_dir, exist_ok=True)
            for fname in split_files:
                src_file = os.path.join(src_dir, cls, fname)
                dst_file = os.path.join(dest_class_dir, fname)
                shutil.copy2(src_file, dst_file)


split_dataset("../raw_images", "../data")
