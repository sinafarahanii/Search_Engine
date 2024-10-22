import re
import json
from parsivar import FindStems


def read_file():
    with open('IR_data_news_12k.json', 'r', encoding="utf-8", errors="surrogateescape") as f:
        stuff = json.load(f)
    f.close()
    return stuff


docs = read_file()
first_doc = docs['4092']
number_of_docs = len(docs)
stemmer = FindStems()

def normalize(text):

    # remove some characters
    text = text.translate({ord(c): None for c in
                           ['\u066c', '\u0621', '\u0674', '\u0085', '\u0670', '\u002c', '\u003a',
                            '\u003b', '\u003d', '\u0021', '\u003f', '\u003e', '\u003c', '\u064b', '\u064c',
                            '\u064d', '\u064e', '\u064f', '\u0650', '\u0651', '\u0652']})
    text = text.translate({ord("؛"): " "})
    text = text.translate({ord('\u060c'): " "})
    text = text.translate({ord(")"): " "})
    text = text.translate({ord("("): " "})
    text = text.translate({ord("«"): " "})
    text = text.translate({ord("-"): " "})
    text = text.translate({ord("_"): " "})
    text = text.translate({ord("\""): " "})
    text = text.translate({ord("¬"): " "})
    text = text.translate({ord("»"): " "})
    text = text.translate({ord("؟"): None})
    text = text.translate({ord("*"): None})
    # correct spacing
    text = text.translate({ord("\n"): " "})
    text = text.replace(u'\xa0', u' ')
    text = re.sub(r"\u200c{2,}", "\u200c", text)
    text = text.replace(r" {2,}", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"([^ ]ه) ی ", r"\1‌ی ", text)  # fix ی space
    text = re.sub(r"(^| )(ن?می) ", r"\1\2‌", text)  # put zwnj after می, نمی
    # put zwnj before تر, تری, ترین, گر, گری, ها, های
    text = re.sub(r"(?<=[^\n\d "
                  + r"\.:!،؛؟»\]\)\}"
                  + r"«\[\(\{"
                  + "]{2}) (تر(ین?)?|گری?|های?)(?=[ \n"
                  + r"\.:!،؛؟»\]\)\}"
                  + r"«\[\(\{"
                  + "]|$)", r"‌\1", text)

    text = re.sub(r"([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n" + r"\.:!،؛؟»\]\)\}" + "]|$)", r"\1‌\2", text)
    text = re.sub(r"([^ ]) (ا(م|ش|ت))(?=[ \n" + r"\.:!،؛؟»\]\)\}" + "]|$)", r"\1‌\2", text)
    # put space after a number
    text = re.sub(r"(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2", text)
    # put space before a number
    text = re.sub(r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)", r"\1 \2", text)
    # dots
    text = re.sub(r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\.)", r"\1 \2", text)
    text = re.sub(r"(\.)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2", text)
    text = re.sub(r"(\s)(\.)", r"", text)
    text = re.sub(r"(\.)(\s)", r"", text)
    # slash
    text = re.sub(r"(\/)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2", text)
    text = re.sub(r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\/)", r"\1 \2", text)
    text = text.translate({ord("/"): None})
    # separate mi and nemi
    matches = re.findall(r"\bن?می[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+", text)
    for m in matches:
        r = re.sub("^(ن?می)", r"\1‌", m)
        tmp = stemmer.convert_to_stem(r).split("&")
        if len(tmp) == 2:
            text = text.replace(m, r)
    # persian numbers
    text = text.translate({ord("0"): "٠"})
    text = text.translate({ord("1"): "١"})
    text = text.translate({ord("2"): "٢"})
    text = text.translate({ord("3"): "٣"})
    text = text.translate({ord("4"): "٤"})
    text = text.translate({ord("5"): "٥"})
    text = text.translate({ord("6"): "٦"})
    text = text.translate({ord("7"): "٧"})
    text = text.translate({ord("8"): "٨"})
    text = text.translate({ord("9"): "٩"})
    # unicode replacement
    text = text.translate({ord("﷽"): "بسم الله الرحمن الرحیم"})
    text = text.translate({ord("ﷴ"): "محمد"})
    text = text.translate({ord("ﷳ"): "اکبر"})
    text = text.translate({ord("﷼"): "ریال"})
    text = text.translate({ord("ﷵ"): "صلعم"})
    text = text.translate({ord("ﷶ"): "رسول"})
    text = text.translate({ord("ﷷ"): "علیه"})
    text = text.translate({ord("ﷸ"): "وسلم"})
    text = text.translate({ord("ﷸ"): "وسلم"})
    text = text.translate({ord("ي"): "ی"})
    text = text.translate({ord("ك"): "ک"})
    return text


def tokenizer(normalized_text):
    final_token_list = []
    normalized_text = re.split(r"\s+", normalized_text)
    for word in normalized_text:
        final_token_list.append(word)
    return final_token_list

