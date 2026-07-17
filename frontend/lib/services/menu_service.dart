import 'dart:convert';

import 'package:http/http.dart' as http;

import '../config/api_config.dart';
import '../models/main_menu.dart';

class MenuService {
  Future<MainMenu> fetchMainMenu(int userId) async {
    final response = await http
        .get(Uri.parse('${ApiConfig.mainMenuEndpoint}?user_id=$userId'))
        .timeout(const Duration(seconds: 10));

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode != 200) {
      throw Exception(body['message'] as String? ?? 'Failed to load main menu.');
    }

    return MainMenu.fromJson(body);
  }

  Future<void> logout(int userId) async {
    final response = await http
        .post(
          Uri.parse(ApiConfig.logoutEndpoint),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({'user_id': userId}),
        )
        .timeout(const Duration(seconds: 10));

    if (response.statusCode != 200) {
      final body = jsonDecode(response.body) as Map<String, dynamic>;
      throw Exception(body['message'] as String? ?? 'Logout failed.');
    }
  }
}
