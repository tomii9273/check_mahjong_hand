import shutil

kinds_before = ["man", "pin", "sou", "ji"]
kinds_after = ["m", "p", "s", "z"]

for i in range(4):
    rng = range(1, 10) if i != 3 else range(1, 8)  # 字牌のみ7種類
    for j in rng:
        shutil.copyfile(f"imgs_raw/{kinds_before[i]}{j}-66-90-l.png", f"imgs/{j}{kinds_after[i]}.png")
