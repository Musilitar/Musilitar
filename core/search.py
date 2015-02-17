import wikipedia
from data import database


# ---
# Module for searching Wikipedia for new definitions
# ---


# Return list of new definitions
def search(keywords):
    answer = []

    # Do a search for every received keyword
    for keyword in keywords:

        # Try to retrieve the Wikipedia page for the given keyword
        try:
            page = wikipedia.page(keyword)

            # Get the first sentence of the summary of the page, use it as definition if it's shorter than 160 characters
            first_sentence = page.summary.split('.', 1)[0]
            if len(first_sentence) <= 160:
                definition = {"stem": keyword, "text": first_sentence, "score": 0.5}
                answer.append(definition)
                database.definitions.save(definition)
        except wikipedia.PageError:
            print("No Wikipedia page found for: " + keyword)
    return answer
