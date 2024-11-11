import re

class Date:
    def validate_date(self, date):
        check = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$"

        if re.match(check, date):
            return True
        else:
            return False