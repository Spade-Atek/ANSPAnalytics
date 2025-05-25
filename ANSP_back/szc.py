# encoding: utf-8
# @File  : szc.py
# @Author: XIE Yutai
# @Date  : 2025/05/16/16:30

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
#设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

SZC_EXCEL_UPLOAD_FOLDER = 'upload_szc_data'
if not os.path.exists(SZC_EXCEL_UPLOAD_FOLDER):
    os.makedirs(SZC_EXCEL_UPLOAD_FOLDER)
SZC_OUTPUT_FOLDER = 'output_szc_data'
if not os.path.exists(SZC_OUTPUT_FOLDER):
    os.makedirs(SZC_OUTPUT_FOLDER)

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


if __name__ == "__main__":
    # 读取第一期数据（修改为你的实际文件名）
    input_filename = "output.xlsx"
    input_path = os.path.join(SZC_EXCEL_UPLOAD_FOLDER, input_filename)
    save_path = os.path.join(SZC_OUTPUT_FOLDER, "szc_fig.jpeg")

    weights_time1 = read_pollution_weights(input_path)
    # 计算重心
    centroid = calculate_weighted_centroid(points, weights_time1)
    # 绘图
    plt.figure(figsize=(12, 10))
    plt.scatter(points[:, 0], points[:, 1], s=weights_time1 * 300, c='blue', alpha=0.6,
                label='城市点位(大小表示污染强度)')
    for i, city in enumerate(city_names):
        plt.annotate(city, (points[i, 0], points[i, 1]), textcoords="offset points", xytext=(0, 5), ha='center')
    plt.scatter(centroid[0], centroid[1], s=200, c='red', marker='*', label='加权重心')
    plt.title('湖北省农业面源污染源分布与加权重心', fontsize=15)
    plt.xlabel('经度', fontsize=12)
    plt.ylabel('纬度', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)

    print(f"第一期加权重心坐标: 经度={centroid[0]:.4f}°, 纬度={centroid[1]:.4f}°")