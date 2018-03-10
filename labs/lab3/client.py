import zmq
import sys
import threading
import json


def client_window():
    poller = zmq.Poller()
    poller.register(sock_sub, zmq.POLLIN)

    while True:
        usr_input = input("[{0}]>".format(usr_name))
        data = {}
        data['username'] = usr_name
        data['message'] = usr_input
        sock_req.send_json(data)
        resp_msg = sock_req.recv().decode()
        while True:
            socks = dict(poller.poll())
            if socks[sock_sub] == zmq.POLLIN:
                data1 = sock_sub.recv_json()
                username, msg = data1['username'], data1['message']
                if username != usr_name:
                    print('[{0}]: {1}'.format(username, msg))
                else:
                    break


if __name__ == '__main__':
    context = zmq.Context()

    # Define the socket using the "Context"
    sock_sub = context.socket(zmq.SUB)
    sock_sub.connect("tcp://127.0.0.1:5678")
    sock_sub.setsockopt_string(zmq.SUBSCRIBE, "")

    sock_req = context.socket(zmq.REQ)
    sock_req.connect("tcp://127.0.0.1:5679")

    usr_name = sys.argv[1]

    print("[{0}] joined the server".format(usr_name))
    client_window()