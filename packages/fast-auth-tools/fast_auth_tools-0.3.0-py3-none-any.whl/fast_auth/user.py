import asyncio
import os
import uuid

from getpass import getpass
from typing import Optional

import aiosqlite
from fastapi import Depends
from pydantic import BaseModel, constr

from fast_auth.logger import logger
from .constants import oauth2_scheme
from .exceptions import (
    DatabaseError,
    FastAuthException,
    InvalidPassword,
    CredentialsException,
    UserNotFound,
)
from .funcs import replace, get_data_from_token, insert
from .funcs import get_password_hash as _hash
from .funcs import verify_password as _verify
from .settings import settings


class User(BaseModel):
    __table__ = "users"
    username: str
    password: str
    id: uuid.UUID

    def check_password(self, password):
        return _verify(password, self.password)

    @staticmethod
    def hash_password(password):
        return _hash(password)

    @classmethod
    def create_table_query(cls):
        return f"""
        CREATE TABLE IF NOT EXISTS {cls.__table__} (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
            id TEXT NOT NULL
        );
        """

    @classmethod
    async def create_table(cls) -> bool:
        # Check if the table already exists
        logger.debug(f"Using file {settings.user_db_path}")
        async with aiosqlite.connect(settings.user_db_path) as db:
            async with db.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                (cls.__table__,),
            ) as cursor:
                if await cursor.fetchone():
                    return False  # Table already exists

        async with aiosqlite.connect(settings.user_db_path) as db:
            await db.execute(cls.create_table_query())
            await db.commit()

        return True  # Table was created

    @classmethod
    async def get(
        cls, *, username: Optional[str] = None, user_id: Optional[uuid.UUID] = None
    ):
        if username is None and user_id is None:
            raise ValueError("Either `username` or `user_id` must be provided")

        if user_id is not None:
            query = f"SELECT * FROM users WHERE id = ?;"
            value = (user_id.hex,)
        else:
            query = f"SELECT * FROM users WHERE username = ?;"
            value = (username,)

        async with aiosqlite.connect(settings.user_db_path) as db:
            async with db.execute(query, value) as cursor:
                from_db = await cursor.fetchone()
                if from_db is None:
                    return None
                return cls(username=from_db[0], password=from_db[1], id=from_db[2])

    async def save(self):
        if len(self.password) != 60:
            self.password = self.hash_password(self.password)
        await replace(
            self.__table__, {"username": self.username, "password": self.password}
        )

    @staticmethod
    def sanitise_username(username: str):
        """
        Sanitise the username by taking only the first word and converting to lowercase

        :param username: str - the username to sanitise
        :return: str - the sanitised username
        """
        return username.split(" ")[0].lower()

    @classmethod
    async def create(cls, username: str, password: constr(max_length=59)):
        password = cls.hash_password(password)
        username = cls.sanitise_username(username)
        user_id = uuid.uuid4()
        try:
            await insert(
                cls.__table__,
                {"username": username, "password": password, "id": user_id.hex},
            )
        except aiosqlite.IntegrityError as e:
            raise DatabaseError(f"Could not create user `{username}`; {e}")

        return cls(username=username, password=password, id=user_id)

    async def update_password(self, old_password, password: constr(max_length=59)):
        if not self.check_password(old_password):
            raise InvalidPassword
        self.password = self.hash_password(password)
        await self.save()

    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> Optional["User"]:
        user = await cls.get(username=username)
        if user is None:
            raise UserNotFound
        try:
            if not _verify(password, user.password):
                raise InvalidPassword
            return user
        except Exception:
            raise CredentialsException


async def logged_in_user(token: str = Depends(oauth2_scheme)):
    data = await get_data_from_token(token)
    user = await User.get(user_id=data.user_id)
    if user is None:
        raise UserNotFound
    return user


async def run():
    if os.path.dirname(str(settings.user_db_path)) == os.path.dirname(__file__):
        logger.warning(
            "User database will be created in the site_packages directory! Specify a `user_db_path`  in the config file "
            "specified by the SETTINGS_PATH environment variable (yaml), or otherwise set the `settings.user_db_path` "
            "variable."
        )

    created = await User.create_table()
    if created:
        print(f"`{User.__table__}` table created!")

    suggestion = "[Y/n]"
    check = {"y", "yes", ""}
    article = "a"

    while input(f"Create {article} user? {suggestion}: ").strip().lower() in check:
        username = input("Username: ")
        password = getpass("Password: ")
        password_confirm = getpass("Confirm password: ")
        if password != password_confirm:
            print("Passwords do not match!")
            continue
        try:
            await User.create(username, password)
        except FastAuthException as e:
            print(f"Error creating user: {e}")
            continue
        print(f"User `{username}` created!")

        suggestion = "[y/N]"
        check = {"y", "yes"}
        article = "another"


def main():
    try:
        asyncio.run(run())
        print("Done!")
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")


async def migrate():
    async with aiosqlite.connect(settings.user_db_path) as db:
        # Add the new column with a default value
        await db.execute(
            "ALTER TABLE users ADD COLUMN id TEXT NOT NULL DEFAULT 'temp_id';"
        )

        # Update existing rows with a new UUID
        async with db.execute("SELECT username FROM users;") as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                username = row[0]
                user_id = uuid.uuid4().hex
                await db.execute(
                    "UPDATE users SET id = ? WHERE username = ?;", (user_id, username)
                )

        # Remove the default value constraint
        await db.execute("PRAGMA writable_schema = 1;")
        await db.execute(
            "UPDATE sqlite_master SET sql = REPLACE(sql, 'DEFAULT ''temp_id''', '') WHERE type = 'table' AND name = 'users';"
        )
        await db.execute("PRAGMA writable_schema = 0;")

        # Commit the changes
        await db.commit()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        asyncio.run(migrate())
    else:
        main()
