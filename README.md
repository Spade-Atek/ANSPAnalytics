# 农业面源污染分析软件 V1.0（湖北专版）


## 一、成员及项目分工

### 项目名称：

基于面源污染的时空规律分析项目—数据分析、软件开发、网站建设（采用前后端分离的思想，基于 RESTful 开发风格）


### 项目成员与分工：
- [🧑‍💻2024303120163 组长](https://github.com/Spade-Atek)  
  1. 项目整体架构协调；  
  2. 前后端 API 接口对接；  
  3. 编写前端功能页面：清单分析、重心分析、迁移分析功能页面，辅助后端；  
  4. PR 审核，项目打包。  

- [🧑‍⚖️2024303120152](https://github.com/mxttt173)  
  1. 数据收集和整理；  
  2. 后端代码编写：基于农业面源污染的相关参考文献和年鉴指标数据实现了清单计算、重心分析、迁移分析功能；  
  3. 软件说明文档编写。  

- [👩‍💼2024303120076](https://github.com/Pyq-bit)  
  1. 前端页面编写：主页、导航、设置页面；  
  2. 接口文档编写；  
  3. 软件测试 bug 反馈。  

- [🙋‍♀️2024303120149](https://github.com/Ylj0617)  
  1. 前端页面编写：登录、错误页面引导；  
  2. 软件风格、色彩统一、素材提供；  
  3. 软件测试 bug 反馈。  

## 二、项目架构
```bash
📂ANSPAnalytics/
├── ANSP_back/                     # 后端代码
├── ANSP_front/                    # 前端代码
├── 示例数据.zip                   # 测试数据
├── ANSP_API.md                    # API 文档
├── LICENSE                        # 许可证
├── README.md                      # 项目说明文档
├── package.json                   # 项目配置文件
└── 湖北省农业面源污染分析软件说明文档.pdf  # 软件说明文档，基于quarto生成
```
* **前端**：使用 Flutter 框架 (Dart) 构建 Windows 平台应用，使用Flutter最开始目的是做多端应用。
* **后端**：使用 Flask 框架 (Python) 搭建服务端，RESTful 风格 API 提供数据支持
* **通信方式**：前端基于 dio 库进行网络请求，实现前后端数据交互
* **虚拟环境**：Conda管理环境，pip安装包
* **软件说明文档**：[*软件说明文档*](https://github.com/Spade-Atek/ANSPAnalytics/blob/main/%E6%B9%96%E5%8C%97%E7%9C%81%E5%86%9C%E4%B8%9A%E9%9D%A2%E6%BA%90%E6%B1%A1%E6%9F%93%E5%88%86%E6%9E%90%E8%BD%AF%E4%BB%B6%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.pdf)基于[*quarto*](https://quarto.org/)生成
```bash
quarto preview "c:/Users/农业面源污染分析软件_V1.0_湖北专版.md" --to typst --no-browser --no-watch-inputs
```
* **接口文档**：🔗接口文档基于md格式

## 三、软件使用说明

### 🖥️  客户端使用方式
> ✅ 客户端支持 Windows 系统，无需额外安装依赖。
1. 进入项目的 GitHub 仓库主页
2. 点击右侧的 [*Releases*](https://github.com/Spade-Atek/ANSPAnalytics/releases)标签页
3. 在最新版本的 Release 页面中下载 `ANSPools.exe` 可执行文件
4. 下载后直接双击运行即可启动客户端程序


### 📡 服务端运行方式
> ✅ 服务端虽然也提供了直接运行的[*Releases*](https://github.com/Spade-Atek/ANSPAnalytics/releases)版本。基于pyinstaller进行打包，但是打包版本存在一个路径问题，下载结果功能无法实现（打包后自己电脑是相对路径可以运行，但是到其他同学的电脑测试是绝对路径导致的错误߹ᯅ߹ ，测试了几天暂时无法解决）。

因此想体验完整功能，建议采用手动部署的方式部署后端，以实现下载服务。
1. 下载仓库中的 `ANSP_back` 文件夹（包含templates文件夹，app.py和requirements.txt）
2. 可根据文件 requirements.txt(包含项目依赖项)创建虚拟环境
3. 以 `app.py` 为启动入口运行后端服务：
   ```
   python app.py
   ```
4. 默认服务运行地址为：`http://127.0.0.1:5000/`

### 🌐 [*Releases*](https://github.com/Spade-Atek/ANSPAnalytics/releases)页面示意图

![image](https://github.com/user-attachments/assets/ceabaaeb-4c9a-486a-b201-34220f4f75b4)

## 四、提供 EXCEL 示例测试数据

* 提供 [示例数据](https://github.com/Spade-Atek/ANSPAnalytics/blob/main/%E7%A4%BA%E4%BE%8B%E6%95%B0%E6%8D%AE.zip)，示例数据也在仓库中的 `Data_test` 文件夹获取样例。
* 如需使用自定义年鉴数据，请严格遵守以下 Excel 表格字段注释规范：

| 字段名         | 含义说明                     |
| ----------- | ------------------------ |
| `tn`        | 农用化肥含氮量（吨-t）             |
| `tp`        | 农用化肥含磷量（吨-t）             |
| `tc`        | 农药施用量（吨-t）               |
| `tf`        | 农膜施用量（吨-t）               |
| `area`      | 耕地面积（公顷-hm²）             |
| `intensity` | 耕地面源污染强度（t/hm²），由清单计算法得到 |

## 五、客户端界面设计与软件运行效果截图

### 🏠 主页面

![image](https://github.com/user-attachments/assets/2630cb00-8b83-4e17-a1e9-d7a7d4d3666d)

---

### 🔐 登录模块

![image](https://github.com/user-attachments/assets/3282ebcb-9303-4407-ac11-4ce22d2ef1cb)

---

### 🗺 湖北行政区划图（支持鼠标滚轮缩放）

![image](https://github.com/user-attachments/assets/fc0b7b56-4546-40eb-bfee-f36ce79974e5)


---

### 📊 清单分析计算模块（结果图可下载）

![image](https://github.com/user-attachments/assets/2a7fa223-4f51-4bfa-854c-b29a4d8a867c)


---

### 📍 重心分析计算模块（结果图可下载）

![image](https://github.com/user-attachments/assets/e004daef-35bd-4047-a332-1a7a0b24b64d)


---

### 🚛 迁移分析模块（文字输出 + 图示，可下载）

![image](https://github.com/user-attachments/assets/1b66b99f-15aa-4232-bd1f-387fa4778851)

---

### 🧭 导航栏设计

![image](https://github.com/user-attachments/assets/b17e3576-bab6-44fc-9aaa-18f2af89e852)

## 五、农业面源污染相关资料

### 🌿 概念说明：

农业面源污染（Agricultural Non-point Source Pollution, ANSP）是指在农业生产活动中，氮、磷等营养盐，农药、重金属以及其他有机或无机污染物，通过地表径流、土壤侵蚀、淋溶等途径扩散到水体、土壤和大气中，形成的广泛性、分散性污染。
与点源污染（如工业废水集中排放）不同，面源污染具有排放时空不确定、污染范围广、监测与控制难度大等特点。主要来源包括：

* 化肥农药过量施用
* 畜禽养殖废弃物
* 农田地表径流
* 农村生活污水等


### 🌍 治理必要性：

1. **水体富营养化的主要成因**：

   * 农业面源污染是河流、湖泊和近海富营养化的首要污染源。
   * 氮、磷流失导致藻类爆发（如蓝藻水华），破坏水生态，威胁饮用水安全。

2. **土壤退化与食品安全风险**：

   * 化肥农药滥用会造成土壤板结、酸化及重金属累积。
   * 降低耕地质量，并通过食物链危害人体健康。

3. **气候变化与生物多样性威胁**：

   * 氮肥分解产生的氧化亚氮（N₂O）是强效温室气体；
   * 农药滥用破坏农田生态系统稳定性。

4. **制约农业可持续发展**：

   * 粗放式农业模式导致资源利用效率低、治理成本高；
   * 运用**清单分析法**定量估算污染负荷，结合**重心迁移分析**揭示污染的时空演化规律，能为精准治理提供数据支持（如生态拦截工程、科学施肥技术推广）。

## 七、其他参考数据来源

### 1️⃣ [湖北省行政区划图 - 标准地图服务](https://hubei.tianditu.gov.cn/)

### 2️⃣ [部分素材来源 - 阿里巴巴矢量图标库](https://www.iconfont.cn/)

### 3️⃣ [ico格式图标生成](https://ico.elespaces.com/)

### 4️⃣ [前端Flutter项目打包Windows端安装包(exe文件)参考](https://juejin.cn/post/7085280466483281928)

### 5️⃣ [后端Flask项目打包参考-基于pyinstaller](https://pyinstaller.org/en/stable/)
