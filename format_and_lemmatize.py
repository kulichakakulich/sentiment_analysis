from pymystem3 import Mystem
import csv
from collections import Counter

# from nltk.corpus import stopwords
# import nltk
# nltk.download('stopwords')
# stop_words = stopwords.words('russian')
# stop_words.remove('не')
# print(stop_words)

mystem = Mystem()

NEG_MARKERS = {'санкция', 'санкционный', 'антироссийский', 'запрет', 'запрещать',
               'угроза', 'против России', 'блокирующий', 'конфликт', 'заблокировать'}
POS_MARKERS = {'рост', 'улучшение', 'выстоять', 'устойчивый', 'выдержать',
               'положительный результат', 'обход санкции', 'провал санкции', 'стабильность'}
STOP_WORDS = {'и', 'в', 'во', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот',
              'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех',
              'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда',
              'конечно', 'всю', 'между', 'INTERFAX', 'RU', 'INTERFAX.RU',  'москва', 'интерфакс'}
STOP_ARTICLES = {'сводка', 'COVID', 'заболевание'}
old_date = '01.01.2022'
neg_per_day = 0
pos_per_day = 0


def clearing_text(text: list) -> list:
    if any(word in STOP_ARTICLES for word in text):
        return None
    return [i for i in text if i not in STOP_WORDS]


def counting_words(date: str, text: list, all_words: list):
    global neg_per_day
    global pos_per_day
    try:
        for word in text:
            if word.isalpha():
                all_words.append(word)
            if word in NEG_MARKERS:
                neg_per_day += 1
            if word in POS_MARKERS:
                pos_per_day += 1
        if date != old_date:
            with open('count_neg_markers.csv', 'w', newline='', encoding='utf-8') as file_neg, \
                    open('count_pos_markers.csv', 'w', newline='', encoding='utf-8') as file_pos:
                write_neg = csv.writer(file_neg)
                write_pos = csv.writer(file_pos)
                write_neg.writerow([old_date, neg_per_day])
                write_pos.writerow([old_date, pos_per_day])
                neg_per_day = 0
                pos_per_day = 0
                global old_date
                old_date = date
    except TypeError:
        print(text)


def main():
    all_words = []
    with open('data.csv', 'r', encoding='utf-8') as input, \
            open("lem_data.csv", "w", newline='', encoding='utf-8') as output:
        raw_data = csv.reader(input)
        data = csv.writer(output)
        for row in raw_data:
            lemmas = mystem.lemmatize(row[1])
            clear_text = clearing_text(lemmas)
            if clear_text == None:
                continue
            counting_words(row[0], clear_text, all_words)
            lem_text = "".join(clear_text)
            temp = lem_text.split("-", 1)
            temp = temp[1].strip()
            print(temp)
            temp = temp.replace('"', '')
            temp = temp.split()
            temp = " ".join(temp)
            data.writerow([row[0], temp])
        cntr = Counter(all_words).most_common(1000)
        print(cntr)


if __name__ == "__main__":
    main()
