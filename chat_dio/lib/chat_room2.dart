import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'utilities.dart';
import 'main.dart';

class SecondChatRoom extends StatefulWidget {
  const SecondChatRoom({Key? key}) : super(key: key);

  @override
  SecondChatRoomState createState() => SecondChatRoomState();
}

class SecondChatRoomState extends State<SecondChatRoom> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '5303f2d6-9410-4b1b-a4f7-b244c71b2f57');

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chat Room 2')),
      drawer: const AppDrawer(),
      body: Chat(
        user: _user,
        messages: _messages,
        onSendPressed: _handleSendPressed,
        showUserAvatars: true,
        showUserNames: true,
      ),
    );
  }

  void _addMessage(types.Message message) {
    setState(() {
      _messages.insert(0, message);
    });
  }

  void _handleSendPressed(types.PartialText message) {
    final textMessage = types.TextMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: message.text,
    );

    _addMessage(textMessage);
  }
}
