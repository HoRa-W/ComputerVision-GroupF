import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import heapq
from itertools import product


def read_img(img_path):
    return cv.imread(img_path, cv.IMREAD_GRAYSCALE).astype('int')

def show_img(img, Content = "Result"):
    cv.imshow(Content, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def is_empty(stack):
    return len(stack) == 0

def lan_can_4(p):
    # p co the la dia chi cua 1 diem: y, x
    # return: North, West, East, South
    N = [-1, 0]
    W = [0, -1]
    E = [0, 1]
    S = [1, 0]
    connectivity_4 = np.array([N, W, E, S])
    return np.array(p) + connectivity_4

def lan_can_8(p):
    connectivity_8 = [d for d in product([-1, 0, 1], repeat = 2)]
    return np.array(p) + connectivity_8
    
"""
Tạm thời chưa cần xài đến
def doLabel(img, p, t = 40):
    # Nếu p < seed - t or p > seed + t thì thỏa
    # Trong trường hợp không thỏa ta gán chỗ đó là -1
    # Trong trường hợp thỏa ta giữ nguyên và đặt đó là int32
    Cond1 = abs(img[p[0], p[1]] - mean_vung(img, p, 4)) < t
    Cond2 = abs(img[p[0], p[1]] + mean_vung(img, p, 4)) > t
    
    if Cond1 or Cond2:
        return np.int32(img[p[0], p[1]])
    else:
        return -1
"""

def is_label(img, q):
    # img can be a Label if you need
    # Return False if it isn't Labeled
    if (img[q[0], q[1]]) == -1:
        return False
    return True

def region_growing_classic(img, seeds, T, order="stack"):
    """
    Region growing cổ điển, một hoặc nhiều hạt giống.
    order: "stack" (LIFO) hoặc "queue" (FIFO).
    -> mảng nhãn int32,-1 cho pixel không thuộc vùng nào.
    """
    h, w = img.shape
    label = -1 * np.ones([h, w], dtype= np.int32)

    for i, seed in enumerate(seeds):
        mu = img[seed[0], seed[1]]
        stack = [seed]
        label[seed[0], seed[1]] = i

        while not is_empty(stack):
            p = stack.pop() if order == "stack" else stack.pop(0)
            for q in lan_can_4(p):
                if not is_label(q) and np.abs(img[q[0], q[1]] - mu) <= T:
                    # is_label trả về giá trị là True nếu đã gán
                    # khi đó not sẽ trả ra là False và đi tới trường hợp khác
                    label[q[0], q[1]] = i
                    stack.append(q) 

    return label

def ApplyRegion_Grow():
    pass

def mean_vung(img, p, vung_so : int):
    if vung_so == 4:
        location = lan_can_4(p)
        sum = 0
        for y, x in location:
            sum += img[y, x]
        
        return int(sum/4)
    
    if vung_so == 8:
        location = lan_can_8(p)
        sum = 0
        for y, x in location:
            sum += img[y, x]
        
        return int(sum/8)

def delta_calculation(img, point, connectivity : int, stale="Lazy"):
    # Nếu delta là fronzen thì delta tính theo giá trị của hạt giống không tính theo 
    # trung bình vùng
    if stale == "frozen":
        return img[point[0], point[1]]
    # Còn đây là trường hợp cho Lazy
    return np.abs(img[point[0], point[1]] - mean_vung(img, point, connectivity))

def Quy_Tac_Pha_Hoa(img, seeds, connectivity):
    pass

def srg(img, seeds, connectivity=4, stale="lazy", tie="insertion"):
    """
    Seeded Region Growing (Adams & Bischof 1994), công thức (5). Dùng heapq.
    stale: 
    "lazy"-> tính lại delta khi pop, đẩy lại nếu đã cũ
    "frozen"-> delta theo giá trị hạt giống
    tie: quy tắc phá hoà tất định: "insertion" | "raster" | "random"
    -> (labels, boundary_mask); mọi pixel đều có nhãn >= 0.
    """
    h, w = img.shape
    Labels = -1 * np.ones([h, w], dtype= np.int32)
    seed_value = -1 * np.ones([h, w], dtype= np.int32)
    Boundary_mask = np.zeros([h, w], dtype=bool)

    n = len(seeds)
    region_sum = np.zeros(n)
    region_count = np.zeros(n)

    # Khoi tao mang heap
    my_heap = []
    counter = 0
    last_pushed = {}  # (q, index) <- delta and q is lan_can(seed) 

    if tie == "random":
        rng = np.random.default_rng(seed=42)
        random = rng.random((h, w))
    

    for i, seed in enumerate(seeds):
        y, x = map(seed)
        Labels[y, x] = i
        seed_value[i] = img[y, x]

        # Luu gia tri goc cho stale = "frozen"
        region_sum[i] = img[y, x]
        # Tong cuong do vung cho stale = "lazy"
        region_count[i] = 1

    for i, seed in enumerate(seeds):
        lan_can = lan_can_4(seed) if connectivity==4 else lan_can_8(seed)
        for q in lan_can:
            if not is_label(Labels, q):
                delta = delta_calculation(img, q, connectivity)
                counter += 1
                last_pushed[(q, i)] = delta 
                heapq.heappush(my_heap, )


    
def srg_step_frames(img, seeds, n_frames=8, **kwargs):
    """
    Ảnh nhãn tại các mốc tiến trình (12%, 25%, ...).
    -> danh sách n_frames mảng nhãn.
    """
    frames = srg(img, seeds, connectivity=n_frames, **kwargs)
    return frames

def seed_sensitivity(img, seeds, segment_fn, n_trials=20, jitter=3):
    """
    Chạy lại segment_fn với hạt giống bị nhiễu +-jitter px.
    -> bản đồ tần suất: mỗi pixel đổi nhãn bao nhiêu lần trên n_trials.
    Cách định lượng độ ổn định mà không cần ground truth.
    """
    segment_fn(img, seeds)