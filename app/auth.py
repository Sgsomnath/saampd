from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from passlib.context import CryptContext

# Load environment variables from .env file
load_dotenv()

# Configuration for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    :param password: Plain text password.
    :return: Hashed password.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    :param plain_password: Plain text password.
    :param hashed_password: Hashed password.
    :return: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

hashed_password = get_password_hash("my_secure_password")
print(hashed_password)  # Outputs a bcrypt hash

is_valid = verify_password("my_secure_password", hashed_password)
print(is_valid)  # Outputs True if the password matches

def create_access_token(data: dict):
    """
    Create a JWT access token.
    :param data: Dictionary containing the payload (e.g., {"sub": email}).
    :return: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    """
    Verify and decode a JWT access token.
    :param token: The JWT token to verify.
    :return: Decoded payload as a dictionary.
    :raises HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
