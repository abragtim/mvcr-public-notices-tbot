import json
from dataclasses import dataclass, asdict
from typing import Set, Optional


@dataclass(frozen=True)
class User:
    id: int
    application_number: str


class UsersStorage:
    __PATH_TO_USERS_JSON = 'data/storage/users.json'

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        actual_users = UsersStorage.get_all()
        return UsersStorage._get_from_list_by_id(user_id, actual_users)

    @staticmethod
    def update(user: User):
        actual_users = UsersStorage.get_all()
        existing = UsersStorage._get_from_list_by_id(user.id, actual_users)
        if existing is not None:
            actual_users.remove(existing)
        actual_users.add(user)
        UsersStorage._update_json(actual_users)

    @staticmethod
    def remove(user: User):
        actual_users = UsersStorage.get_all()
        existing = UsersStorage._get_from_list_by_id(user.id, actual_users)
        if existing is None:
            raise KeyError(f'User {user.id} does not exist.')
        actual_users.remove(existing)
        UsersStorage._update_json(actual_users)

    @staticmethod
    def get_all() -> Set[User]:
        with open(UsersStorage.__PATH_TO_USERS_JSON, 'r') as fd:
            return {User(**user) for user in json.load(fd)}

    @staticmethod
    def _update_json(users: Set[User]):
        users_dict = map(asdict, users)
        with open(UsersStorage.__PATH_TO_USERS_JSON, 'w') as fd:
            json.dump(list(users_dict), fd)

    @staticmethod
    def _get_from_list_by_id(user_id: int, users: Set[User]) -> Optional[User]:
        user = next((user for user in users if user.id == user_id), None)
        return user
