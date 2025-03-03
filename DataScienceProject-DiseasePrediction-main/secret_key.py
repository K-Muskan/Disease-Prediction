import secrets

admin_key = secrets.token_urlsafe(32)
print(f"Your secret admin key is: {admin_key}")