from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.user_schema import UserRegister

from app.utils.hashing import hash_password
from app.utils.hashing import verify_password


def create_user(
    db: Session,
    user: UserRegister
):

    hashed_pwd = hash_password(user.password)

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_pwd,
        role=user.role
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user