from flask import Flask
from flask_graphql import GraphQLView
from graphene import (
    ObjectType,
    InputObjectType,
    Mutation,
    Schema,
    String,
    Int,
    ID,
    Boolean,
    DateTime,
    Float,
    Field,
)
import datetime

books = [
    {
        "book_id": 1,
        "readers": 2000,
        "name": "Book One",
        "description": "Description One",
        "author": "Author One",
        "price": 2022.912,
        "is_published": True,
        "will_be_sold": datetime.datetime.now(),
    },
    {
        "book_id": 2,
        "readers": 2000,
        "name": "Book Two",
        "description": "Description Two",
        "author": "Author Two",
        "price": 2022.912,
        "is_published": True,
        "will_be_sold": datetime.datetime.now(),
    },
]


class Book(ObjectType):
    book_id = ID(required=True)
    readers = Int(required=True)
    name = String(required=True)
    description = String(required=True)
    author = String(required=True)
    price = Float(required=True)
    is_published = Boolean(required=True)
    will_be_sold = DateTime(required=True)


class BookInput(InputObjectType):
    book_id = ID(required=True)
    readers = Int(required=True)
    name = String(required=True)
    description = String(required=True)
    author = String(required=True)
    price = Float(required=True)
    is_published = Boolean(required=True)


class Query(ObjectType):
    status = String()
    get_book = Field(Book, id=Int(required=True))

    def resolve_status(self, info):
        return "API is UP!"

    def resolve_get_book(self, info, id):
        for book in books:
            if book["book_id"] == id:
                return book


class CreateBook(Mutation):
    book = Field(Book)

    class Arguments:
        data = BookInput(required=True)

    def mutate(self, info, data):
        print(data)
        book = {
            "book_id": len(books) + 1,
            "readers": data["readers"],
            "name": data["name"],
            "description": data["description"],
            "author": data["author"],
            "price": data["price"],
            "is_published": data["is_published"],
            "will_be_sold": datetime.datetime.now(),
        }
        books.append(book)
        return CreateBook(book=book)


class UpdateBook(Mutation):
    book = Field(Book)

    class Arguments:
        id = Int(required=True)
        data = BookInput(required=True)

    def mutate(self, info, id, data):
        book = {
            "book_id": len(books) + 1,
            "readers": data["readers"],
            "name": data["name"],
            "description": data["description"],
            "author": data["author"],
            "price": data["price"],
            "is_published": data["is_published"],
            "will_be_sold": datetime.datetime.now(),
        }
        for book in books:
            if book["book_id"] == id:
                data = book
                return UpdateBook(book=data)


class DeleteBook(Mutation):
    book = Field(Book)

    class Arguments:
        id = Int(required=True)

    def mutate(self, info, id):
        for book in books:
            if book["book_id"] == id:
                data = book
                books.remove(book)
                return DeleteBook(book=data)


class Mutations(ObjectType):
    createBook = CreateBook.Field()
    updateBook = UpdateBook.Field()
    deleteBook = DeleteBook.Field()


schema = Schema(query=Query, mutation=Mutations)


app = Flask(__name__)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(debug=True)

