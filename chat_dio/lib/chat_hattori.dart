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
    firstName: "",
    lastName: "コナン",
    imageUrl: ImageUrls.conanFace0,
  );
  String? hattoriText;
  //String? conanText;
  final firstComment = "なんや、何か聞きたいことあるんか？";


  @override
  void initState() {
    super.initState();
    _addMessage(types.TextMessage(
      author: _hattori,
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
  Future<String> fetchConanMessage(String message) async {
    const String url =
        'https://u5fhd9aj1l.execute-api.ap-northeast-1.amazonaws.com/Prod/chat-comic';
    final Map<String, String> headers = {'Content-Type': 'application/json'};
    //服部のコメントをコナンのDBに格納
    debugPrint("hattoriText:$hattoriText");
    hattoriText ??= firstComment;
    hattoriText = hattoriText?.replaceAll('工藤', 'コナン');
    Map<String, String> commentData = {
      'input_text': hattoriText??firstComment,
      'userid': 'user_Conan',
      'convid': 'Conan',
      'system': 'false',
      'response_necessary': 'false',
    };
    await http.post(Uri.parse(url), headers: headers, body: json.encode(commentData));

    //systemからヒントし、コナン君回答 DB格納
    debugPrint("userText:$message");
    commentData = {
      'input_text': 'user:$message',
      'userid': 'user_Conan',
      'convid': 'Conan',
      'system': 'false',
      'response_necessary': 'true',
    };
    final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(commentData));

    //systemからヒントし、服部のDBに格納
    debugPrint("conanText:$response");
    commentData = {
      'input_text': 'user:$message',
      'userid': 'user_Heiji',
      'convid': 'Heiji',
      'system': 'false',
      'response_necessary': 'false',
    };
    await http.post(Uri.parse(url), headers: headers, body: json.encode(commentData));

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
    String receiveConanMessage = await fetchConanMessage(message.text);
    RegExp exp = RegExp(r"^[^:]*:");
    receiveConanMessage = receiveConanMessage.replaceAll(exp, '');
    final conanMessage = types.TextMessage(
      author: _conan,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: receiveConanMessage,
    );
    _addMessage(conanMessage);

    // 服部が応答
    Map<String, dynamic> receiveHattoriMessage = await fetchHattoriMessage(conanMessage.text);
    Future.delayed(const Duration(seconds: 1), () {
      String responseText = receiveHattoriMessage['Response'] ?? 'なんや';
      RegExp exp = RegExp(r"^[^:]*:");
      responseText = responseText.replaceAll(exp, '');
      final responseMessage = types.TextMessage(
        author: _hattori,
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: randomString(),
        text: responseText,
      );
      _addMessage(responseMessage);
    });
  }

  Future<Map<String, dynamic>> fetchHattoriMessage(String conanMessageText) async {
    const String url =
        'https://u5fhd9aj1l.execute-api.ap-northeast-1.amazonaws.com/Prod/chat-comic';
    final Map<String, String> headers = {'Content-Type': 'application/json'};
    Map<String, String> commentData = {
      'input_text': conanMessageText,
      'userid': 'user_Heiji',
      'convid': 'Heiji',
      'system': 'false',
      'response_necessary': 'true',
    };
    final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(commentData));

    if (response.statusCode == 200) {
      var jsonResponse = json.decode(response.body);
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
