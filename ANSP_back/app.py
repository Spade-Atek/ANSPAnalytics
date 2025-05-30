from flask import Flask, request, send_file, jsonify, Response
import os
import io
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import gridspec
import re

app = Flask(__name__)

#设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 配置上传文件的保存路径、excel结果文件的保存路径
EXCEL_UPLOAD_FOLDER = '/templates/uploads'
EXCEL_OUTPUT_FOLDER = '/templates/output_excel'
IMAGE_UPLOAD_FOLDER = "/templates/image"
SZC_EXCEL_UPLOAD_FOLDER = '/templates/upload_szc_data'
SZC_OUTPUT_FOLDER = '/templates/output_szc_data'
MZC_EXCEL_UPLOAD_FOLDER = '/templates/upload_mzc_data'
MZC_OUTPUT_FOLDER = '/templates/output_mzc_data'
if not os.path.exists(EXCEL_UPLOAD_FOLDER):
    os.makedirs(EXCEL_UPLOAD_FOLDER)
if not os.path.exists(EXCEL_OUTPUT_FOLDER):
    os.makedirs(EXCEL_OUTPUT_FOLDER)
if not os.path.exists(IMAGE_UPLOAD_FOLDER):
    os.makedirs(IMAGE_UPLOAD_FOLDER)
if not os.path.exists(SZC_EXCEL_UPLOAD_FOLDER):
    os.makedirs(SZC_EXCEL_UPLOAD_FOLDER)
if not os.path.exists(SZC_OUTPUT_FOLDER):
    os.makedirs(SZC_OUTPUT_FOLDER)
if not os.path.exists(MZC_EXCEL_UPLOAD_FOLDER):
    os.makedirs(MZC_EXCEL_UPLOAD_FOLDER)
if not os.path.exists(MZC_OUTPUT_FOLDER):
    os.makedirs(MZC_OUTPUT_FOLDER)

# 设置允许上传的文件类型
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#计算加权重心
def calculate_weighted_centroid(points, weights):
    total_weight = np.sum(weights)
    weighted_x = np.sum(points[:, 0] * weights) / total_weight
    weighted_y = np.sum(points[:, 1] * weights) / total_weight
    return np.array([weighted_x, weighted_y])

#城市坐标数据
cities = {
    '武汉市': [114.00, 30.50],
    '黄石市': [115.00, 30.00],
    '十堰市': [110.00, 32.00],
    '宜昌市': [111.00, 30.50],
    '襄阳市': [112.13, 32.00],
    '荆门市': [112.21, 30.50],
    '鄂州市': [114.89, 30.39],
    '孝感市': [113.87, 30.89],
    '荆州市': [112.23, 30.32],
    '黄冈市': [114.89, 30.45],
    '咸宁市': [114.32, 29.86],
    '随州市': [113.37, 31.68],
    '恩施州': [109.47, 30.29],
    '仙桃市': [113.45, 30.32],
    '潜江市': [112.68, 30.43],
    '天门市': [113.17, 30.65],
    '神农架林区': [110.67, 31.65]
}

city_names = list(cities.keys())
points = np.array([cities[city] for city in city_names])

#读取某一期污染强度数据
def read_pollution_weights(filepath):
    df = pd.read_excel(filepath)
    city_to_weight = dict(zip(df.iloc[:, 0], df.iloc[:, 6]))
    weights = np.array([city_to_weight.get(city, 0) for city in city_names])
    return weights

def szc():
    # 读取第一期数据（修改为你的实际文件名）
    input_filename = "output.xlsx"
    input_path = os.path.join(SZC_EXCEL_UPLOAD_FOLDER, input_filename)
    save_path = os.path.join(SZC_OUTPUT_FOLDER, "szc_fig.jpeg")

    weights_time1 = read_pollution_weights(input_path)
    # 计算重心
    centroid = calculate_weighted_centroid(points, weights_time1)
    # 绘图
    plt.figure(figsize=(14, 10))
    plt.scatter(points[:, 0], points[:, 1], s=weights_time1 * 400, c='blue', alpha=0.6,
                label='城市点位(大小表示污染强度)')
    for i, city in enumerate(city_names):
        plt.annotate(city, (points[i, 0], points[i, 1]), textcoords="offset points", xytext=(0, 5), ha='center')
    plt.scatter(centroid[0], centroid[1], s=300, c='red', marker='*', label='加权重心')
    plt.title('湖北省农业面源污染源分布与加权重心', fontsize=20)
    plt.xlabel('经度', fontsize=15)
    plt.ylabel('纬度', fontsize=15)
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path,dpi=300)

    print(f"第一期加权重心坐标: 经度={centroid[0]:.4f}°, 纬度={centroid[1]:.4f}°")

