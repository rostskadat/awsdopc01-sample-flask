
from flask import Blueprint
from microservice.api.dao import BookDAO
from microservice.api.models import Book, BookDetails

blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api')


__all__ = [
    "blueprint"
]
