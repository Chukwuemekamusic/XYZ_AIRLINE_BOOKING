from datetime import datetime

from card import Card


class Customer:
    all_customers = []
    all_members = []

    def __init__(
        self, first_name, last_name, email_address, flight="", card=""
    ) -> None:
        self._first_name = first_name
        self._last_name = last_name
        self._email_address = email_address
        self._flight = flight
        self._booked_flights = []
        self._has_paid = False
        self._membership_status = False
        self._frequent_flyer = False
        self._booked_flights.append({"flight": flight, "date": datetime.now()})
        self._card = card
        # print("customer created")

    @property
    def name(self):
        name = f"{self._first_name} {self._last_name}"
        return name

    @property
    def email_address(self):
        return self._email_address

    @property
    def flight(self):
        return self._flight

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card: Card):
        self._card = card

    @flight.setter
    def flight(self, flight):
        self._flight = flight

    @property
    def membership_status(self):
        return self._membership_status

    def has_booked_flight(self, flight):
        return flight in self._booked_flights

    @property
    def booked_flights(self):
        return self._booked_flights

    @property
    def has_paid(self):
        return self._has_paid

    @classmethod
    def add_to_customers(cls, customer):
        if customer not in cls.all_customers:
            cls.all_customers.append(customer)

    @classmethod
    def add_to_members(cls, customer):
        if (
            customer.membership_status is True
            and customer not in cls.all_members  # fomatting
        ):
            cls.all_members.append(customer)

    @classmethod
    def remove_from_members(cls, customer):
        if customer.membership_status is False and customer in cls.all_members:
            cls.all_members.remove(customer)

    def add_booking(self, flight):
        self._booked_flights.append({"flight": flight, "date": datetime.now()})

    def pay(self):
        self._has_paid = True

    def add_membership(self):
        self._membership_status = True
        self.__class__.add_to_members(self)

    def remove_membership(self):
        self._membership_status = False
        self.__class__.remove_from_members(self)

    def __repr__(self):
        if self.membership_status:
            return (
                f"Name: {self.name}\nEmail: {self.email_address}"
                "\nMembership status: Active"
            )
        else:
            return (
                f"Name: {self.name}\nEmail: {self.email_address}"
                "\nMembership status: Inactive"
            )
