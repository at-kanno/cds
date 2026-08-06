import 'package:flutter/foundation.dart';

/// Build-time branding for subject store apps (CDS / SPANISH4 / TOEIC).
///
/// Example:
/// ```
/// flutter build appbundle --flavor toeic --release \
///   --dart-define=APP_FLAVOR=toeic \
///   --dart-define=APP_TITLE=TOEIC 模擬試験 \
///   --dart-define=API_BASE_URL=https://traveltokio.com/toeic
/// ```
class AppBranding {
  const AppBranding._();

  /// `cds`, `spanish4`, or `toeic` (informational; URL/title are the real switches).
  static const String flavor = String.fromEnvironment(
    'APP_FLAVOR',
    defaultValue: 'cds',
  );

  /// Shown on login and as MaterialApp title.
  static const String title = String.fromEnvironment(
    'APP_TITLE',
    defaultValue: 'CDS',
  );

  /// When set at build time, the login screen hides the server URL field.
  static const String bakedApiBaseUrl = String.fromEnvironment('API_BASE_URL');

  static bool get hasFixedApiUrl => bakedApiBaseUrl.trim().isNotEmpty;

  /// Dev-only: show URL field when no API URL was baked into the binary.
  static bool get showServerField => !kIsWeb && !hasFixedApiUrl;
}
