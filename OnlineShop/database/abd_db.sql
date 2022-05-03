-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th5 03, 2022 lúc 11:06 AM
-- Phiên bản máy phục vụ: 10.4.22-MariaDB
-- Phiên bản PHP: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `abd_db`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `fullName` varchar(125) COLLATE utf8_vietnamese_ci NOT NULL,
  `email` varchar(100) COLLATE utf8_vietnamese_ci NOT NULL,
  `mobile` varchar(25) COLLATE utf8_vietnamese_ci NOT NULL,
  `address` text COLLATE utf8_vietnamese_ci NOT NULL,
  `password` varchar(100) COLLATE utf8_vietnamese_ci NOT NULL,
  `type` varchar(20) COLLATE utf8_vietnamese_ci NOT NULL,
  `confirmCode` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `admin`
--

INSERT INTO `admin` (`id`, `fullName`, `email`, `mobile`, `address`, `password`, `type`, `confirmCode`) VALUES
(4, 'Nguyen Huu Dang', 'manager@gmail.com', '0123456789', 'Tay Ninh', '$5$rounds=535000$WOAOMdgoK2JpZLY5$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', 'manager', '0'),
(5, 'Bao', 'emp1@gmail.com', '0123456789', 'Dong Thap', '$5$rounds=535000$WOAOMdgoK2JpZLY5$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', 'emp', '0'),
(6, 'Nguyen Van A', 'emp3@gmail.com', '+847866282809', '454 Đường Nguyễn Chí Thanh', '$5$rounds=535000$Z9aodPH2/cgVLFcq$SiKFn4EsztYSk4u47r6LINu72QLxyAYWNrype2qtlV7', 'emp', ''),
(7, 'cskh', 'cskh@gmail.com', '+847866282809', '454 Đường Nguyễn Chí Thanh', '$5$rounds=535000$Z9aodPH2/cgVLFcq$SiKFn4EsztYSk4u47r6LINu72QLxyAYWNrype2qtlV7', 'cskh', '');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `body` text NOT NULL,
  `msg_by` int(11) NOT NULL,
  `msg_to` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `uid` int(11) DEFAULT NULL,
  `ofname` text CHARACTER SET utf8 COLLATE utf8_vietnamese_ci NOT NULL,
  `pid` int(11) NOT NULL,
  `pName` varchar(100) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci NOT NULL,
  `quantity` int(11) NOT NULL,
  `total` int(11) NOT NULL,
  `oplace` text CHARACTER SET utf8 COLLATE utf8_vietnamese_ci NOT NULL,
  `mobile` varchar(15) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci NOT NULL,
  `dstatus` varchar(10) CHARACTER SET utf8 COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `odate` timestamp NOT NULL DEFAULT current_timestamp(),
  `ddate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `orders`
--

INSERT INTO `orders` (`id`, `uid`, `ofname`, `pid`, `pName`, `quantity`, `total`, `oplace`, `mobile`, `dstatus`, `odate`, `ddate`) VALUES
(33, NULL, 'admin', 6, '', 1, 21000, 'NguyenHuu Dnawg', '+84786628280', 'no', '2022-05-03 08:50:37', '2022-05-10'),
(34, NULL, 'admin', 6, 'Laptop Dell Vostro 14 3400 Office', 1, 21000, 'NguyenHuu Dnawg', '+84786628280', 'no', '2022-05-03 08:54:48', '2022-05-10'),
(35, 16, 'dang', 8, 'Laptop APPLE MacBook Pro 2021 14', 2, 106000, 'NguyenHuu Dnawg', '01234567891', 'no', '2022-05-03 08:58:13', '2022-05-10'),
(36, 16, 'dang', 2, 'Laptop ASUS Gaming FX506LH-HN188W', 1, 18000, 'TPHCM', '01234567891', 'no', '2022-05-03 09:04:42', '2022-05-10');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `pName` varchar(100) COLLATE utf8_vietnamese_ci NOT NULL,
  `price` int(11) NOT NULL,
  `description` mediumtext COLLATE utf8_vietnamese_ci NOT NULL,
  `available` int(11) NOT NULL,
  `category` varchar(100) COLLATE utf8_vietnamese_ci NOT NULL,
  `item` varchar(100) COLLATE utf8_vietnamese_ci NOT NULL,
  `pCode` varchar(20) COLLATE utf8_vietnamese_ci NOT NULL,
  `picture` mediumtext COLLATE utf8_vietnamese_ci NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `products`
--

INSERT INTO `products` (`id`, `pName`, `price`, `description`, `available`, `category`, `item`, `pCode`, `picture`, `date`) VALUES
(1, 'Laptop ACER Gaming Aspire 7 ', 16000, '- CPU: AMD Ryzen 5 5500U\r\n- Màn hình: 15.6\" IPS (1920 x 1080), 144Hz\r\n- RAM: 1 x 8GB DDR4 3200MHz\r\n- Đồ họa: NVIDIA GeForce GTX 1650 4GB GDDR6 / AMD Radeon Graphics\r\n- Lưu trữ: 512GB SSD M.2 NVMe /\r\n- Hệ điều hành: Windows 11 Home\r\n- 48 Wh\r\n- Khối lượng: 2.1 kg', 10, 'laptop', 'balo', 'l-001', 'lap1.png', '2022-05-02 15:42:36'),
(2, 'Laptop ASUS Gaming FX506LH-HN188W', 18000, '- CPU: Intel Core i5-10300H\r\n- Màn hình: 15.6\" IPS (1920 x 1080), 144Hz\r\n- RAM: 1 x 8GB DDR4\r\n- Đồ họa: NVIDIA GeForce GTX 1650 4GB GDDR6 / Intel UHD Graphics\r\n- Lưu trữ: 512GB SSD M.2 NVMe /\r\n- Hệ điều hành: Windows 11 Home\r\n- Pin: 3 cell 48 Wh\r\n- Khối lượng: 2.3 kg', 4, 'laptop', 'Balo', 'l-002', 'lap2.png', '2022-05-02 16:14:07'),
(3, 'Laptop ASUS TUF Gaming ', 17000, '- CPU: AMD Ryzen 5 4600H\r\n- Màn hình: 15.6\" IPS (1920 x 1080), 144Hz\r\n- RAM: 1 x 8GB DDR4 3200MHz\r\n- Đồ họa: NVIDIA GeForce GTX 1650 4GB GDDR6 / AMD Radeon Graphics\r\n- Lưu trữ: 512GB SSD M.2 NVMe /\r\n- Hệ điều hành: Windows 11 Home\r\n- Pin: 3 cell 48 Wh Pin liền\r\n- Khối lượng: 2.3 kg', 15, 'laptop', 'None', 'l-003', 'lap3.png', '2022-05-02 16:25:22'),
(4, 'Laptop Lenovo Ideapad Gaming 3', 17500, '- CPU: Intel Core i5-10300H\r\n- Màn hình: 15.6\" IPS (1920 x 1080), 120Hz\r\n- RAM: 1 x 8GB DDR4 2933MHz\r\n- Đồ họa: NVIDIA GeForce GTX 1650 4GB GDDR6 / Intel UHD Graphics\r\n- Lưu trữ: 512GB SSD M.2 NVMe /\r\n- Hệ điều hành: Windows 10 Home 64-bit\r\n- 45 Wh Pin liền\r\n- Khối lượng: 2.2 kg', 29, 'laptop', 'None', 'l-004', 'lap4.png', '2022-05-02 16:31:15'),
(5, 'Laptop Lenovo Yoga Slim 7 Pro', 33000, '- CPU: Intel Core i7-11370H\r\n- Màn hình: 14\" OLED (2880 x 1800), 90Hz\r\n- RAM: 16GB Onboard LPDDR4X 4266MHz\r\n- Đồ họa: NVIDIA GeForce MX450 2GB GDDR6 / Intel Iris Xe Graphics\r\n- Lưu trữ: 1TB SSD M.2 NVMe /\r\n- Hệ điều hành: Windows 11 Home\r\n- 61 Wh Pin liền\r\n- Khối lượng: 1.3 kg', 12, 'laptop', 'balo', 'l-005', 'lap5.png', '2022-05-02 16:33:30'),
(6, 'Laptop Dell Vostro 14 3400 Office', 21000, '- CPU: Intel Core i5-1135G7\r\n- Màn hình: 14\" (1920 x 1080)\r\n- RAM: 1 x 8GB DDR4 3200MHz\r\n- Đồ họa: NVIDIA GeForce MX330 2GB GDDR5 / Intel Iris Xe Graphics\r\n- Lưu trữ: 512GB SSD M.2 NVMe /\r\n- Hệ điều hành: Windows 11 Home SL 64-bit + Office\r\n- Pin: 3 cell 42 Wh\r\n- Khối lượng: 1.6 kg', 8, 'laptop', 'None', 'l-006', 'lap6.png', '2022-05-02 16:35:04'),
(7, 'Laptop ASUS Vivobook Office S533EQ', 19000, '- CPU: Intel Core i5-1135G7\r\n- Màn hình: 15.6\" IPS (1920 x 1080)\r\n- RAM: 8GB Onboard DDR4 3200MHz\r\n- Đồ họa: NVIDIA GeForce MX350 2GB GDDR5 / Intel Iris Xe Graphics\r\n- Lưu trữ: 512GB SSD M.2 NVMe /\r\n- Hệ điều hành: Windows 10 Home SL 64-bit\r\n- Pin: 3 cell 50 Wh Pin liền\r\n- Khối lượng: 1.6 kg', 19, 'laptop', 'balo', 'l-007', 'lap7.png', '2022-05-02 16:36:36'),
(8, 'Laptop APPLE MacBook Pro 2021 14', 53000, '- CPU: Apple M1 Pro\r\n- Màn hình: 14\" (3024 x 1964)\r\n- RAM: 16GB\r\n- Đồ họa:\r\n- Lưu trữ: 512GB SSD /\r\n- Hệ điều hành: macOS\r\n- 70 Wh\r\n- Khối lượng: 1.6 kg', 39, 'laptop', 'None', 'l-008', 'lap8.png', '2022-05-02 16:38:16'),
(9, 'Màn Hình Dell 21.5\" E2216HV', 3600, '- Kích thước: 21.5\"\r\n- Độ phân giải: 1920 x 1080 ( 16:9 )\r\n- Công nghệ tấm nền: TN\r\n- Góc nhìn: 90 (H) / 65 (V)\r\n- Tần số quét: 60Hz\r\n- Thời gian phản hồi: 5 ms', 20, 'screen', 'none', 's-001', 'sc1.png', '2022-05-02 17:01:49'),
(10, 'Màn hình LCD Dell E2222HS ', 4000, '- Kích thước: 21.5\" (1920 x 1080), Tỷ lệ 16:9\r\n- Tấm nền VA, Góc nhìn: 178 (H) / 178 (V)\r\n- Tần số quét: 60Hz , Thời gian phản hồi 5 ms\r\n- HIển thị màu sắc: 16.7 triệu màu\r\n- Cổng hình ảnh: 1 x DisplayPort 1.2, 1 x HDMI 1.2, 1 x VGA/D-sub', 30, 'screen', 'none', 's-002', 'sc2.png', '2022-05-02 17:03:45'),
(11, 'Màn hình LCD Dell U2520D', 10000, '- Kích thước: 25\"\r\n\r\n- Độ phân giải: 2560 x 1440 ( 16:9 )\r\n\r\n- Công nghệ tấm nền: IPS\r\n\r\n- Góc nhìn: 178 (H) / 178 (V)\r\n\r\n- Tần số quét: 60Hz\r\n\r\n- Thời gian phản hồi: 8 ms', 10, 'screen', 'none', 's-003', 'sc3.png', '2022-05-02 17:05:56'),
(12, 'Màn Hình Acer Nitro 23.8', 4200, '- Kích thước: 23.8\"\r\n- Độ phân giải: 1920 x 1080 ( 16:9 )\r\n- Công nghệ tấm nền: IPS\r\n- Góc nhìn: 178 (H) / 178 (V)\r\n- Tần số quét: 75Hz\r\n- Thời gian phản hồi: 1 ms', 10, 'screen', 'none', 's-004', 'sc4.png', '2022-05-02 17:07:34'),
(13, 'Bàn phím cơ Gaming Logitech G Pro X', 3800, '- Loại kết nối bàn phím: Bàn phím có dây\r\n- Kết nối của bàn phím: USB\r\n- Kích thước của bàn phím: Tenkeyless', 50, 'keyboard', 'none', 'k-001', 'kb1.png', '2022-05-02 17:22:19'),
(14, 'Bàn phím cơ Logitech Gaming G813', 3100, '- Bàn phím cơ\r\n- Kết nối: USB\r\n- Switch: GL Clicky\r\n- Phím chức năng: Có', 30, 'keyboard', 'none', 'k-002', 'kb2.png', '2022-05-02 17:23:30'),
(15, 'Bàn phím Logitech Bluetooth K380', 800, '- Bàn phím thường\r\n- Kết nối Bluetooth', 100, 'keyboard', 'none', 'k-003', 'kb3.png', '2022-05-02 17:25:18'),
(16, 'Bàn phím gập Bluetooth MIPOW MINI', 1600, '- 65 phím với 120 chức năng\r\n- Túi có thể gập lại gọn gàng\r\n- Nguồn điện Chế độ tiết kiệm năng lượng\r\n- Không hoạt động 10 phút tự chuyển sang chế độ Ngủ\r\n- Khi hết pin, đèn LED đỏ nhấp nháy\r\n- Không thấm nước\r\n- Hỗ trợ Apple TV, Smart TV bật', 20, 'keyboard', 'none', 'k-004', 'kb4.png', '2022-05-02 17:27:12'),
(17, 'Chuột gaming Logitech G502 HERO', 1100, '- Kiểu kết nối: Có dây\r\n- Cảm biến: HERO\r\n- Độ phân giải: 16000 DPI\r\n- Tốc độ phản hồi: 1000 Hz (1ms)\r\n- Màu sắc: Đen', 10, 'mouse', 'none', 'm-001', 'm1.png', '2022-05-02 17:30:09'),
(18, 'Chuột chơi game Logitech G304 Wireless', 800, '- Kiểu kết nối: Không dây\r\n- Dạng cảm biến: HERO\r\n- Độ phân giải: 12000 DPI\r\n- Tốc độ phản hồi: 1000 Hz (1 ms)\r\n- Màu sắc: Đen', 10, 'mouse', 'none', 'm-002', 'm2.png', '2022-05-02 17:31:31'),
(19, 'Chuột GIGABYTE Aorus M5 Gaming', 1200, '- Thương hiệu: Gigabyte \r\n- Chuẩn kết nối: USB \r\n- Omron Switch, RGB Led tích hợp', 0, 'mouse', 'none', 'm-003', 'm3.png', '2022-05-02 17:32:28'),
(20, 'Chuột gaming CORSAIR IRONCLAW Wireless', 2000, '- Chuột chơi game IRONCLAW RGB dành cho game FPS và MOBA \r\n- Cảm biến quang học với DPI lên đến 18.000 \r\n- Khối lượng thân chuột 105g cùng thiết kế dạng cong phù hợp cho kiểu cầm palm-grips và người dùng có bàn tay to', 30, 'mouse', 'none', 'm-004', 'm4.png', '2022-05-02 17:33:24');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `product_level`
--

CREATE TABLE `product_level` (
  `id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `dell` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `asus` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `apple` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `lenovo` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `gaming` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `office` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `acer` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `screen_4k` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `screen_2k` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `bluetooth` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `cable` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `screen_22` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `screen_24` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `screen_gaming` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `screen_graphics` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `new_product` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `logitech` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `razer` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no',
  `edra` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'no'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `product_level`
