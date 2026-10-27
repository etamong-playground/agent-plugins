def isolated_environment(environment):
    allowed = {'PATH', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TZ', 'SYSTEMROOT', 'WINDIR'}
    return {key: value for key, value in environment.items() if key in allowed}
