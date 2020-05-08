# Jennie Klein, 324686492, Renana Malkiel, 209125806

import hashlib

class Node:

    def __init__(self, left, right, hash_value=None):
        self.left = left
        self.right = right
        self.hash_value = self.calc_hash() if not hash_value else hash_value


    def calc_hash(self):
        return str(hashlib.sha256((self.left.hash_value + self.right.hash_value).encode()).hexdigest())

