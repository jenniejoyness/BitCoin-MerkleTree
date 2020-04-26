from Node import Node


def request_handler(client_request):
    client_request = client_request.split(" ")
    func = switcher.get(client_request[0], illegal_request)
    func(client_request[1:])

def make_tree(user_input):
    nodes = []
    for str in user_input:
        nodes.append(Node(None,None,str))
    root = recursive_tree(nodes)
    return root

def recursive_tree(nodes):
    if len(nodes) == 1:
        return nodes[0]
    lst = list(zip(nodes, nodes[1:]))[::2]
    new_nodes = []
    for left, right in lst:
        new_nodes.append(Node(left, right))
    return make_tree(new_nodes)


switcher = {
    "1": make_tree
}


def illegal_request():
    print("error")


if __name__ == '__main__':
    user_input = input()
    request_handler(user_input)
