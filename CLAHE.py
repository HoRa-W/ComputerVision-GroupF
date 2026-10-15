import numpy as np
import cv2 as cv2
import matplotlib.pyplot as plt

img = cv2.imread("H:\\HK1_2026-2027\\ComputerVision\\ComputerVision40\\anhTest.jpg", cv2.IMREAD_GRAYSCALE)

def clip_histogram(hist, clip_limit):
    """Cắt và phân phối lại lược đồ.
    hist: mảng (L,) số nguyên. Trả về mảng (L,) đã cắt, tổng không đổi."""
    pass
def build_tile_luts(img, grid=(8, 8), clip_limit=2.0):
    """Trả về mảng (Gy, Gx, L) uint8: bảng tra của từng ô."""
    pass
def clahe(img, grid=(8, 8), clip_limit=2.0):
    """CLAHE đầy đủ. img: (H, W) uint8. Trả về (H, W) uint8."""
    pass

print(img)