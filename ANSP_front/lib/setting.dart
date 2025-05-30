import 'package:flutter/material.dart';
import 'login_page.dart';
import 'ansp_qdfx.dart';
import 'ansp_szc.dart';
import 'ansp_mzc.dart';
import 'error_page.dart';
import 'main.dart ';
import 'navigation_drawer.dart' as my_drawer3;

class SettingsPage extends StatefulWidget {
  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  String _selectedLanguage = '中文'; // 默认语言
  bool _isNotificationEnabled = true; // 默认通知开启

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('设置'),
      ),
      drawer: my_drawer3.NavigationDrawer(),
      body: ListView(
        children: <Widget>[
          // 主题设置
          ListTile(
            title: Text('主题'),
            trailing: Switch(
              value: Theme.of(context).brightness == Brightness.dark,
              activeColor: Colors.red,
              onChanged: (value) {
                // 切换主题逻辑
                final theme = value ? ThemeData.dark() : ThemeData.light();
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(
                    builder: (context) => MaterialApp(
                      theme: theme,
                      home: SettingsPage(),
                      onUnknownRoute: (settings) {
                        return MaterialPageRoute(builder: (_) => ErrorPage());
                      },
                      routes: {   
                        '/login': (context) => LoginPage(),
                        '/single': (context) => InputOutputPage(),
                        '/multi': (context) => MultiInputOutputPage(), 
                        '/multi_2nd': (context) => MultiInputOutputPage2(), 
                        '/set': (context) => SettingsPage(),
                        '/main': (context) => MyHomePage(),
                      },
                    ),
                  ),
                );
                setState(() {
                  // 更新主题状态
                });
              },
            ),
          ),
          // 语言设置
          ListTile(
            title: Text('语言'),
            trailing: DropdownButton<String>(
              value: _selectedLanguage,
              items: <String>['中文', 'English', 'Español'].map((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  _selectedLanguage = newValue!;
                });
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('语言已切换为: $_selectedLanguage')),
                );
              },
            ),
          ),
          // 通知设置
          ListTile(
            title: Text('通知'),
            trailing: Switch(
              value: _isNotificationEnabled,
              activeColor: Colors.green,
              onChanged: (bool newValue) {
                setState(() {
                  _isNotificationEnabled = newValue;
                });
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('通知已${newValue ? '开启' : '关闭'}')),
                );
              },
            ),
          ),
          // 关于
          ListTile(
            title: Text('关于'),
            onTap: () => _showAboutDialog(context),
          ),
        ],
      ),
    );
  }

  void _showAboutDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('关于应用', style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold)),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Text('版本: 1.0', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 1),
              Text('Copyright(C) 2025. 数据驱动课第25组 All Rights Reserved', style: TextStyle(fontWeight: FontWeight.w800)),
              const SizedBox(height: 30),
              Center( // 使用 Center 组件来居中显示特定的 Text
                child: 
                  InkWell(
                    onTap: () {
                      Navigator.of(context).pop(); // 关闭对话框
                    },
                    child: const Icon(Icons.check, color: Colors.green),
                  ),
              ),
              const SizedBox(height: 20), // 添加一些垂直间距
            ],
          ),
        );
      },
    );
  }
}