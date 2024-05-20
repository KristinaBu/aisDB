from PyQt5.QtCore import QDate


def is_database_connected(db):
    return db.isOpen()


def is_not_empty(value):
    return bool(value.strip())


def is_not_future_date(date):
    return date <= QDate.currentDate()


def is_date_order_valid(earlier_date, later_date):
    return later_date >= earlier_date and 150 >= later_date.year() - earlier_date.year() >= 10
