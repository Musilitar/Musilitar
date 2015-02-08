import wikipedia
from data import database


def search(keywords):
    answer = ""
    for keyword in keywords:
        try:
            page = wikipedia.page(keyword)
            first_sentence = page.summary.split('.', 1)[0]
            if len(first_sentence) <= 160:
                answer += first_sentence
                database.definitions.save({"stem": keyword,
                                           "text": first_sentence,
                                           "score": 0.5})
        except wikipedia.PageError:
            print("No Wikipedia page found for: " + keyword)
    return answer
