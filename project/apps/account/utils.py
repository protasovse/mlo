from apps.account.models import Info


def delete_nonexistent_photos():
    """
    Удаляем из базы фото, файлов который нет
    :return:
    """
    info = Info.objects.all()
    for i in info:
        try:
            print(i.orig.file)
        except:
            i.orig = None
            i.pic = ''
            i.photo = ''
            i.save()
