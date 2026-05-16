from auth.user_auth import UserAuth, TripAuth, TicketAuth, ChairAuth, TransactionAuth
from auth.audit_auth import Audit, logger
from exception.ticketservice import (
    TicketAlreadyExist,
    TicketNotSubmitted,
    InsufficientInventory,
    TicketNotFound,
    NoChairFound,
    NoCapacity,
)
import datetime

"""responsible for control objects"""


class User:
    def __init__(self, user_id, username, password, name):
        self._id = user_id
        self.username = username
        self.__password = password
        self.name = name

        self.auth = UserAuth()
        self.transaction = TransactionAuth()
        self.audit = Audit()

    @property
    def wallet(self):
        return self.auth.wallet(self._id)[0][0]

    def change_password(self, new_password):
        self.auth.change_password(self._id, new_password)
        self.__password = new_password

        logger.info(f"USER {self._id} Changed Password")

        self.audit.user("change password", f"User ID {self._id} Changed Password")


class UserService(User):

    def increase_wallet(self, value, reason="increase"):

        self.auth.increase_wallet(self._id, value)

        print(f"Wallet increased by +{value}")

        logger.info(f"USER ({self._id}) Wallet increased +{value}")

        if reason == "increase":
            self.transaction.increase(value, self._id)

            self.audit.user(
                self.username,
                "increase wallet",
                f"User ID {self._id} topped up their wallet",
            )
        else:
            self.transaction.cancel(value, self._id)

    def update_wallet(self, value: str):

        self.auth.update_wallet(self._id, value)

        print(f"Wallet decreased by -{value}")

        logger.info(f"USER ({self._id}) Wallet decreased -{value}")

        self.transaction.buy(value, self._id)


class Trip:
    def __init__(self):
        self.auth = TripAuth()

    def __expire_control(self):
        trips = self.auth.available_trips()

        for trip in trips:

            trip_id = trip[0]
            trip_departure_date = trip[3]

            if datetime.datetime.now() >= trip_departure_date:

                self.auth.expire_edit(trip_id)

                logger.info(f"Trip {trip_id} Expired")

    def available_trips(self):
        """Return available list of tuple tickets"""

        self.__expire_control()

        available_trips = self.auth.available_trips()

        return available_trips

    def get_special_trip(self, trip_id: int):
        """Return available trip (trip_id, price, capacity, departure_date) for future or None"""
        """FOR INTERNAL USE"""

        self.__expire_control()

        trip = self.auth.get_special_trip(trip_id)

        return trip[0] if trip else None


class Chair:
    def __init__(self):
        self.trip = Trip()
        self.auth = ChairAuth()

    def available_chairs(self, trip_id: int) -> list:
        """Return list of tuples free chairs"""
        """FOR EXTERNAL USE"""

        chairs = self.auth.available_chairs(trip_id)

        return chairs

    def get_special_chair(self, chair_number, trip_id) -> bool:
        """Return True if chair is free False if booked"""
        """FOR INTERNAL USE"""

        chair = self.auth.get_special_chair(chair_number, trip_id)

        return True if chair else False


