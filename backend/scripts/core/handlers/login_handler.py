from pydantic import EmailStr
from scripts.db.postgres.users import Users
from scripts.utils.security.jwt_util import JWT
from scripts.utils.security.hash import verifyPass

class LoginHandler:

    def validate_user(self, cred: dict,db):
        try:
            users = Users(db)
            res = users.read_one_by_email(cred["email"])
            if res:
                if cred["email"] == res[2] and verifyPass(
                    cred["password"], res[3]
                ):

                    return (True,res[5],res[0])
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


    def check_new_user(self, email: EmailStr, db):
        try:
            users = Users(db)
            ret = users.read_one_by_email(email=email)
            if ret:
                return False
            return True
        
        except Exception as e:
            print(e.args)
            raise
            