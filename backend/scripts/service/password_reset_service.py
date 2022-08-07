from fastapi import APIRouter, status, HTTPException, Depends, BackgroundTasks
from scripts.constants.secrets import Secrets
from scripts.db.mongo.raabta.collections.users import Users
from scripts.schemas.password_reset_schema import PasswordScheme
from scripts.core.handlers.user_handler import UserHandler
from scripts.utils.security.hash import hashPassword
from scripts.utils.security.jwt_util import JWT
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jose import jwt


conf = ConnectionConfig(
    MAIL_USERNAME="Raabta Sabse",
    MAIL_PASSWORD="strong_password",
    MAIL_FROM="raabtasabse@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="mail.google.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER="scripts/utils/templates/",
)


def send_email_background(
    background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict
):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html",
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message, template_name="email.html")


passwd_reset = APIRouter()
# external_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')


@passwd_reset.post("/forgotpasswd", status_code=status.HTTP_202_ACCEPTED)
def passwordReset(
    background_tasks: BackgroundTasks, data: dict):
    try:
        user = Users()
        ret = user.find_user_by_mail(data["email"])
        if not ret:
            raise
        link = "http://localhost/newpasswd/" + JWT().create_token(
            {"id": ret["user_id"], "email": ret["email"]}
        )
        send_email_background(
            background_tasks,
            "Password Reset",
            data["email"],
            {
                "title": "Password Reset",
                "name": "Link to reset your password",
                "link": link,
            },
        )
        return "Success"
        # return {"access_token":JWT().create_token({"id": ret[0], "email": ret[2]})}

    except Exception as e:
        print(e.args)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with the mail: {data['email']}",
        )


@passwd_reset.post("/newpasswd" + "/{token}", status_code=status.HTTP_202_ACCEPTED)
def newpassword(token: str, data: PasswordScheme):
    try:
        if data.new_passwd != data.conf_passwd:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        passwd = hashPassword(data.conf_passwd)
        payload = jwt.decode(token, Secrets.UNIQUE_KEY, algorithms=[Secrets.ALG])
        email = payload.get("email")
        user_handler = UserHandler()
        user_handler.update_password(email=email, password=passwd)
        return {"new_passwd": passwd}

    except Exception as e:
        print(e.args)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
