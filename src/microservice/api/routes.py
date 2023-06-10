import json
from http import HTTPStatus
from typing import List

from flask import request
from flask_restx import Api, Resource, fields
from microservice.api import blueprint
from microservice.api.models import Book, BookDetails
from microservice.api.dao import BookDAO
from microservice.api.exceptions import BookNotFound

api = Api(blueprint)

ns = api.namespace("books", description="CRUD Operations for Books")
api.add_namespace(ns)

book_detail_model = api.model(
    "BookDetail",
    {
        "key": fields.String(description='The key identifing the detail', required=True),
        "value": fields.String(description='The value for this detail', required=False),
    }
)

book_model = api.model(
    "Book",
    {
        "id": fields.Integer,
        "title": fields.String(description='The title of the book', required=True),
        "author": fields.String(description='The author of the book', required=True),
        "details": fields.List(fields.Nested(book_detail_model)),
    },
)

books_model = api.model(
    "Books",
    {
        "books": fields.List(fields.Nested(book_model)),
    },
)

books_dao = BookDAO()
books_dao.create({'title': 'La Marea', 'author': 'Cristina Gumuzio Irala', 'details':[{"key": "ISBN", "value": '841212720X'}]})
books_dao.create({'title': 'Jaque al Rey', 'author': 'Mario Escobar', 'details':[{"key": "ISBN", "value": 'B0BW2K4CX1'}]})
books_dao.create({'title': 'EL CONSEJO', 'author': 'Carlos Palanco Vázquez', 'details':[{"key": "ISBN", "value": 'B074L76YY3'}]})

book_parser = api.parser()
book_parser.add_argument("id", type=int, location="form")
book_parser.add_argument("title", type=str, location="form")
book_parser.add_argument("author", type=str, location="form")
#book_parser.add_argument('cover', type=FileStorage, location='files')

detail_parser = api.parser()
detail_parser.add_argument("key", type=str, location="form")
detail_parser.add_argument("value", type=str, location="form")

@ns.route("/", endpoint='books')
class BooksApi(Resource):


    @api.doc(description="Return the list of all known books")
    @api.marshal_list_with(book_model)
    @api.response(200, "Success", books_model)
    def get(self):
        return books_dao.get()

    @api.doc(description="Add a new book")
    @api.expect(book_parser)
    @api.marshal_with(book_model)
    @api.response(200, "Success")
    def post(self):
        book = book_parser.parse_args()
        if 'details' not in book: 
            book['details'] = []
        return books_dao.create(book)

@ns.route("/<int:book_id>")
@ns.param('book_id', 'The book id')
class BookApi(Resource):

    @api.doc(description="Get the book with the given `book_id`")
    @api.response(200, "Success", book_model)
    @api.response(404, "Book not found")
    def get(self, book_id: int) -> Book:
        return books_dao.get(book_id)

    @api.doc(description="Update the book with the given `book_id` with new details")
    @api.expect(detail_parser)
    @api.response(201, "Book updated", book_model)
    @api.response(404, "Book not found")
    def post(self, book_id: int) -> Book:
        args = detail_parser.parse_args()
        if book := books_dao.get(book_id):
            book["details"].append(args)
        return book

    @api.doc(description="Delete the book with the given `book_id`")
    @api.expect(detail_parser)
    @api.response(200, "Book deleted", book_model)
    def delete(self, book_id: int) -> None:
        try:
            return books_dao.delete(book_id)
        except BookNotFound:
            return None

    @api.errorhandler(BookNotFound)
    def handle_error(e):
        return {'message': f"Book '{e.id}' was not found"}, 404

