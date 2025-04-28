# # 혹시 몰라 만들어둔 데베 -> 사용 안할 시 삭제 가능
# from pydantic import BaseModel, EmailStr

# class UserBase(BaseModel):
#     username: str
#     email: EmailStr

# class UserCreate(UserBase):
#     password: str

# class User(UserBase):
#     id: int

#     class Config:
#         orm_mode = True
