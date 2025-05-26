//清单分析法
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:dio/dio.dart';
import 'navigation_drawer.dart' as my_drawer2;

// 创建一个用来存储输出信息的类
class ExcelData {
  final String city;
  final double tn;
  final double tp;
  final double tc;
  final double tf;
  final double area;
  final double intensity;

  ExcelData({
    required this.city,
    required this.tn,
    required this.tp,
    required this.tc,
    required this.tf,
    required this.area,
    required this.intensity
  });

  factory ExcelData.fromJson(Map<String, dynamic> json) => ExcelData(
        city: json['city']?.toString() ?? '',
        tn: (json['tn'] as num?)?.toDouble() ?? 0.0,
        tp: (json['tp'] as num?)?.toDouble() ?? 0.0,
        tc: (json['tc'] as num?)?.toDouble() ?? 0.0,
        tf: (json['tf'] as num?)?.toDouble() ?? 0.0,
        area: (json['area'] as num?)?.toDouble() ?? 0.0,
        intensity: (json['intensity'] as num?)?.toDouble() ?? 0.0,
      );
}

class MultiInputOutputPage extends StatefulWidget {
  const MultiInputOutputPage({super.key});

  @override
  _MultiInputOutputPageState createState() => _MultiInputOutputPageState();
}

class _MultiInputOutputPageState extends State<MultiInputOutputPage> {
  FilePickerResult? _selectedFile;
  String? _filename;
  bool _buttonEnabled1 = false;
  bool _buttonEnabled2 = false;
  bool _buttonEnabledWait = false;
  bool isLoading = false; // 控制加载状态
  bool isRemind1 = false;
  OverlayEntry? _overlayEntry; // 用于管理 Overlay
  List<dynamic>? _excelData;

