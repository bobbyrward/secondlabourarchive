from django import template


register = template.Library()


def archive_menu_button(current_path, path, label):
    return { 'current_path': current_path, 'button_path': path, 'button_label': label }


def archive_menu_secondary_button(current_path, path, label):
    return { 'current_path': current_path, 'button_path': path, 'button_label': label }


register.inclusion_tag('menu_button.html')(archive_menu_button)
register.inclusion_tag('menu_secondary_button.html')(archive_menu_secondary_button)


