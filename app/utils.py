from passlib.context import CryptContext    # for password hashing

# setting up hashing algo
pwd_context = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def hash(password: str):
    return pwd_context.hash(password)

# verify user's password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)