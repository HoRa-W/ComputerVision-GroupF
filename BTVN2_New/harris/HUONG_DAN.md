# Kiểm chứng Harris A.2 và A.3 trên VS Code / Windows

Đây là hướng dẫn thao tác và khung thí nghiệm. Không có cài đặt Harris, Harris–Laplace hoặc repeatability trong bộ file này. Nhóm phải tự viết các hàm đó theo quy định bài tập. Các kết quả chỉ xuất hiện khi bạn chạy thật.

## 1. Trạng thái repository đã kiểm tra

Bản main tại commit c24f38bfa9e0149ae205d84fcadf64576c6e4478:

- BTVN2/harris.py có harris_laplace(img, so_thang_do=10, sigma_0=1.5, factor=1.2, nguong_log=0.01), trả (x, y, sigma). Hàm tự chia ảnh cho 255, nên khung gửi ảnh xám uint8 cho API này.
- Chưa có hàm tên harris_classic và repeatability trong file đó.
- tinh_harris trả mặt nạ bool tại một thang; nó không có giao diện harris_classic trong PDF. Khung không tự thay thế hoặc đổi tên các hàm.
- Chạy harris.py trực tiếp chỉ tạo hình vuông tổng hợp trong bộ nhớ và in kết quả của harris_laplace. Nó không đọc ảnh bạn vừa đặt vào anh/, không quay ảnh và không tính repeatability.
- BTVN2/Cv_Task2.ipynb trên main vẫn chưa có các cell chạy đủ hai kiểm chứng này.

Các file trên máy bạn có thể có thay đổi chưa đẩy lên GitHub. Lệnh --test check đọc chính file trên máy, không lấy file từ mạng và không ghi đè thuật toán.

## 2. Mở đúng project và chọn Python

VS Code: File > Open Folder > C:\Users\USER\Documents\GitHub\ComputerVision-GroupF.

Ctrl+Shift+P > Python: Select Interpreter > Enter interpreter path:

    C:\Users\USER\Documents\GitHub\ComputerVision-GroupF\.venv\Scripts\python.exe

Đóng terminal cũ bằng nút thùng rác, Terminal > New Terminal, chọn PowerShell.

Chạy từng dòng (không chép phần PS C:\...> của dấu nhắc):

```powershell
cd 'C:\Users\USER\Documents\GitHub\ComputerVision-GroupF'
Test-Path .\.venv\Scripts\python.exe
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); import cv2, numpy; print(cv2.__version__); print(numpy.__version__)"
```

Lệnh đầu kiểm tra phải trả True, lệnh sau phải hiện đường dẫn .venv và hai phiên bản. Môi trường .venv đã được bạn tạo trước đó; không cần tạo lại hoặc thay thế.

Cài thêm phần vẽ và kernel notebook vào đúng môi trường:

```powershell
uv pip install --python .\.venv\Scripts\python.exe matplotlib scipy ipykernel
```

Nếu không dùng được uv nhưng .venv có pip, lệnh tương đương là:

```powershell
.\.venv\Scripts\python.exe -m pip install matplotlib scipy ipykernel
```

Trong notebook, Select Kernel là lựa chọn riêng: cũng chọn .venv\Scripts\python.exe. Run Code của Code Runner có thể dùng Python khác; các lệnh chỉ định đầy đủ đường dẫn ở đây không phụ thuộc vào nó.

## 3. Đặt file và ảnh

Giải nén bộ file tải về. Chép kiem_chung_A.py và kiem_chung_A.ipynb vào thẳng BTVN2, cạnh harris.py. Không để chúng ở một thư mục con vừa giải nén.

```text
ComputerVision-GroupF/
  .venv/
  BTVN2/
    harris.py                 # code nhóm tự viết
    kiem_chung_A.py            # khung chạy terminal
    kiem_chung_A.ipynb         # khung notebook, chưa phải bài nộp hoàn chỉnh
    anh/
      kiem_chung_goc.jpg       # ảnh đầu vào bạn tự chọn
    ket_qua_A/                # được tạo/lưu kết quả khi chạy
```

Tạo thư mục bằng terminal, đang ở gốc project:

```powershell
New-Item -ItemType Directory -Force .\BTVN2\anh | Out-Null
New-Item -ItemType Directory -Force .\BTVN2\ket_qua_A | Out-Null
```

