import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import heapq
from itertools import product
import random


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

def lan_can_sample(p, connectivity):
    if connectivity == 4:
        return lan_can_4(p)
    else:
        return lan_can_8(p)

def is_inside(img, p):
    """Kiểm tra điểm có nằm trong ảnh không."""
    h, w = img.shape
    return 0 <= p[0] < h and 0 <= p[1] < w

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
        y, x = seed[0], seed[1]
        mu = img[y, x]
        stack = [seed]
        label[y, x] = i

        sum_mu = img[y, x]
        count = 1
        
        while len(stack) > 0:
            p = stack.pop() if order == "stack" else stack.pop(0)
            mu = sum_mu / count
            
            for q in lan_can_4(p):
                if is_inside(img, q): continue 
                if not is_label(q) and np.abs(img[q[0], q[1]] - mu) <= T:
                    # is_label trả về giá trị là True nếu đã gán
                    # khi đó not sẽ trả ra là False và đi tới trường hợp khác
                    sum_mu += mu
                    count += 1
                    label[q[0], q[1]] = i
                    stack.append(q) 

    return label

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

"""
def find_minimum_delta(img, pixel, connectivity, label_map):
    min_delta = float("inf")

    neighbors = lan_can_sample(img, pixel, connectivity)

    for q in neighbors:
        # Chỉ tính delta với những lân cận đã được gán nhãn vùng (>= 0)
        if label_map[q[0], q[1]] >= 0:
            # Lưu ý: Bên trong delta_calculation cần lấy hiệu của img[pixel] và vùng của q
            d = float(delta_calculation(img, pixel, q, connectivity))
            if d < min_delta:
                min_delta = d

    return min_delta

def Quy_Tac_Pha_Hoa(img, label, seed, regions, connectivity):
    # REGION_MEAN is an array used to hold the current mean grey value
    # for each region
    REGION_MEAN = []
    # NHQ: Neighbours holding queue
    # using to hold pixels that neighbour one or more regions
    NHQ = [lan_can_sample(seed, connectivity)]
    PQ = [] # List of LIFO queues
    FQ = [] # First (Highest priority) queue in the PQ
    HQ = [] # Holding Queue <- accumulate pixels removed from the NHQ
    LQ = [] # Labels Queue <- Used to hold region labels corresponding to the pixels in the HQ
    TIED = -2 # Label Denoting a tied pixel
    IN_QUEUE = -3 # Label indicating that the pixel is in HQ or NHQ
    IN_PRIORITY_QUEUE = -4 # Label indicating that pixels is in the PQ
    counter = 0
    while (len(PQ) > 0) or (len(NHQ) > 0):
        while (len(NHQ) > 0):
            p = NHQ.pop()
            minimum = find_minimum_delta(img, p, connectivity, label)
            heapq.heappush(PQ, (minimum, counter, p))
            counter += 1
            IN_PRIORITY_QUEUE.append(p)

        if not is_empty(PQ):
            FQ = heapq.heappop(PQ)
            while not is_empty(FQ):
                pixel = FQ.pop()
                if (pixel in IN_PRIORITY_QUEUE) or (pixel in TIED):
                    # Examine all its neighbours that have a region label
                    lancan = lan_can_sample(pixel, connectivity)
                    if (lancan.all in label):
                        Check = True
                    else:
                        Check = False
                    
                    if Check:
                        LQ.append(label)
                    else:
                        find_minimum_delta()
                        if TIED == None:
                           LQ.append() # Trong day han la 1 cai gi do
                        else:
                            LQ.append(TIED)
                            if pixel not in TIED:
                                heapq.heappush(PQ, (np.inf, counter, pixel)) 
                HQ.append(pixel)
                IN_QUEUE.append(pixel)
        
        while not is_empty(HQ):
            lb = LQ.pop()
            pixel = HQ.pop()
            # Assign label to pixel
            if lb is not TIED:
                k = lan_can_sample(pixel, connectivity)
                REGION_MEAN[lb] = k
                if (not is_label(label, k)) or (k.any in IN_PRIORITY_QUEUE):
                    NHQ.append(k)
                    IN_QUEUE.append(k) 
    return PQ
"""           
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
    img_f = img.astype(np.float64)
    Labels = -1 * np.ones([h, w], dtype= np.int32)
    seed_value = -1 * np.ones([h, w], dtype= np.int32)
    Boundary_mask = np.zeros([h, w], dtype=bool)

    n = len(seeds)
    region_sum = np.zeros(n)
    region_count = np.zeros(n)

    # Khoi tao mang heap
    my_heap = []
    counter = 0
    last_pushed = {}  # (point, index)
    
    random_grid = None
    if tie == "random":
        rng = np.random.default_rng(seed=42)
        random_grid = rng.random((h, w))
        
    def delta_calculation(point, reg_id):
        if stale == "frozen":
            ref_val = seed_value[reg_id]
        else: # Lazy
            ref_val = region_sum[reg_id] / region_count[reg_id]
        return abs(img_f[point[0], point[1] - ref_val]) # Image - Mean
         
    def get_tie_key(cnt, point):
        # cnt: counter
            if tie == "insertion":
                return cnt
            elif tie == "raster":
                return point
            elif tie == "random":
                return random_grid[point[0], point[1]]
            return cnt
        
    for i, seed in enumerate(seeds):
        y, x = seed[0], seed[1]
        Labels[y, x] = i
        seed_value[i] = img[y, x]

        # Luu gia tri goc cho stale = "frozen"
        region_sum[i] = img[y, x]
        # Tong cuong do vung cho stale = "lazy"
        region_count[i] = 1

    for i, seed in enumerate(seeds):
        lan_can = lan_can_sample(seed, connectivity)
        for q in lan_can:
            if not is_label(Labels, q):
                delta = delta_calculation(q, connectivity)
                counter += 1
                last_pushed[(q, i)] = delta 
                heapq.heappush(
                    my_heap, (delta, 
                              get_tie_key(counter, q), q, i)
                    )
    while my_heap:
        delta, _, point, reg_id = heapq.heappop(my_heap)
        if is_label(Labels, point):
            continue
        if stale == "lazy":
            # Chong Lazy
            current_delta = delta_calculation(img, point, reg_id)
            if not np.isclose(delta, current_delta):
                # Neu co su thay doi do trung binh vung thay doi
                counter += 1
                last_pushed[(point, reg_id)] = current_delta
                heapq.heappush(
                    my_heap, (delta, 
                            get_tie_key(counter, point), point, reg_id)
                    )
                continue
        y, x = point[0], point[1]
        Labels[y, x] = reg_id
        region_sum[reg_id] += img_f[y, x]
        region_count[reg_id] += 1
        
        lan_can = lan_can_sample(point, connectivity)
        for q in lan_can:
            qy, qx = int(q[0]), int(q[1])
            
            if not is_inside(img, q): 
                continue
            if not is_label(Labels, point):
                new_delta = delta_calculation(point, reg_id)
                if ((q, reg_id) not in last_pushed) or \
                            new_delta < last_pushed[((q, reg_id))]:
                    counter += 1
                    last_pushed[((q, reg_id))] = new_delta
                    heapq.heappush(
                    my_heap, (new_delta, 
                            get_tie_key(counter, q), q, reg_id)
                        )
            elif Labels[qy, qx] != reg_id:
                Boundary_mask[y, x] = True
                Boundary_mask[qy, qx] = True
                
    return Labels, Boundary_mask
            
