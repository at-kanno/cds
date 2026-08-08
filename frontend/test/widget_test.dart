import 'package:cds_app/main.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Login screen renders', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.text('ログイン'), findsWidgets);
    expect(find.text('CDS'), findsOneWidget);
  });
}
