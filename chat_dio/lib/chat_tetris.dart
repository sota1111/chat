import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'utilities.dart';
import 'main.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatRoomTetris extends StatefulWidget {
  const ChatRoomTetris({Key? key}) : super(key: key);

  @override
  ChatRoomState createState() => ChatRoomState();
}

class ChatRoomState extends State<ChatRoomTetris> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4ad9-ae75-a22bf8e6f3ac');
  final types.User _tetris = const types.User(
    id: 'tetris',
    firstName: "Tetris猫",
    lastName: "",
    imageUrl: ImageUrls.tetrisFace0,
  );


  @override
  void initState() {
    super.initState();
    _addMessage(types.TextMessage(
      author: _tetris,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: "ルール把握してないけど、ヨシ！",
    ));

    initializeAsyncMethods();
  }
  Future<void> initializeAsyncMethods() async {
    //サーバサイドを実装したら、追記する
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('tetris知らんけど、ヨシ！')),
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

  void _handleSendPressed(types.PartialText message) async {
    final textMessage = types.TextMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: message.text,
    );

    _addMessage(textMessage);

    Map<String, dynamic> apiResponseData = await fetchResponseFromApi(message.text);

    Future.delayed(const Duration(seconds: 1), () {
      final responseText = apiResponseData['Response'] ?? 'Failed';
      debugPrint(responseText);

      // Remove first newline character from the responseText
      final sanitizedResponseText = responseText.replaceFirst('\n', '');

      // Append "ヨシ！" to the responseText
      final finalResponseText = sanitizedResponseText + "\n\n多分、ヨシ！";

      final responseMessage = types.TextMessage(
        author: _tetris,
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: randomString(),
        text: finalResponseText,
      );
      _addMessage(responseMessage);
    });


  }

  Future<Map<String, dynamic>> fetchResponseFromApi(String inputText) async {
    const String url =
        'https://r30snkhpsj.execute-api.ap-northeast-1.amazonaws.com/Prod/hello';
    final Map<String, String> headers = {'Content-Type': 'application/json'};
    //debugPrint("inputText:$inputText");
    final Map<String, String> data = {
      'input_text': inputText,
    };
    final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(data));
    //debugPrint("response.statusCode:${response.statusCode}");
    if (response.statusCode == 200) {
      var jsonResponse = json.decode(response.body);
      debugPrint(jsonResponse['Response']);
      return {
        'Response': jsonResponse['Response'],
      };
    } else {
      return {'Response': 'Failed'};
    }
  }
}
