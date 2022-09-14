import typing
from zipfile import ZipFile
from io import BytesIO
from os import listdir, remove, rmdir
from os.path import isdir, isfile


# Добавляет файл/папку в архив
from aiogram import types


def add_to_archive(archive: ZipFile, path: str, arcname: str) -> ZipFile:
    if isfile(path):
        archive.write(path, arcname)
    elif isdir(path):
        for entity in listdir(path):
            add_to_archive(archive, path + '/' + entity, arcname + '/' + entity)
    return archive


# Создаёт архив из папки
def create_archive_from_dir(src: str, comment: str = '', need_delete: bool = True) -> bytes:
    dst = src + '.zip'
    archive = ZipFile(file=dst, mode='a')
    archive = add_to_archive(archive, src, '')
    archive.comment = comment.encode(encoding='utf-8')
    archive.close()

    with open(dst, 'rb') as f:
        byte_data = f.read()

    if need_delete:
        sdelete(dst)

    return byte_data


# Удаляет файл/папку не вызывая исключений
def sdelete(path: str):
    if isfile(path):
        try:
            remove(path)
        except:
            ...
    elif isdir(path):
        for entity in listdir(path):
            sdelete(path + '/' + entity)
        try:
            rmdir(path)
        except:
            ...
