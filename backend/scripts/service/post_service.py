from fastapi import Depends, HTTPException
from fastapi import APIRouter, status
from scripts.core.handlers.posts_handler import PostsHandler
from scripts.schemas.posts_schema import PostsSchema
from scripts.constants.api_endpoints import APIEndpoints
from scripts.core.handlers.posts_handler import PostsHandler
from scripts.core.handlers.user_handler import UserHandler
from scripts.schemas.user_schemas import DefaultResponse
from scripts.utils.security.jwt_util import JWT

posts_router = APIRouter(prefix=APIEndpoints.posts)

jwt = JWT()


@posts_router.get(APIEndpoints.find_posts, status_code=status.HTTP_200_OK)
def find_posts(user=Depends(jwt.get_current_user)):
    try:
        posts_handler = PostsHandler()
        response = posts_handler.find_posts(user_id=user["user_id"])
        return DefaultResponse(
            status="Success", message="Found All posts Available", data=response
        )
    except Exception as e:
        print(e.args)
        return DefaultResponse(message="Error Occured")


@posts_router.get(APIEndpoints.find_post + "/{id}", status_code=status.HTTP_200_OK)
def get_post_by_id(id: str, user_data=Depends(jwt.get_current_user)):
    try:

        posts_handler = PostsHandler()
        response = posts_handler.find_one(id=id, user_id=user_data["user_id"])
        if response:
            return DefaultResponse(
                status="Success", message=f"Found Post with ID: {id}", data=response
            )
        else:
            return DefaultResponse(message=f"Couldn't find a post with ID {id}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)


@posts_router.post(
    APIEndpoints.create_post,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostsSchema, user_data=Depends(jwt.get_current_user)):
    try:
        posts_handler = PostsHandler()
        posts_handler.create_one(data=post.dict(), user_id=user_data["user_id"])
        return post
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args
        )


@posts_router.put(APIEndpoints.update_post + "/{id}", status_code=status.HTTP_200_OK)
def update_post(id: str, post: PostsSchema, user=Depends(jwt.get_current_user)):
    try:
        posts_handler = PostsHandler()
        posts_handler.update_one(user_id=user["user_id"], id=id, data=post.dict())
        return DefaultResponse(
            status="Success", message="Successfully updated post", data=post
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args
        )


@posts_router.delete(APIEndpoints.delete_post + "/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: str, user_data=Depends(jwt.get_current_user)):
    try:
        posts_handler = PostsHandler()
        ret = posts_handler.delete_one(id=id, user_id=user_data["user_id"])
        if ret != 0:
            
            return DefaultResponse(
                status="Success", message=f"Successfully deleted post with {id}"
            )
        else:
            return DefaultResponse(
                status="Failed", message="Failed to delete post"
            )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)


@posts_router.get(APIEndpoints.get_posts, status_code=status.HTTP_200_OK)
def get_posts(user=Depends(jwt.get_current_user)):
    try:
        user_handler = UserHandler()
        user_data = user_handler.find_one(user_id=user["user_id"])
        user_data["followings"].append(user["user_id"])
        posts_handler = PostsHandler()
        posts = posts_handler.get_all_the_posts(user_data["followings"])
        return posts
    except Exception as e:
        print(e.args)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@posts_router.get(APIEndpoints.like + "/{id}", status_code=status.HTTP_200_OK)
def post_like(id:str,user_data=Depends(jwt.get_current_user)):
    try:
        post_handler = PostsHandler()
        return post_handler.post_like(post_id=id, user_id=user_data["user_id"])
    except Exception as e:
        print(e.args)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
