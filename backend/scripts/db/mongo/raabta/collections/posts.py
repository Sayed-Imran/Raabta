from datetime import datetime
from typing import Optional
from scripts.constants import DatabasesNames, CollectionNames
from scripts.db.mongo.schema import MongoBaseSchema
from scripts.utils.mongo_util import MongoCollectionBaseClass


class PostsSchema(MongoBaseSchema):
    user_id: str
    post_title: str
    desc: Optional[str] = ""
    img: Optional[str] = ""
    likes: Optional[list] = []
    created_at: datetime
    updated_at: datetime


class Posts(MongoCollectionBaseClass):
    def __init__(self, mongo_client):
        super().__init__(
            mongo_client=mongo_client,
            database=DatabasesNames.raabta,
            collection=CollectionNames.posts,
        )

    def find_all_posts(self, user_id: int):
        posts = self.find(query={"user_id": user_id})
        if posts:
            return list(posts)

    def find_post(self, id, user_id: int):
        post = self.find_one(query={"user_id": user_id, "id": id})
        if post:
            return post

    def create_post(self, data: dict):
        self.insert_one(data=data)

    def update_post(self, user_id: int, id: str, data: dict):
        self.update_one(query={"id": id, "user_id": user_id}, data=data, upsert=True)

    def delete_post(self, user_id: int, id: str):
        ret = self.delete_one(query={"user_id": user_id, "id": id})
        return ret


    def post_like(self, user_id: int, post_id: str):
        self.update_push_array(
            query={"id": post_id}, array_key="likes", data=user_id
        )

    def post_dislike(self, user_id: int, post_id: str):
        self.update_pull_array(
            query={"id": post_id}, array_key="likes", data=user_id
        )

    def timeline_posts(self,query):
        posts = self.find(query=query)
        return posts