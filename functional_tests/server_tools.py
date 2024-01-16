from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(host):
    """Получить manage.py"""
    return f"~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py"

def reset_database(host):
    """Обнулить базу данных"""
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f"jim9502@{host}"):
        run(f"{manage_dot_py} flush --noinput")

def create_session_on_server(host, email):
    """Создать сессию на сревере"""
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f"jim9502@{host}"):
        session_key = run(f"{manage_dot_py} create_session {email}")
        return session_key.strip()
