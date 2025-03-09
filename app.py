import streamlit as st
import json
import os
import re
import random
import string

# File to store saved credentials
CREDENTIALS_FILE = "credentials.json"

# Function to generate a random password
def generate_password(length=8, use_digits=True, use_special=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to check password strength
def check_password_strength(password):
    score = 0
    tips = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        tips.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        tips.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        tips.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        tips.append("❌ Include at least one special character (!@#$%^&*).")

    # Strength Rating
    if score == 4:
        return "✅ Strong Password!", "Strong"
    elif score == 3:
        return "⚠️ Moderate Password - Consider adding more security features.", "Moderate"
    else:
        return "\n".join(tips), "Weak"

# Function to load stored credentials
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save credentials
def save_credentials(credentials):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file, indent=4)

# Load existing credentials
credentials = load_credentials()

# Streamlit UI
st.title("🔐 Secure Login Page")

email = st.text_input("📧 Email")

# Autofill password if email exists
password_placeholder = ""
if email in credentials:
    st.info("Existing user detected. Autofilling password...")
    password_placeholder = credentials[email]  # Autofilled password

password = st.text_input("🔑 Password", value=password_placeholder, type="password")

# Password strength check
if password:
    result, strength = check_password_strength(password)
    if strength == "Strong":
        st.success(result)
    elif strength == "Moderate":
        st.warning(result)
    else:
        st.error("❌ Weak Password - Improve it using these tips:")
        for tip in result.split("\n"):
            st.write(tip)

remember_me = st.checkbox("💾 Remember Me")

# Login button
if st.button("🔓 Login"):
    if email and password:
        if email in credentials and credentials[email] == password:
            st.success(f"🎉 Welcome back, {email}!")
        else:
            st.warning("🛑 Incorrect email or password!")
        
        # Store credentials if "Remember Me" is checked
        if remember_me:
            credentials[email] = password
            save_credentials(credentials)
            st.info("🔒 Password saved securely!")
    else:
        st.error("⚠️ Please enter both email and password")
