import 'package:chat_dio/chat_hattori.dart';
import 'package:flutter/material.dart';
import 'chat_hospi.dart';
import 'chat_dio.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          const DrawerHeader(
            decoration: BoxDecoration(
              color: Colors.deepPurple,
            ),
            child: Text(
              'Drawer Header',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
              ),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.message),
            title: const Text('案内ホスピちゃん'),
            onTap: () {
              Navigator.pushReplacement(context,
                  MaterialPageRoute(builder: (BuildContext context) => const ChatRoom()));
            },
          ),
          ListTile(
            leading: const Icon(Icons.message),
            title: const Text('ディオ課長'),
            onTap: () {
              Navigator.pushReplacement(context,
                  MaterialPageRoute(builder: (BuildContext context) => const ChatRoomDio()));
            },
          ),
          ListTile(
            leading: const Icon(Icons.message),
            title: const Text('コナンと服部'),
            onTap: () {
              Navigator.pushReplacement(context,
                  MaterialPageRoute(builder: (BuildContext context) => const ChatRoomHattori()));
            },
          ),
        ],
      ),
    );
  }
}

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Chat Application',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
      ),
      home: const ChatRoomHattori(),
    );
  }
}
