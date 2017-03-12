import unicodedata
# word = unicodedata.normalize('NFD', unicode(word)).encode('ascii','ignore')

def normalize_word(word_in):
    word_out = word_in.lower()
    word_out = ''.join((c for c in unicodedata.normalize('NFD', unicode(word_out)) if unicodedata.category(c) != 'Mn'))

    return word_out