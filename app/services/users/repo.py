from app.database import Database, SQLAlchemyRepository
from app.services.users.model import UserModel
from app.services.users.schemas import UserCreate, UserUpdate


class UserRepository(SQLAlchemyRepository[UserModel, UserCreate, UserUpdate]):
    def __init__(self, db: Database):
        super().__init__(UserModel, db)
