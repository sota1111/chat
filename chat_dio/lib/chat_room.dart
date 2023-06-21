import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'utilities.dart';
import 'main.dart';
import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatRoom extends StatefulWidget {
  const ChatRoom({Key? key}) : super(key: key);

  @override
  ChatRoomState createState() => ChatRoomState();
}

class ChatRoomState extends State<ChatRoom> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4a89-ae75-a22bf8d6f3ac');
  types.User _hospi = const types.User(
    id: 'hospi-blue',
    firstName: "ホスピ",
    lastName: "",
    imageUrl: ImageUrls.hospiFace0,
  );


  @override
  void initState() {
    super.initState();
    _addMessage(types.TextMessage(
      author: _hospi,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      text: "こんにちは、ホスピです。\n何かお困りですか？",
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chat Room 1')),
      drawer: const AppDrawer(),
      body: Chat(
        user: _user,
        messages: _messages,
        onSendPressed: _handleSendPressed,
        //onAttachmentPressed: () => _addNetworkImageAsMessage('https://images-hospi.s3.ap-northeast-1.amazonaws.com/Face03.jpg'), // ここを修正
        //onMessageTap: _handleMessageTap,
        //onPreviewDataFetched: _handlePreviewDataFetched,
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
      final responseEmotion = apiResponseData['MaxIndex_Emotion'] ?? '0';
      final floorUrl = apiResponseData['FloorUrl'] ?? 'None';
      final needMap = apiResponseData['NeedMap'] ?? 'false';
      print(floorUrl);


      Map<String, String> emotionToImageUrl = {
        '0': ImageUrls.hospiFace0,
        '1': ImageUrls.hospiFace1,
        '2': ImageUrls.hospiFace2,
        '3': ImageUrls.hospiFace3,
      };

      String imageUrl = emotionToImageUrl[responseEmotion] ?? ImageUrls.hospiFace0;

      _hospi = types.User(
        id: 'hospi-blue',
        firstName: "ホスピ",
        lastName: "",
        imageUrl: imageUrl,
      );

      final responseMessage = types.TextMessage(
        author: _hospi,
        createdAt: DateTime.now().millisecondsSinceEpoch,
        id: randomString(),
        text: responseText,
      );
      _addMessage(responseMessage);

      // 画像メッセージを送信
      if(needMap == "true"){
        final imageMessage = types.ImageMessage(
          author: _hospi,
          createdAt: DateTime.now().millisecondsSinceEpoch,
          id: randomString(),
          uri: floorUrl,
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
      'convid': 'hospi',
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
