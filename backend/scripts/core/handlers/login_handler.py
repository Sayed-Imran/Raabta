from pydantic import EmailStr
from scripts.db.mongo.raabta.collections.users import Users
from scripts.utils.security.jwt_util import JWT
from scripts.utils.security.hash import verifyPass
from scripts.db.mongo import mongo_client
class LoginHandler:

    def validate_user(self, cred: dict):
        try:
            users = Users(mongo_client)
            res = users.find_user_by_mail(cred["email"])
            if res:
                if cred["email"] == res['email'] and verifyPass(
                    cred["password"], res['password']
                ):

                    return (True,cred["email"],res['isAdmin'],res["user_id"])
                else:
                    return (False,None)
            else:
                return (False,None)

        except Exception as e:
            print(e.args)

    def create_jwt_token(self, cred: dict):
        try:
            return JWT().create_token(cred)
        except Exception as e:
            print(e.args)


    def check_new_user(self, email: EmailStr):
        try:
            users = Users(mongo_client)
            ret = users.find_user_by_mail(email=email)
            if ret == None:
                return False
            return True
        
        except Exception as e:
            print(e.args)
            raise
            