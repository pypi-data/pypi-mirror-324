"""
Absfuyu: Human
--------------
Human related stuff

Version: 1.4.0
Date updated: 15/08/2024 (dd/mm/yyyy)
"""

# Module level
###########################################################################
__all__ = ["Human", "Person"]


# Library
###########################################################################
import re
from datetime import datetime, time
from typing import Optional, Union
from urllib.parse import urlencode

from dateutil.relativedelta import relativedelta

from absfuyu.fun import zodiac_sign
from absfuyu.general.data_extension import IntNumber
from absfuyu.tools.web import soup_link
from absfuyu.version import Version  # type: ignore


# Sub-Class
###########################################################################
class _FloatBase:
    """To show some unit"""

    def __init__(self, value: float) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value.__str__()

    def to_float(self) -> float:
        return float(self.value)


class _Height(_FloatBase):
    def __repr__(self) -> str:
        return f"{self.value:.2f} cm"


class _Weight(_FloatBase):
    def __repr__(self) -> str:
        return f"{self.value:.2f} kg"


# Class
###########################################################################
class BloodType:
    A_PLUS = "A+"
    A_MINUS = "A-"
    AB_PLUS = "AB+"
    AB_MINUS = "AB-"
    B_PLUS = "B+"
    B_MINUS = "B-"
    O_PLUS = "O+"
    O_MINUS = "O-"
    A = "A"
    AB = "AB"
    B = "B"
    O = "O"
    OTHER = None
    BLOOD_LIST = [A_MINUS, A_PLUS, B_MINUS, B_PLUS, AB_MINUS, AB_PLUS, O_MINUS, O_PLUS]


class Human:
    """
    Basic human data
    """

    __MEASUREMENT = "m|kg"  # Metric system
    __VERSION = Version(1, 1, 1)  # Internal version class check

    def __init__(
        self,
        first_name: str,
        last_name: Optional[str] = None,
        birthday: Union[str, datetime, None] = None,
        birth_time: Optional[str] = None,
        gender: Union[bool, None] = None,
    ) -> None:
        """
        :param first_name: First name
        :param last_name: Last name
        :param birthday: Birthday in format: ``yyyy/mm/dd``
        :param birth_time: Birth time in format: ``hh:mm``
        :param gender: ``True``: Male; ``False``: Female (biologicaly)
        """
        # Name
        self.first_name = first_name
        self.last_name = last_name
        self.name = (
            f"{self.last_name}, {self.first_name}"
            if self.last_name is not None
            else self.first_name
        )

        # Birthday
        now = datetime.now()
        if birthday is None:
            modified_birthday = now.date()
        elif isinstance(birthday, str):
            for x in ["/", "-"]:
                birthday = birthday.replace(x, "/")
            modified_birthday = datetime.strptime(birthday, "%Y/%m/%d")
        else:
            modified_birthday = birthday
            # birthday = list(map(int, birthday.split("/")))
            # modified_birthday = date(*birthday)
            # modified_birthday = date(birthday[0], birthday[1], birthday[2])

        if birth_time is None:
            modified_birthtime = now.time()
        else:
            birth_time = list(map(int, birth_time.split(":")))  # type: ignore
            modified_birthtime = time(*birth_time)
            # modified_birthtime = time(birth_time[0], birth_time[1])

        self.birthday = modified_birthday.date()  # type: ignore
        self.birth_time = modified_birthtime

        self.birth = datetime(
            modified_birthday.year,
            modified_birthday.month,
            modified_birthday.day,
            modified_birthtime.hour,
            modified_birthtime.minute,
        )

        # Others
        self.gender: bool = gender  # type: ignore # True: Male; False: Female
        self.height: float = None  # type: ignore # centimeter
        self.weight: float = None  # type: ignore # kilogram
        self.blood_type: Union[str, BloodType] = BloodType.OTHER  # type: ignore

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({str(self.name)})"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        name = str(self.name)
        gender = "M" if self.is_male else "F"
        return f"{class_name}({name} ({self.age}|{gender}))"

    @classmethod
    def JohnDoe(cls):
        """
        Dummy Human for test

        Returns
        -------
        Human
            Dummy Human instance
        """
        temp = cls("John", "Doe", "1980/01/01", "00:00")
        temp.update({"gender": True, "height": 180, "weight": 80, "blood_type": "O+"})
        return temp

    @property
    def is_male(self) -> bool:
        """
        Check if male (biological)

        Returns
        -------
        bool
            | ``True``: Male
            | ``False``: Female
        """
        return self.gender

    @property
    def age(self):
        """
        Calculate age based on birthday

        Returns
        -------
        float
            Age

        None
            When unable to get ``self.birthday``
        """
        if self.birthday is not None:
            now = datetime.now()
            # age = now - self.birthday
            try:
                rdelta = relativedelta(now, self.birthday)
            except Exception:
                date_str = self.birthday
                if date_str is None:
                    self.birthday = datetime.now().date()
                else:
                    for x in ["/", "-"]:
                        date_str = date_str.replace(x, "/")
                    date = datetime.strptime(date_str, "%Y/%m/%d")
                    self.birthday = date
                rdelta = relativedelta(now, self.birthday)
            return round(rdelta.years + rdelta.months / 12, 2)
        else:
            return None

    @property
    def is_adult(self):
        """
        Check if ``self.age`` >= ``18``

        :rtype: bool
        """
        return self.age >= 18

    @property
    def bmi(self):
        r"""
        Body Mass Index (kg/m^2)

        Formula: :math:`\frac{weight (kg)}{height (m)^2}`

        - BMI < 18.5: Skinny
        - 18.5 < BMI < 25: normal
        - BMI > 30: Obesse

        Returns
        -------
        float
            BMI value

        None
            When unable to get ``self.height`` and ``self.weight``
        """
        try:
            temp = self.height / 100
            bmi = self.weight / (temp * temp)
            return round(bmi, 2)
        except Exception:
            return None

    # @property
    def dir_(self) -> list:
        """
        List property

        Returns
        -------
        list[str]
            List of available properties
        """
        return [x for x in self.__dir__() if not x.startswith("_")]

    def update(self, data: dict) -> None:
        """
        Update Human data

        Parameters
        ----------
        data : dict
            Data

        Returns
        -------
        None
        """
        self.__dict__.update(data)
        # return self


