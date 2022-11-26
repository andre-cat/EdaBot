from eda_bot import constants as __constants
import os as __os


def get_path(folder: str = '', file: str = '') -> str:
    path = __constants.PATH.replace('\\', '/')

    if folder != '':
        folder = folder.replace('\\', '/')
        path = f'{path}/{folder}'

    try:
        __os.makedirs(path, exist_ok=True)
    except OSError as error:
        print(f'Directory {path} can not be created.')

    if file != '':
        file = file.replace('\\', '/')
        path = f'{path}/{file}'

    return path