--

INSERT INTO `product_level` (`id`, `product_id`, `dell`, `asus`, `apple`, `lenovo`, `gaming`, `office`, `acer`, `screen_4k`, `screen_2k`, `bluetooth`, `cable`, `screen_22`, `screen_24`, `screen_gaming`, `screen_graphics`, `new_product`, `logitech`, `razer`, `edra`) VALUES
(1, 1, 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(2, 2, 'no', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(3, 3, 'no', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(4, 4, 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(5, 5, 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(6, 6, 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(7, 7, 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(8, 8, 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(9, 9, 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(10, 10, 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(11, 11, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(12, 12, 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(13, 13, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no'),
(14, 14, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(15, 15, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no'),
(16, 16, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(17, 17, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(18, 18, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(19, 19, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(20, 20, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `product_view`
--

CREATE TABLE `product_view` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) COLLATE utf8_vietnamese_ci NOT NULL,
  `email` varchar(50) COLLATE utf8_vietnamese_ci NOT NULL,
  `username` varchar(25) COLLATE utf8_vietnamese_ci NOT NULL,
  `password` varchar(100) COLLATE utf8_vietnamese_ci NOT NULL,
  `mobile` varchar(20) COLLATE utf8_vietnamese_ci NOT NULL,
  `reg_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `online` varchar(1) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT '0',
  `activation` varchar(3) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'yes',
  `role` varchar(10) COLLATE utf8_vietnamese_ci NOT NULL DEFAULT 'user'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_vietnamese_ci;

--
-- Đang đổ dữ liệu cho bảng `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `mobile`, `reg_time`, `online`, `activation`, `role`) VALUES
(16, 'dang', 'a@gmail.com', 'dang', '$5$rounds=535000$lGtW0lOiCG2IW47Y$sqN34AZA1fsmSiDF9cCuR3FBUE2Jd1NRD7K9CTjg9y/', '01234567891', '2022-05-01 13:18:36', '1', 'yes', 'user'),
(17, 'cskh', 'cskh@gmail.com', 'cskh', '$5$rounds=535000$lGtW0lOiCG2IW47Y$sqN34AZA1fsmSiDF9cCuR3FBUE2Jd1NRD7K9CTjg9y/', '01234567891', '2022-05-01 13:18:36', '1', 'yes', 'cskh'),
(18, 'Nguyen Van A', 'nguyenvana@gmail.com', 'user1', '$5$rounds=535000$cu3AqpcSBdUABVFb$zCHuny/k7ie1CbARi.UIO7YAbhYhVrTTYpDnUvj4Tj.', '078225134737', '2022-05-03 05:41:22', '1', 'yes', 'user');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `product_level`
--
ALTER TABLE `product_level`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `product_view`
--
ALTER TABLE `product_view`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT cho bảng `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT cho bảng `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT cho bảng `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT cho bảng `product_level`
--
ALTER TABLE `product_level`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT cho bảng `product_view`
--
ALTER TABLE `product_view`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
