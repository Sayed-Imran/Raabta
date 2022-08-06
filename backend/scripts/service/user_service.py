from dataclasses import dataclass
from fastapi import Depends, HTTPException
from fastapi import APIRouter, status
from scripts.constants.api_endpoints import APIEndpoints
from scripts.core.handlers.user_handler import UserHandler
from scripts.schemas.user_schemas import DefaultResponse, UserRequestSchema, ResponseModel, UpdateUserData, GetUserResponse
from scripts.utils.security.jwt_util import JWT

users_router = APIRouter(prefix=APIEndpoints.users)


@users_router.get(APIEndpoints.find_users, status_code=status.HTTP_200_OK)
def find_users(user_id: str = Depends(JWT().get_admin_user)):
    try:
        
        user_handler = UserHandler()
        response = user_handler.find_users()
        return DefaultResponse(
            status="Success", message="Found All users Available", data=response
        )
    except Exception as e:
        print(e.args)
        return DefaultResponse(message="Error Occured")


@users_router.get(APIEndpoints.find_user, status_code=status.HTTP_200_OK, response_model=GetUserResponse)
def get_user_by_id(user = Depends(JWT().get_current_user)):
    try:

        user_handler = UserHandler()
        response = user_handler.find_one(user_id=user["user_id"])
        if response:
            return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)


@users_router.post(APIEndpoints.add_user, status_code=status.HTTP_201_CREATED,response_model=ResponseModel)
def create_user(user: UserRequestSchema,user_id: str = Depends(JWT().get_admin_user)):
    try:
        user_handler = UserHandler()
        user_handler.create_one(data=user.dict())
        return user
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args
        )


@users_router.put(APIEndpoints.update_user, status_code=status.HTTP_200_OK)
def update_user(data: UpdateUserData,user = Depends(JWT().get_current_user)):
    try:
        print(user)
        user_handler = UserHandler()
        user_handler.update_one(user_id=user["user_id"], data=data.dict())
        return DefaultResponse(
            status="Success", message="Successfully updated user", data=data.dict()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.args
        )


@users_router.delete(APIEndpoints.remove_user + "/{id}", status_code=status.HTTP_200_OK)
def delete_user(id, admin: str = Depends(JWT().get_admin_user)):
    try:
        user_handler = UserHandler()
        user_handler.delete_one(user_id=id)
        return DefaultResponse(
            status="Success", message=f"Successfully deleted user with {id}"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args)

@users_router.put(APIEndpoints.follow+"/{id}",status_code=status.HTTP_200_OK)
def follow(id:str, user = Depends(JWT().get_current_user)):
    try:
        user_handler = UserHandler()
        if id == user["user_id"]:
            raise
        ret = user_handler.follow(user["user_id"],id)
        if ret:
            
            return DefaultResponse(
                status="Success", message=f"User {id} followed"
            )
        else:
            return DefaultResponse(
                status="Failed", message=f"You are already following this user {id}"
            )
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="You cannot follow yourself"
        )

@users_router.put(APIEndpoints.unfollow+"/{id}",status_code=status.HTTP_200_OK)
def unfollow(id:str,user=Depends(JWT().get_current_user)):
    try:
        user_handler = UserHandler()
        if id == user["user_id"]:
            raise
        user_handler.unfollow(user["user_id"],id)
        return DefaultResponse(
            status="Success", message=f"User {id} unfollowed"
        )
    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="You cannot unfollow yourself")