class Person(Human):
    """
    More detailed ``Human`` data
    """

    __VERSION = Version(1, 1, 1)  # Internal version class check

    def __init__(
        self,
        first_name: str,
        last_name: Optional[str] = None,
        birthday: Union[str, datetime, None] = None,
        birth_time: Optional[str] = None,
        gender: Union[bool, None] = None,
    ) -> None:
        super().__init__(first_name, last_name, birthday, birth_time, gender)
        self.address: str = None  # type: ignore
        self.hometown: str = None  # type: ignore
        self.email: str = None  # type: ignore
        self.phone_number: str = None  # type: ignore
        self.nationality = None  # type: ignore
        self.likes: list = None  # type: ignore
        self.hates: list = None  # type: ignore
        self.education = None  # type: ignore
        self.occupation: str = None  # type: ignore
        self.personality = None  # type: ignore
        self.note: str = None  # type: ignore

    @property
    def zodiac_sign(self):
        """
        Zodiac sign of ``Person``

        Returns
        -------
        str
            Zodiac sign

        None
            When unable to get ``self.birthday``
        """
        try:
            return zodiac_sign(self.birthday.day, self.birthday.month)
        except Exception:
            return None

    @property
    def zodiac_sign_13(self):
        """
        Zodiac sign of ``Person`` (13 zodiac signs version)

        Returns
        -------
        str
            Zodiac sign

        None
            When unable to get ``self.birthday``
        """
        try:
            return zodiac_sign(self.birthday.day, self.birthday.month, zodiac13=True)
        except Exception:
            return None

    @property
    def numerology(self) -> int:
        """
        Numerology number of ``Person``

        Returns
        -------
        int
            Numerology number
        """
        temp = f"{self.birthday.year}{self.birthday.month}{self.birthday.day}"
        return IntNumber(temp).add_to_one_digit(master_number=True)


class Human2:
    """W.I.P for cli"""

    def __init__(self, birthday_string: str, is_male: bool = True) -> None:
        """
        :param birthday_string: Format ``<yyyymmddhhmm>`` or ``<yyyymmdd>``
        """
        if len(birthday_string) == 12:
            day = datetime(
                year=int(birthday_string[:4]),
                month=int(birthday_string[4:6]),
                day=int(birthday_string[6:8]),
                hour=int(birthday_string[8:10]),
                minute=int(birthday_string[10:]),
            )
        else:
            day = datetime(
                year=int(birthday_string[:4]),
                month=int(birthday_string[4:6]),
                day=int(birthday_string[6:]),
            )
        self._date_str = birthday_string[:8]
        self.day = day
        self.is_male = is_male

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({str(self.day)})"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({str(self.day)})"

    def numerology(self) -> int:
        # numerology
        return IntNumber(self._date_str).add_to_one_digit(master_number=True)

    def _make_fengshui_check_query(self) -> str:
        """
        Generate query to check Feng-shui
        """
        params = {
            "ngay": self.day.day.__str__().rjust(2, "0"),
            "thang": self.day.month.__str__().rjust(2, "0"),
            "nam": self.day.year,
            "gio": self.day.hour.__str__().rjust(2, "0"),
            "phut": self.day.minute.__str__().rjust(2, "0"),
            "gioitinh": "nam" if self.is_male else "nu",
        }
        output = urlencode(params)
        return output

    def fs(self, number_string: str) -> float:
        # fengshui
        base = "https://thanglongdaoquan.vn/boi-so-tai-khoan/?taikhoan="
        link = f"{base}{number_string}&{self._make_fengshui_check_query()}"
        soup = soup_link(link)
        val = soup.find_all(class_="total_point")[0].get_text()
        pattern = r"([0-9.]{1,3})/10"
        res = re.findall(pattern, val)[0]
        return float(res)

    def info(self) -> dict:
        out = {
            "numerology": self.numerology(),
            "zodiac": zodiac_sign(self.day.day, self.day.month),
        }
        return out


# Run
###########################################################################
if __name__ == "__main__":
    # print(Person.JohnDoe().__dict__)
    pass
