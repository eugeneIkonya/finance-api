from marshmallow import Schema, fields

user = {
    "id" : 1,
    "email" : "eugeneikonya@gmail",
    "username" : "eugeneIkonya",
    "password_hash" : "password",
    "is_admin" : True,
    "is_verified" : True,
    "created_at" : "some date",
    "updated_at" : "some date"
 }
class CreateUserSchema(Schema):
    email = fields.Email()
    username = fields.String()
    password = fields.String()

class UpdateUsernameSchema(Schema):
    username = fields.String()

class UpdateEmailSchema(Schema):
    email = fields.Email()

class UpdatePasswordSchema(Schema):
    password = fields.String()

class UpdateAdminSchema(Schema):
    is_admin = fields.Boolean()

class UserSchema(Schema):
    id = fields.Integer()
    email = fields.Email()
    username = fields.String()
    password = fields.String()
    is_verified = fields.Boolean()
    is_admin = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class LoginUserSchema(Schema):
    email = fields.Email()
    password = fields.String()



