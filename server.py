#!/usr/bin/env python3

import selectors
import socket

'''
  printf ("Multi client chat server, using telnet, programmed in C.\n");
  printf ("To connect:\n");
  printf ("    telnet 127.0.0.1 %d\n", PORT);
  printf ("\n");
  printf ("Everything typed by one chat user will be copied to other chat users.\n");
  printf ("Typing 'quit' on telnet sessions will disconnect.\n");

'''
PORT = 4025
TIME_OUT = 10
CHAT_SIZE = 50
print ("Multi client chat server, using telnet, programmed in C.")
print ("To connect:")
print ("    telnet 127.0.0.1", PORT)
print ("")
print ("Everything typed by one chat user will be copied to other chat users.")
print ("Typing 'quit' on telnet sessions will disconnect.")

print ("socket.gethostname(): ", socket.gethostname());

listen_sock = socket.socket(
  socket.AF_INET, socket.SOCK_STREAM
  )

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

listen_sock.bind( ('127.0.0.1', PORT ) )
listen_sock.listen(5)
print ("listen_sock",listen_sock);

selector = selectors.DefaultSelector()
selector.register(listen_sock, selectors.EVENT_READ)
client_socks = set();
while (True):
  events = selector.select(TIME_OUT)
  for selector_key,mask in events:
    #print(selector_key);
    #print(mask);
    read_sock = selector_key.fileobj;
    if read_sock == listen_sock:
      conn, addr = listen_sock.accept()
      print ('accepted client',conn.fileno(),'from',addr);
      conn.setblocking(False);
      selector.register(conn, selectors.EVENT_READ)
      client_socks.add(conn);
      continue;

    read_fd = read_sock.fileno();
    data = read_sock.recv(CHAT_SIZE);
    read_string = data.rstrip().decode();
    
    if len(data) == 0 or read_string == "quit":
      print ("client closed connection")
      selector.unregister(read_sock)
      client_socks.remove(read_sock)
      read_sock.close()
      continue;
    
    print("read:", read_string);
    for write_sock in client_socks:
      if write_sock == read_sock:
        continue
      write_sock.send(data)

  