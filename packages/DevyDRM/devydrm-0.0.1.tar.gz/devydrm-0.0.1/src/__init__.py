import random
import string
import hashlib

class DevyDRM:

    def generate_license_key(self, length=16):
        self.key = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return hashlib.sha256(self.key.encode()).hexdigest(), self.key

    def verify_license_key(self, key1):
        return hashlib.sha256(self.key.encode()).hexdigest() == hashlib.sha256(key1.encode()).hexdigest()

    def get_license_key(self):
        return self.key