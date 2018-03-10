import zmq
import threading

# ZeroMQ Context

context = zmq.Context()

# Define the socket using the "Context"
sock_pub = context.socket(zmq.PUB)
sock_pub.bind("tcp://127.0.0.1:5678")

sock_rep = context.socket(zmq.REP)
sock_rep.bind("tcp://127.0.0.1:5679")


# Run a simple "Echo" server
def chat_window():
    while True:
        msg = sock_rep.recv_json()
        sock_rep.send_string('0')
        sock_pub.send_json(msg)


if __name__ == "__main__":
    # t = threading.Thread(target=chat_window())
    # t.daemon = True
    # t.start()
    chat_window()
