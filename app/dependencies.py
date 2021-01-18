from pyject import BaseContainer

from app.modules.auth.use_cases.interfaces import IJwtService, IPasswordHashService
from app.modules.auth.use_cases.jwt_service import JwtService
from app.modules.auth.use_cases.passwordhash_service import PasswordHashService
from app.modules.cards.use_cases.interfaces import ICardRepository, ICardService
from app.modules.cards.repositories.card_repository import CardRepository
from app.modules.cards.use_cases.card_service import CardService
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.users.use_cases.interfaces import IUserRepository, IUserService
from app.modules.users.use_cases.user_service import UserService


def configure_dependencies(container: BaseContainer) -> None:
    container.add_singleton(ICardRepository, CardRepository)
    container.add_singleton(ICardService, CardService)

    container.add_singleton(IUserRepository, UserRepository)
    container.add_singleton(IUserService, UserService)

    container.add_singleton(IJwtService, JwtService)
    container.add_singleton(IPasswordHashService, PasswordHashService)
