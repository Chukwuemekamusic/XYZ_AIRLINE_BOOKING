from datetime import datetime


class Card:
    def __init__(
        self, card_number, expiry_month, expiry_year, cvv, payment_class
    ):  # formatting
        self._card_number = card_number
        self._expiry_month = expiry_month
        self._expiry_year = expiry_year
        self._cvv = cvv
        self._payment_class = payment_class

    def is_valid(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        try:
            int(self._expiry_month)
            int(self._expiry_year)
        except:  # noqa: E722 # TODO: Remove noqa
            return False
        if int(self._expiry_year) < current_year or (
            int(self._expiry_year) == current_year
            and int(self._expiry_month) < current_month
        ):
            return False

        card_number = str(self._card_number)
        if len(self._card_number) < 13 or len(self._card_number) > 19:
            return False

        if not card_number.isnumeric():
            return False

        sum = 0
        num_digits = len(card_number)
        oddeven = num_digits & 1

        for count in range(0, num_digits):
            digit = int(card_number[count])

            if not ((count & 1) ^ oddeven):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9

            sum = sum + digit

        return (sum % 10) == 0

    def make_payment(self, flight):
        # the abstract deduction should be effected here
        return flight.cost(self._payment_class)

    def get_payment_class(self):
        return self._card.payment_class
