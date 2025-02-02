import toml
from os.path import join, exists
from django.conf import settings


def permission_message_return(language: str, data: str) -> str:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        with open(message_path, 'r', encoding='utf-8') as message:
            message_data = toml.load(message)
        try:
            return message_data['permission'][data]
        except KeyError:
            return data
    else:
        return data


def detail_message_return(language: str, data: str) -> dict:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        with open(message_path, 'r', encoding='utf-8') as message:
            message_data = toml.load(message)
        try:
            return {'detail': message_data['detail'][data]}
        except KeyError:
            return {'detail': data}
    else:
        return {'detail': data}


def msg_message_return(language: str, data: str) -> dict:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        with open(message_path, 'r', encoding='utf-8') as message:
            message_data = toml.load(message)
        try:
            return {'msg': message_data['msg'][data]}
        except KeyError:
            return {'msg': data}
    else:
        return {'msg': data}

def login_message_return(language: str, data: str) -> dict:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        with open(message_path, 'r', encoding='utf-8') as message:
            message_data = toml.load(message)
        try:
            return {'login': message_data['login'][data]}
        except KeyError:
            return {'login': data}
    else:
        return {'login': data}

def others_message_return(language: str, data: str) -> str:
    message_path = join(settings.LANGUAGE_DIR, language + '.toml')
    if exists(message_path):
        with open(message_path, 'r', encoding='utf-8') as message:
            message_data = toml.load(message)
        try:
            return message_data['others'][data]
        except KeyError:
            return data
    else:
        return data
