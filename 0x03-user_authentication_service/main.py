#!/usr/bin/env python3
"""Module for end to end integration"""

import requests


def register_user(EMAIL, PASSWD):
    """Test the register_user endpoint"""
    r = requests.post(f"{URL}/users", {"email": EMAIL, "password": PASSWD})
    assert r.status_code == 200
    assert r.json() == {"email": EMAIL, "message": "user created"}


def log_in_wrong_password(EMAIL, NEW_PASSWD):
    """Test the log_in endpoint when a wrong password is given"""
    r = requests.post(f"{URL}/sessions", {"email": EMAIL,
                                          "password": NEW_PASSWD})
    assert r.status_code == 401


def profile_unlogged():
    """Test if the profile is not logged in"""
    r = requests.get(f"{URL}/profile", cookies={"session_id": " "})
    assert r.status_code == 403


def log_in(EMAIL, PASSWD):
    """Test if the user is logged in"""
    r = requests.post(f"{URL}/sessions", {"email": EMAIL, "password": PASSWD})
    assert r.status_code == 200
    assert r.json() == {"email": EMAIL, "message": "logged in"}
    session_id = r.cookies.get("session_id")

    return session_id


def profile_logged(session_id):
    """Test if profile is still logged in"""
    r = requests.get(f"{URL}/profile", cookies={"session_id": session_id})
    assert r.status_code == 200
    assert r.json() == {"email": EMAIL}


def log_out(session_id):
    """Test if the user is logged out"""
    r = requests.delete(f"{URL}/sessions", cookies={"session_id": session_id})
    assert r.status_code == 200
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(EMAIL):
    """Test the reset_password_token endpoint"""
    r = requests.post(f"{URL}/reset_password", {"email": EMAIL})
    assert r.status_code == 200
    reset_token = r.json().get("reset_token")
    assert r.json() == {"email": EMAIL, "reset_token": reset_token}
    return reset_token


def update_password(EMAIL, reset_token, NEW_PASSWD):
    """Test the update_password endpoint updates password"""
    r = requests.put(f"{URL}/reset_password", {
        "email": EMAIL,
        "reset_token": reset_token,
        "NEW_PASSWD": NEW_PASSWD
    })
    assert r.status_code == 200
    assert r.json() == {"email": EMAIL, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://localhost:5000"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