def srg_step_frames(img, seeds, n_frames=8, **kwargs):
    """
    Ảnh nhãn tại các mốc tiến trình (12%, 25%, ...).
    -> danh sách n_frames mảng nhãn.
    """
    _, frames = srg(img, seeds, connectivity=n_frames, **kwargs)
    return frames

def seed_sensitivity(img, seeds, segment_fn, n_trials=20, jitter=3):
    """
    Chạy lại segment_fn với hạt giống bị nhiễu +-jitter px.
    -> bản đồ tần suất: mỗi pixel đổi nhãn bao nhiêu lần trên n_trials.
    Cách định lượng độ ổn định mà không cần ground truth.
    """
    h, w = img.shape
    change_map = np.zeros((h, w), dtype=np.float32)

    # Chạy baseline
    nhan_goc, _ = segment_fn(img, seeds)

    # Lặp n_trials lần
    for lan in range(n_trials):
        # Tạo seed nhiễu
        seed_nhieu = []
        for s in seeds:
            y = int(s[0]) + random.randint(-jitter, jitter)
            x = int(s[1]) + random.randint(-jitter, jitter)
            # Giới hạn trong ảnh
            if y < 0: y = 0
            if y >= h: y = h - 1
            if x < 0: x = 0
            if x >= w: x = w - 1
            seed_nhieu.append((y, x))

        # Chạy segmentation
        nhan_moi, _ = segment_fn(img, seed_nhieu)

        # Đếm pixel đổi nhãn
        for y in range(h):
            for x in range(w):
                if nhan_moi[y, x] != nhan_goc[y, x]:
                    change_map[y, x] = change_map[y, x] + 1

    # Chia trung bình
    change_map = change_map / n_trials
    return change_map