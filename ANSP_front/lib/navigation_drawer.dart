import 'package:flutter/material.dart';

class NavigationDrawer extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Drawer(
      width: 260,
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          DrawerHeader(
            decoration: BoxDecoration(
              color: Colors.green
            ),
            child: const Text(
              '导航',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
              ),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.home_filled,color: Colors.green,),
            title: const Text('主页',style: TextStyle(color: Colors.green, ),),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushReplacementNamed(context, '/main');
            },
          ),
          ListTile(
            leading: const Icon(Icons.earbuds,color: Colors.green,),
            title: const Text('清单分析计算',style: TextStyle(color: Colors.green, ),),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushReplacementNamed(context, '/multi');
            },
          ),
          ListTile(
            leading: const Icon(Icons.euro_sharp,color: Colors.green,),
            title: const Text('重心分析计算',style: TextStyle(color: Colors.green, ),),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushReplacementNamed(context, '/single');
            },
          ),
          ListTile(
            leading: const Icon(Icons.compare_outlined,color: Colors.green,),
            title: const Text('迁移分析计算',style: TextStyle(color: Colors.green, ),),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushReplacementNamed(context, '/multi_2nd');
            },
          ),
          ListTile(
            leading: const Icon(Icons.settings,color: Colors.green,),
            title: const Text('软件设置',style: TextStyle(color: Colors.green, ),),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushReplacementNamed(context, '/set');
            },
          ),
          ListTile(
            leading: const Icon(Icons.logout,color: Colors.green,),
            title: const Text('退出登录',style: TextStyle(color: Colors.green, ),),
            onTap: () {
              Navigator.pop(context);
              Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ],
      ),
    );
  }
}
