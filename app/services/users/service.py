import structlog

from app.database import Database, SQLAlchemyService
from app.services.users.model import UserModel
from app.services.users.repo import UserRepository
from app.services.users.schemas import User, UserCreate, UserUpdate

logger = structlog.get_logger(__name__)


class UserService(SQLAlchemyService[UserModel, UserCreate, UserUpdate, User]):
    def __init__(self, db: Database):
        repo = UserRepository(db)
        super().__init__(repo, User)

    async def startup(self):
        logger.info("User service started")

    async def shutdown(self):
        logger.info("User service stopped")
