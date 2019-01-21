import random, string


def token_generator(size=120, chars=string.ascii_letters + string.digits):
    return "".join([random.choice(chars) for _ in range(size)])
