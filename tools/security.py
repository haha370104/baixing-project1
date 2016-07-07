import random
import string


def get_salt(num):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return salt