Bạn tự quyết định ảnh kiểm chứng và ghi lý do chọn. Ảnh có các góc nhìn được bằng mắt giúp đối chiếu. Ảnh đầu vào khoảng vài trăm pixel mỗi chiều giúp phép chạy nhiều tầng ở ảnh lớn 3 lần nhẹ hơn. Đây không phải kích thước bắt buộc.

Để kiểm tra đường dẫn bằng ảnh đã có trong repository, có thể chép Face.jpg (chưa khẳng định đó là ảnh tốt nhất để đánh giá):

```powershell
Copy-Item .\BTVN2\Face.jpg .\BTVN2\anh\kiem_chung_goc.jpg
```

Nếu dùng ảnh riêng, chép ảnh đó vào anh/. Giữ đúng phần mở rộng thực tế: đổi tên .jpg thành .png không phải chuyển định dạng. Nếu tên là anh_cua_toi.png, các lệnh chạy cần dùng --image .\anh\anh_cua_toi.png.

Chỉ cần một ảnh gốc. Khung tự tạo ảnh quay và ảnh phóng to, không phải chỉnh ảnh thủ công bằng Paint/Photos. Phóng lớn cửa sổ xem ảnh không phải tăng kích thước dữ liệu ảnh.

## 4. Chuyển terminal vào BTVN2 và kiểm tra ảnh

```powershell
cd 'C:\Users\USER\Documents\GitHub\ComputerVision-GroupF\BTVN2'
Test-Path .\harris.py
Test-Path .\kiem_chung_A.py
Test-Path .\anh\kiem_chung_goc.jpg
..\.venv\Scripts\python.exe -c "import cv2; from pathlib import Path; p=Path('anh/kiem_chung_goc.jpg'); a=cv2.imread(str(p), cv2.IMREAD_GRAYSCALE); print(p.resolve()); print('KHONG DOC DUOC' if a is None else (a.shape, str(a.dtype)))"
```

Ba Test-Path phải trả True. Sau đó phải có kích thước (H,W) và uint8. Nếu không đọc được ảnh, giải quyết đường dẫn/file trước khi chạy detector. Đừng chuyển sang xử lý lỗi .shape của None như thể đó là lỗi thuật toán.

Từ bước này, dùng ..\.venv\Scripts\python.exe vì terminal đang trong BTVN2. Nếu ở gốc project thì đường dẫn Python là .\.venv\Scripts\python.exe.

## 5. Kiểm tra các hàm nhóm đã có

```powershell
..\.venv\Scripts\python.exe .\kiem_chung_A.py --test check
```

Khung sẽ in đường dẫn module thực sự được import và chữ CO hoặc THIEU trước từng hàm. Với bản main đã kiểm tra, harris_classic và repeatability còn thiếu. Đây là trạng thái chưa đủ cài đặt, không phải lỗi OpenCV.

Nhóm cần tự hoàn thiện chúng. Không có lệnh cài thư viện nào tạo ra các hàm của bài tập. Kiểm tra tên hàm có mặt cũng không chứng minh hàm tính đúng.

Khung mong đợi giao diện theo PDF:

- harris_classic(img, sigma_i=2.0, sigma_d=1.4, k=0.04, thresh_rel=0.01) -> (N,3), các cột row,col,response.
- repeatability(pts_a, pts_b, transform, img_shape, eps=3.0) -> một số trong [0,1]. pts_a và pts_b mà khung gửi là các mảng (N,2) row,col. transform nhận một cặp row,col và trả cặp row,col trong ảnh đích. img_shape là kích thước ảnh đích.
- harris_laplace: khung gọi được cả API hiện có trong harris.py và API sigmas trong PDF. Đầu ra API hiện tại x,y,sigma được đổi thứ tự tọa độ trong phần thí nghiệm, không sửa detector.

Nếu hàm cổ điển cần ảnh float [0,1], thêm --classic-input float01 vào lệnh chạy. Mặc định gửi uint8; bạn phải chọn theo hợp đồng đầu vào mà nhóm đã tự viết. API Harris–Laplace hiện tại tự chuẩn hóa nên luôn nhận uint8.

