import numpy as np
from scipy.ndimage import gaussian_filter


def gaussian_blur(img, sigma):
    """Làm mờ Gauss. Được phép gọi scipy.ndimage.gaussian_filter."""
    return gaussian_filter(np.asarray(img, dtype=np.float64), sigma=sigma)


def structure_tensor(img, sigma_i, sigma_d):
    """Ma trận mô-men bậc hai theo công thức (1), đã nhân sigma_d**2.
    sigma_d: độ mờ trước khi lấy đạo hàm.
    sigma_i: bán kính cửa sổ lấy trung bình các tích đạo hàm.
    -> (Mxx, Mxy, Myy), mỗi phần tử cùng kích thước ảnh.
    """
    # L(x; sigma_d) = G(sigma_d) * I
    L = gaussian_blur(img, sigma_d)

    # Đạo hàm bằng sai phân trung tâm (numpy). axis 0 = y (hàng), axis 1 = x (cột)
    Ly, Lx = np.gradient(L)

    # Tích đạo hàm, làm mờ bằng G(sigma_i), nhân chuẩn hoá sigma_d^2
    s2 = sigma_d ** 2
    Mxx = s2 * gaussian_blur(Lx * Lx, sigma_i)
    Mxy = s2 * gaussian_blur(Lx * Ly, sigma_i)
    Myy = s2 * gaussian_blur(Ly * Ly, sigma_i)
    return Mxx, Mxy, Myy


def harris_response(img, sigma_i, sigma_d, k=0.04):
    """Đáp ứng R theo công thức (2). -> mảng float cùng kích thước ảnh."""
    Mxx, Mxy, Myy = structure_tensor(img, sigma_i, sigma_d)
    det = Mxx * Myy - Mxy ** 2
    tr = Mxx + Myy
    return det - k * tr ** 2


def nms_2d(response, window=3):
    """Cực đại địa phương trong cửa sổ window x window. -> mảng bool."""
    r = window // 2
    H, W = response.shape
    padded = np.pad(response, r, mode="constant", constant_values=-np.inf)
    keep = np.ones((H, W), dtype=bool)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dy == 0 and dx == 0:
                continue
            neighbor = padded[r + dy:r + dy + H, r + dx:r + dx + W]
            if dy > 0 or (dy == 0 and dx > 0):
                # láng giềng đứng sau theo thứ tự quét: phải lớn hơn hẳn
                keep &= response > neighbor
            else:
                # láng giềng đứng trước: lớn hơn hoặc bằng
                keep &= response >= neighbor
    # Phá hòa: khi nhiều pixel có response bằng nhau (bình nguyên, ví dụ giao
    # điểm bàn cờ nằm giữa 2x2 pixel), chỉ giữ đúng một pixel.
    return keep


def harris_classic(img, sigma_i=2.0, sigma_d=1.4, k=0.04, thresh_rel=0.01):
    """Harris một tỉ lệ: R -> nms_2d -> ngưỡng tương đối theo max(R).
    -> mảng (N, 3): (row, col, response), sắp xếp giảm dần theo response.
    """
    R = harris_response(img, sigma_i, sigma_d, k)
    r_max = R.max()
    if r_max <= 0:
        return np.zeros((0, 3))

    mask = nms_2d(R) & (R > thresh_rel * r_max)
    rows, cols = np.nonzero(mask)
    vals = R[rows, cols]

    order = np.argsort(-vals)
    return np.column_stack((rows[order], cols[order], vals[order]))


if __name__ == "__main__":
    # Kiểm tra nhanh: hình vuông trắng trên nền đen -> 4 góc
    img = np.zeros((100, 100))
    img[30:70, 30:70] = 255.0
    pts = harris_classic(img)
    print("Số điểm:", len(pts))
    print(pts[:8])