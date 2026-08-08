import 'package:cds_app/models/main_menu.dart';
import 'package:cds_app/models/single_question_session.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('hierarchical menu parses Part5 field-quiz categories 141-146', () {
    final menu = MainMenu.fromJson({
      'user_id': 1,
      'email': 't@example.com',
      'status': 0,
      'title': 'TOEIC メニュー',
      'hierarchy': true,
      'sections': [
        {
          'id': 'home',
          'title': '',
          'items': [
            {
              'category': 0,
              'action': 'openSubmenu',
              'submenu': 'area_quiz',
              'label': '分野別問題',
              'subtitle': '',
              'color': '#2563EB',
              'enabled': true,
            },
          ],
        },
      ],
      'actions': [],
      'submenus': {
        'area_quiz': {
          'id': 'area_quiz',
          'title': '分野別問題',
          'items': [
            for (final id in [10, 11, 12, 13, 141, 142, 143, 144, 145, 146, 15, 16])
              {
                'category': id,
                'action': 'makeExam',
                'label': 'exam $id',
                'subtitle': '',
                'color': '#059669',
                'enabled': true,
              },
          ],
        },
      },
    });

    expect(menu.hierarchy, isTrue);
    final cats =
        menu.submenus['area_quiz']!.items.map((item) => item.category).toList();
    expect(cats, [10, 11, 12, 13, 141, 142, 143, 144, 145, 146, 15, 16]);
    expect(cats, isNot(contains(14)));
  });

  test('single-question time_limit defaults to 90 when omitted', () {
    final session = SingleQuestionSession.fromJson({
      'user_id': 1,
      'category': 94,
      'area': 'P4',
      'title': 'P4：一問一答（問題）',
      'question': 'Q',
      'selection1': 'A',
      'selection2': 'B',
      'selection3': 'C',
      'selection4': 'D',
      'choice_count': 4,
      'crct': 0,
      'cid': 1,
      'num': '401',
      'permutation': '1234',
    });
    expect(session.timeLimitSeconds, 90);
  });
}
