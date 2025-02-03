from datetime import datetime, timezone, date, timedelta
from typing import Union, Optional
from pytz import timezone as tz


DEFAULT_TIME_ZONE = "America/Mexico_City"

NON_WORKING_DAYS = [
    (1, 1),  # New Year's Day
    (2, 3),  # Constitution Day
    (2, 17),  # Benito Juarez Day
    (5, 1),  # Labor Day
    (9, 16),  # Independence Day
    (11, 17),  # Revolution Day
    (12, 12),  # Revolution Day
    (12, 25),  # Christmas Day
]


class Calendar():

    """
    Given a local zone, return the actual date
    """
    @staticmethod
    def get_default_datetime() -> datetime:
        tz_arg = tz(DEFAULT_TIME_ZONE)
        return datetime.now(tz_arg)

    @staticmethod
    def get_mexican_datetime() -> datetime:
        return datetime.now(tz(DEFAULT_TIME_ZONE))

    @staticmethod
    def add_default_timezone(date: datetime) -> datetime:
        tz_arg = tz(DEFAULT_TIME_ZONE)
        return tz_arg.localize(date)

    @staticmethod
    def get_default_date() -> datetime:
        return datetime.now(timezone.utc).date()

    @staticmethod
    def get_default_mexican_date() -> datetime:
        return datetime.now(tz(DEFAULT_TIME_ZONE)).date()

    @staticmethod
    def from_utc_to_local(utc_date: Optional[datetime] = None, tz_data: Optional[str] = None) -> datetime:
        if utc_date is None:
            utc_date = datetime.now(timezone.utc)
        if tz_data is None:
            tz_data = DEFAULT_TIME_ZONE
        return utc_date.astimezone(tz(DEFAULT_TIME_ZONE))

    @staticmethod
    def from_local_to_utc(local_date: Optional[datetime] = None) -> datetime:
        if not local_date:
            local_date = datetime.now(tz(DEFAULT_TIME_ZONE))
        return local_date.astimezone(timezone.utc)

    @staticmethod
    def get_date_string(date: date) -> str:
        months_spanish = [
            'Enero',
            'Febrero',
            'Marzo',
            'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        return date.strftime(f"%d de {months_spanish[date.month - 1]} de %Y")

    @staticmethod
    def is_working_day(date: Union[datetime, date]) -> bool:
        if (date.month, date.day) in NON_WORKING_DAYS:
            return False
        if date.weekday() >= 5:
            return False
        return True

    @staticmethod
    def get_next_working_day(time: Optional[Union[datetime, date]] = None) -> datetime:
        if time is None:
            time = datetime.now(tz(DEFAULT_TIME_ZONE))
        while not Calendar.is_working_day(time):
            time += timedelta(days=1)
        return time

    @staticmethod
    def utc_from_local_date_str(date_str: str, format: str) -> datetime:
        if len(date_str) == 0:
            return None

        date = datetime.strptime(date_str, format)

        if date.tzinfo is None:
            date = Calendar.add_default_timezone(date)

        return Calendar.from_local_to_utc(date)

    @staticmethod
    def is_local_morning() -> bool:
        return Calendar.get_mexican_datetime().hour < 12
