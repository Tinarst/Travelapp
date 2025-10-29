from model.user_model import UserService, Trip, TicketService, Chair
from model.admin_model import AdminService
from validation.validation import MainService, validate_password
from exception.enter import EmptyUsername, EmptyPassword, InvalidPassword


def CLI():
    print("MENU")
    print("1- Login User")
    print("2- Register User")
    print("3- Adminestrator")
    print("4- Available Ticket")

    try:
        command = int(input("Command: "))
    except:
        print("Unavailable Command")
        CLI()

    trip_agent = Trip()
    chair_agent = Chair()
    cli_agent = MainService()

    def available_ticket():
        available_ticket = Trip().available_trips()
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
            return False

    def user_panel(user: UserService):
        print("PANEL")
        print("1- Increase Wallet")
        print("2- Show Wallet")
        print("3- Ticket History")
        print("4- Available Tickets")
        print("5- Buy Ticket (with wallet)")
        print("6- Cancel Ticket")
        print("7- Change Password")

        user_ticket_service = TicketService(user)

        try:
            command = int(input("Command: "))
        except:
            print("Unavailable Command")

        if command == 1:
            amount = float(input("enter amount for increase wallet: ").strip())
            if amount <= 0:
                raise TypeError("amount must be possetive")

            user.increase_wallet(amount)

        elif command == 2:
            print(f"your inventory: {user.wallet}")

        elif command == 3:
            history = user_ticket_service.user_ticket_history()
            if history:
                for ticket in history:
                    print(
                        f"Origin: {ticket[1]}, To: {ticket[2]}, in {ticket[3].strftime("%Y-%m-%d %H:%M")} chair {ticket[4]}; status: {ticket[5]}"
                    )
            else:
                print("no history founded")

        elif command == 4:
            available_ticket()

        elif command == 5:

            available = available_ticket()

            if available:

                trip_id = int(input("enter ticket id: ").strip())

                if trip_agent.get_special_trip(trip_id):

                    available_chairs = chair_agent.available_chairs(trip_id)

                    if available_chairs:

                        print(f"Available chairs: {available_chairs}")

                        chair_number = int(
                            input("enter chair number position: ").strip()
                        )

                        status = input("Enter pay or reserve: ")

                        user_ticket_service.buy_ticket(trip_id, chair_number, status)

                    else:
                        print("No Available Chairs")

                else:
                    print(f"Unavailable trip ID {trip_id}")
            else:
                print("Unavailable trip for future")

        elif command == 6:
            history = list(
                filter(
                    lambda i: i[5] in ("paid", "reserved")
                    and i[0] in map(lambda i: i[0], trip_agent.available_trips()),
                    user_ticket_service.user_ticket_history(),
                )
            )
            if not history:
                print("There is no history for the future days")

            else:
                for ticket in history:
                    print(
                        f"Ticket ID: {ticket[0]}, {ticket[1]} - {ticket[2]}, in {ticket[3].strftime("%Y-%m-%d %H:%M")} chair {ticket[4]}; status: {ticket[5]}"
                    )

                trip_id = int(input("Enter trip id for canceling: "))

                chair_number = int(input("Enter position: "))

                user_ticket_service.cancel_ticket(trip_id, chair_number)

        elif command == 7:
            try:
                new_password = validate_password(
                    input("Enter New Password: ")
                )

                user.change_password(new_password)

                print("Password changed successfully")
            except InvalidPassword:
                print("Invalid Password")

        user_panel(user)

    def __admin_panel(adminservice: AdminService):
        print("1- Create a Trip")
        print("2- Delete a Trip")
        print("3- Show All Trips")
        print("4- All users")
        print("5- Show Issued Trips")
        print("6- Show All Sold Tickets")
        print("7- Update Departure Of Trip")
        print("8- Show Transaction")

        command = int(input("Enter Command: "))

        if command == 1:
            origin = input("origin: ")
            destination = input("destination: ")
            departure_date = input("departure: ")
            price = input("price: ")
            capacity = int(input("capacity: "))

            adminservice.create_trip(
                origin, destination, departure_date, price, capacity
            )

        elif command == 2:
            trip_id = int(input("Enter Trip ID: "))

            adminservice.delete_trip(trip_id)

        elif command == 3:
            all_trips = adminservice.all_trips()
            if all_trips:
                for trip in all_trips:
                    trip_id = trip[0]
                    origin = trip[1]
                    destination = trip[2]
                    datetime = trip[3]
                    price = trip[4]
                    capacity = trip[5]
                    expired = "expired" if trip[6] == True else "available"
                    print(
                        f"Trip ID: {trip_id}; {origin} - {destination}, Price: {price}, Capacity {capacity}, {expired} AT {datetime}"
                    )
            else:
                print("No Trip left")

        elif command == 4:
            users = adminservice.all_users()
            if users:
                for user in users:
                    user_id = user[0]
                    username = user[1]
                    wallet = user[2]
                    count_of_tickets = user[3]
                    print(
                        f"User ID {user_id}, {username} Wallet: {wallet} Total Tickets {count_of_tickets}"
                    )
            else:
                print("no user")

        elif command == 5:
            issued_trip = adminservice.issued_trip()
            if issued_trip:
                for trip in issued_trip:
                    trip_id = trip[0]
                    origin = trip[1]
                    destination = trip[2]
                    datetime = trip[3]
                    price = trip[4]
                    capacity = trip[5]
                    print(
                        f"Trip ID: {trip_id}; {origin} - {destination}, Price: {price}, Capacity {capacity}"
                    )
            else:
                print("No trip issued")

        elif command == 6:
            sold_tickets = adminservice.sold_ticket()
            if sold_tickets:
                for ticket in sold_tickets:
                    datetime = ticket[0]
                    user_id = ticket[1]
                    ticket_id = ticket[2]
                    chair_number = ticket[3]
                    status = ticket[4]
                    print(
                        f"IN {datetime} User ID {user_id} prepared Ticket ID {ticket_id} and {status} In position {chair_number}"
                    )

        elif command == 7:
            trips = available_ticket()
            if trips:
                try:
                    trip_id = int(input("Enter Trip ID for update: "))
                    
                    departure_date = input("Enter Date For update: ")

                    admin.update_trip(trip_id, departure_date)

                except:
                    print("Update Faild")
                    
        elif command == 8:
            try:
                limit = int(input("limit for show transaction(0 for see all): "))
                if limit < 0:
                    raise TypeError()
                transaction = admin.show_transaction(limit)
                for t in transaction:
                    date = t[0].strftime("%Y-%m-%d %H:%M:%S")
                    wallet = t[1]
                    status = t[2]
                    reason = t[3]
                    user_id = t[4]
                    print(f"IN {date} ACTION {reason} - {status} FROM USER ID {user_id}")
                    
            except TypeError:
                print("Invalid limit")

        __admin_panel(admin)

    if command == 1:
        try:
            username = input("enter your username: ")
            password = input("enter password: ")
            if not username:
                raise EmptyUsername()
            elif not password:
                raise EmptyPassword()
        except EmptyUsername:
            print("Username Cannot be empty")
        except EmptyPassword:
            print("Password Cannot be empty")
        else:
            try:
                user_id, username, password, name = cli_agent.login(username, password)
                USER = UserService(user_id, username, password, name)

                print(f"{username} Logged in")

                user_panel(USER)
            except Exception as e:
                print(e)
                CLI()

    elif command == 2:
        try:
            username = input("enter your username: ")
            password = input("enter password: ")
            name = input("enter your name: ")
            if not username:
                raise EmptyUsername()
            elif not password:
                raise EmptyPassword()
        except EmptyUsername:
            print("Username Cannot be empty")
        except EmptyPassword:
            print("Password Cannot be empty")
        else:
            try:
                user_id, username, password, name = cli_agent.register(
                    username, password, name
                )
                USER = UserService(user_id, username, password, name)

                print(f"{username} Registered")

                user_panel(USER)
            except:
                CLI()

    elif command == 3:
        try:
            admin_username = input("Enter Username: ")
            admin_password = input("Enter Password: ")
            
            if not admin_username:
                raise EmptyUsername()
            elif not admin_password:
                raise EmptyPassword()

        except EmptyUsername:
            print("Username Cannot be empty")
        except EmptyPassword:
            print("Password Cannot be Empty")
        else:

            if cli_agent.login_admin(admin_username, admin_password):
                admin = AdminService()
                __admin_panel(admin)
            else:
                print("Coud not login")

    elif command == 4:
        available_ticket()

        CLI()


if __name__ == "__main__":
    CLI()
    
