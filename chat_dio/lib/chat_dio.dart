import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'utilities.dart';
import 'main.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatRoomDio extends StatefulWidget {
  const ChatRoomDio({Key? key}) : super(key: key);

  @override
  ChatRoomState createState() => ChatRoomState();
}

class ChatRoomState extends State<ChatRoomDio> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4a89-ae75-a22bf8e6f3ac');
  final types.User _dio = const types.User(
    id: 'dio',
    firstName: "Dio",
    lastName: "",
    imageUrl: ImageUrls.dioFace0,
  );


  @override
  void initState() {
    super.initState();
    _addMessage(types.TextMessage(
      author: _dio,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: "このディオに何か聞きたいことがあるか。",
    ));

    initializeAsyncMethods();
  }
  Future<void> initializeAsyncMethods() async {
    const String url = 'https://1fi888qkjc.execute-api.ap-northeast-1.amazonaws.com/Prod/chat-comicc';
    final Map<String, String> headers = {'Content-Type': 'application/json'};
    Map<String, String> jsonData = {
      'userid': 'user_Dio',
      'convid': 'Dio',
      'method': 'Delete',
    };
    var response = await http.post(Uri.parse(url), headers: headers, body: json.encode(jsonData));
    debugPrint('Response status: ${response.statusCode}');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('教えて！ディオ課長！！')),
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
      final quote = apiResponseData['Quote'] ?? 'false';
      final quoteUrl = apiResponseData['Url'] ?? '';
      debugPrint(quoteUrl);

      // 画像メッセージを送信
      if(quote == "true"){
        final imageMessage = types.ImageMessage(
          author: _dio,
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: randomString(),
          uri: quoteUrl,
          name: 'image',
          size: 1,
          width: 100,
          height: 70,
        );
        _addMessage(imageMessage);
      }else{
        final responseMessage = types.TextMessage(
          author: _dio,
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: randomString(),
          text: responseText,
        );
        _addMessage(responseMessage);
      }
    });
  }

  Future<Map<String, dynamic>> fetchResponseFromApi(String inputText) async {
    const String url =
        'https://1fi888qkjc.execute-api.ap-northeast-1.amazonaws.com/Prod/chat-comic';
    final Map<String, String> headers = {'Content-Type': 'application/json'};
    final Map<String, String> data = {
      'input_text': inputText,
      'userid': 'user_Dio',
      'convid': 'Dio',
    };
    final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(data));

    if (response.statusCode == 200) {
      var jsonResponse = json.decode(response.body);
      debugPrint(jsonResponse['Response']);
      debugPrint(jsonResponse['Quote']);
      return {
        'Response': jsonResponse['Response'],
        'Quote': jsonResponse['Quote'],
        'Url': jsonResponse['Url'],
      };
    } else {
      return {'Response': 'Failed', 'Quote': '0', 'Url': ''};
    }
  }
}
