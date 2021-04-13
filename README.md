# Chrome-Password-Extractor Project

Being able to extract saved passwords in the most popular browser is a useful and handy task in forensics, as Chrome saves passwords locally in a sqlite3 database. However, this can be time consuming when doing it manually.

Since Chrome saves a lot of your browsing data locally in your disk, In this tutorial, we will write Python code to extract saved passwords in Chrome on your Windows machine, we will also make a quick script to protect ourselves from such attack.

We will install required libraries:

1.	PyCryptodome - PyCryptodome is a self-contained Python package of low-level cryptographic primitives. It brings the following enhancements:

  	Authenticated encryption modes (GCM, CCM, EAX, SIV, OCB)
  	Accelerated AES on Intel platforms via AES-NI
  	Elliptic curves cryptography (NIST P-256, P-384 and P-521 curves only)
  	SHA-3 (including SHAKE XOFs), truncated SHA-512 and BLAKE2 hash algorithms, etc.
  	Symmetric ciphers:
    o	AES
    o	Single and Triple DES (legacy)
    o	CAST-128 (legacy)
    o	RC2 (legacy)
  	Traditional modes of operations for symmetric ciphers:
    o	ECB
    o	CBC
    o	CFB
    o	OFB

2.	pypiwin32 - Python extensions for Microsoft Windows Provides access to much of the Win32 API, the ability to create and use COM objects, and the Pythonwin environment.

3.	Pyfiglet & Termcolor – for beautify, render and add colour to our script/project name.

Following functions are used:
  	get_chrome_datetime() function is responsible for converting chrome date format into a human readable datetime format.
  	get_encryption_key() function extracts and decodes the AES key that was used to encrypt the passwords, this is stored in "%USERPROFILE%\AppData\Local\Google\Chrome\User
    Data\Local State" path as a JSON file.
  	decrypt_password() takes the encrypted password and the AES key as arguments, and returns a decrypted version of the password.

First, we get the encryption key using the previously defined get_encryption_key() function, then we copy the sqlite database (located at "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\default\Login Data" that has the saved passwords to the current directory and connects to it, this is because the original database file will be locked when Chrome is currently running.

After that, we make a select query to logins table and iterate over all login rows, we also decrypt each password and reformat the date_created () and date_last_used() date times to more human readable format.

Finally, we print the credentials and remove the database copy from the current directory.

References:
http://timgolden.me.uk/pywin32-docs/win32crypt.html
