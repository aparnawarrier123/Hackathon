from werkzeug.security import generate_password_hash, check_password_hash

h = generate_password_hash("mypassword")
print(h)
print(check_password_hash(h, "mypassword"))
print(check_password_hash(h, "wrong"))