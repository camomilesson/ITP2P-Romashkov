import os
import re

def load_hiscores(file_path, top_n=5):
    if not os.path.exists(file_path):
        return []
    hiscores = []
    with open(file_path, "r") as f:
        for line in f:
            try:
                name, score = line.strip().split(",")
                hiscores.append((name, int(score)))
            except:
                continue
    hiscores.sort(key=lambda x: x[1], reverse=True)
    return hiscores[:top_n]

def save_hiscore(file_path, name, score):
    with open(file_path, "a") as f:
        f.write(f"{name},{score}\n")

def validate_name(name):
    return bool(re.match(r"^[A-Za-z]{1,3}$", name))
