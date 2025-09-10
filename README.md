# String Search Studio

Ứng dụng mô phỏng thuật toán tìm kiếm chuỗi với giao diện trực quan.

## Cấu trúc dự án

```
APP_Search/
├── main.py                 # Entry point chính
├── config/                 # Cấu hình ứng dụng
│   ├── __init__.py
│   └── settings.py         # Các cấu hình UI, màu sắc, thuật toán
├── algorithms/             # Các thuật toán tìm kiếm
│   ├── __init__.py
│   ├── brute_force.py      # Thuật toán Brute Force
│   └── boyer_moore.py      # Thuật toán Boyer-Moore
├── ui/                     # Giao diện người dùng
│   ├── __init__.py
│   ├── base_widget.py      # Base widget cho các thuật toán
│   ├── brute_force_widget.py  # Widget cho Brute Force
│   ├── boyer_moore_widget.py  # Widget cho Boyer-Moore
│   └── main_window.py      # Main window
└── README.md
```

## Cách chạy

```bash
python main.py
```

## Tính năng

- **Brute Force Algorithm**: Thuật toán tìm kiếm chuỗi đơn giản
- **Boyer-Moore Algorithm**: Thuật toán tìm kiếm chuỗi tối ưu với Bad Character Rule
- **Giao diện trực quan**: Hiển thị từng bước của thuật toán
- **Điều khiển tốc độ**: Có thể điều chỉnh tốc độ mô phỏng
- **Zoom**: Có thể phóng to/thu nhỏ giao diện
- **Metrics**: Hiển thị thống kê về hiệu suất thuật toán

## Cấu trúc code

### 1. Config Package
- Chứa tất cả cấu hình của ứng dụng
- Dễ dàng thay đổi màu sắc, font, kích thước

### 2. Algorithms Package
- Tách biệt logic thuật toán khỏi giao diện
- Dễ dàng mở rộng thêm thuật toán mới
- Có thể test độc lập

### 3. UI Package
- Base widget cho các thuật toán
- Widget riêng cho từng thuật toán
- Main window quản lý toàn bộ ứng dụng

### 4. Main
- Entry point đơn giản
- Chỉ khởi tạo và chạy ứng dụng

## Lợi ích của cấu trúc mới

1. **Tách biệt concerns**: Logic thuật toán tách khỏi giao diện
2. **Dễ bảo trì**: Mỗi file có trách nhiệm rõ ràng
3. **Dễ mở rộng**: Thêm thuật toán mới chỉ cần tạo class mới
4. **Cấu hình tập trung**: Tất cả cấu hình ở một nơi
5. **Code reuse**: Base widget có thể dùng cho nhiều thuật toán
