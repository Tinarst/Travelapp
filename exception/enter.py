class AdminNotFound(Exception): ...


class EmptyUsername(Exception):
    def __init__(self):
        self.message = "Username Cannot be empty"
        super().__init__(self.message)


class EmptyPassword(Exception):
    def __init__(self):
        self.message = "Password cannot be Empty"
        super().__init__(self.message)


class UserNotFound(Exception): ...


class UserAlreadyExist(Exception): ...


class UserAlreadyLoggedin(Exception): ...

class InvalidLogin(Exception): ...


class IncorrectPassword(Exception): ...


class InvalidUsername(Exception):
    def __init__(self):
        self.message = "Username must only contain numbers and letters"
        super().__init__(self.message)


class InvalidPassword(Exception):
    def __init__(self):
        self.message = "Password must be equal or more than 8 characters and include English letters with capital and numbers"
        super().__init__(self.message)
