from exception.enter import (
    UserNotFound,
    IncorrectPassword,
    InvalidUsername,
    InvalidPassword,
    UserAlreadyExist,
    AdminNotFound,
    UserAlreadyLoggedin,
    InvalidLogin,
)
from auth.user_auth import UserAuth
from auth.admin_auth import AdminAuth
from auth.audit_auth import logger
import re


def PASSWORD(password):
    return re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}", password)


def USERNAME(username):
    return re.match(r"^[a-zA-Z0-9]+$", username)


admin_auth_agent = AdminAuth()


class ParserService:
    def __init__(self):
        self.user_auth = UserAuth()
        self.main = MainService()

    def login(self, username, password):
        entered = self.user_auth._username(username)
        try:
            if entered:
                raise UserAlreadyLoggedin()

            enter = self.main.login(username, password)

            if enter:
                self.user_auth.enter_flag(username, password)
                return True

        except UserAlreadyLoggedin:
            print("User Already Logged In")
            
    def register(self, username, password, name):
        register = self.main.register(username, password, name)
        if register:
            self.user_auth.enter_flag(username, password)
            return True
            

    def user(self, username):
        entered = self.user_auth._username(username)
        try:
            if not entered:
                raise InvalidLogin()

            password = entered[0][1]

            enter = self.main.login(username, password)

            return enter

        except InvalidLogin:
            print("Did not Login Before")


class MainService:
    def __init__(self):
        self.auth = UserAuth()
        

    def login(self, username, password):

        user = self.auth.login(username)

        try:
            if not user:
                raise UserNotFound()
            if user[0][2] != password:
                raise IncorrectPassword()

        except UserNotFound:
            print(f"User Not Found For {username}")
        except IncorrectPassword:
            print("Incorrect Password")
        else:
            user = user[0]

            user_id = user[0]
            name = user[3]

            logger.info(f"User {username} Signed In")

            return (user_id, username, password, name)


    def register(self, username, password, name=None):

        try:

            if not USERNAME(username):
                raise InvalidUsername()
            elif not bool(PASSWORD(password)):
                raise InvalidPassword()

            user = self.auth.login(username)
            if user:
                raise UserAlreadyExist(f"User {username} Is Already Exist")

        except UserAlreadyExist:
            print(f"User {username} Already Exist")
        except InvalidUsername:
            print("Username Can Only Contain lowercase and uppercase letters and numbers")
        except InvalidPassword:
            print(
                "The password must be 8 or more characters; Must contain at least one lowercase letter, one uppercase letter and one number"
            )
        else:
            self.auth.register(username, password, name)
            user_id = self.auth.get_user_id(username)[0][0]

            logger.info(f"User {username} Registered")

            return (user_id, username, password, name)


    def login_admin(self, username, password):
        try:
            admin = admin_auth_agent.login(username)

            if not admin:
                raise AdminNotFound()

            if password != admin[0][1]:
                raise IncorrectPassword()

        except AdminNotFound:
            print("Admin does not exist")
        except IncorrectPassword:
            print("Incorrect password")

        else:
            logger.info(f"Admin {username} Logged in")

            return True

def validate_password(value):
    if bool(PASSWORD(value)):
        return value

    raise InvalidPassword()