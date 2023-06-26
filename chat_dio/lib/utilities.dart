import 'dart:convert';
import 'dart:math';

String randomString() {
  final random = Random.secure();
  final values = List<int>.generate(16, (i) => random.nextInt(255));
  return base64UrlEncode(values);
}

class ImageUrls {
  static const hospiFace0 = "https://images-hospi.s3.ap-northeast-1.amazonaws.com/Face00.jpg";
  static const hospiFace1 = "https://images-hospi.s3.ap-northeast-1.amazonaws.com/Face01.jpg";
  static const hospiFace2 = "https://images-hospi.s3.ap-northeast-1.amazonaws.com/Face02.jpg";
  static const hospiFace3 = "https://images-hospi.s3.ap-northeast-1.amazonaws.com/Face03.jpg";

  static const dioFace0 = "https://images-dio.s3.ap-northeast-1.amazonaws.com/face.png";

  static const hattoriFace0 = "https://images-comics.s3.ap-northeast-1.amazonaws.com/Conan/HeijiFace.png";
}

