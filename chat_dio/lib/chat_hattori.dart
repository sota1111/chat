import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'utilities.dart';
import 'main.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatRoomHattori extends StatefulWidget {
  const ChatRoomHattori({Key? key}) : super(key: key);

  @override
  ChatRoomState createState() => ChatRoomState();
}

class ChatRoomState extends State<ChatRoomHattori> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4a89-ae75-a22bf8d6f3ac');
  final types.User _hattori = const types.User(
    id: 'hattori',
    firstName: "服部",
    lastName: "平次",
    imageUrl: ImageUrls.hattoriFace0,
  );
  final types.User _conan = const types.User(
    id: 'conan',
    firstName: "名探偵",
    lastName: "コナン",
    imageUrl: ImageUrls.conanFace0,
  );
  String? hattoriText;
  //String? conanText;
  final firstComment = "あれれー、面白そうな問題見つけたよー！";


  @override
  void initState() {
    super.initState();
    _addMessage(types.TextMessage(
      author: _conan,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: firstComment,
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('真実はいつも一つ')),
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

  // ここでコナン君が話す
  Future<String> fetchMessage() async {
    const String url =
        'https://u5fhd9aj1l.execute-api.ap-northeast-1.amazonaws.com/Prod/chat-comic';
    final Map<String, String> headers = {'Content-Type': 'application/json'};
    final Map<String, String> data = {
      'input_text': hattoriText?? firstComment,
      'userid': 'user_0000',
      'convid': 'Conan',
    };
    debugPrint("hattoriText:$hattoriText");
    final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(data));

    if (response.statusCode == 200) {
      var jsonResponse = json.decode(response.body);
      String conanText = jsonResponse['Response'];
      debugPrint("conanText:$conanText");
      return jsonResponse['Response'];
    } else {
      return 'あれれ〜';
    }
  }

  void _handleSendPressed(types.PartialText message) async {
    // ユーザーが送信したメッセージをチャットに追加
    final userMessage = types.TextMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: message.text,
    );
    _addMessage(userMessage);

    // ここでコナン君が話す
    final sendMessage = await fetchMessage();
    final conanMessage = types.TextMessage(
      author: _conan,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: sendMessage,
    );
    _addMessage(conanMessage);

    // 服部が応答
    Map<String, dynamic> apiResponseData = await fetchResponseFromApi(conanMessage.text);
    Future.delayed(const Duration(seconds: 1), () {
      final responseText = apiResponseData['Response'] ?? 'なんや';
      final responseMessage = types.TextMessage(
        author: _hattori,
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: randomString(),
        text: responseText,
      );
      _addMessage(responseMessage);
    });
  }

  Future<Map<String, dynamic>> fetchResponseFromApi(String inputText) async {
    const String url =
        'https://u5fhd9aj1l.execute-api.ap-northeast-1.amazonaws.com/Prod/chat-comic';
    final Map<String, String> headers = {'Content-Type': 'application/json'};
    final Map<String, String> data = {
      'input_text': inputText,
      'userid': 'user_0001',
      'convid': 'Heiji',
    };
    final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(data));

    if (response.statusCode == 200) {
      var jsonResponse = json.decode(response.body);
      debugPrint(jsonResponse['Response']);
      debugPrint(jsonResponse['Quote']);
      hattoriText = jsonResponse['Response'];
      return {
        'Response': jsonResponse['Response'],
        'Quote': jsonResponse['Quote'],
        'Url': jsonResponse['Url'],
      };
    } else {
      debugPrint("確認");
      return {'Response': 'Failed', 'Quote': '0', 'Url': ''};
    }
  }
}
