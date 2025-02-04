# test_api.py
import requests
import random
import string

BASE_URL = "https://finceptapi.share.zrok.io"  # or your real URL

def random_username():
    return "testuser_" + ''.join(random.choices(string.ascii_lowercase, k=6))

def main():
    username = random_username()
    email = f"{username}@example.com"
    password = "TestPass123!"
    register_payload = {
        "username": username,
        "email": email,
        "password": password
    }
    r = requests.post(f"{BASE_URL}/register", json=register_payload)
    print("Register:", r.status_code, r.json())

    otp = 111111  # works if TESTING_MODE=True
    verify_payload = {
        "email": email,
        "otp": otp
    }
    r = requests.post(f"{BASE_URL}/verify-otp", json=verify_payload)
    print("Verify OTP:", r.status_code, r.json())
    api_key = r.json().get("api_key", "")

    login_payload = {
        "email": email,
        "password": password
    }
    r = requests.post(f"{BASE_URL}/login", json=login_payload)
    print("Login:", r.status_code, r.json())

    headers = {"X-API-Key": api_key}
    r = requests.get(f"{BASE_URL}/user-details", headers=headers)
    print("User Details:", r.status_code, r.json())

    link_payload = {"amount_in_inr": 50}
    r = requests.post(f"{BASE_URL}/create-payment-link", json=link_payload, headers=headers)
    print("Create Payment Link:", r.status_code, r.json())
    if r.status_code == 200:
        link_data = r.json()
        payment_link = link_data.get("payment_link")
        print("Payment Link:", payment_link)
        print("Open the link in a browser to complete payment.")

    input("Press Enter after payment is completed...")

    r = requests.get(f"{BASE_URL}/user-details", headers=headers)
    print("Updated User Details:", r.status_code, r.json())

if __name__ == "__main__":
    main()
