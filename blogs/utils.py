import random
import string

from django.utils.text import slugify

from transliterate import translit

import unicodedata as ud

latin_letters= {}
def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))


def random_string_generator(size=10, chrs=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chrs) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        if is_latin(instance.title[0]) == False:
            instance.title = translit(instance.title, 'ru', reversed=True)
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        randstr = random_string_generator(size=4)
        new_slug = f"{slug}-{randstr}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
