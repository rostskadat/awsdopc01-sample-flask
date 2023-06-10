
from typing import List
from flask_restx import Api, Resource, fields


class BookDetails(Resource):
    id: int
    isbn: str


class Book(Resource):
    id: int
    title: str
    author: str
    details: List[BookDetails]
