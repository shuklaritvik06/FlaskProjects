from ariadne import QueryType, MutationType, make_executable_schema, gql
from ..models.model import db, Orders, Customers

query = QueryType()

mutation = MutationType()

types = gql("""
    type Query {
        orders: [Order]
        customers: [Customer]
    }
    type Order {
        id: Int!
        amount: Int!
        delivery_address: String!
        delivery_date: Int!
        customer_id: Int!
    }
    type Customer {
        id: Int!
        name: String!
        age: Int!
        address: String!
        orders: [Order]
    }
    type Mutation{
        add_order(amount: Int!, delivery_address: String!, delivery_date: Int!, customer_id: Int!): Order
        add_customer(name: String!, address: String!, age: Int!): Customer
        delete_order(id: Int!): Order
        update_order(id: Int!, amount: Int, address: String, delivery_date: Int, customer_id: Int): Order
        }
    """)


def prettify(data, name):
    list_res = []
    dict_res = {}
    for i in data:
        if name == "customer":
            dict_res["name"] = i.name
            dict_res["id"] = i.id
            dict_res["age"] = i.age
            dict_res["address"] = i.address
            dict_res["orders"] = i.orders
        else:
            dict_res["amount"] = i.amount
            dict_res["id"] = i.id
            dict_res["delivery_address"] = i.delivery_address
            dict_res["delivery_date"] = i.delivery_date
            dict_res["customer_id"] = i.customer_id
        list_res.append(dict_res)
        dict_res = {}
    return list_res


@query.field("customers")
def customers(*_):
    customer_data = prettify(db.session.execute(db.select(Customers)).scalars(), "customer")
    return customer_data


@query.field("orders")
def orders(*_):
    order_data = prettify(db.session.execute(db.select(Orders)).scalars(), "order")
    return order_data


@mutation.field("add_order")
def add_order(_, info, amount, delivery_address, delivery_date, customer_id):
    customer = db.get_or_404(Customers, customer_id)
    order = Orders(
        amount=amount,
        delivery_address=delivery_address,
        delivery_date=delivery_date,
        customer=customer
    )
    db.session.add(order)
    db.session.commit()
    return {"id": order.id, "amount": amount, "address": delivery_address, "delivery_date": delivery_date,
            "customer_id": customer_id}


@mutation.field("add_customer")
def add_customer(_, info, name, address, age):
    customer = Customers(
        name=name,
        address=address,
        age=age
    )
    db.session.add(customer)
    db.session.commit()
    return {"id": customer.id, "name": name, "address": address, "age": age}


@mutation.field("update_order")
def update_order(_, info, id, **kwargs):
    order = db.get_or_404(Orders, id)
    for key, val in kwargs.items():
        if key == "amount":
            order.amount = val
        if key == "delivery_address":
            order.delivery_address = val
        if key == "delivery_date":
            order.delivery_date = val
        if key == "customer_id":
            order.customer_id = val
    db.session.commit()
    return {"id": order.id, "amount": order.amount, "delivery_address": order.delivery_address, "delivery_date": order.delivery_date,
            "customer_id": order.customer_id}


@mutation.field("delete_order")
def delete_order(_, info, id):
    order = db.get_or_404(Orders, id)
    db.session.delete(order)
    db.session.commit()
    return {"id": order.id, "amount": order.amount, "address": order.delivery_address,
            "delivery_date": order.delivery_date,
            "customer_id": order.customer_id}


schema = make_executable_schema(types, [query, mutation])
