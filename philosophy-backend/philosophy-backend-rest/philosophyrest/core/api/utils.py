import random
import string

def randomStr(size=8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))
