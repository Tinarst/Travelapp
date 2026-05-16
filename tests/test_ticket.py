from model.user_model import UserService, TicketService
from db.database import Connection
import pytest

username = "test"
password = "Test01234"

user = UserService(7, username, password, None)

ticket_service = TicketService(user)

connection = Connection()
def test_increase_wallet():
    current_wallet = user.wallet
    user.increase_wallet(10)
    update_wallet = user.wallet
    assert current_wallet + 10 == update_wallet
    
def test_buy_ticket():
    #Except Success
    ticket_service.buy_ticket(21, 1, "pay")
    
    history = ticket_service.user_ticket_history()
    find = []
    for i in history:
        trip_id = i[0]
        status = i[5]
        if trip_id == 21 and status == "paid":
            find.append((trip_id, status))
    assert len(find) == 1
    
    
def test_cancel_ticket():
    ticket_service.cancel_ticket(21, 1)
    
    history = ticket_service.user_ticket_history()
    find = []
    for i in history:
        trip_id = i[0]
        status = i[5]
        if trip_id == 21 and status == "canceled":
            find.append((trip_id, status))
            
    assert len(history) == 1
    
    with connection:
        query = f"DELETE FROM ticket WHERE user_id = {user._id} and trip_id = {trip_id}"
        connection.POST(query)
    
    