Nếu các hàm nằm ở file riêng, khai báo module, bỏ .py. Ví dụ classic ở harris_classic_module.py và phép đo ở do_dac.py, đặt cả hai cạnh kiem_chung_A.py:

```powershell
..\.venv\Scripts\python.exe .\kiem_chung_A.py --test check --classic-module harris_classic_module --metric-module do_dac
```

Các tùy chọn module tương tự phải đi cùng những lệnh chạy tiếp theo. Đây là cách xác định nơi gọi hàm, không phải yêu cầu đổi tên file harris.py.

## 6. Quy ước đo chung

Chạy detector độc lập trên ảnh gốc A và ảnh đích B để có P_A và P_B. Dùng phép biến đổi T để đưa điểm gốc đến vị trí dự đoán T(P_A).

Theo PDF, mẫu số là số điểm gốc có vị trí chiếu còn nằm trong ảnh B. Một điểm được tìm lại nếu có điểm phát hiện trên B trong bán kính eps=3 pixel tại ảnh B. Không chia theo tổng điểm của cả hai ảnh; không ghép theo thứ tự dòng trong danh sách.

Khung KHÔNG cài đặt phép đo này: nó gọi repeatability của nhóm. Số N_valid hiển thị dùng điều kiện 0 <= row < H_B và 0 <= col < W_B; phép đo nhóm cần nhất quán với điều kiện đó. Không có điểm gốc hợp lệ thì báo N/A, không báo thành công 100%.

Trước các kiểm chứng, nhóm nên tự xác minh repeatability trên cùng tập điểm không rỗng với phép biến đổi đồng nhất phải bằng 1.

## 7. Chạy kiểm chứng quay 30 độ

Chỉ chạy khi các hàm cần thiết đã có:

```powershell
..\.venv\Scripts\python.exe .\kiem_chung_A.py --test rotation --image .\anh\kiem_chung_goc.jpg
```

Khung thực hiện:

1. Đọc ảnh xám A, không đổi kích thước ảnh gốc.
2. Quay +30 độ bằng OpenCV quanh tâm ((W-1)/2,(H-1)/2), giữ nguyên khung W,H. Có thể có phần nội dung bị cắt và vùng nền đen.
3. Dùng cùng ma trận quay để biến đổi tọa độ. Ma trận lưu trong JSON.
4. Chạy harris_classic trên A và B với cùng tham số. Mặc định sigma_i=2, sigma_d=1.4, k=0.04, thresh_rel=0.01.
5. Gọi repeatability của nhóm với eps=3 pixel trên B.
6. Lưu bảng và ảnh đối chiếu.

Mở kết quả:

```powershell
Get-Content .\ket_qua_A\bao_cao_quay30.csv
Invoke-Item .\ket_qua_A\quay30_harris_classic_doi_chieu.png
```

CSV chứa method,N_A,N_B,N_valid,repeatability,eps_target_px. Repeatability trong CSV ở dạng 0..1; terminal in thêm phần trăm.

Ảnh bên trái: điểm phát hiện trên ảnh gốc. Ảnh bên phải: vòng tròn xanh lam là vị trí dự đoán, dấu x cam là điểm phát hiện lại. Hai loại dấu gần nhau là bằng chứng định vị tương ứng.

Không có ngưỡng pass cố định trong PDF cho mục này. Số điểm hai ảnh không bắt buộc bằng nhau. Nội suy, lấy mẫu, NMS và biên ảnh có thể làm kết quả lệch khỏi mô hình liên tục lý tưởng. Chỉ kết luận sau khi xem cả hình và số liệu.

## 8. Chạy kiểm chứng phóng to 3 lần

```powershell
..\.venv\Scripts\python.exe .\kiem_chung_A.py --test scale --image .\anh\kiem_chung_goc.jpg --sigma0 1.5 --factor 1.2 --levels 18
```

Khung tạo B có kích thước 3H,3W bằng warpAffine với x'=3x, y'=3y, nội suy tuyến tính. Vì dùng affine nên không có sự nhập nhằng quy ước tâm pixel của resize trong phép đối chiếu. Mỗi ảnh B được tạo trực tiếp từ A, không phóng to ảnh đã quay.

Sau đó chạy riêng:

