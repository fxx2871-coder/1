import os
import json
import glob

# 你的 json 标签文件夹路径（根据你昨天的搜索，就是这个）
json_dir = r"C:\Users\Lenovo\ultralytics\labels" 
# 你想保存 txt 的文件夹路径
txt_dir = r"C:\Users\Lenovo\ultralytics\labels_yolo"

os.makedirs(txt_dir, exist_ok=True)

# 映射你的中文类别到 YOLO 的数字 ID（0, 1, 2...）
# 请确保这里的类别名和你 AnyLabeling 里输入的一模一样！
class_mapping = {
    "电动车": 0,
    "汽车": 1,
    "自行车": 2
}

# 遍历所有 json 文件
for json_file in glob.glob(os.path.join(json_dir, "*.json")):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取原图宽高，用于归一化
    img_width = data.get("imageWidth", 1920) 
    img_height = data.get("imageHeight", 1080) 

    txt_lines = []
    for shape in data.get("shapes", []):
        label = shape.get("label")
        if label not in class_mapping:
            continue
        
        class_id = class_mapping[label]
        points = shape.get("points")
        
        # 提取左上角和右下角坐标
        x_min = min(p[0] for p in points)
        y_min = min(p[1] for p in points)
        x_max = max(p[0] for p in points)
        y_max = max(p[1] for p in points)
        
        # 转换为 YOLO 格式：中心点 x, 中心点 y, 宽度, 高度 （全部归一化到 0~1）
        x_center = ((x_min + x_max) / 2) / img_width
        y_center = ((y_min + y_max) / 2) / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height
        
        txt_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    
    # 保存为 txt
    base_name = os.path.basename(json_file).replace(".json", ".txt")
    txt_path = os.path.join(txt_dir, base_name)
    with open(txt_path, 'w') as f:
        f.write("\n".join(txt_lines))
        
    print(f"成功转换: {base_name}")

print("全部转换完成！")