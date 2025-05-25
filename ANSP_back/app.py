import runpy
from flask import Flask, request, send_file, jsonify, Response
import os
import io
import pandas as pd
from PIL import Image

app = Flask(__name__)

# 配置上传文件的保存路径、excel结果文件的保存路径
EXCEL_UPLOAD_FOLDER = 'uploads'
EXCEL_OUTPUT_FOLDER = 'output_excel'
IMAGE_UPLOAD_FOLDER = "image"
SZC_EXCEL_UPLOAD_FOLDER = 'upload_szc_data'
SZC_OUTPUT_FOLDER = 'output_szc_data'
MZC_EXCEL_UPLOAD_FOLDER = 'upload_mzc_data'
MZC_OUTPUT_FOLDER = 'output_mzc_data'
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
            output_filename = "output2.xlsx"
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
        runpy.run_path('szc.py', run_name="__main__")
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
            # 为文件生成新的名字，如 output1.xlsx, output2.xlsx 等
            new_filename = f"output{index + 1}.xlsx"
            save_path = os.path.join(MZC_EXCEL_UPLOAD_FOLDER, new_filename)
            file.save(save_path)
            saved_files.append({"filename": new_filename, "path": save_path})
        else:
            return jsonify({"error": f"Invalid file type for file {file.filename}"}), 400
    # 在所有文件处理完成后运行 mzc.py
    runpy.run_path('mzc.py', run_name="__main__")
    # 返回所有文件的处理结果
    return jsonify({"message": "Files uploaded successfully!", "files": saved_files}), 200


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    if filename == "mzc_fig.jpeg":
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
