import openpyxl
import random

def get_user(file):
	students=openpyxl.open(file,read_only=True)
	sheet=students.active


	return sheet

def generate_login():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password=''
    login=''
    for i in range(8):
        password += random.choice(chars)
    for i in range(8):
        login += random.choice(chars)
    return login,password