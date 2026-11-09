"""
Mục đích:
Cung cấp hàm harris_laplace để các bạn trong nhóm có thể import dùng chung:
    from harris_laplace_module import harris_laplace
"""
import sys
import cv2
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def tinh_harris(img_gray, sigma, k=0.04, nguong_ti_le=0.01):
    """
    Bước 1: Tìm góc Harris ở một thang đo sigma (Tiêu chí góc).
    Trả về: Ma trận boolean (True tại các tọa độ là góc).
    """
    # 1. Làm mịn ảnh theo thang đo sigma
    img_blur = cv2.GaussianBlur(img_gray, (0, 0), sigmaX=sigma, sigmaY=sigma)
    
    # 2. Đạo hàm theo x và y bằng Sobel
    Ix = cv2.Sobel(img_blur, cv2.CV_64F, 1, 0, ksize=3)
    Iy = cv2.Sobel(img_blur, cv2.CV_64F, 0, 1, ksize=3)
    
    # 3. Chuẩn hóa đạo hàm theo thang đo sigma
    Ix = sigma * Ix
    Iy = sigma * Iy
    
    # 4. Ma trận Moment thứ hai M (làm mịn ở sigma_i = 1.4 * sigma)
    sigma_i = 1.4 * sigma
    Ixx = cv2.GaussianBlur(Ix**2, (0, 0), sigmaX=sigma_i, sigmaY=sigma_i)
    Iyy = cv2.GaussianBlur(Iy**2, (0, 0), sigmaX=sigma_i, sigmaY=sigma_i)
    Ixy = cv2.GaussianBlur(Ix*Iy, (0, 0), sigmaX=sigma_i, sigmaY=sigma_i)
    
    # 5. Phản ứng góc R = det(M) - k * trace(M)^2
    det = Ixx * Iyy - Ixy**2
    trace = Ixx + Iyy
    R = det - k * (trace**2)
    
    # 6. Lọc cực đại địa phương (NMS 3x3)
    kernel = np.ones((3, 3), np.uint8)
    local_max = cv2.dilate(R, kernel)
    
    nguong = nguong_ti_le * R.max() if R.max() > 0 else 0
    mat_na_goc = (R == local_max) & (R > nguong)
    
    return mat_na_goc


def tinh_laplace_chuan_hoa(img_gray, sigma):
    """
    Bước 2: Tính toán tử LoG chuẩn hóa |sigma^2 * Laplacian| (Tiêu chí đốm).
    """
    img_blur = cv2.GaussianBlur(img_gray, (0, 0), sigmaX=sigma, sigmaY=sigma)
    laplace = cv2.Laplacian(img_blur, cv2.CV_64F)
    log_chuan_hoa = (sigma ** 2) * np.abs(laplace)
    return log_chuan_hoa


def harris_laplace(img, so_thang_do=10, sigma_0=1.5, factor=1.2, nguong_log=0.01):
    """
    Bước 3: Ghép hai phần lại thành Harris-Laplace hoàn chỉnh.
    Trả về: Danh sách các điểm đặc trưng, mỗi phần tử là (x, y, sigma).
    """
    # Đưa về ảnh xám số thực [0, 1]
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    gray = gray.astype(np.float64) / 255.0
    
    # 1. Danh sách các thang đo sigma
    sigmas = [sigma_0 * (factor ** i) for i in range(so_thang_do)]
    
    ds_goc_theo_thang = []
    ds_log = []
    
    # 2. Quét qua từng thang đo để lấy góc Harris và bản đồ LoG
    for s in sigmas:
        ds_goc_theo_thang.append(tinh_harris(gray, sigma=s))
        ds_log.append(tinh_laplace_chuan_hoa(gray, sigma=s))
        
    # 3. Chọn thang đo: Giữ lại điểm nếu LoG đạt cực đại theo chiều sigma
    cac_diem_dac_trung = []
    
    for i in range(1, len(sigmas) - 1):
        s = sigmas[i]
        mat_na = ds_goc_theo_thang[i]
        ys, xs = np.where(mat_na)
        
        for y, x in zip(ys, xs):
            val_hien_tai    = ds_log[i][y, x]
            val_thang_truoc = ds_log[i - 1][y, x]
            val_thang_sau   = ds_log[i + 1][y, x]
            
            # Cực trị theo chiều thang đo sigma (Slide bài giảng của Thầy)
            if val_hien_tai > val_thang_truoc and val_hien_tai > val_thang_sau:
                if val_hien_tai > nguong_log:
                    cac_diem_dac_trung.append((int(x), int(y), float(s)))
                    
    return cac_diem_dac_trung


def ve_diem_dac_trung(img, keypoints, color=(0, 0, 255), thickness=1):
    """
    Hàm tiện ích vẽ các vòng tròn đặc trưng lên ảnh:
    - Bán kính r = 1.414 * sigma thể hiện kích thước thang đo.
    """
    if len(img.shape) == 2:
        out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        out = img.copy()
        
    for (x, y, s) in keypoints:
        radius = int(round(1.414 * s))
        cv2.circle(out, (x, y), radius, color, thickness)
        cv2.circle(out, (x, y), 2, (0, 255, 0), -1) # Chấm tâm màu xanh
        
    return out


# Chạy thử nghiệm nếu bấm run trực tiếp file này
if __name__ == "__main__":
    print("Đang chạy kiểm tra nhanh module harris_laplace_module.py...")
    test_img = np.zeros((200, 200), dtype=np.uint8)
    cv2.rectangle(test_img, (50, 50), (150, 150), 255, -1)
    
    kps = harris_laplace(test_img)
    print(f"Kiểm tra thành công! Phát hiện {len(kps)} điểm đặc trưng trên hình vuông thử nghiệm.")
    for i, (x, y, s) in enumerate(kps[:4]):
        print(f"  • Điểm {i+1}: tọa độ x={x}, y={y}, thang đo sigma={s:.2f}")
