import pytest
from flight import Flight
from customer import Customer
from project import (
    search_flights,
    is_email,
    get_customer_detail,
    seat_allocation,
    process_payment,
    book_flight_menu,
)


flight = Flight(
    "TK2372", "Istanbul", "Istanbul", "2022-05-25T17:30", "2022-05-25T19:30", 600, 1000
)
# Create a flight object that matches the required parameters for the Flight class constructor
flight1 = Flight(
    "flight1", "Lagos", "Abuja", "2022-09-01 10:00", "2022-09-01 12:00", "economy", 100
)
flight2 = Flight(
    "flight2", "Lagos", "Abuja", "2022-09-01 14:00", "2022-09-01 16:00", "economy", 100
)
flight3 = Flight(
    "flight3", "Lagos", "Abuja", "2022-09-01 18:00", "2022-09-01 20:00", "economy", 100
)
flight4 = Flight(
    "flight4", "Abuja", "Lagos", "2022-09-01 21:00", "2022-09-02 20:00", "business", 600
)
# Add the flight object to the list of all flights
Flight.all_flights = [flight1, flight2, flight3, flight4]

customer = Customer("John", "Doe", "johndoe@example.com", flight)


def test_search_flights():
    # Test the search_flights function

    search_results = search_flights("Lagos", "Abuja")
    assert len(search_results) == 3
    assert flight1 in search_results
    assert flight2 in search_results
    assert flight3 in search_results

    # testing lower cases too
    search_results2 = search_flights("abuja", "lagos")
    assert len(search_results2) == 1
    assert flight4 in search_results2
    assert flight2 not in search_results2


def test_no_result_found():
    search_results = search_flights("London", "Abuja")
    assert len(search_results) == 0


def test_is_email():
    assert is_email("joefredy2@yahoo.com") is True
    assert is_email("davidmalan@harvard.edu") is True
    assert is_email("joe@emeka.co.emeka") is False
    assert is_email("da@malan.com") is False
    assert is_email("christopher@rgu.ac.uk") is True


def test_collect_customer_detail_valid_email(mocker):
    # test that the function collects the customer's details and returns a dictionary

    # define the mock input function
    mocker.patch("builtins.input", side_effect=["John", "Doe", "john.doe@yahoo.com"])
    # define the mock valid email function
    # mocker.patch('project.is_email', return_value=True)

    customer = get_customer_detail(flight)
    assert customer.name == "John Doe"
    assert customer.name != "jon Doe"
    assert customer.name.split(" ")[1] == "Doe"
    assert customer._email_address == "john.doe@yahoo.com"
    assert customer.flight == flight


def test_collect_customer_invalid_email(mocker):
    mocker.patch("builtins.input", side_effect=["John", "Doe", "john.doe@yhel"])
    mocker.patch("project.is_email", return_value=False)
    with pytest.raises(Exception) as e:
        get_customer_detail(flight)

        assert str(e.value) == "Email not valid, try again!"


def test_seat_allocation(mocker):
    # test with right seat no
    mocker.patch("builtins.input", side_effect=["1a"])
    # mocker.patch.object(flight, 'allocate_seat', return_value=True)
    # mocker.patch('flight.check_seat_in_already_booked', return_value=True)
    assert seat_allocation(customer, flight) is True
    mocker.stopall()

    # test with wrong seat no and choice set to 0
    mocker.patch("builtins.input", side_effect=["1f", "0"])
    assert seat_allocation(customer, flight) is False

    # test with wrong seat, choice not 0, and right seat entered
    mocker.patch("builtins.input", side_effect=["1f", "5", "2c"])
    assert seat_allocation(customer, flight) is True
    mocker.stopall()


def test_process_payment(mocker):
    # Test successful payment
    mocker.patch(
        "builtins.input",
        side_effect=["4111111111111111", "12", "2030", "233", "business"],
    )
    assert process_payment(flight, customer) is True
    assert flight.is_customer_booked(customer) is True
    assert customer.has_paid is True
    mocker.stopall()

    # Test failed payment
    mocker.patch(
        "builtins.input",
        side_effect=[
            "41111111",
            "12",
            "2030",
            "233",  # wrong card number
            "4111111111111111",
            "02",
            "2022",
            "233",  # expired date
            "4111111111111111",
            "12",
            "2030",
            "abc123",  # wrong cvv
        ],
    )
    # mocker.patch('validate.CardValidator.is_valid', side_effect=[False, False, False])
    assert process_payment(flight, customer) is False
    mocker.stopall()


def test_book_flight_menu(mocker):
    # a successful patch
    mocker.patch(
        "builtins.input",
        side_effect=[
            "Lagos",
            "Abuja",  # destination and arrival
            "2",  # flight index
            "John",  # customer_details
            "Doe",
            "john.doe@yahoo.com",
            "1a",  # seat allocation
            "4111111111111111",  # card detail
            "12",
            "2030",
            "233",
            "business",  # payment_class
        ],
    )

    assert book_flight_menu() is True
    mocker.stopall()
    print()
    # test when card flight in
    mocker.patch(
        "builtins.input",
        side_effect=[
            "Lagos",
            "Abuja",  # destination and arrival
            "2",  # flight index
            "John",  # customer_details
            "Doe",
            "john.doe@yahoo.com",
            "1a",  # seat_already taken
            "try_again",
            "2b",  # seat allocation
            "41111111",
            "12",
            "2030",
            "233",  # wrong card number
            "4111111111111111",
            "02",
            "2022",
            "233",  # expired date
            "4111111111111111",
            "12",
            "2030",
            "abc123",  # wrong cvv
        ],
    )

    assert book_flight_menu() is False


def test_confirmation_seat():
    flight = Flight(
        "XYZ123", "New York", "Los Angeles", "10:00 AM", "1:00 PM", 500, 1000
    )

    customer1 = Customer("John", "Doe", "johndoe@example.com", flight)
    customer2 = Customer("Jane", "Smith", "janesmith@example.com", flight)

    flight.allocate_seat(customer1, "1A")
    flight.allocate_seat(customer2, "1A")

    #  msg = (f"Seat number {seat_no} on flight {self._flight_number.upper()},"
    #                f"\nfrom {self._departure_city.title()} {self._departure_time}")
    #         msg += f" to {self._arrival_city} {self._arrival_time} \nis reserved for {customer.name}"
    assert (
        (flight.seat_confirmation_text(customer1))
        == "Seat number {'1A'} on flight XYZ123,\nfrom New York 10:00 am to Los Angeles 1:00 pm \nis reserved for John Doe"
    )

    assert (
        (flight.seat_confirmation_text(customer2))
        == "no seat on flight XYZ123,\nfrom New York 10:00 am to Los Angeles 1:00 pm \nis reserved for Jane Smith"
    )
