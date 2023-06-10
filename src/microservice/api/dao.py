from microservice.api.exceptions import BookNotFound

class BookDAO(object):
    def __init__(self, ):
        self.counter = 0
        self.books = []

    def create(self, data):
        book = data
        book['id'] = self.counter = self.counter + 1
        self.books.append(book)
        return book

    def get(self, id=None):
        if not id:
            return self.books
        for book in self.books:
            if book['id'] == id:
                return book
        raise BookNotFound(id)

    def update(self, id, data):
        book = self.get(id)
        book.update(data)
        return book

    def delete(self, id):
        book = self.get(id)
        self.books.remove(book)
        return book