import hashlib
import base64
import os

##function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

##creating a protected file
def create_protected_file(path, password, content=""):
   
    ##check if file already exists
    if os.path.exists(path):
        return "File already exists."

    ##hashing the password
    password_hash = hash_password(password)
    ##store content encoded 
    encoded_content = base64.b64encode(content.encode()).decode()

    with open(path, "w") as f:
        f.write("HASH:" + password_hash + "\n")
        f.write(encoded_content)

    return "Protected file created successfully."


##function to read protected file
def read_protected_file(path, password):
    if not os.path.exists(path):
        return "File does not exist."

    with open(path, "r") as f:
        stored_hash_full = f.readline().strip()
        stored_hash =  stored_hash_full[len("HASH:"):]
        encoded_content = f.read()

    if hash_password(password) != stored_hash:
        return "Access denied: Incorrect password."

    ##showing the decoded content
    decoded_content = base64.b64decode(encoded_content).decode()
    return decoded_content

##check protected file
def is_protected_file(path):
    try:
        with open(path, "r") as f:
            first_line = f.readline().strip()
        return first_line.startswith("HASH:")
    except:
        return False