  Future<void> _pickExcel() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['xls', 'xlsx'], // 只允许选择 Excel 文件
      allowMultiple: true,
    );

    if (result != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Excel 文件选择成功'),
          backgroundColor: Colors.green,
          duration: Duration(seconds: 2),
        ),
      );
      setState(() {
        _selectedFile = result;
        if (_buttonEnabled1 == false) _buttonEnabled1 = !_buttonEnabled1;
        if (_buttonEnabled2 == true) _buttonEnabled2 = !_buttonEnabled2;
        if (isRemind1 == false) isRemind1 = !isRemind1;
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('用户取消选择')),
      );
      return;
    }
  }

  //处理按钮方法
  Future<void> _uploadExcel() async {
    showLoading(); //表示正在处理数据
    final stopwatch = Stopwatch()..start();

    if (_selectedFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please select a file first')),
      );
      return;
    }

    try {
     var dio = Dio();
      // 获取文件路径和文件名
      String filePath = _selectedFile!.files.single.path!;
      String fileName = _selectedFile!.files.single.name;

      // 创建 FormData 对象
      var formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          filePath,
          filename: fileName, // 文件名
        ),
      });

      // 发送 POST 请求
      var response = await dio.post(
        'http://127.0.0.1:5000/process_qdfx', // 后端接口地址
        data: formData,
        onSendProgress: (int sent, int total) {
          // 可以在这里处理上传进度
          print('Progress: ${sent / total * 100}%');
        },
      );

      // 检查响应状态码
    if (response.statusCode == 200) {
      stopwatch.stop();
      setState(() {
        _buttonEnabled2 = !_buttonEnabled2;
        _buttonEnabledWait = !_buttonEnabledWait;
        _buttonEnabled1 = !_buttonEnabled1;//成功后关闭上传处理按钮
        if(stopwatch.elapsedMilliseconds < 2000){
          Future.delayed(Duration(seconds: 2));
          hideLoading(); //结束处理
          
        }else{
          hideLoading(); //大于就不用管
        }
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('处理成功，或者可通过[结果下载]获取相应excel数据'),backgroundColor: Colors.green,),
        );
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to upload file')),
      );
    }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  Future<void> _presentExcelData() async {
    setState(() {
      _filename = 'output.xlsx';
    });
    var dio_res = Dio();
    try{
      var response = await dio_res.get(
        'http://127.0.0.1:5000/get_result/$_filename',
        options: Options(responseType: ResponseType.json),
      );
      if(response.statusCode == 200){
        // ${response.data[0].runtimeType} $response.data
        print('Data type: ${response.data.runtimeType}'); 
        //print(response.data);
        setState(() {
          _excelData = response.data;
        });
        //LoggerLite.log(_excelData);
      }
    }catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e'), duration: Duration(seconds: 2)));
    }
  }

  Future<void> _downloadFile() async {
    setState(() {
      _filename = 'output.xlsx';
    });
    if (_filename == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('没有可下载的文件')));
      return;
    }
    try {
      var dio = Dio();
      var response = await dio.get(
        'http://127.0.0.1:5000/download/$_filename',
        options: Options(responseType: ResponseType.bytes),
      );
      if (response.statusCode == 200) {
        String fileName = "result";
        String timestamp = DateTime.now().millisecondsSinceEpoch.toString(); // 获取当前时间戳
        String newFileName = '$fileName-$timestamp.xlsx'; // 文件名加上时间戳

        final result = await FilePicker.platform.getDirectoryPath(
          dialogTitle: '选择保存文件的文件夹位置',
        );
        if (result == null) { // 用户取消选择
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('用户取消下载')),
          );
          return;
        }
        final filePath = '$result/$newFileName';
        File file = File(filePath);
        await file.writeAsBytes(response.data);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$newFileName Excel文件已下载到 $filePath'),duration: Duration(seconds: 4),backgroundColor: const Color.fromARGB(255, 49, 138, 49),));
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Excel文件下载失败'),duration: Duration(seconds: 4),backgroundColor: Colors.redAccent,));
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e'),duration: Duration(seconds: 2)));
    }
  }

    // 显示加载状态
  void showLoading() {
    setState(() {
      isLoading = true;
    });
    _overlayEntry = OverlayEntry(
      builder: (context) {
        return Positioned.fill(
          child: Container(
            color: Colors.black.withValues(alpha: 128), // 半透明背景
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                CircularProgressIndicator(), // 旋转的加载图标
                SizedBox(height: 16), // 间距
                Text(
                  '处理数据中...',
                  style: TextStyle(color: Colors.white, fontSize: 16),
                ),
              ],
            ),
          ),
        );
      },
    );
    Overlay.of(context).insert(_overlayEntry!); // 插入 Overlay
  }

  // 隐藏加载状态
  void hideLoading() {
    setState(() {
      isLoading = false;
    });
    _overlayEntry?.remove(); // 移除 Overlay
    _overlayEntry = null;
  }

    void showMapDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          content: Container(
            width: 800, // 设置弹窗宽度
            height: 900, // 设置弹窗高度
            child: InteractiveViewer(
              boundaryMargin: EdgeInsets.all(100), // 设置边界外的可操作区域
              minScale: 1, // 最小缩放比例
              maxScale: 5.0, // 最大缩放比例
              child: Image.asset('assets/images/hubei_map.jpg'), // 显示地图图片
            ),
          ),
          actions: <Widget>[
            // 将关闭按钮居中
            Center(
              child: TextButton(
                child: Text('关闭 [注:滚动滑轮可缩放地图]'),
                onPressed: () {
                  Navigator.of(context).pop(); // 关闭弹窗
                },
              ),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final dataList = _excelData?.map((item) => ExcelData.fromJson(item as Map<String, dynamic>)).toList();
    return Scaffold(
      appBar: AppBar(
        title: Text('清单分析计算',style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),),
      ),
      drawer: my_drawer2.NavigationDrawer(),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: <Widget>[
          // 第一部分：提示文本
          Padding(
            padding: const EdgeInsets.all(6), // 添加内边距
            child: _selectedFile == null
                ? Text(
                    '选择一期未处理数据以进行清单计算分析',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  )
                : Text(
                    '已选择文件：${_selectedFile!.files.single.name}',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
          ),
          // 第二部分：4 个按钮
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                ElevatedButton(
                  onPressed: () {
                    _pickExcel();
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.green,
                    disabledBackgroundColor: Colors.grey,
                    disabledForegroundColor: Colors.white,
                  ),
                  child: Text('数据导入', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                ),
                SizedBox(width: 20),
                ElevatedButton(
                  onPressed: _buttonEnabled1 ? () async {
                    await _uploadExcel();
                    await Future.delayed(Duration(seconds: 2)); //等待上传结束
                    _presentExcelData();
                  } : null,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.green,
                    disabledBackgroundColor: Colors.grey,
                    disabledForegroundColor: Colors.white,
                  ),
                  child: Text('数据处理', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                ),
                SizedBox(width: 20),
                ElevatedButton(
                  onPressed: _buttonEnabled2 ? _downloadFile : null,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white,
                    foregroundColor: Colors.green,
                    disabledBackgroundColor: Colors.grey,
                    disabledForegroundColor: Colors.white,
                  ),
                  child: Text('结果下载', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                ),
                SizedBox(width: 20),
                  ElevatedButton(
                    onPressed: () {
                      // 调用显示地图弹窗的方法
                      showMapDialog(context);
                    },
                    child: Text('湖北行政区划图', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  ),
              ],
            ),
          ),
          // 第三部分：Excel 数据显示
          Expanded(
            child: Container(
              width: 1200, // 设置最大宽度
              height: 450, // 设置最大高度
              decoration: BoxDecoration(
                border: Border.all(color: Colors.blue), // 添加边框
              ),
              child: SingleChildScrollView(
                scrollDirection: Axis.vertical,
                child: DataTable(
                  columns: const [
                    DataColumn(label: Text('湖北省城市名', style: TextStyle(fontWeight: FontWeight.bold))),
                    DataColumn(label: Text('农用化肥中含氮量(吨-t)', style: TextStyle(fontWeight: FontWeight.bold))),
                    DataColumn(label: Text('农药施用量(吨-t)', style: TextStyle(fontWeight: FontWeight.bold))),
                    DataColumn(label: Text('耕地面积(公顷-hm²)', style: TextStyle(fontWeight: FontWeight.bold))),
                    DataColumn(label: Text('耕地面源污染强度(t/hm²)', style: TextStyle(fontWeight: FontWeight.bold))),
                  ],
                  rows: dataList?.map((data) => DataRow(
                    cells: [
                      DataCell(Text(data.city, style: TextStyle(fontWeight: FontWeight.bold))),
                      DataCell(Text(data.tn.toString(), style: TextStyle(fontWeight: FontWeight.bold))),
                      DataCell(Text(data.tc.toString(), style: TextStyle(fontWeight: FontWeight.bold))),
                      DataCell(Text(data.area.toString(), style: TextStyle(fontWeight: FontWeight.bold))),
                      DataCell(Text(data.intensity.toString(), style: TextStyle(fontWeight: FontWeight.bold, color: Colors.blue))),
                    ],
                  )).toList() ?? [],
                ),
              ),
            ),
          ),
          SizedBox(height: 50),
        ],
      ),
    );
  }
}