- harris_classic(A) và harris_classic(B), giữ sigma_i và sigma_d cố định theo pixel. Không nhân chúng lên 3 trong kiểm chứng Harris cố định tỉ lệ.
- harris_laplace(A) và harris_laplace(B), cùng cấu hình tháp sigma đã chọn, sau đó gọi repeatability riêng cho phương pháp này.

18 tầng là cấu hình khởi đầu minh họa, không phải giá trị bảo đảm kết quả tốt. Dải từ 1.5 đến khoảng 33.28 pixel có các tầng trong để kiểm tra cực đại LoG. Bạn cần xem thang đặc trưng sigma và 3*sigma có được bao phủ và có tầng lân cận hay không. Nếu chưa đủ, đó là giới hạn cấu hình cần ghi nhận; không chỉnh tham số chỉ để tạo một kết luận mong muốn.

Đối với API harris_laplace hiện tại, k=0.04 và ngưỡng Harris=0.01 nằm trong các hàm của nhóm; khung không thay chúng. --log-thresh là ngưỡng LoG. Nhóm tự xác định cấu hình trước khi chạy và ghi nhận đầy đủ.

Mở kết quả:

```powershell
Get-Content .\ket_qua_A\bao_cao_tile3.csv
Invoke-Item .\ket_qua_A\tile3_harris_classic_doi_chieu.png
Invoke-Item .\ket_qua_A\tile3_harris_laplace_doi_chieu.png
```

Cần báo cả hai con số repeatability, không dùng số điểm 16 trên hình vuông thay cho chúng. Harris–Laplace không được bảo đảm thắng trên mọi ảnh. Harris cổ điển có thể tìm lại tốt trên một ảnh đơn giản; cần phân tích cơ chế và điều kiện cụ thể.

## 9. Những file kết quả dùng để báo cáo

- anh_goc_xam.png, anh_quay30.png, anh_tile3.png: ảnh đầu vào thực tế của các lần chạy.
- bao_cao_quay30.csv: một dòng Harris cổ điển.
- bao_cao_tile3.csv: hai dòng Harris cổ điển và Harris–Laplace.
- *_doi_chieu.png: ảnh điểm dự đoán và điểm phát hiện.
- *_goc.csv, *_dich.csv: toàn bộ điểm detector trả về, giữ cả metadata.
- *_du_doan.csv: tọa độ dự đoán và cờ nằm trong khung.
- cau_hinh_*.json: cấu hình, kích thước, ma trận biến đổi, phiên bản và module sử dụng.

Không có file kết quả không có nghĩa là kết quả bằng 0. Có thể khung đã dừng do thiếu hàm, sai đường dẫn, hoặc hàm của nhóm báo lỗi. Đọc dòng DUNG/THIEU trong terminal.

## 10. Notebook và khai báo AI

PDF yêu cầu một notebook đã Restart & Run All, lưu output, kèm thư mục anh/. Chạy terminal là bước kiểm tra thuận tiện, chưa thay cho yêu cầu nộp đó.

kiem_chung_A.ipynb là khung tự chứa phần điều phối thí nghiệm. Bạn đưa phần cài đặt do nhóm tự viết vào cell trống dưới tiêu đề Cài đặt — KHÔNG dùng AI. Khung không chứa các hàm thuật toán, nên notebook chưa thể chạy đủ ngay khi tải về.

Sau đó chọn đúng kernel .venv, chạy từ trên xuống. Các cell thí nghiệm gọi các hàm trong chính notebook bằng module __main__, không bắt buộc import harris.py khi nộp. Thư mục làm việc cần là BTVN2; cell chuẩn bị tự nhận diện BTVN2 nếu kernel mở từ gốc project.

Cell Markdown ngay trước mỗi cell hỗ trợ AI đã chép nguyên văn yêu cầu gần nhất của bạn. Giữ các cell đó; bổ sung nguyên văn prompt thực tế của các lần hỗ trợ khác nếu có. Chỉ đổi tên file thành bt1_GroupF.ipynb khi bạn đã tích hợp vào notebook bài nộp duy nhất của nhóm và tránh ghi đè bản đã có.

Bạn tự chọn ảnh, tự viết phần nhận xét và kết luận từ kết quả thực tế. Hai mục kiểm chứng này không thay thế phần thí nghiệm mở mục 5 hoặc những mục kiểm chứng khác.
