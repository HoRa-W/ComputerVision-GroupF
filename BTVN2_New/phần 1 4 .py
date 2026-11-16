import numpy as np
import cv2
from harris_classic import harris_classic ,nms_2d


# ----------------------------------------------------------------------
# Kiểm chứng 1: bàn cờ tổng hợp
# ----------------------------------------------------------------------
def make_checkerboard(n_squares=8, sq=40):
    """Ảnh bàn cờ n x n ô, mỗi ô sq px. Trả về ảnh và tọa độ giao điểm trong."""
    size = n_squares * sq
    img = np.zeros((size, size), dtype=np.float64)
    for i in range(n_squares):
        for j in range(n_squares):
            if (i + j) % 2 == 0:
                img[i * sq:(i + 1) * sq, j * sq:(j + 1) * sq] = 255.0
    inner = [(sq * a - 0.5, sq * b - 0.5)
             for a in range(1, n_squares) for b in range(1, n_squares)]
    return img, np.array(inner)


def check_1():
    print("=" * 60)
    print("KIỂM CHỨNG 1: Bàn cờ tổng hợp")
    print("=" * 60)
    img, gt = make_checkerboard(8, 40)
    pts = harris_classic(img, sigma_i=2.0, sigma_d=1.4, k=0.04, thresh_rel=0.01)
    det = pts[:, :2]

    errs = []
    for g in gt:
        d = np.hypot(det[:, 0] - g[0], det[:, 1] - g[1])
        errs.append(d.min())
    errs = np.array(errs)

    extra = 0
    for p in det:
        d = np.hypot(gt[:, 0] - p[0], gt[:, 1] - p[1])
        if d.min() > 1.0:
            extra += 1

    print(f"Số giao điểm trong (thật)      : {len(gt)}")
    print(f"Số điểm Harris phát hiện       : {len(det)}")
    print(f"Sai số vị trí lớn nhất         : {errs.max():.3f} px")
    print(f"Sai số vị trí trung bình       : {errs.mean():.3f} px")
    print(f"Số giao điểm bị bỏ sót (>1 px) : {(errs > 1.0).sum()}")
    print(f"Số điểm thừa (cách mọi giao điểm >1 px): {extra}")
    ok = (errs.max() <= 1.0) and (len(det) == len(gt)) and extra == 0
    print("KẾT QUẢ:", "ĐẠT" if ok else "KHÔNG ĐẠT")
    return ok


# ----------------------------------------------------------------------
# Kiểm chứng 4: đối chiếu cv2.cornerHarris
# ----------------------------------------------------------------------
def make_test_image(seed=0, size=256):
    """Ảnh tổng hợp có nhiều hình chữ nhật/đa giác, làm mờ nhẹ + nhiễu nhẹ."""
    rng = np.random.default_rng(seed)
    img = np.full((size, size), 60.0)
    for _ in range(25):
        x0, y0 = rng.integers(0, size - 40, 2)
        w, h = rng.integers(20, 70, 2)
        img[y0:y0 + h, x0:x0 + w] = rng.integers(0, 256)
    img = cv2.GaussianBlur(img, (0, 0), 1.0)
    img += rng.normal(0, 2.0, img.shape)
    return np.clip(img, 0, 255)


def opencv_points(img, block=5, ksize=3, k=0.04, thresh_rel=0.01):
    R = cv2.cornerHarris(img.astype(np.float32), block, ksize, k)
    mask = nms_2d(R.astype(np.float64)) & (R > thresh_rel * R.max())
    r, c = np.nonzero(mask)
    return np.column_stack((r, c))


def check_4(img=None, name="ảnh tổng hợp nhiều hình chữ nhật"):
    print()
    print("=" * 60)
    print("KIỂM CHỨNG 4: Đối chiếu cv2.cornerHarris")
    print("=" * 60)
    if img is None:
        img = make_test_image()

    mine = harris_classic(img, sigma_i=2.0, sigma_d=1.4, k=0.04, thresh_rel=0.01)[:, :2]
    cvp = opencv_points(img)

    print(f"Ảnh: {name}, kích thước {img.shape}")
    print(f"Số điểm của mình : {len(mine)}")
    print(f"Số điểm OpenCV   : {len(cvp)}")

    # Với mỗi điểm của mình: khoảng cách tới điểm OpenCV gần nhất
    d = np.array([np.hypot(cvp[:, 0] - p[0], cvp[:, 1] - p[1]).min() for p in mine])
    # Chiều ngược lại: OpenCV có điểm nào mình bỏ sót
    d_rev = np.array([np.hypot(mine[:, 0] - p[0], mine[:, 1] - p[1]).min() for p in cvp])

    for r in (1, 2, 3):
        print(f"Điểm của mình nằm trong bán kính {r} px của điểm OpenCV: "
              f"{(d <= r).mean() * 100:5.1f}%")
    print(f"Điểm OpenCV có điểm của mình trong 3 px (chiều ngược) : "
          f"{(d_rev <= 3).mean() * 100:5.1f}%")
    print(f"Khoảng cách trung vị: {np.median(d):.2f} px, lớn nhất: {d.max():.2f} px")
    frac = (d <= 3).mean()
    print("KẾT QUẢ:", "ĐẠT (phần lớn điểm trong 2-3 px)" if frac >= 0.8 else "CẦN XEM LẠI")
    return frac


if __name__ == "__main__":
    check_1()
    check_4()
