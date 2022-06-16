from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car.db'

app.config['SQLALCHEMY_BINDS'] = {
    'blog': 'sqlite:///blog.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100))
    price = db.Column(db.Integer)
    color = db.Column(db.String(50))

    def __init__(self, name, company, price, color):
        self.name = name
        self.company = company
        self.price = price
        self.color = color


class Blogs(db.Model):
    __bind_key__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    blog_name = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    body = db.Column(db.String(100))

    def __init__(self, blog_name, author, subject, body):
        self.blog_name = blog_name
        self.author = author
        self.subject = subject
        self.body = body


class CarsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'company', 'price', 'color')


class BlogsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'blog_name', 'author', 'subject', 'body')


# db.create_all()

car_schema = CarsSchema()
cars_schema = CarsSchema(many=True)

blog_schema = BlogsSchema()
blogs_schema = BlogsSchema(many=True)


# CARS DECORATORS

# CREATE A NEW CAR
@app.route('/cars/register', methods=['POST'])
def create_car():
    data = request.get_json()
    name = data['name']
    company = data['company']
    price = data['price']
    color = data['color']
    new_car = Cars(name, company, price, color)

    db.session.add(new_car)
    db.session.commit()
    result = car_schema.jsonify(new_car)

    return result


# GET A SINGLE CAR
@app.route('/cars/<id>', methods=['GET'])
def get_car(id):
    one_car = Cars.query.get(id)
    result = car_schema.dump(one_car)

    return jsonify(result)


# GET EVERY CAR ON THE DATABASE
@app.route('/cars', methods=['GET'])
def get_cars():
    all_cars = Cars.query.all()
    result = cars_schema.dump(all_cars)

    return jsonify(result)


# UPDATE A SINGLE CAR
@app.route('/cars/<id>', methods=['PUT'])
def update_car(id):
    car = Cars.query.get(id)
    data = request.get_json()
    name = data['name']
    company = data['company']
    price = data['price']
    color = data['color']

    car.name = name
    car.company = company
    car.price = price
    car.color = color

    db.session.commit()
    result = car_schema.jsonify(car)
    return result


# DELETE A SINGLE CAR
@app.route('/cars/<id>', methods=['DELETE'])
def delete_car(id):
    car = Cars.query.get(id)
    db.session.delete(car)
    db.session.commit()

    result = car_schema.jsonify(car)
    return result


# BLOGS DECORATORS

# CREATE A NEW BLOG
@app.route('/blog/register', methods=['POST'])
def create_blog():
    data = request.get_json()
    blog_name = data['blog_name']
    author = data['author']
    subject = data['subject']
    body = data['body']
    new_blog = Blogs(blog_name, author, subject, body)

    db.session.add(new_blog)
    db.session.commit()
    result = blog_schema.jsonify(new_blog)

    return result


# GET A SINGLE BLOG
@app.route('/blog/<id>', methods=['GET'])
def get_blog(id):
    one_blog = Blogs.query.get(id)
    result = blog_schema.dump(one_blog)

    return jsonify(result)


# GET EVERY BLOG ON THE DATABASE
@app.route('/blog', methods=['GET'])
def get_blogs():
    all_blogs = Blogs.query.all()
    result = blogs_schema.dump(all_blogs)

    return jsonify(result)


# UPDATE A SINGLE BLOG
@app.route('/blog/<id>', methods=['PUT'])
def update_blog(id):
    blog = Blogs.query.get(id)
    data = request.get_json()
    blog_name = data['blog_name']
    author = data['author']
    subject = data['subject']
    body = data['body']

    blog.blog_name = blog_name
    blog.author = author
    blog.subject = subject
    blog.body = body

    db.session.commit()
    result = blog_schema.jsonify(blog)
    return result


# DELETE A SINGLE BLOG
@app.route('/blog/<id>', methods=['DELETE'])
def delete_blog(id):
    blog = Blogs.query.get(id)
    db.session.delete(blog)
    db.session.commit()

    result = blog_schema.jsonify(blog)
    return result


if __name__ == "__main__":
    app.run(debug=True)
