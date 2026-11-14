import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def read_img(img_path):
    return cv.imread(img_path, cv.IMREAD_COLOR_BGR).astype('int')

def show_img(img):
    cv.imshow(img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def create_seeds(h, w):
    return [
        [h/2, w/2],
        [h/3, w/3],[2*h/3, w/3],[h/3-10, w/3],
        [h/3, 2*w/3],[2*h/3, 2*w/3],[h/3-10, 2*w/3],
        [h/3, w-10],[2*h/3, w-10],[h/3-10, w-10]
            ]

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

def is_label(img, q):
    if (img[q[0], q[1]]) == -1:
        return False

def region_growing_classic(img, seeds, T, order="stack"):
    """
    Region growing cổ điển, một hoặc nhiều hạt giống.
    order: "stack" (LIFO) hoặc "queue" (FIFO).
    -> mảng nhãn int32,-1 cho pixel không thuộc vùng nào.
    """
    if order == "stack":
        for seed in seeds:
            stack = [seed]
            label[seed] = i
            mu = img[seed]
            n = 1
            while not is_empty(stack):
                p = stack.pop()
                for q in lan_can_4(p):
                    if is_label(q) and np.abs(I[q[0], q[1]] - mu) <= T:
                        label[q] = i 

    elif order == "queue":
        pass
    else:
        pass

def srg(img, seeds, connectivity=4, stale="lazy", tie="insertion"):
    """
    Seeded Region Growing (Adams & Bischof 1994), công thức (5). Dùng heapq.
    stale: "lazy"-> tính lại delta khi pop, đẩy lại nếu đã cũ
    "frozen"
    -> delta theo giá trị hạt giống
    tie: quy tắc phá hoà tất định: "insertion" | "raster" | "random"
    -> (labels, boundary_mask); mọi pixel đều có nhãn >= 0.
    """
def srg_step_frames(img, seeds, n_frames=8, **kwargs):
    """
    Ảnh nhãn tại các mốc tiến trình (12%, 25%, ...).
    -> danh sách n_frames mảng nhãn.
    """
def seed_sensitivity(img, seeds, segment_fn, n_trials=20, jitter=3):
    """
    Chạy lại segment_fn với hạt giống bị nhiễu +-jitter px.
    -> bản đồ tần suất: mỗi pixel đổi nhãn bao nhiêu lần trên n_trials.
    Cách định lượng độ ổn định mà không cần ground truth.
    """