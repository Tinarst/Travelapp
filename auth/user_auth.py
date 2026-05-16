from db.database import Connection

"""responsible for interacting with the database"""

connection = Connection()


class UserAuth:

    def _username(self, username):
        """Return list - tuple of username info else none"""
        query = f"SELECT * FROM entered WHERE username = '{username}'"
        with connection:
            responce = connection.GET(query)
            return responce

    def enter_flag(self, username, password):
        query = f"INSERT INTO entered (username, password) VALUES ('{username}', '{password}')"
        with connection:
            connection.POST(query)

    def login(self, username):
        query = f"SELECT * FROM users WHERE username='{username}'"
        with connection:
            responce = connection.GET(query)
            return responce

    def register(self, username, password, name):
        query = f"INSERT INTO users (username, password, name) VALUES ('{username}', '{password}', '{name}');"
        with connection:
            connection.POST(query)

    def get_user_id(self, username):
        query = f"SELECT id FROM users WHERE username = '{username}';"
        with connection:
            return connection.GET(query)

    def change_password(self, user_id, password):
        query = f"UPDATE users SET password = '{password}' WHERE id = {user_id};"
        with connection:
            connection.POST(query)

    def wallet(self, user_id):
        query = f"SELECT wallet FROM users WHERE id = {user_id}"
        with connection:
            responce = connection.GET(query)
            return responce

    def increase_wallet(self, user_id, amount):
        query = f"UPDATE users SET wallet = wallet + {amount} WHERE id = {user_id};"
        with connection:
            connection.POST(query)

    def update_wallet(self, user_id, price):
        query = f"UPDATE users SET wallet = wallet - {price} WHERE id = {user_id};"
        with connection:
            connection.POST(query)


class TripAuth:

    def expire_edit(self, trip_id):
        query = f"UPDATE trip SET expired = true WHERE id = {trip_id};"
        with connection:
            connection.POST(query)

    def available_trips(self):
        query = "SELECT * FROM trip WHERE expired = false"
        with connection:
            responce = connection.GET(query)
            return responce

    def get_special_trip(self, trip_id):
        """Return trip if not expired"""

        query = f"SELECT id, price, capacity, departure_date FROM trip WHERE id = {trip_id} and expired = false"
        with connection:
            responce = connection.GET(query)
            return responce


class ChairAuth:

    def available_chairs(self, trip_id):
        query = (
            f"SELECT number FROM chair WHERE trip_id = {trip_id} AND status = 'free';"
        )
        with connection:
            responce = connection.GET(query)
            return responce

    def get_special_chair(self, chair_number, trip_id):
        query = f"SELECT * FROM chair WHERE trip_id = {trip_id} AND number = {chair_number} AND status = 'free';"
        with connection:
            responce = connection.GET(query)
            return responce


class TicketAuth:

    def get_special_ticket_status(self, user_id, trip_id, chair_number):
        """Return status if ticket exist for current user else"""
        query = f"""
        SELECT status FROM ticket
        WHERE user_id = {user_id}
        AND trip_id = {trip_id}
        AND chair_number = {chair_number}
        """
        with connection:
            responce = connection.GET(query)
            return responce

    def user_ticket_history(self, user_id):
        query = f"""
        SELECT trip.id, trip.origin, trip.destination, trip.departure_date, ticket.chair_number, ticket.status
        FROM ticket
        JOIN trip
        ON trip.id = ticket.trip_id
        WHERE ticket.user_id = {user_id};
        """
        with connection:
            responce = connection.GET(query)
            return responce

    def buy_ticket(self, user_id, trip_id, chair_number, status):
        query1 = f"INSERT INTO ticket (user_id, trip_id, chair_number, status) VALUES ({user_id}, {trip_id}, {chair_number}, '{status}')"
        query2 = f"UPDATE chair SET status = 'booked' WHERE trip_id = {trip_id} AND number = {chair_number}"
        query3 = f"UPDATE trip SET capacity = capacity - 1 WHERE id = {trip_id}"
        with connection:
            connection.POST(query1, query2, query3)

    def status_edit(self, user_id, trip_id, chair_number):
        """Use for after trip"""
        query = f"""
        UPDATE ticket SET status = 'used'
        WHERE user_id = {user_id}
        AND trip_id = {trip_id}
        AND chair_number = {chair_number}
        AND status = 'paid'"""

        with connection:
            connection.POST(query)

    def cancel_ticket(self, user_id, ticket_id, chair_number):
        query1 = f"UPDATE ticket SET status = 'canceled' WHERE user_id = {user_id} AND trip_id = {ticket_id} AND chair_number = {chair_number}"
        query2 = f"UPDATE chair SET status = 'free' WHERE trip_id = {ticket_id} AND number = {chair_number}"
        query3 = f"UPDATE trip SET capacity = capacity + 1 WHERE id = {ticket_id}"
        with connection:
            connection.POST(query1, query2, query3)


class TransactionAuth:

    def increase(self, amount, user_id):
        query = f"""
        INSERT INTO transaction (amount, status, reason, user_id)
        VALUES ({amount}, 'deposit', 'increase', {user_id})
        """
        with connection:
            connection.POST(query)

    def cancel(self, amount, user_id):
        query = f"""
        INSERT INTO transaction (amount, status, reason, user_id)
        VALUES ({amount}, 'deposit', 'cancel ticket', {user_id})
        """
        with connection:
            connection.POST(query)

    def buy(self, amount, user_id):
        query = f"""
        INSERT INTO transaction (amount, status, reason, user_id)
        VALUES ({amount}, 'withdraw', 'buy ticket', {user_id})
        """
        with connection:
            connection.POST(query)
