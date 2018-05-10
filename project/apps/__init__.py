import hashlib
import random
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    h = hashlib.md5()
    filename_string = "%s-%s" % (random.random(), filename)
    h.update(filename_string.encode('utf-8'))
    filename = "%s.%s" % (h.hexdigest(), ext)
    return os.path.join(
        instance.directory_string_var,
        filename[0:3],
        filename[3:6],
        filename[6:9],
        filename
    )