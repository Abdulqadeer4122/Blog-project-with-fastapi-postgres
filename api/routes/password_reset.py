from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from ..models.user_model import User
from ..schemas import password_reset_schema
from ..Oath2 import create_access_token
from ..send_mail import send_reset_email
from ..Oath2 import get_current_user
from ..utils import get_password_hash
router = APIRouter(
    prefix='/password',
    tags=["Password reset"],
)


@router.post('/reset-password', response_description="User reset password", )
async def reset_password(user_email: password_reset_schema.Email, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email.email).first()
    if user:
        token = create_access_token({"id": user.id})
        reset_link = f"http://localhost:8000/reset?{token}"
        await send_reset_email(subject="Password Reset Email", email_to=user.email, body={
            'title': "Password reset email",
            'name': user.username,
            'reset_link': reset_link,

        })
        return {"status": status.HTTP_200_OK, "detail": "Check you email"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email not exist"
        )


@router.put('/reset', response_description="Password reset")
async def reset(token: str, new_password: password_reset_schema.Password, db: Session = Depends(get_db)):
    user = await get_current_user(token=token, db=db)
    if user:
        user.hashed_password = get_password_hash(password=new_password.password)
        db.add(user)
        db.commit()
        return {"msg": "Password reset successful"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

