import string

translation_table = string.maketrans(string.punctuation, ' ' * len(string.punctuation))

rev_classes = ["truthful", "deceptive", "positive", "negative"]
veracity_vals = ["truthful", "deceptive"]
sentiment_vals = ["positive, negative"]

# list of frequent 3 letter words
li_freq_3_letter_words = "the, and, for, are, can, had, was, one, our, " \
                "get, his, how, who, did, its, let, " \
                "put, "
li_freq_4_letter_words = "from, that, were, will, with, "
li_other_freq_words = "which, "

# with open("stop_words.txt") as f_stop_words:
#     stop_words = f_stop_words.read().splitlines()
# # print stop_words

li_freq_words = (li_freq_3_letter_words + li_freq_4_letter_words + li_other_freq_words).split(", ")

if __name__ == "__main__":
    print li_freq_words

# li_freq_words = (li_freq_3_letter_words + li_freq_4_letter_words + li_other_freq_words).split(", ") + stop_words
