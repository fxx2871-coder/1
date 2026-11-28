import torch
import torch.nn as nn

# ==========================================
# 1. 定义一个极简的 CNN（卷积神经网络）模型
# 用来模拟“输入图片 -> 提取特征 -> 输出信息”的过程
# ==========================================
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # 第一层：卷积层 (提取边缘、颜色等基础特征)
        # 输入通道3（RGB图片），输出通道16（提取16种不同的特征图）
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
        # 激活函数：增加非线性，让模型更聪明
        self.relu = nn.ReLU()
        # 池化层：把图片缩小一半，保留最重要的特征（压缩信息）
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # 第二层：全连接层 (将提取到的特征映射到最终的分类结果)
        # 假设输入图片是 64x64，经过池化后变成 32x32，16个通道就是 16*32*32
        self.fc = nn.Linear(16 * 32 * 32, 10) # 假设最终分10个类别

    def forward(self, x):
        # 对应大白话：数据向前传播
        x = self.conv1(x)       # 1. 卷积提取特征
        x = self.relu(x)        # 2. 激活
        x = self.pool(x)        # 3. 池化降维
        x = x.view(x.size(0), -1) # 4. 展平成一维向量（准备进全连接层）
        x = self.fc(x)          # 5. 输出最终的10个类别的得分
        return x

# ==========================================
# 2. 模拟输入一张图片并运行
# ==========================================
if __name__ == "__main__":
    # 模拟输入一张 3通道(RGB)、64x64大小的图片
    # (batch_size=1表示一次输入1张图)
    fake_image = torch.randn(1, 3, 64, 64) 
    
    print(f"输入图片的维度: {fake_image.shape}")
    
    # 实例化我们的网络模型
    model = SimpleCNN()
    
    # 前向传播：把图片扔给模型
    output = model(fake_image)
    
    print(f"经过网络处理后，输出的特征向量维度: {output.shape}")
    print("这代表了模型对这张图片提取出的抽象信息（比如预测为各类别的概率）。")