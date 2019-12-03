import concurrent.futures
import logging
import queue
import random
import threading
import time
import socket

TCP_IP = '192.168.43.195' # <-current IP from Jaakkos phone. default: 127.0.0.1
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Connection address:', addr)

def producer(queue, event):
    """Pretend we're getting a number from the network."""
    while not event.is_set():
        # message = random.randint(1, 101)
        data = conn.recv(BUFFER_SIZE)
        logging.info("Producer got message: %s", data)
        queue.put(data)
        print ("received data:", data.decode('utf-8'))
        conn.send(data)  # echo
    

    logging.info("Producer received event. Exiting")

#def consumer(queue, event):
    """Pretend we're saving a number in the database."""
    #while 1: # not event.is_set() or not queue.empty():
        #data = queue.get()
        #logging.info(
            #"Consumer storing message: %s (size=%d)", data, queue.qsize()
        #)

    #logging.info("Consumer received event. Exiting")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    pipeline = queue.Queue()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()