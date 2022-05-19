##### https://github.com/grahammitchell/google-authenticator/blob/master/google-authenticator.py #####
##### https://towardsdatascience.com/do-you-know-python-has-a-built-in-database-d553989c87bd #####
from . import google_2fa_encrypt
from datetime import datetime, timezone
import hmac, base64, struct, hashlib, time, os, sqlite3

GOOGLE_TOTP_TIME = 30
SECRETS = {}
PASSWORD = "adminadmin"

def get_hotp_token(secret, intervals_no):
	"""This is where the magic happens."""
	key = base64.b32decode(normalize(secret), True) # True is to fold lower into uppercase
	msg = struct.pack(">Q", intervals_no)
	h = bytearray(hmac.new(key, msg, hashlib.sha1).digest())
	o = h[19] & 15
	h = str((struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000)
	return prefix0(h)

def get_totp_token(secret, totp_time):
	"""The TOTP token is just a HOTP token seeded with every 30 seconds."""
	return get_hotp_token(secret, intervals_no=int(time.time())//totp_time)

def normalize(key):
	"""Normalizes secret by removing spaces and padding with = to a multiple of 8"""
	k2 = key.strip().replace(' ','')
	# k2 = k2.upper()	# skipped b/c b32decode has a foldcase argument
	if len(k2)%8 != 0:
		k2 += '='*(8-len(k2)%8)
	return k2

def prefix0(h):
	"""Prefixes code with leading zeros if missing."""
	if len(h) < 6:
		h = '0'*(6-len(h)) + h
	return h

def get_totp_time(totp_time):
    unix_time = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    time_counter = int(totp_time - ((unix_time / 1000) % totp_time))
    return str(time_counter)

def load_secrets():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        with open(dir_path + '/secrets.txt') as f:
            global SECRETS
            try:
                lines = f.readlines()
                br = 0
                for i, line in enumerate(lines):
                    SECRETS[lines[br].strip()] = lines[br+1].strip()
                    br = br+2
            except Exception as e:
                pass
    except Exception:
        print("File secrets.txt doesn't exist!")

def get_secrets():
    load_secrets()
    secrets_dict = {}
    for i, (k,v) in enumerate(SECRETS.items()):
        print("**************************** Email {} ***************************".format(i+1))
        print("Email: {}".format(k))
        print("2FA: {}".format(v))
        print("TOTP: {}".format(get_totp_token(v, GOOGLE_TOTP_TIME)))
        print("**************************** Email {} ***************************".format(i+1))
        """ secrets_dict_temp = {
                "Email": k,
                "2FA": v,
                "TOTP": get_totp_token(v, GOOGLE_TOTP_TIME)
            } """
        sqlite3_db_add(google_2fa_encrypt.encode(k, PASSWORD), google_2fa_encrypt.encode(v, PASSWORD))
        secrets_dict[k] = [v, get_totp_token(v, GOOGLE_TOTP_TIME)]
    #sqlite3_db_read()
    #return secrets_dict
    return sqlite3_db_read()

def get_valid_time():
    valid_time = get_totp_time(GOOGLE_TOTP_TIME)
    print("\nTOTP time left: {}s".format(valid_time))
    return valid_time

def sqlite3_create_db():
    connection = sqlite3.connect('secrets.db')
    with connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS SECRETS (
                email TEXT,
                key2fa TEXT,
                UNIQUE(email, key2fa)
            );
        """)
    return connection

def sqlite3_db_add(email, key2fa):
    sql = 'INSERT OR IGNORE INTO SECRETS (email, key2fa) values(?, ?)'
    data = [
        (email, key2fa),
    ]
    connection = sqlite3_create_db()
    with connection:
        connection.executemany(sql, data)

def sqlite3_db_read():
    connection = sqlite3_create_db()
    secrets_dict = {}
    with connection:
        data = connection.execute("SELECT * FROM SECRETS")
        print("**************************** Database ***************************")
        for row in data:
            email = google_2fa_encrypt.decode(bytes(row[0]), PASSWORD)
            key2fa = google_2fa_encrypt.decode(bytes(row[1]), PASSWORD)
            secrets_dict[email] = [key2fa, get_totp_token(key2fa, GOOGLE_TOTP_TIME)]
            print(email)
            print(key2fa)
        print("**************************** Database ***************************")
    return secrets_dict


if __name__ == "__main__":
    """ get_secrets()
    get_valid_time() """

    
