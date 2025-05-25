# encoding: utf-8
# @File  : mzc.py
# @Author: XIE Yutai
# @Date  : 2025/05/16/16:41

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

#设置中文字体显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

MZC_EXCEL_UPLOAD_FOLDER = 'upload_mzc_data'
if not os.path.exists(MZC_EXCEL_UPLOAD_FOLDER):
    os.makedirs(MZC_EXCEL_UPLOAD_FOLDER)
MZC_OUTPUT_FOLDER = 'output_mzc_data'
if not os.path.exists(MZC_OUTPUT_FOLDER):
    os.makedirs(MZC_OUTPUT_FOLDER)

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

#计算加权重心
def calculate_weighted_centroid(points, weights):
    total_weight = np.sum(weights)
    weighted_x = np.sum(points[:, 0] * weights) / total_weight
    weighted_y = np.sum(points[:, 1] * weights) / total_weight
    return np.array([weighted_x, weighted_y])

#读取污染强度权重
def read_pollution_weights(filepath):
    df = pd.read_excel(filepath)
    city_to_weight = dict(zip(df.iloc[:, 0], df.iloc[:, 6]))  # 可改为列名
    weights = np.array([city_to_weight.get(city, 0) for city in city_names])
    return weights

#计算两点间距离与方向
def calculate_movement(centroid1, centroid2):
    dx = centroid2[0] - centroid1[0]
    dy = centroid2[1] - centroid1[1]
    distance = np.sqrt(dx**2 + dy**2)
    angle = np.degrees(np.arctan2(dy, dx))
    return distance, angle

#获取符合规则的污染文件
def get_sorted_pollution_files(directory):
    files = [f for f in os.listdir(directory) if re.match(r'output\d+\.xlsx', f)]
    files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))
    return [os.path.join(directory, f) for f in files]

#主函数
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

    ax1.set_title('农业面源污染重心多期迁移路径图', fontsize=16)
    ax1.set_xlabel('经度', fontsize=13)
    ax1.set_ylabel('纬度', fontsize=13)
    ax1.legend(fontsize=10)
    ax1.grid(True)

    # 图层2：信息文本 + 墨绿色边框方框
    ax2 = fig.add_subplot(spec[1])
    ax2.axis('off')

    # 墨绿色边框 + 灰色背景 + 包含文字
    bbox_props = dict(boxstyle="round,pad=0.5", facecolor='#f9f9f9',
                      edgecolor='darkgreen', linewidth=2)

    ax2.text(0.03, 0.97, full_text,
             fontsize=12,
             va='top', ha='left',
             transform=ax2.transAxes,
             bbox=bbox_props,
             wrap=True,
             linespacing=1.8,
             color='black')

    plt.tight_layout()
    plt.savefig(save_path)

#程序入口
if __name__ == "__main__":
    save_path = os.path.join(MZC_OUTPUT_FOLDER, "mzc_fig.jpeg")
    analyze_migration(data_dir=MZC_EXCEL_UPLOAD_FOLDER, save_path=save_path)