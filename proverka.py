import os

print("Database Name:", os.getenv("NAME"))
print("Database User:", os.getenv("DB_USER"))
print("Database Password:", os.getenv("PASSWORD"))
print("Database Host:", os.getenv("HOST"))
print("Database Port:", os.getenv("PORT"))