class TicketService:
    def __init__(self, user: UserService):
        self.user = user
        self.trip = Trip()
        self.chair = Chair()

        self.auth = TicketAuth()

        self.audit = Audit()

    def __status_control(self):
        """For INTERNAL Use"""

        history = self.auth.user_ticket_history(self.user._id)

        for travel in history:
            user_id = self.user._id
            trip_id = travel[0]
            time = travel[3]
            chair_number = travel[4]
            status = travel[5]

            if datetime.datetime.now() >= time:

                if status == "paid":

                    self.auth.status_edit(user_id, trip_id, chair_number)

                    logger.info(f"TRIP {trip_id} Used From User {user_id}")

    def user_ticket_history(self):
        """Return list of (trip_id, trip_origin, trip_destination, trip_departure_date, ticket_chair_number, ticket_status)"""

        self.__status_control()

        history = self.auth.user_ticket_history(self.user._id)

        return history

    def invetory_check(self, price) -> bool:
        """FOR INTERNAL USE"""

        return True if self.user.wallet >= price else False

    def buy_ticket(self, trip_id, chair_number, status: str):
        status = status.lower().strip()

        trip = self.trip.get_special_trip(trip_id)

        chair = self.chair.get_special_chair(chair_number, trip_id)

        price = trip[1]

        active_ticket = next(
            (
                ticket
                for ticket in self.user_ticket_history()
                if ticket[0] == trip_id
                and ticket[4] == chair_number
                and ticket[5] in ("paid", "reserved")
            ),
            None,
        )

        balance = self.invetory_check(price)

        try:
            if not trip:
                # Check trip existance/ expire or invalid
                raise TicketNotFound()
            elif active_ticket:
                # Check used ticket for current user
                raise TicketAlreadyExist()
            elif not chair:
                # Check free position/ booked or invalid
                raise NoChairFound()
            elif not balance and status == "pay":
                # Check balance
                raise InsufficientInventory()

        except TicketNotFound:
            print(f"No Ticket Found For Trip ID {trip_id}")
        except NoCapacity:
            print("No Capacity Left")
        except NoChairFound:
            print(f"Unavailable Chair in Position {chair_number}")
        except TicketAlreadyExist:
            print("Ticket Already Exist In History")
        except InsufficientInventory:
            print(
                f"Insufficient Account Balance (About {price - self.user.wallet} less)"
            )

        else:

            if status == "pay":
                self.auth.buy_ticket(self.user._id, trip_id, chair_number, "paid")
                self.user.update_wallet(price)

                print(f"Your ticket submitted")

                logger.info(
                    f"Ticket {trip_id} for User {self.user._id} submitted In Position {chair_number}"
                )
                self.audit.user(
                    self.user.username,
                    "buy ticket",
                    f"User ID {self.user._id} bought the ticket ID {trip_id} in the {chair_number} place",
                )
            elif status == "reserve":
                self.auth.buy_ticket(self.user._id, trip_id, chair_number, "reserved")

                print(f"Your ticket reserved")

                logger.info(
                    f"Ticket {trip_id} for User {self.user._id} reserved In Position {chair_number}"
                )
                self.audit.user(
                    self.user.username,
                    "reserve ticket",
                    f"User ID {self.user._id} reserved the ticket ID {trip_id} in the {chair_number} place",
                )

    def cancel_ticket(self, trip_id, chair_number):

        trip = self.trip.get_special_trip(trip_id)

        active_ticket = next(
            (
                ticket
                for ticket in self.user_ticket_history()
                if ticket[0] == trip_id
                and ticket[4] == chair_number
                and ticket[5] in ("paid", "reserved")
            ),
            None,
        )

        try:
            if not trip:
                # Check trip existance/ expire or invalid
                raise TicketNotFound()
            elif not active_ticket:
                # Check used for current user
                raise TicketNotSubmitted()
            else:
                remaining = trip[3] - datetime.datetime.now()

                status = active_ticket[5]

                if remaining >= datetime.timedelta(hours=24):

                    if status == "paid":
                        amount = trip[1] * 8 / 10
                        self.user.increase_wallet(amount, "cancel ticket")

                elif 0 <= remaining < 24:

                    print(
                        "Less than 24 hours left until departure; No refund will be made to the wallet"
                    )

                self.auth.cancel_ticket(self.user._id, trip_id, chair_number)

                print(f"Ticket {trip_id} Canceled")

                logger.info(
                    f"Ticket {trip_id} Has been Canceled in Position {chair_number}"
                )

                self.audit.user(
                    self.user.username,
                    "cancel ticket",
                    f"User ID {self.user._id} canceled the ticket ID {trip_id} in the {chair_number} place",
                )

        except TicketNotFound:
            print(f"No Ticket Found For Trip ID {trip_id}")
        except TicketNotSubmitted:
            print(
                f"Chair does not Submitted in position {chair_number} For trip {trip_id}"
            )
