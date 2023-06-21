import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'utilities.dart';
import 'main.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class SecondChatRoom extends StatefulWidget {
  const SecondChatRoom({Key? key}) : super(key: key);

  @override
  ChatRoomState createState() => ChatRoomState();
}

class ChatRoomState extends State<SecondChatRoom> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4a89-ae75-a22bf8d6f3ac');
  types.User _dio = const types.User(
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
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chat with Dio')),
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

  void _addNetworkImageAsMessage(String imageUrl) {
    final message = types.ImageMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      // ここで他のプロパティを設定する必要があるかもしれません
      uri: imageUrl,
      name: 'image', // 画像の名前 (任意で設定)
      size: 1, // 画像のサイズ (必要に応じて設定)
      width: 100, // 画像の幅 (必要に応じて設定)
      height: 100, // 画像の高さ (必要に応じて設定)
    );

    _addMessage(message);
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
      final quote = apiResponseData['MaxIndex_Emotion'] ?? '0';
      final quoteNumber = apiResponseData['MaxIndex_Emotion'] ?? '0';
      final quoteUrl = apiResponseData['MaxIndex_Emotion'] ?? '0';
      print(quoteNumber);

      final responseMessage = types.TextMessage(
        author: _dio,
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: randomString(),
        text: responseText,
      );
      _addMessage(responseMessage);

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
      }
    });
  }

  Future<Map<String, dynamic>> fetchResponseFromApi(String inputText) async {
    const String url =
        'https://as7ol49p7g.execute-api.ap-northeast-1.amazonaws.com/Prod/chatroom';
    final Map<String, String> headers = {'Content-Type': 'application/json'};
    final Map<String, String> data = {
      'input_text': inputText,
      'userid': 'user_0001',
      'convid': 'dio',
    };
    final response = await http.post(Uri.parse(url), headers: headers, body: json.encode(data));

    if (response.statusCode == 200) {
      var jsonResponse = json.decode(response.body);
      return {
        'Response': jsonResponse['Response'],
        'Emotion': jsonResponse['Emotion']['Emotion'],
        'MaxIndex_Emotion': jsonResponse['Emotion']['MaxIndex'],
        'NeedMap': jsonResponse['Map']['Need'],
        'FloorUrl': jsonResponse['Map']['Url'],
      };
    } else {
      return {'Response': 'Failed', 'Emotion': '[嬉しい:0, 心配:0, 困惑:0, 懸命:0]', 'MaxIndex_Emotion': '0'};
    }
  }
}
