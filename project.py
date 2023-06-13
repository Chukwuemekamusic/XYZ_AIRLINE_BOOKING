import sys
from email_validator import validate_email, EmailNotValidError
from datetime import datetime

from flight import Flight
from customer import Customer
from card_validator import CardValidator
from card import Card


def main():
    Flight.instantiate_flights_from_schedule()
    while True:
        print("Welcome to XYZ Airline")
        print("Please select an option:")
        option = menu()
        if option == "1":
            action = book_flight_menu()
            if action:
                if not back_to_menu():
                    sys.exit(
                        "Thank you for booking with XYZ airline \nDetails of your booking are forwarded to your email"
                    )

        elif option == "2":
            check_in_menu()
        elif option == "3":
            membership_menu()
        elif option == "4":
            exit()


def menu():
    while True:
        print("1. Search and Book for flights")
        print("2. Check in for a flight")
        print("3. Register for membership")
        print("4. Exit")
        option = input().strip()
        if option in ["1", "2", "3", "4"]:
            return option
        else:
            print("Invalid option. Please try again.")


def book_flight_menu():
    while True:
        # get depature and arrival cities
        print("Search for flights")
        print("Please enter the departure city:")
        departure = input().strip()
        print("Please enter the destination city")
        arrival = input().strip()

        # search if flight is available
        search_results = search_flights(departure, arrival)

        if search_results:
            for i, flight in enumerate(search_results):
                print(f"{i+1}: {flight}")
            # choose number of the list
            print("please select a flight number to book or enter 0 to exit to menu")

            while True:
                try:
                    flight_index = int(input())
                    if flight_index == 0:
                        return False
                    flight = search_results[flight_index - 1]
                    break
                except:
                    print("choose a number from the available flight")
                    # enter 0 to exit

        else:
            print("No flight found, please try again")
            continue  # starts the next iteration

        # gather customer detail
        customer = get_customer_detail(flight)

        # get list of available seats on flight
        seats_available = flight.seats_available()
        print("Available seats on flight:")
        print(*seats_available)

        # choose a seat
        seat = seat_allocation(customer, flight)
        if seat:
            print(flight.seat_confirmation_text(customer))
            if process_payment(flight, customer):
                Customer.add_to_customers(customer)
                flight.print_ticket(customer)
                return True
            else:
                print("Payment failed")
                return False

        return False


def search_flights(departure_city, arrival_city):
    flight_found = []
    for flight in Flight.all_flights:
        if (
            flight.departure_city == departure_city.lower()
            and flight.arrival_city == arrival_city.lower()
        ):
            flight_found.append(flight)
    return flight_found


def is_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def get_customer_detail(flight=""):
    print("Kindly put in your details: ")
    first_name = input("first name: ")
    last_name = input("last name: ")
    while True:
        email_address = input("email: ")
        valid = is_email(email_address)
        if valid:
            break
        print("Email not valid, please try again!")
    customer = fetch_or_create_customer(first_name, last_name, email_address)
    customer.flight = flight
    return customer


def fetch_or_create_customer(first_name, last_name, email_address):
    # check if customer exists as member
    for customer in Customer.all_customers:
        if (
            customer.name == f"{first_name} {last_name}"
            and customer.email_address == email_address
        ):
            return customer

    customer = Customer(first_name, last_name, email_address)
    return customer


def get_membership_detail():
    print("Kindly put in your details: ")
    first_name = input("first name: ")
    last_name = input("last name: ")
    while True:
        email_address = input("email: ")
        valid = is_email(email_address)
        if valid:
            break
        print("Email not valid, please try again!")
    return first_name, last_name, email_address


def seat_allocation(customer, flight):
    while True:
        seat_no = input("choose seat no: ").upper().strip()
        seat_picked = flight.allocate_seat(customer, seat_no)
        if not seat_picked:
            if flight.check_seat_in_already_booked(seat_no):
                print("seat already taken! Please choose from available seats")
            else:
                print("Invalid choice!")
            choice = input(
                "Enter 0 to go back to the menu or any other key to try again: \n"
            ).strip()
            if choice == "0":
                return False
            else:
                pass
        else:
            return True


def process_payment(flight, customer):
    attempt_count = 0
    while attempt_count != 3:
        validate_card_details = CardValidator()
        if validate_card_details.is_valid():
            card = Card(*validate_card_details.card_content)
            # attach the card to a customer to get details when needed
            customer._card = card
            customer.card.make_payment(flight)
            print(f"Payment of {card.make_payment(flight)} successful!")
            update_data_after_payment(flight, customer)
            return True
        attempt_count += 1
        if attempt_count != 3:
            print("Payment unsuccessful. Please check your card details and try again.")
        if attempt_count == 2:
            print("At 3rd failed attempt, booking will be cleared!")
        if attempt_count == 3:
            print("Payment failed")
            flight.clear_booking(customer)
            return False


def update_data_after_payment(flight, customer):
    # update flight.is_booked paid status
    flight.confirm_payment(customer)
    # update that the customer has paid
    customer.pay()  # TODO change .pay() to .has_paid
    # add to customer list if customer not existing
    Customer.add_to_customers(customer)


def back_to_menu():
    back_to_menu = input(
        "would you like to go back to menu? yes/no: ").lower().strip()
    if back_to_menu == "no" or back_to_menu == "n":
        return False
    return True


def check_in_menu():
    ...


def membership_menu():
    while True:
        print("Membership Menu")
        print("1. View Membership Information")
        print("2. Enrol Membership")
        print("3. Cancel Membership")
        print("4. Exit")

        choice = input("Select an Option: ")

        if choice == "1":
            first_name, last_name, email_address = get_membership_detail()
            # check if customer exists as member
            customer_found = None
            for customer in Customer.all_customers:
                if (
                    customer.name == f"{first_name} {last_name}"
                    and customer.email_address == email_address
                ):
                    customer_found = customer
                    if customer.membership_status is True:
                        print("Name: ", customer.name)
                        print("Membership status: Active")
                    else:
                        print(f"{first_name} {last_name} has no membership")
                        print("Would you like to register for membership? yes/no ")
                        action = input().lower().strip()
                        if action == "yes" or action == "y":
                            customer.add_membership()
                            print("Name: ", customer.name)
                            print("Membership status: Active")
            if customer_found is None:
                print(f"{first_name} {last_name} not found")
                print("Would you like to register for membership? yes/no ")
                action = input().lower().strip()
                if action == "yes" or action == "y":
                    customer = Customer(first_name, last_name, email_address)
                    customer.add_membership()
                    Customer.add_to_customers(customer)
                    print("Enrolled!")
                    print("Name: ", customer.name.title())
                    print("Membership status: Active")

        elif choice == "2":
            customer = get_customer_detail()
            if customer.membership_status is False:
                customer.add_membership()
                Customer.add_to_customers(customer)
                print("Enrolled!")
                print("Name: ", customer.name.title())
                print("Membership status: Active")
            else:
                print(f"{customer.name} is already a member")

        elif choice == "3":
            customer.remove_membership()
            print("Membership canceled.")
            break
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
