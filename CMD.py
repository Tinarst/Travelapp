from model.user_model import UserService, Trip, TicketService, Chair
from model.admin_model import AdminService
from validation.validation import ParserService, validate_password
from exception.enter import InvalidPassword

import argparse


parent = argparse.ArgumentParser(add_help=False)
parent.add_argument("--username", help="Username for stay sign in")

parser = argparse.ArgumentParser(description="Use Travel app")
subparser = parser.add_subparsers(dest="command")

# Login Command
login_parser = subparser.add_parser("login")
login_parser.add_argument("-user", required=True)
login_parser.add_argument("-passwd", required=True)


# Register Command
register_parser = subparser.add_parser("register")
register_parser.add_argument("-user", required=True)
register_parser.add_argument("-passwd", required=True)
register_parser.add_argument("-name")

# User Panel
topup = subparser.add_parser("topup", parents=[parent])
topup.add_argument("amount")

wallet = subparser.add_parser("wallet", parents=[parent])

trips = subparser.add_parser("trips", help="Show Available Trips")

history = subparser.add_parser("history", parents=[parent])

book = subparser.add_parser("book", parents=[parent], help="Book ticket")
book.add_argument("-tripid", help="Trip ID")
book.add_argument("-seat", required=True, help="position")
book.add_argument("-status", choices=["pay", "reserve"])

cancel = subparser.add_parser("cancel", parents=[parent])
cancel.add_argument("-tripid", help="Trip ID")
cancel.add_argument("-seat", required=True, help="position")

setpass = subparser.add_parser("setpass", parents=[parent], help="Change Password")
setpass.add_argument("newpass")

args = parser.parse_args()


class ParserPanel:
    def __init__(self):
        self.parser = ParserService()
        self.trip = Trip()

    def login(self, username, password):

        if self.parser.login(username, password):
            print(f"{username} Logged in")
            
    def register(self, username, password, name=None):
        if self.parser.register(username, password, name):
            print(f"{username} Registered")

    def userdetail(self, username):
        user_detail = self.parser.user(username)

        if user_detail:
            user_id, username, password, name = user_detail

            USER = UserService(user_id, username, password, name)

            return UserPanel(USER)

    def available_ticket(self):
        available_ticket = self.trip.available_trips()
        if available_ticket:

            for ticket in available_ticket:
                ticket_id = ticket[0]
                origin = ticket[1]
                destination = ticket[2]
                departure_date = ticket[3]
                price = ticket[4]
                capacity = ticket[5]
                print(
                    f"Trip id {ticket_id}, From {origin} To {destination} In {departure_date} Price {price} Capacity: {capacity}"
                )
            return True
        else:
            print("no available ticket")


class UserPanel(ParserPanel):
    def __init__(self, user: UserService):
        self.user = user
        self.ticket = TicketService(self.user)
        self.chair = Chair()
        super().__init__()

    def increase_wallet(self, amount):
        amount = float(amount)
        try:
            if amount <= 0:
                raise TypeError()

            self.user.increase_wallet(amount)

        except TypeError:
            print("amount must be possetive")

    def show_wallet(self):
        print(f"your inventory: {self.user.wallet}")

    def ticket_history(self):
        history = self.ticket.user_ticket_history()
        if history:
            for ticket in history:
                print(
                    f"Origin: {ticket[1]}, To: {ticket[2]}, in {ticket[3].strftime("%Y-%m-%d %H:%M")} chair {ticket[4]}; status: {ticket[5]}"
                )
        else:
            print("no history founded")

    def book(self, trip_id, seat, status):
        available = self.trip.available_trips()
        trip_id = int(trip_id)
        seat = int(seat)
        if available:

            if self.trip.get_special_trip(trip_id):

                available_chairs = self.chair.available_chairs(trip_id)

                if available_chairs:

                    self.ticket.buy_ticket(trip_id, seat, status)

                else:
                    print("No Available Chairs")

            else:
                print(f"Unavailable trip ID {trip_id}")
        else:
            print("Unavailable trip for future")

    def cancel(self, trip_id, seat):
        history = list(
            filter(
                lambda i: i[5] in ("paid", "reserved")
                and i[0] in map(lambda i: i[0], self.trip.available_trips()),
                self.ticket.user_ticket_history(),
            )
        )
        if not history:
            print("There is no history for the future days")

        else:
            trip_id = int(trip_id)

            seat = int(seat)

            self.ticket.cancel_ticket(trip_id, seat)

    def change_password(self, value):
        try:
            validate_password(self.user.change_password(value))

            print("Password changed successfully")
        except InvalidPassword:
            print("Invalid Password")


panel = ParserPanel()

try:
    user = panel.userdetail(args.username)
    
    if args.command == "topup":

        user.increase_wallet(args.amount)

    elif args.command == "wallet":

        user.show_wallet()

    elif args.command == "history":

        user.ticket_history()

    elif args.command == "book":

        user.book(args.tripid, args.seat, args.status)

    elif args.command == "cancel":
        user.cancel(args.tripid, args.seat)
    
except AttributeError:
    ...
    
finally:
    if args.command == "login":
        panel.login(args.user, args.passwd)
        
    elif args.command == "register":
        panel.register(args.user, args.passwd, args.name)

    elif args.command == "trips":
        panel.available_ticket()