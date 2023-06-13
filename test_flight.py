from customer import Customer
from flight import Flight


def main():
    test_confirmation_seat()


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


if __name__ == "__main__":
    main()
