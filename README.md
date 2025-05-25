# Agricultural Nonpoint Source Pollution Analytics 
# 农业面源污染分析软件 V1.0（湖北专版）
## 一、成员及项目分工
- 谢育泰：项目整体架构协调；api对接；pr审核；编写前段功能页面：清单分析、重心分析、迁移分析功能页面
- 宓小童[https://github.com/mxttt173]：后端，软件测试bug反馈
- 剡丽娟：前端
- 庞宇琦[https://github.com/Pyq-bit]：前端核心页面：主页、导航、错误页面引导；软件测试bug反馈
  
## 二、项目架构（基于前后端分离开发）
- 前端：使用 Flutter (Dart) 构建Windows平台应用
- 后端：使用 Flask矿建 (Python) 搭建 RESTful API 提供数据支持
- 通信方式：前端基于dio库进行网络请求，进行前后端数据交互

## 二、客户端界面设计和软件运行效果截图
- 主页
   ![image](https://github.com/user-attachments/assets/dc895dc9-57aa-474a-8cf7-bb2255e36dc2)
- 登录模块
   ![image](https://github.com/user-attachments/assets/3fd1d907-8091-45f5-b2f3-74a094310fef)
- 自带湖北行政区划图(可鼠标滑动缩放)
   ![image](https://github.com/user-attachments/assets/9178b183-662a-47bd-bef4-82eec2580d1f)
- 清单分析计算模块
   ![image](https://github.com/user-attachments/assets/4a72552f-5edf-46c9-abaf-8b24cd61df4a)
- 重心分析计算模块
   ![image](https://github.com/user-attachments/assets/674d16e3-f546-4f7a-b3af-1cec007c7b9b)
- 重心迁移分析模块
   ![image](https://github.com/user-attachments/assets/1b66b99f-15aa-4232-bd1f-387fa4778851)
- 导航栏
  ![image](https://github.com/user-attachments/assets/b17e3576-bab6-44fc-9aaa-18f2af89e852)
  
## 三、提供EXCEL示例测试数据
- 第一期数据
- 第二期数据

*注释*
   - `tn` -- 农用化肥含氮量（吨-t）
   - `tp` -- 农用化肥含磷量（吨-t）
   - `tc` -- 农药施用量（吨-t）
   - `tf` -- 农膜施用量（吨-t）
   - `area` -- 耕地面积（公顷-hm²）
   - `intensity` -- 耕地面源污染强度（t/hm²）-- 清单计算法得到
     
## 四、农业面源污染背景资料
### 概念
- 农业面源污染（Agricultural Non-point Source Pollution, ANPSP）是指在农业生产活动中，氮、磷等营养盐，农药、重金属以及其他有机或无机污染物，通过地表径流、土壤侵蚀、淋溶等途径扩散到水体、土壤和大气中，形成的广泛性、分散性污染。与点源污染（如工业废水集中排放）不同，面源污染具有排放时空不确定、污染范围广、监测与控制难度大等特点，主要来源包括化肥农药过量施用、畜禽养殖废弃物、农田地表径流、农村生活污水等。

### 治理必要性
- 水体富营养化的主要成因 
   农业面源污染是河流、湖泊和近海富营养化的首要污染源。氮、磷等营养盐的流失会导致藻类爆发性增殖（如蓝藻水华），破坏水生生态系统，威胁饮用水安全。
- 土壤退化与食品安全风险  
   长期过量使用化肥农药会造成土壤板结、酸化及重金属累积，降低耕地质量，同时通过食物链危害人体健康。
- 气候变化与生物多样性威胁  
   例如，氮肥分解产生的氧化亚氮（N₂O）是强效温室气体；农药滥用会破坏农田生物多样性，削弱自然生态系统的调节能力。
- 制约农业可持续发展
   粗放的农业生产模式导致资源利用效率低下，污染治理成本逐年增加，影响农业长期生产力。  
   通过清单分析法量化污染负荷，结合重心迁移分析揭示污染时空演变规律，可为精准治理（如生态拦截工程、科学施肥技术推广）提供科学依据，最终实现农业发展与环境保护的协同。
   
### 五、其他参考数据来源
**湖北省行政区划图-标准地图服务**
- https://hubei.tianditu.gov.cn/


