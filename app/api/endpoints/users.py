# # 혹시 몰라 만들어둔 데베 -> 사용 안할 시 삭제 가능
# from fastapi import APIRouter, HTTPException
# from app.schemas.user import User, UserCreate
# from app.models.user import User as UserModel
# from app.database.session import SessionLocal
# from sqlalchemy.exc import IntegrityError

# router = APIRouter()

# @router.post("/", response_model=User)
# def create_user(user: UserCreate):
#     db = SessionLocal()
#     # 비밀번호 -> 나중에 해싱 적용
#     db_user = UserModel(username=user.username, email=user.email, hashed_password=user.password)
#     db.add(db_user)
#     try:
#         db.commit()
#         db.refresh(db_user)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="User already exists")
#     finally:
#         db.close()
#     return db_user

# @router.get("/{user_id}", response_model=User)
# def get_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(UserModel).filter(UserModel.id == user_id).first()
#     db.close()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
