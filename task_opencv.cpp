#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main() {
    // 0. 读取原图 (确保同一目录下有一张 image.png)
    Mat img = imread("image.png");
    if (img.empty()) {
        cout << "兄弟，图没找到，检查下图片名字是不是叫 image.png" << endl;
        return -1;
    }

    // ==========================================
    // TASK2: 变成灰度图
    // ==========================================
    Mat gray;
    cvtColor(img, gray, COLOR_BGR2GRAY);
    imshow("TASK2 - Gray", gray);

    // ==========================================
    // TASK3: 背景白色变黑色 (按位取反)
    // ==========================================
    Mat black_bg;
    bitwise_not(img, black_bg);
    imshow("TASK3 - White to Black", black_bg);

    // ==========================================
    // TASK4: 单RGB输出 (分离通道，这里只展示蓝色通道)
    // ==========================================
    vector<Mat> channels;
    split(img, channels); // 分离成 B, G, R
    Mat only_blue = Mat::zeros(img.size(), img.type());
    // 只保留 B 通道 (OpenCV 默认是 BGR，所以索引 0 是蓝色)
    // 把蓝色通道数据塞进空图的对应位置
    vector<Mat> blue_channels = { channels[0], Mat::zeros(img.size(), CV_8UC1), Mat::zeros(img.size(), CV_8UC1) };
    merge(blue_channels, only_blue);
    imshow("TASK4 - Only Blue (BGR)", only_blue);

    // ==========================================
    // TASK5: 文字部分用红线圈出
    // 灰度图 -> 二值化 -> 膨胀 -> 描边
    // ==========================================
    // 1. 二值化 (反向)：为了找轮廓，黑底白字。THRESH_BINARY_INV
    Mat thresh;
    threshold(gray, thresh, 127, 255, THRESH_BINARY_INV);

    // 2. 膨胀：用一个 15x15 的大方块核，强行把字粘连在一起
    Mat dilated;
    Mat kernel = getStructuringElement(MORPH_RECT, Size(15, 15));
    dilate(thresh, dilated, kernel, Point(-1, -1), 2); // 膨胀2次

    // 3. 找轮廓
    vector<vector<Point>> contours;
    findContours(dilated, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    // 4. 在原图上画红线
    Mat img_boxed = img.clone();
    // 参数：(图片, 轮廓, 画所有(-1), 颜色红色, 线宽4)
    drawContours(img_boxed, contours, -1, Scalar(0, 0, 255), 4);
    imshow("TASK5 - Red Box", img_boxed);

    // ==========================================
    // TASK6: 向左旋转 45 度
    // ==========================================
    Point2f center(img.cols / 2.0, img.rows / 2.0); // 图片中心点
    // 获取旋转矩阵：正数45度代表逆时针(向左)
    Mat M = getRotationMatrix2D(center, 45, 1.0);
    Mat rotated;
    // 仿射变换，后面露出来的黑边用白色填补 (Scalar(255,255,255))
    warpAffine(img, rotated, M, img.size(), INTER_LINEAR, 0, Scalar(255, 255, 255));
    imshow("TASK6 - Rotate 45 Left", rotated);

    // 等待按键，按任意键关闭
    waitKey(0);
    destroyAllWindows();

    return 0;
}