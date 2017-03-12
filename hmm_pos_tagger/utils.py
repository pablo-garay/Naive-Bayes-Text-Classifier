import unicodedata
import re
# word = unicodedata.normalize('NFD', unicode(word)).encode('ascii','ignore')

def normalize_word(word_in):
    word_out = word_in.lower() # to lowercase
    # remove accents and tildes
    word_out = ''.join((c for c in unicodedata.normalize('NFD', unicode(word_out)) if unicodedata.category(c) != 'Mn'))
    word_out = unicodedata.normalize('NFD', unicode(word_out)).encode('ascii','ignore')

    # Replace numbers/digits by "NUM"
    word_out = re.sub(r'[0-9]+', 'NUM', word_out)

    # if len(word_out) >= 2:
    #     word_out = ''.join([i for i in word_out if i != "'"])

    if len(word_out) > 2:
        word_out = ''.join([i for i in word_out if i not in ["-"]])
        # word_out = ''.join([i for i in word_out if i not in ["-", "'", "."]])

    # if len(word_out) >= 2:
    #     word_out = ''.join([i for i in word_out if i != "'"])

    # if len(word_out) >= 2:
    #     word_out = word_out[0] + ''.join([i for i in word_out[1:] if i != "."])

    return word_out