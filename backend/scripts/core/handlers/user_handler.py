from scripts.db.mongo.raabta.collections.users import Users
from scripts.db.mongo import mongo_client
from scripts.utils.security.hash import hashPassword
import string
import random

class UserHandler:
    def __init__(self):
        self.users = Users(mongo_client=mongo_client)

    def find_users(self):
        try:
            return self.users.find_all_users()
        except Exception as e:
            print(e.args)
            return None

    def find_one(self, user_id: str):
        try:
            return self.users.find_user(user_id)
        except Exception as e:
            print(e.args)
            return None

    def create_one(self, data: dict):
        try:
            data["password"] = hashPassword(data["password"])
            data["user_id"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            self.users.create_user(data=dict(data))
            return True
        except Exception as e:
            print(e.args)
            return False

    def update_one(self, user_id: str, data: dict):
        try:
            self.users.update_user(user_id=user_id, data=dict(data))
        except Exception as e:
            print(e.args)

    def delete_one(self, user_id: str):
        try:
            self.users.delete_user(user_id=user_id)
        except Exception as e:
            print(e.args)

    def follow(self,user_id:str,follow_user_id:str):
        try:
            user = self.users.find_one(query={"user_id":user_id})
            if follow_user_id not in user["followings"]:
                self.users.follow_user(user_id,follow_user_id)
                return True
            else:
                return False
        except Exception as e:
            print(e.args)

    def unfollow(self,user_id:str,follow_user_id:str):
        try:
            self.users.unfollow_user(user_id,follow_user_id)
        except Exception as e:
            print(e.args)
