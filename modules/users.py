import openpyxl
import random


def get_user(file):
    students = openpyxl.open(file, read_only=True)
    sheet = students.active

    ws = students.Sheets(sheet)
    begrow = 1
    endrow = ws.UsedRange.Rows.Count
    for row in range(begrow, endrow + 1):  # just an example
        if ws.Range('A{}'.format(row)).Value is None:
            ws.Range('A{}'.format(row)).EntireRow.Delete(Shift=-4162)  # shift up

        return sheet


def generate_login():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    login = ''
    for i in range(8):
        password += random.choice(chars)
    for i in range(8):
        login += random.choice(chars)
    return login, password
