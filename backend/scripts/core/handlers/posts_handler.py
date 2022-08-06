from datetime import datetime
from scripts.db.mongo.raabta.collections.posts import Posts
from scripts.db.mongo import mongo_client
import random
import string

class PostsHandler:
    def __init__(self):
        self.posts = Posts(mongo_client=mongo_client)

    def find_posts(self, user_id: int):
        try:
            return self.posts.find_all_posts(user_id)
        except Exception as e:
            print(e.args)
            return None

    def find_one(self, id: str, user_id: int):
        try:
            return self.posts.find_post(id, user_id)
        except Exception as e:
            print(e.args)
            return None

    def create_one(self, data: dict, user_id: int):
        try:
            data["id"] = str(user_id) + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            data["user_id"] = user_id
            data["created_at"] = "{}".format(datetime.now())
            data["updated_at"] = "{}".format(datetime.now())
            data["likes"] = []
            self.posts.create_post(data=dict(data))
        except Exception as e:
            print(e.args)

    def update_one(self, user_id: int, id: str, data: dict):
        try:

            self.posts.update_post(user_id=user_id, id=id, data=dict(data))
        except Exception as e:
            print(e.args)

    def delete_one(self, id: str, user_id: int):
        try:
            ret = self.posts.delete_post(user_id=user_id, id=id)
            return ret
        except Exception as e:
            print(e.args)

    def get_all_the_posts(self):
        try:
            return self.posts.timeline_posts()
        except Exception as e:
            print(e.args)
            raise

    def post_like(self, post_id: str, user_id: int):
        try:
            post = self.posts.find(query={"id": post_id})
            for p in post:
                if p == None:
                    raise
                elif user_id not in p["likes"]:
                    self.posts.post_like(user_id=user_id, post_id=post_id)
                    return len(p["likes"]) + 1
                else:
                    self.posts.post_dislike(user_id=user_id, post_id=post_id)
                    return len(p["likes"]) - 1
                
            

        except Exception as e:
            print(e.args)
            raise
