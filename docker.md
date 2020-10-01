# Running Docker

    # Don't forget the trailing dot in this command
    docker image build --tag multi_chat_python:latest -f Dockerfile .

    # Stop the previous multi_chat_python docker instance, if there is one
    docker container stop multi_chat_python

    docker container run \
      --rm \
      --detach \
      --name multi_chat_python \
      --publish 127.0.0.1:4020:4020 \
      multi_chat_python:latest

    # Do we see the docker multi_chat_python?
    docker container ls

    # From one terminal
    telnet 127.0.0.1 4020

    # From another terminal
    telnet 127.0.0.1 4020

    # From yet another terminal
    telnet 127.0.0.1 4020

    # Optional: if you want to shell into the docker instance
    docker container exec --interactive --tty multi_chat_python /bin/sh

    # Optional: normally the docker instance will quit on system shutdown
    docker container stop multi_chat_python

# second docker container

    # Notice we use a different name to differentiate this docker instance
    docker container run \
      --rm \
      --detach \
      --name multi_chat_python-4021 \
      --publish 127.0.0.1:4021:4020 \
      multi_chat_python:latest


    # From one terminal
    telnet 127.0.0.1 4021

    # From another terminal
    telnet 127.0.0.1 4021
