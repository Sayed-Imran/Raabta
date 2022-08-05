from typing import Optional
from pydantic import EmailStr
from scripts.constants import DatabasesNames, CollectionNames
from scripts.db.mongo.schema import MongoBaseSchema
from scripts.utils.mongo_util import MongoCollectionBaseClass


class UsersSchema(MongoBaseSchema):
    name: str
    email: EmailStr
    password: str
    profilePicture: Optional[str] = ""
    followers: Optional[list] = []
    following: Optional[list] = []


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

    def find_user(self, eid):
        user = self.find_one(query={"eid": eid})
        if user:
            return user
    
    def find_user_by_mail(self,email):
        user = self.find_one(query={"email":email})
        if user:
            return user

    def create_user(self, data: dict):
        self.insert_one(data=data)

    def update_user(self, eid: str, data: dict):
        self.update_one(query={"eid": eid}, data=data, upsert=True)

    def delete_user(self, eid: str):
        self.delete_one(query={"eid": eid})
