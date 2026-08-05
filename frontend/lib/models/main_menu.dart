class MenuItem {
  const MenuItem({
    required this.category,
    required this.action,
    required this.label,
    required this.subtitle,
    required this.color,
    required this.enabled,
    this.submenu,
  });

  factory MenuItem.fromJson(Map<String, dynamic> json) {
    return MenuItem(
      category: (json['category'] as num?)?.toInt() ?? 0,
      action: json['action'] as String,
      label: json['label'] as String,
      subtitle: json['subtitle'] as String? ?? '',
      color: json['color'] as String? ?? '#808080',
      enabled: json['enabled'] as bool? ?? true,
      submenu: json['submenu'] as String?,
    );
  }

  final int category;
  final String action;
  final String label;
  final String subtitle;
  final String color;
  final bool enabled;
  final String? submenu;
}

class MenuSection {
  const MenuSection({
    required this.id,
    required this.title,
    required this.items,
    this.message,
  });

  factory MenuSection.fromJson(Map<String, dynamic> json) {
    return MenuSection(
      id: json['id'] as String,
      title: json['title'] as String? ?? '',
      message: json['message'] as String?,
      items: (json['items'] as List<dynamic>)
          .map((item) => MenuItem.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  final String id;
  final String title;
  final String? message;
  final List<MenuItem> items;
}

class MenuAction {
  const MenuAction({
    required this.id,
    required this.label,
    required this.action,
    required this.enabled,
    this.category,
  });

  factory MenuAction.fromJson(Map<String, dynamic> json) {
    return MenuAction(
      id: json['id'] as String,
      label: json['label'] as String,
      action: json['action'] as String,
      enabled: json['enabled'] as bool? ?? true,
      category: (json['category'] as num?)?.toInt(),
    );
  }

  final String id;
  final String label;
  final String action;
  final bool enabled;
  final int? category;
}

class MainMenu {
  const MainMenu({
    required this.userId,
    required this.email,
    required this.status,
    required this.title,
    required this.sections,
    required this.actions,
    this.hierarchy = false,
    this.submenus = const {},
  });

  factory MainMenu.fromJson(Map<String, dynamic> json) {
    final rawSubmenus = json['submenus'] as Map<String, dynamic>? ?? {};
    return MainMenu(
      userId: json['user_id'] as int,
      email: json['email'] as String? ?? '',
      status: json['status'] as int? ?? 0,
      title: json['title'] as String? ?? 'Main Menu',
      hierarchy: json['hierarchy'] as bool? ?? false,
      sections: (json['sections'] as List<dynamic>)
          .map((section) => MenuSection.fromJson(section as Map<String, dynamic>))
          .toList(),
      actions: (json['actions'] as List<dynamic>)
          .map((action) => MenuAction.fromJson(action as Map<String, dynamic>))
          .toList(),
      submenus: rawSubmenus.map(
        (key, value) => MapEntry(
          key,
          MenuSection.fromJson(value as Map<String, dynamic>),
        ),
      ),
    );
  }

  final int userId;
  final String email;
  final int status;
  final String title;
  final bool hierarchy;
  final List<MenuSection> sections;
  final List<MenuAction> actions;
  final Map<String, MenuSection> submenus;
}
