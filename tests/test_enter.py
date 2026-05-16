from validation.validation import MainService
service = MainService()
def test_invalid_username():
    #Username must only contain numbers and letters
    username = "test@"
    password = "Test01234"
    user = service.register(username, password)
    assert not user
    
def test_invalid_password():
    #Password must be equal or more than 8 characters and include English letters with capital and numbers
    username = "test"
    password = "test"
    user = service.register(username, password)
    assert not user
    
def test_login():
    #Valid input
    username = "test"
    password = "Test01234"
    user = service.login(username, password)
    assert user
    
def test_incorrect_password():
    #Incorrect password
    username = "test"
    password = "test"
    user = service.login(username, password)
    assert not user
    