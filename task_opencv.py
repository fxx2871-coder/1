import cv2
import numpy as np

# 0. 读取原图（确保同目录下有个叫 image.jpg 的图片）
img = cv2.imread('image.png')
if img is None:
    print("兄弟，图没找到，检查下图片名字是不是叫 image.png")
    exit()

# ==========================================
# TASK2: 变成灰度图
# ==========================================
# 把三通道彩色图转成单通道，也就是黑白灰
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('TASK2 - Gray', gray)

# ==========================================
# TASK3: 背景白色变黑色
# ==========================================
# 白底黑字看着难受，直接用 bitwise_not 取反，白的变黑，黑的变白
black_bg = cv2.bitwise_not(img)
cv2.imshow('TASK3 - White to Black', black_bg)

# ==========================================
# TASK4: 单RGB输出
# ==========================================
# OpenCV读进来是BGR格式，直接切片强行分离出来
b, g, r = cv2.split(img)
# 把只有蓝通道的图输出看看（只保留B通道，G和R全变0）
only_blue = np.zeros_like(img)
only_blue[:, :, 0] = b
cv2.imshow('TASK4 - Only Blue (BGR)', only_blue)

# ==========================================
# TASK5: 文字部分用红线圈出
# 按照提示：灰度图 -> 二值化 -> 膨胀 -> 描边
# ==========================================
# 1. 灰度图已经有了
# 2. 二值化：为了找轮廓，最好弄成黑底白字。THRESH_BINARY_INV 就是反向二值化
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# 3. 膨胀：因为字体的笔画可能断开，用膨胀让字变胖连在一起，方便后面圈个大框
# 弄个 15x15 的方形核，简单粗暴
kernel = np.ones((15, 15), np.uint8)
# 膨胀 2 次，让字彻底连成一片
dilated = cv2.dilate(thresh, kernel, iterations=2)

# 4. 找轮廓
contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 5. 描边：在原图上画红线
img_boxed = img.copy()
# 参数：(图片, 轮廓列表, -1表示画所有轮廓, 颜色(0,0,255是红色), 线宽)
cv2.drawContours(img_boxed, contours, -1, (0, 0, 255), 4)
cv2.imshow('TASK5 - Red Box', img_boxed)

# ==========================================
# TASK6: 向左旋转 45 度
# ==========================================
h, w = img.shape[:2]
# 找图片正中心
center = (w // 2, h // 2)
# 获取旋转矩阵，正数 45 代表逆时针（也就是向左）
M = cv2.getRotationMatrix2D(center, 45, 1.0)
# 执行旋转，边框用白色(255,255,255)填补
rotated = cv2.warpAffine(img, M, (w, h), borderValue=(255, 255, 255))
cv2.imshow('TASK6 - Rotate 45', rotated)

# 按任意键退出并销毁窗口
cv2.waitKey(0)
cv2.destroyAllWindows()