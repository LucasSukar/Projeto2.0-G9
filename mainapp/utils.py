import requests
def fetch_book_info_by_title(title):
    google_books_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': title, 'projection': 'lite'}
    response = requests.get(google_books_url, params=params)
    response_json = response.json()

    if response_json['totalItems'] == 0:
        return None

    book_info = response_json['items'][0]  
    cover_url = book_info['volumeInfo'].get('imageLinks', {}).get('thumbnail')
    isbn_list = [identifier['identifier'] for identifier in book_info['volumeInfo'].get('industryIdentifiers', []) if identifier['type'] == 'ISBN_13']
    isbn = isbn_list[0] if isbn_list else None

    return {
        'isbn': isbn,
        'cover_url': cover_url
    }