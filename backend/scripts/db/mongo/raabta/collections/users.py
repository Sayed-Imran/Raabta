from typing import Optional
from pydantic import EmailStr
from scripts.constants import DatabasesNames, CollectionNames
from scripts.db.mongo.schema import MongoBaseSchema
from scripts.utils.mongo_util import MongoCollectionBaseClass


class UsersSchema(MongoBaseSchema):
    username: str
    email: EmailStr
    password: str
    profilePicture: Optional[str] = ""
    coverPicture: Optional[str] = ""
    followers: Optional[list] = []
    followings: Optional[list] = []


class Users(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(
            mongo_client=mongo_client,
            database=DatabasesNames.raabta,
            collection=CollectionNames.users,
        )

    def find_all_users(self):
        users = self.find(query={})
        if users:
            return list(users)

    def find_user(self, user_id):
        user = self.find_one(query={"user_id": user_id})
        if user:
            return user
    
    def find_user_by_mail(self,email):
        user = self.find_one(query={"email":email})
        return user

    def create_user(self, data: dict):
        self.insert_one(data=data)

    def update_user(self, user_id: str, data: dict):
        ret = self.update_one(query={"user_id": user_id}, data=data, upsert=True)

    def delete_user(self, user_id: str):
        self.delete_one(query={"user_id": user_id})

    def follow_user(self,user_id:str,follow_user_id:str):
        self.update_push_array(query={"user_id":user_id},data=follow_user_id,array_key="followings")
        self.update_push_array(query={"user_id":follow_user_id},data=user_id,array_key="followers")

    def unfollow_user(self,user_id:str,follow_user_id:str):
        self.update_pull_array(query={"user_id":user_id},data=follow_user_id,array_key="followings")
        self.update_pull_array(query={"user_id":follow_user_id},data=user_id,array_key="followers")
        