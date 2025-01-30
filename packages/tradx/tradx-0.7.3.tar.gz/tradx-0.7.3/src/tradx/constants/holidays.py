"""
This module defines a list of holidays for the years 2024 and 2025.

The holidays are represented as `datetime.date` objects and include major
festivals and public holidays such as Christmas, Mahashivratri, Holi, 
Id-Ul-Fitr, Shri Mahavir Jayanti, Dr. Baba Saheb Ambedkar Jayanti, 
Good Friday, Maharashtra Day, Independence Day, Ganesh Chaturthi, 
Mahatma Gandhi Jayanti/Dussehra, Diwali Laxmi Pujan, Diwali-Balipratipada, 
and Prakash Gurpurb Sri Guru Nanak Dev.

The holidays list can be used for various purposes such as checking if a 
given date is a holiday, scheduling events, or generating holiday calendars.
"""
from datetime import datetime

holidays = [
    datetime(2024, 12, 25).date(),  # Christmas
    datetime(2025, 2, 26).date(),  # Mahashivratri
    datetime(2025, 3, 14).date(),  # Holi
    datetime(2025, 3, 31).date(),  # Id-Ul-Fitr (Ramadan Eid)
    datetime(2025, 4, 10).date(),  # Shri Mahavir Jayanti
    datetime(2025, 4, 14).date(),  # Dr. Baba Saheb Ambedkar Jayanti
    datetime(2025, 4, 18).date(),  # Good Friday
    datetime(2025, 5, 1).date(),  # Maharashtra Day
    datetime(2025, 8, 15).date(),  # Independence Day
    datetime(2025, 8, 27).date(),  # Ganesh Chaturthi
    datetime(2025, 10, 2).date(),  # Mahatma Gandhi Jayanti/Dussehra
    datetime(2025, 10, 21).date(),  # Diwali Laxmi Pujan
    datetime(2025, 10, 22).date(),  # Diwali-Balipratipada
    datetime(2025, 11, 5).date(),  # Prakash Gurpurb Sri Guru Nanak Dev
    datetime(2025, 12, 25).date(),  # Christmas
]