# 计算加权重心
def calculate_weighted_centroid(points, weights):
    total_weight = np.sum(weights)
    weighted_x = np.sum(points[:, 0] * weights) / total_weight
    weighted_y = np.sum(points[:, 1] * weights) / total_weight
    return np.array([weighted_x, weighted_y])

# 读取污染强度权重
def read_pollution_weights(filepath):
    df = pd.read_excel(filepath)
    city_to_weight = dict(zip(df.iloc[:, 0], df.iloc[:, 6]))  # 可改为列名
    weights = np.array([city_to_weight.get(city, 0) for city in city_names])
    return weights

# 计算两点间距离与方向
def calculate_movement(centroid1, centroid2):
    dx = centroid2[0] - centroid1[0]
    dy = centroid2[1] - centroid1[1]
    distance = np.sqrt(dx**2 + dy**2)
    angle = np.degrees(np.arctan2(dy, dx))
    return distance, angle

# 获取符合规则的污染文件
def get_sorted_pollution_files(directory):
    files = [f for f in os.listdir(directory) if re.match(r'output\d+\.xlsx', f)]
    files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
    return [os.path.join(directory, f) for f in files]

# mzc主函数
def analyze_migration(data_dir='.', save_path=None):
    filepaths = get_sorted_pollution_files(data_dir)
    print(filepaths)
    if len(filepaths) < 2:
        print("❗ 至少需要两个时间段的文件（如 pollution_time1.xlsx 和 pollution_time2.xlsx）")
        return

    centroids = []
    for path in filepaths:
        weights = read_pollution_weights(path)
        centroid = calculate_weighted_centroid(points, weights)
        centroids.append(centroid)

    # 构造信息文本
    info_lines = []
    total_distance = 0
    for i in range(len(centroids) - 1):
        c1, c2 = centroids[i], centroids[i + 1]
        distance, angle = calculate_movement(c1, c2)
        total_distance += distance
        info_lines.append(f"第{i+1}期 → 第{i+2}期：迁移距离 = {distance:.4f} 度, 方向角 = {angle:.1f}°")

    for i, c in enumerate(centroids):
        info_lines.append(f"第{i+1}期重心坐标：经度 = {c[0]:.4f}, 纬度 = {c[1]:.4f}")

    info_lines.append(f"总迁移距离：{total_distance:.4f} 度")
    full_text = "\n\n".join(info_lines)  # 加大行间距

    # 创建图和信息区域
    fig = plt.figure(figsize=(16, 8))
    spec = gridspec.GridSpec(nrows=1, ncols=2, width_ratios=[3, 2])

    # 图层1：地图 + 路径
    ax1 = fig.add_subplot(spec[0])
    ax1.scatter(points[:, 0], points[:, 1], s=50, c='gray', alpha=0.3, label='城市点位')

    for city in ['武汉市', '宜昌市', '襄阳市', '十堰市']:
        idx = city_names.index(city)
        ax1.annotate(city, (points[idx, 0], points[idx, 1]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)

    colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown']
    for i, centroid in enumerate(centroids):
        ax1.scatter(centroid[0], centroid[1], s=150, c=colors[i % len(colors)], marker='o', label=f'第{i+1}期重心')

    for i in range(len(centroids) - 1):
        c1, c2 = centroids[i], centroids[i + 1]
        ax1.arrow(c1[0], c1[1], c2[0] - c1[0], c2[1] - c1[1],
                  head_width=0.05, head_length=0.07, fc='black', ec='black',
                  linewidth=1, length_includes_head=True)

    ax1.set_title('农业面源污染重心多期迁移路径图', fontsize=20)
    ax1.set_xlabel('经度', fontsize=15)
    ax1.set_ylabel('纬度', fontsize=15)
    ax1.legend(fontsize=10)
    ax1.grid(True)

    # 图层2：信息文本 + 墨绿色边框方框
    ax2 = fig.add_subplot(spec[1])
    ax2.axis('off')

    # 墨绿色边框 + 灰色背景 + 包含文字
    bbox_props = dict(boxstyle="round,pad=0.5", facecolor='#f9f9f9',
                      edgecolor='darkgreen', linewidth=2)

    ax2.text(0.03, 0.97, full_text,
             fontsize=16,
             va='top', ha='left',
             transform=ax2.transAxes,
             bbox=bbox_props,
             wrap=True,
             linespacing=1.8,
             color='black')

    plt.tight_layout()
    plt.savefig(save_path,dpi=500)
@app.route('/')
def hello_world():  # put application's code here
    return 'ANSP_back!'

# 清单分析
@app.route('/process_qdfx',methods=['POST'])
def process_qdfx():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    # 检查文件是否为空
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # 检查文件扩展名是否为 Excel 文件
    if file and file.filename.endswith(('.xlsx', '.xls')):
        try:
            # 保存上传的文件
            file_path = os.path.join(EXCEL_UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            # 读取 Excel 文件
            df = pd.read_excel(file_path)
            # 检查必要的列是否存在
            required_columns = ['tn', 'tp', 'tc', 'tf', 'area']
            if not all(column in df.columns for column in required_columns):
                return jsonify({'error': 'Missing required columns in the Excel file'}), 400
            # 计算耕地面源污染排放量
            intensity_all = (
                    0.2 * df["tn"] +
                    0.1 * df["tp"] +
                    0.01 * df["tc"] +
                    0.05 * df["tf"]
            )
            # 计算耕地面源污染强度
            df["intensity"] = intensity_all / df["area"]
            # 保存结果到新的 Excel 文件
            # output_filename = f"{os.path.splitext(file.filename)[0]}_计算结果.xlsx"
            output_filename = "output.xlsx"
            output_path = os.path.join(EXCEL_OUTPUT_FOLDER, output_filename)
            df.to_excel(output_path, index=False)
            return jsonify({'message': 'File processed successfully', 'output_file': output_filename})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

# 重心分析
@app.route('/process_szc',methods=['POST'])
def process_szc():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        # 保存文件到指定的上传文件夹
        filename = "output.xlsx"
        #filename = file.filename
        save_path = os.path.join(SZC_EXCEL_UPLOAD_FOLDER, filename)
        file.save(save_path)
        szc()
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

# 迁移分析
@app.route('/process_mzc',methods=['POST'])
def process_mzc():
    if 'files' not in request.files:
        return jsonify({"error": "No file part"}), 400
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No selected files"}), 400
    saved_files = []
    for index, file in enumerate(files):
        if file and allowed_file(file.filename):
            # 为文件生成新的名字，如 output1.xlsx, output.xlsx 等
            new_filename = f"output{index + 1}.xlsx"
            save_path = os.path.join(MZC_EXCEL_UPLOAD_FOLDER, new_filename)
            file.save(save_path)
            saved_files.append({"filename": new_filename, "path": save_path})
        else:
            return jsonify({"error": f"Invalid file type for file {file.filename}"}), 400
    # 在所有文件处理完成后运行 mzc
    save_path = os.path.join(MZC_OUTPUT_FOLDER, "mzc_fig.jpeg")
    analyze_migration(data_dir=MZC_EXCEL_UPLOAD_FOLDER, save_path=save_path)
    # 返回所有文件的处理结果
    return jsonify({"message": "Files uploaded successfully!", "files": saved_files}), 200


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if filename == "output.xlsx":
        file_path = os.path.join(EXCEL_OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            print("发送", file_path)
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='application/octet-stream'
            )
    elif filename == "mzc_fig.jpeg":
        file_path = os.path.join(MZC_OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(
                file_path,
                mimetype='image/jpeg',  # 指定图片的 MIME 类型
                as_attachment=False,   # 不作为附件下载
            )
    elif filename == "szc_fig.jpeg":
        file_path = os.path.join(SZC_OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(
                file_path,
                mimetype='image/jpeg',  # 指定图片的 MIME 类型
                as_attachment=False,   # 不作为附件下载
            )
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/get_result/<filename>',methods=['GET'])
def get_result(filename):
    file_path = os.path.join(EXCEL_OUTPUT_FOLDER, filename)
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path)
        # 将 DataFrame 转换为 JSON 格式
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_image/<filename>', methods=['GET'])
def get_image(filename):
    """根据文件名返回图片"""
    file_path = os.path.join(SZC_OUTPUT_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/JPEG')
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/mzc_image', methods=['GET'])
def get_mzc_image():
    """根据文件名返回图片"""
    file_path = os.path.join(MZC_OUTPUT_FOLDER, "mzc_fig.jpeg")
    if os.path.exists(file_path):
        image_res = Image.open(file_path)
        img_byte_arr = io.BytesIO()
        image_res.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        return Response(img_byte_arr, mimetype='image/jpeg')
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/szc_image', methods=['GET'])
def get_szc_image():
    """根据文件名返回图片"""
    file_path = os.path.join(SZC_OUTPUT_FOLDER, "szc_fig.jpeg")
    if os.path.exists(file_path):
        image_res = Image.open(file_path)
        img_byte_arr = io.BytesIO()
        image_res.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        return Response(img_byte_arr, mimetype='image/jpeg')
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run()
