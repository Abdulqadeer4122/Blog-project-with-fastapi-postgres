from fastapi import APIRouter, status,HTTPException, Depends
from sqlalchemy.orm import Session
from ..schemas import users_schema
from .. import database
from ..models.user_model import User
from ..helpers import crud
from ..send_mail import send_registration_email

router = APIRouter(
    tags=["Users Routes"]
)


@router.post('/register-user/', response_description="User Registration", response_model=users_schema.UserResponse)
async def registration(user_info: users_schema.User, db: Session = Depends(database.get_db)):
    user_name_exist = db.query(User).filter(User.username == user_info.username).first()
    if user_name_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This name is already taken")
    email_exist = db.query(User).filter(User.email == user_info.email).first()
    if email_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already used")


    await send_registration_email(subject="Registration Successfully", email_to=user_info.email, body={
        'title': "Registration successfully completed",
        'name': user_info.username,

    })
    return crud.create_user(db=db, user=user_info)
