#!/usr/bin/env python3

import selectors
import socket
import time

PORT = 4020
TIME_OUT = 10
CHAT_SIZE = 50
print ("Multi client chat server, using telnet, programmed in Python.")
print ("To connect:")
print ("    telnet 127.0.0.1", PORT)
print ("")
print ("Everything typed by one chat user will be copied to other chat users.")
print ("Typing 'quit' on telnet sessions will disconnect.")

listen_sock = socket.socket()

'''
SO_REUSEADDR

Unix Network Programming, p103.
  A common error from bind is EADDRINUSE
Unix Network Programming, p203.
  SO_REUSEADDR socket option should always be used in the server
  before the call to bind
Unix Network Programming, p210
  All TCP servers should specify this socket option
'''
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

listen_sock.bind( ('0.0.0.0', PORT ) )
listen_sock.listen(5)

selector = selectors.DefaultSelector()
selector.register(listen_sock, selectors.EVENT_READ)
sock_to_expiry = dict();
select_time_out = None;
while (True):
  events = selector.select(select_time_out)

  now = int(time.time());  # integer for zero comparison
  finished_socks = []
  for selector_key,mask in events:
    #print(selector_key);
    #print(mask);
    read_sock = selector_key.fileobj
    if read_sock == listen_sock:
      conn, addr = listen_sock.accept()
      print ('accepted client',conn.fileno(),'from',addr)
      conn.setblocking(False)
      selector.register(conn, selectors.EVENT_READ)
      sock_to_expiry[conn] = now + TIME_OUT
      continue;

    read_fd = read_sock.fileno();
    data = read_sock.recv(CHAT_SIZE);
    read_string = data.rstrip().decode();
    sock_to_expiry[read_sock] = now + TIME_OUT

    # ignore empty string
    if read_string == "":
      continue

    # len(data) == 0
    #   client has disconnected
    # read_string == "quit"
    #   user types "quit" to tell server to close connection
    if len(data) == 0 or read_string == "quit":
      print ("Client sock", read_sock.fileno(), "closed connection")
      finished_socks.append(read_sock)
      continue

    print("read:", read_string);
    for write_sock in sock_to_expiry.keys():
      if write_sock == read_sock:
        continue
      write_sock.send(data)

  select_time_out = None
  for sock in sock_to_expiry.keys():
    if sock in finished_socks:
      continue

    expiry = sock_to_expiry[sock]
    remainder = expiry - now
    if remainder <= 0:
      print ("Client sock", sock.fileno(), "timed out. Now closing.")
      finished_socks.append(sock);
      continue
    if select_time_out == None:
      select_time_out = remainder
      continue
    if remainder < select_time_out:
      select_time_out = remainder
  print ("select_time_out:", select_time_out)

  for sock in finished_socks:
    selector.unregister(sock)
    del sock_to_expiry[sock]
    sock.close()


