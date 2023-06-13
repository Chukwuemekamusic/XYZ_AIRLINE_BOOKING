from datetime import datetime


class CardValidator:
    def __init__(self) -> None:
        self._card_number = input("Card number: ").strip()
        self._expiry_month = input("Expiry month: ").strip()
        self._expiry_year = input("Expiry year: ").strip()
        self._cvv = input("cvv: ")

    def is_valid_card_number(self):
        if len(self._card_number) < 13 or len(self._card_number) > 19:
            return False
        if not self._card_number.isnumeric():
            return False
        return True

    def is_valid_cvv(self):
        if (
            len(self._cvv) < 3
            or len(self._cvv) > 4
            or not self._cvv.isnumeric()  # formatting
        ):
            return False
        return True

    def is_valid_expiry_date(self):
        if (
            not self._expiry_month.isnumeric()
            or not self._expiry_year.isnumeric()  # formatting
        ):
            return False
        current_year = datetime.now().year
        current_month = datetime.now().month
        if int(self._expiry_year) < current_year or (
            int(self._expiry_year) == current_year
            and int(self._expiry_month) < current_month
        ):
            return False
        return True

    def is_valid(self):
        if (
            self.is_valid_card_number()
            and self.is_valid_expiry_date()
            and self.is_valid_cvv()
        ):
            return True
        return False

    @property
    def card_content(self):
        while True:
            payment_class = (
                input("Enter class type (economy/business): ").lower().strip()
            )
            if payment_class in ["economy", "business"]:
                break
        return (
            self._card_number,
            self._expiry_month,
            self._expiry_year,
            self._cvv,
            payment_class,
        )
