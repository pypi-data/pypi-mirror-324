import random

phrases = []

def rand():
    if not phrases:
        return None
    random.shuffle(phrases)
    return random.choice(phrases)

def add(newphrase):
    global phrases
    if newphrase in phrases:
        return False
    phrases.append(newphrase)
    return True

def rm(phrase):
    global phrases
    if phrase not in phrases:
        return False
    phrases.remove(phrase)
    return True
