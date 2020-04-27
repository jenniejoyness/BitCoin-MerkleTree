from Node import Node
import hashlib

root = None
num = None


def request_handler(client_request):
    client_request = client_request.split(" ")
    func = switcher.get(client_request[0], illegal_request)
    func(client_request[1:])


def make_tree(user_input):
    nodes = []
    for str in user_input:
        nodes.append(Node(None, None, str))
    global root
    root = recursive_tree(nodes)
    print(root.hash_value)
    global num
    num = len(nodes)


def recursive_tree(nodes):
    if len(nodes) == 1:
        return nodes[0]
    lst = list(zip(nodes, nodes[1:]))[::2]
    new_nodes = []
    for left, right in lst:
        new_nodes.append(Node(left, right))
    return recursive_tree(new_nodes)


def create_proof(index):
    if root == None:
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


def check_proof(input):
    leaf = input[0]
    local_root = input[1]
    proof = input[2:]
    hash_value = leaf
    lst = list(zip(proof, proof[1:]))[::2]
    for direction, node in lst:
        if direction == "l":
            hash_value = hashlib.sha256((node + hash_value).encode()).hexdigest()
        else:
            hash_value = hashlib.sha256((hash_value + node).encode()).hexdigest()
    print(local_root == hash_value)


def find_path(index):
    index += num
    path = []
    while index != 1:
        path.append("l") if index % 2 == 0 else path.append("r")
        index //= 2
    path.reverse()
    return path


def nonce(difficuty):
    if root == None:
        exit(0)
    i = 0
    hash_result = str(hashlib.sha256((str(i) + root.hash_value).encode()).hexdigest())
    while hash_result.startswith("0" * int(difficuty[0])) == False:
        i += 1
        hash_result = str(hashlib.sha256((str(i) + root.hash_value).encode()).hexdigest())
    print(i, hash_result)


switcher = {
    "1": make_tree,
    "2": create_proof,
    "3": check_proof,
    "4": nonce
}


def illegal_request():
    print("error")


if __name__ == '__main__':

    user_input = input()
    while user_input != '5':
        request_handler(user_input)
        user_input = input()
