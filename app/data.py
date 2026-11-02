from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
fake_staff_db = {
    "yellow": {
        "username": "yellow",
        "full_name": "Yellow Hello",
        "disabled": False,
        "hashed_password": password_hash.hash("secret"),
    },
    "blue": {
        "username": "blue",
        "full_name": "Blue Sky",
        "disabled": True,
        "hashed_password": password_hash.hash("secret2"),
    },
}
fake_books={1: {"title": "Dune", "available": True}, 2: {"title": "Emma", "available": False}}
fake_loans_db={}