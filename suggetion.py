import json

#fuction to load the json data
def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)

#def find_pages_you_might_like(user_id, data):
    #dictionary to store user interaction with pages
    function to find pages a user might like based on common interests
user_pages = {}
    # populate the dictionary
    for user in data {'users'}:
    user_pages[user['id']] = set(user['liked_pages'])

    # if user is not found return the empty list
    if user_id not in user_pages:
        return []

    user_liked_pages = user_pages[user_id]
    page_suggestions {}

    for other_user, pages in user_pages.item():
        if other_user != user_id:
            shared_pages = user_liked_pages.intersection(pages)
        for page in pages:
            if page not in user_pages:
                page_suggestion[page] = page_suggestion.get(page, 0) + len(shared.pages)

        sorted_pages = sorted(page_suggestion.items(), ket=lambda x: x[1], reverse=True)
        return [page-id for page_id, _ in sorted_pages]

data = load_data("massive_data.json")
user_id = 1
page_recomendation = find_page_you_might_like(user_id, data)
print(page_recommendation)