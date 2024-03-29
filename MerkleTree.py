# Jennie Klein, 324686492, Renana Malkiel, 209125806
import hashlib

root = None
num_leaves = None


class Node:

    def __init__(self, left, right, hash_value=None):
        self.left = left
        self.right = right
        self.hash_value = self.calc_hash() if not hash_value else hash_value

    def calc_hash(self):
        return str(hashlib.sha256((self.left.hash_value + self.right.hash_value).encode()).hexdigest())


def request_handler(user_request):
    user_request = user_request.split(" ")
    func = switcher.get(user_request[0], illegal_request)
    func(user_request[1:])


'''
function that initializes the leaves and create the recursive_tree function to get the Merkle Tree
'''


def make_tree(user_input):
    nodes = []
    for str in user_input:
        nodes.append(Node(None, None, str))
    global root
    root = recursive_tree(nodes)
    print(root.hash_value)
    global num_leaves
    num_leaves = len(nodes)


'''
Creating Merkle Tree -
Where each node is the result of the hash function of the two sons' concatenation.
'''


def recursive_tree(nodes):
    if len(nodes) == 1:
        return nodes[0]
    lst = list(zip(nodes, nodes[1:]))[::2]
    new_nodes = []
    for left, right in lst:
        new_nodes.append(Node(left, right))
    return recursive_tree(new_nodes)


'''
create a proof for the leaf index that given
'''


def create_proof(index):
    if root == None:
        exit(0)
    if int(index[0]) >= num_leaves:
        exit(0)
    path = find_path(int(index[0]))
    output = []
    node = root
    while len(path) != 0:
        if path.pop(0) == "l":
            output.append("r " + node.right.hash_value)
            node = node.left
        else:
            output.append("l " + node.left.hash_value)
            node = node.right
    output.reverse()
    print(' '.join(output))


'''
check given proof
'''


def check_proof(input):
    leaf = input[0]
    local_root = input[1]
    proof = input[2:]
    hash_value = leaf
    lst = list(zip(proof, proof[1:]))[::2]
    for direction, node in lst:
        if direction == "l":
            hash_value = hashlib.sha256((node + hash_value).encode()).hexdigest()
        elif direction == "r":
            hash_value = hashlib.sha256((hash_value + node).encode()).hexdigest()
        else:
            exit(0)
    print(local_root == hash_value)


'''
 returns a string of the path to the requested index
'''


def find_path(index):
    index += num_leaves
    path = []
    while index != 1:
        path.append("l") if index % 2 == 0 else path.append("r")
        index //= 2
    path.reverse()
    return path


'''
finds the number of times needed to change the nonce in order to find a hash value lower than the difficulty
'''


def nonce(difficuty):
    if root is None:
        exit(0)
    if not difficuty[0].isdigit():
        exit(0)
    i = 0
    hash_result = str(hashlib.sha256((str(i) + root.hash_value).encode()).hexdigest())
    while not hash_result.startswith("0" * int(difficuty[0])):
        i += 1
        hash_result = str(hashlib.sha256((str(i) + root.hash_value).encode()).hexdigest())
    print(i, hash_result)


switcher = {
    "1": make_tree,
    "2": create_proof,
    "3": check_proof,
    "4": nonce
}


def illegal_request(input):
    exit(0)


if __name__ == '__main__':
    user_input = input()
    while user_input != '5':
        request_handler(user_input)
        user_input = input()
