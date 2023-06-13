import csv
from datetime import datetime

from customer import Customer


class Flight:
    seats = [
        "1A",
        "1B",
        "1C",
        "1D",
        "2A",
        "2B",
        "2C",
        "2D",
        "3A",
        "3B",
        "3C",
        "3D",
        "4A",
        "4B",
        "4C",
        "4D",
        "5A",
        "5B",
        "5C",
        "5D",
        "6A",
        "6B",
        "6C",
        "6D",
        "7A",
        "7B",
        "7C",
        "7D",
        "8A",
        "8B",
        "8C",
        "8D",
        "9A",
        "9B",
        "9C",
        "9D",
        "10A",
        "10B",
        "10C",
        "10D",
        "11A",
        "11B",
        "11C",
        "11D",
        "12A",
        "12B",
        "12C",
        "12D",
    ]
    TOTAL_SEATS = 48
    all_flights = []

    def __init__(
        self,
        flight_number,
        departure_city,
        arrival_city,
        departure_time,
        arrival_time,
        economy_class_cost,
        business_class_cost,
    ):
        self._flight_number = flight_number.lower()
        self._departure_city = departure_city.lower()
        self._arrival_city = arrival_city.lower()
        self._departure_time = departure_time.lower()
        self._arrival_time = arrival_time.lower()
        self._economy_class_cost = economy_class_cost
        self._business_class_cost = business_class_cost
        self._is_booked = False
        self.booked = []
        self._seats_allocated = {}

        Flight.all_flights.append(self)

    @property
    def departure_city(self):
        return self._departure_city

    @property
    def arrival_city(self):
        return self._arrival_city

    @property
    def flight_number(self):
        return self._flight_number

    @property
    def remaining_seats(self):
        return self.TOTAL_SEATS - len(self._seats_allocated)

    @property
    def is_booked(self):
        return self.is_booking_complete()

    def cost(self, payment_class):
        if payment_class == "economy":
            return self._economy_class_cost
        if payment_class == "business":
            return self._business_class_cost

    # once payment is made, this function ensures that
    def booking_confirmed(self, customer):
        self._is_booked = True

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}('{self._flight_number}', "
            f"{self._departure_city}, {self._arrival_city}, "
            f"{self._departure_time}, {self._arrival_time}, "
            f"{self._economy_class_cost}, {self._business_class_cost})"
        )

    def seats_available(self):
        if len(self._seats_allocated) == self.TOTAL_SEATS:
            return []
        return [seat for seat in self.seats if seat not in self._seats_allocated]

    def allocate_seat(self, customer: Customer, seat_no):
        if seat_no in self.seats_available():
            self._seats_allocated[seat_no] = customer
            self.booked.append(
                {
                    "customer": customer,
                    "date": datetime.now(),
                    "seat": seat_no,
                    "paid": False,
                }
            )  # booked_list
            customer.add_booking(self)

            return True
        else:
            return False

    def check_seat_in_already_booked(self, seat_no):
        if seat_no in self._seats_allocated:
            return True
        return False

    def seat_confirmation_text(self, customer: Customer):
        seat_no = {
            seat
            for seat in self._seats_allocated
            if self._seats_allocated[seat] == customer
        }

        if seat_no:
            msg = (
                f"Seat number {seat_no} on flight {self._flight_number.upper()},"
                f"\nfrom {self._departure_city.title()} {self._departure_time}"
            )
            msg += f" to {self._arrival_city.title()} {self._arrival_time} \nis reserved for {customer.name}"
        else:
            msg = (
                f"no seat on flight {self._flight_number.upper()},"
                f"\nfrom {self._departure_city.title()} {self._departure_time}"
            )
            msg += f" to {self._arrival_city.title()} {self._arrival_time} \nis reserved for {customer.name}"
        return msg

    def get_passengers(self):
        passenger = []
        for customer in self.booked:
            passenger.append(customer.get("customer").name)
        return passenger

    def get_number_of_passengers(self):
        return len(self.booked)

    def is_booking_complete(self):
        self._is_booked = len(self._seats_allocated) == self.TOTAL_SEATS
        return self._is_booked

    def clear_booking(self, customer: Customer):
        for booking in self.booked:
            if booking["customer"] == customer:
                seat_no = booking["seat"]
                del self._seats_allocated[seat_no]
                self.booked.remove(booking)
                break

    def print_ticket(self, customer: Customer):
        if self.is_customer_booked(customer):
            ticket_info = {
                "flight_number": self._flight_number,
                "departure_city": self._departure_city,
                "arrival_city": self._arrival_city,
                "departure_time": self._departure_time,
                "arrival_time": self._arrival_time,
                "customer_name": customer.name,
                "payment_class": customer.card._payment_class,
                "cost": self.cost(customer.card._payment_class),
            }
            print(
                f"Ticket Details\n"
                f"Flight Number: {ticket_info['flight_number'].upper()}\n"
                f"Departure City: {ticket_info['departure_city'].title()}\n"
                f"Arrival City: {ticket_info['arrival_city'].title()}\n"
                f"Departure Time: {ticket_info['departure_time']}\n"
                f"Arrival Time: {ticket_info['arrival_time']}\n"
                f"Customer Name: {ticket_info['customer_name'].title()}\n"
                f"Payment Class: {ticket_info['payment_class'].title()}\n"
                f"Cost: {ticket_info['cost']}\n"
            )

    def confirm_payment(self, customer: Customer):
        for booking in self.booked:
            if booking["customer"] == customer:
                booking["paid"] = True
                break

    def is_customer_booked(self, customer):
        for booking in self.booked:
            if booking["customer"] == customer and booking["paid"] is True:
                return True
        return False

    @classmethod
    def instantiate_flights_from_schedule(cls):
        if not cls.all_flights:
            with open("schedule.csv") as f:
                reader = csv.DictReader(f)
                flights = list(reader)
            for flight in flights:
                Flight(
                    flight_number=flight.get("flight_number").lower(),
                    departure_city=flight.get("departure_city").lower(),
                    arrival_city=flight.get("arrival_city").lower(),
                    departure_time=flight.get("departure_time").lower(),
                    arrival_time=flight.get("arrival_time").lower(),
                    economy_class_cost=flight.get("economy_class_cost").lower(),
                    business_class_cost=flight.get("business_class_cost").lower(),
                )

    @classmethod
    def clear_flights_schedule(cls):
        cls.all_flights.clear()
