import cv2 as cv
import numpy as np
import harris as hr

FAST_16_OFFSETS = np.array([
    [-3,  0],  # Point 1  (vị trí 12h)
    [-3,  1],  # Point 2
    [-2,  2],  # Point 3
    [-1,  3],  # Point 4
    [ 0,  3],  # Point 5  (vị trí 3h)
    [ 1,  3],  # Point 6
    [ 2,  2],  # Point 7
    [ 3,  1],  # Point 8
    [ 3,  0],  # Point 9  (vị trí 6h)
    [ 3, -1],  # Point 10
    [ 2, -2],  # Point 11
    [ 1, -3],  # Point 12
    [ 0, -3],  # Point 13 (vị trí 9h)
    [-1, -3],  # Point 14
    [-2, -2],  # Point 15
    [-3, -1]   # Point 16
])

def get_fast_16_pixels(p):
    """
    p chua dia chi (y, x)
    Trả về mảng (16, 2) chứa tọa độ (y, x)
    """
    return np.array(p) + FAST_16_OFFSETS

def HighSpeed_test(img, around, l_max, l_min, minC):
    # Phep kiem tra toc do cao
    ps = around[0:16:4]
    count = 0
    for i in range(len(ps)): # N = 4
        if (img[ps[i][0], ps[i][1]] > l_max or img[ps[i][0], ps[i][1]] < l_min):
            count += 1
    
    if (count >= 3):
        return True
    
    return False

def isGoc(img, p, t, minC):
    # p = np.array([y, x])
    around = get_fast_16_pixels(p)
    count = 0

    center_val = int(img[p[0], p[1]])
    l_max = center_val + t
    l_min = center_val - t

    if not (HighSpeed_test(img, around, l_max, l_min, minC)):
        # Kết quả của HighSpeed nếu không đáp ứng đủ atleast 3 điểm
        # thì sẽ trả ra kết quả là Fasle
        # not False = True -> Loại
        return False
    
    for i in range(len(around)):
        if (img[around[i][0], around[i][1]] > l_max or img[around[i][0], around[i][1]] < l_min):
            count += 1
        elif (count < minC):
            count = 0 # Điều kiện của góc là phải đáp ứng được tính liên tục

    if (count >= minC):
        return True
    else:
        return False

def FAST(img : np.uint8, minC = 12, thresh = 40, NMS = True):
    # Use to detect feature
    H, W =  img.shape
    corner_list = []
    for y in range(3, H - 3):
        for x in range(3, W - 3):
            point = np.array([y, x])

            if (isGoc(img, point, thresh, minC)):
                corner_list.append(point)

    if NMS:
        # Giữ cực đại cục bộ trong cửa sổ 3x3
        pass

    return np.array(corner_list) # Mảng dạng [[y, x]]

def draw_keypoints(image, keypoints, radius=4, color=(0, 0, 255), thickness=-1, coords_format='yx'):
    out = image.copy() if image.ndim == 3 else cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    for y, x in keypoints:
        cv.circle(out, (int(x), int(y)), radius, color, thickness)
    return out

# Harris Score
def Sp(M_p, k):
    # This is a scored function
    return np.linalg.det(M_p) - k * np.trace(M_p)**2

def NMS(img, p, t):
    # p: Pixel center
    # t: Threshold
    # NMS is the shorted of Non Maximal Suppression 
    # NMS is the solution of multiple interest points adjacent to one another
    

    pass

def oFAST():
    #  Vì FAST không có hướng nên tại đây dùng để tính momemt bậc (p, q) trong patch bán kính r
    
    pass

if __name__ == "__main__":
    img = cv.imread("Face.jpg")
    img_gray = cv.imread("Face.jpg", cv.IMREAD_GRAYSCALE)
    corner = FAST(img_gray, 10, 30)
    img_after = draw_keypoints(img, corner)
    cv.imshow("FAST", img_after)
    cv.waitKey(0)
    cv.destroyAllWindows()    
