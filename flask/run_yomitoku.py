
import cv2
import os

from yomitoku import OCR
from yomitoku.data.functions import load_image

def run_yomitoku(src_image, output_dir):
    print("処理を開始。。。。")
    ocr = OCR(visualize=True, device="cpu")
    # PDFファイルを読み込み
    imgs = load_image(src_image)
    import time

    start = time.time()
    results, ocr_vis = ocr(imgs[0])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created.")
    else:
        print(f"Directory '{output_dir}' already exists.")

    json_fname  = 'ocr.json'
    json_fname = os.path.join(output_dir, json_fname)
    jpg_fname  = 'ocr.jpg'
    jpg_fname = os.path.join(output_dir, jpg_fname)

    results.to_json(json_fname)
    cv2.imwrite(jpg_fname, ocr_vis)
    return 0
    