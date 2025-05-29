
# 📄 ANSP_back 接口文档

---

## 🧩 1. 项目概述

`ANSP_back` 是一个用于处理 Excel 文件并生成分析结果的后端服务。提供以下功能：

- ✅ Excel 文件上传与处理
- 📊 分析结果查询
- 📎 文件与图像下载

---

## 📚 2. 接口列表

### 🔍 2.1 清单分析接口

- **接口地址**：`POST /process_qdfx`

#### 📥 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `file` | file | ✅ 是     | 上传的 Excel 文件（`.xlsx` 或 `.xls`） |

#### 📤 返回结果

| 状态码 | 返回示例 | 描述 |
|--------|----------|------|
| `200` | `{"message": "File processed successfully", "output_file": "output.xlsx"}` | 文件处理成功 |
| `400` | `{"error": "No file part"}` | 请求未包含文件 |
| `400` | `{"error": "No selected file"}` | 文件未被选中 |
| `400` | `{"error": "Invalid file type"}` | 文件类型不支持 |
| `400` | `{"error": "Missing required columns in the Excel file"}` | 缺少必要列 |
| `500` | `{"error": "..."}` | 服务器内部错误 |

#### 📌 示例请求

```http
POST /process_qdfx
Content-Type: multipart/form-data

file: (Excel 文件内容)
```

#### 📌 示例响应

```json
{
  "message": "File processed successfully",
  "output_file": "output.xlsx"
}
```

---

### 🧭 2.2 重心分析接口

- **接口地址**：`POST /process_szc`

#### 📥 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `file` | file | ✅ 是     | Excel 文件（`.xlsx` 或 `.xls`） |

#### 📤 返回结果

| 状态码 | 返回示例 | 描述 |
|--------|----------|------|
| `200` | `{"message": "File uploaded successfully"}` | 上传成功 |
| `400` | `{"error": "No file part"}` | 缺少文件部分 |
| `400` | `{"error": "No selected file"}` | 未选择文件 |
| `400` | `{"error": "Invalid file type"}` | 类型错误 |

#### 📌 示例请求

```http
POST /process_szc
Content-Type: multipart/form-data

file: (Excel 文件内容)
```

#### 📌 示例响应

```json
{
  "message": "File uploaded successfully"
}
```

---

### 🔁 2.3 迁移分析接口

- **接口地址**：`POST /process_mzc`

#### 📥 请求参数

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `files` | file | ✅ 是     | 多个 Excel 文件上传 |

#### 📤 返回结果

| 状态码 | 返回示例 | 描述 |
|--------|----------|------|
| `200` | `{"message": "Files uploaded successfully!", "files": [...]}` | 上传成功 |
| `400` | `{"error": "No file part"}` | 未上传内容 |
| `400` | `{"error": "No selected files"}` | 未选择任何文件 |
| `400` | `{"error": "Invalid file type for file <filename>"}` | 某文件格式错误 |

#### 📌 示例请求

```http
POST /process_mzc
Content-Type: multipart/form-data

files: (多个 Excel 文件)
```

#### 📌 示例响应

```json
{
  "message": "Files uploaded successfully!",
  "files": [
    {"filename": "output1.xlsx", "path": "/path/to/output1.xlsx"},
    {"filename": "output2.xlsx", "path": "/path/to/output2.xlsx"}
  ]
}
```

---

### 📎 2.4 文件下载

- **接口地址**：`GET /download/<filename>`

#### 参数说明

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `filename` | string | ✅ 是 | 文件名（如 `output.xlsx`） |

#### 返回结果

| 状态码 | 描述 |
|--------|------|
| `200` | 文件下载成功（附件） |
| `404` | 文件未找到 |

#### 示例请求

```http
GET /download/output.xlsx
```

---

### 🔍 2.5 查询分析结果

- **接口地址**：`GET /get_result/<filename>`

#### 参数说明

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `filename` | string | ✅ 是 | 要查询的分析结果文件名 |

#### 返回结果

| 状态码 | 返回内容 |
|--------|----------|
| `200` | JSON 格式结果 |
| `500` | 服务器错误 |

#### 示例响应

```json
[
  {"tn": 1.0, "tp": 2.0, "tc": 3.0, "tf": 4.0, "area": 5.0, "intensity": 0.1},
  {"tn": 6.0, "tp": 7.0, "tc": 8.0, "tf": 9.0, "area": 10.0, "intensity": 0.2}
]
```

---

### 🖼️ 2.6 获取图片

- **接口地址**：`GET /get_image/<filename>`

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| `filename` | string | ✅ 是 | 图像文件名（如 `szc_fig.jpeg`） |

---

### 🖼️ 2.7 获取迁移分析图片

- **接口地址**：`GET /mzc_image`

无需参数，返回分析图像。

---

### 🖼️ 2.8 获取重心分析图片

- **接口地址**：`GET /szc_image`

无需参数，返回图像。

---

## ⚠️ 3. 错误码说明

| 错误码 | 含义 |
|--------|------|
| `400` | 请求参数错误或缺失 |
| `404` | 文件未找到 |
| `500` | 服务器内部错误 |

---

## 📌 4. 附加说明

- 所有接口支持 **跨域请求（CORS）**
- 文件上传须使用 `multipart/form-data` 编码
