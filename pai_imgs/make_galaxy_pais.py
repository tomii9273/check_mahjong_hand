import cv2
import numpy as np

pai_names = [f"{num}{kind}" for num in range(1, 10) for kind in ["m", "p", "s"]] + [f"{num}z" for num in range(1, 8)]

for pai_name in pai_names:
    file_name = f"imgs/{pai_name}.png"
    img = cv2.imread(file_name, cv2.IMREAD_COLOR)
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imghsv[:, :, 0] = 100  # 水色寄りの青
    imghsv[:, :, 2] = np.clip(imghsv[:, :, 2], 150, 255)  # 真っ白以外の明度を上げる (黒い牌を青くするため)
    imghsv[:, :, 1] = np.where(imghsv[:, :, 2] < 250, 255, imghsv[:, :, 1])  # 白以外の彩度を上げる (黒い牌を青くするため)
    img2 = cv2.cvtColor(imghsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite(f"imgs/{pai_name}g.png", img2)
