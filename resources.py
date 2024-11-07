from flask_restful import Resource, reqparse, fields, marshal_with, abort
from models import UserModel, db

# Definisi field untuk marshal
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
}

# Parser untuk mengambil data dari request
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")

# Resource untuk menampilkan semua user dan menambah user baru
class Users(Resource):
    @marshal_with(user_fields)
    def get(self, page=1):
        per_page = 5
        # Memperbaiki penggunaan paginate untuk menghindari error
        users = UserModel.query.paginate(page=page, per_page=per_page, error_out=False).items
        return users


    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        if UserModel.query.filter_by(email=args['email']).first() or UserModel.query.filter_by(name=args['name']).first():
            abort(400, message="User with this name or email already exists")
        
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        return user, 201

# Resource untuk operasi CRUD berdasarkan ID
class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(user_fields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        
        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    @marshal_with(user_fields)
    def delete(self, id):
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}

# Resource untuk mencari user berdasarkan nama
class UserByName(Resource):
    @marshal_with(user_fields)
    def get(self, name):
        user = UserModel.query.filter_by(name=name).first()
        if not user:
            abort(404, message="User not found")
        return user
