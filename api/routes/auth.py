from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from ..models.user_model import User
from ..utils import verify_password
from ..Oath2 import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["Authentication"],
)


@router.post('', status_code=status.HTTP_201_CREATED)
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=request.username).first()
    if user and verify_password(request.password, user.hashed_password):
        access_token = create_access_token(data={"id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
