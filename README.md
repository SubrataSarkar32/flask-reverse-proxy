# flask-reverse-proxy

Local flask based reverse proxy webapp. The flask app acts as a reverse proxy allowing you to host multiple webapps and redirect based on the url list.

run the application with

`python reverse_proxy.py`

then access some url in any other system's browser to the host system's local ip address lets say you visit http://192.168.1.101

you will get redirected to the locally hosted app lets say http://localhost:5000

if you have pihole setup on your system or network you can configure the dns record and add "A Records" to have your own DNS and access webapps with your own local domain names


Lets say on System A you have hosted a webapp locally.
Now you can bind only one app to port 80.
But you want to host multiple webapps locally. So whats the solution?

Solution:

You can host your webapps on different ports/sockets(.sock) and use this reverse proxy to serve them on port 80.

First host your webapps locally on different ports , lets say 5000 and 5001.

Then you update the reverse proxy python scripts dictionary to

    "webapp1.local":"http://localhost:5000"
    or
    "webapp1.local":"http://unix:/home/subrata32/webapp1/hsecure1.sock"

    "webapp2.local":"http://localhost:5001"
    or
    "webapp1.local":"http://unix:/home/subrata32/webapp2/hsecure2.sock"

Then update your pihole dns A Record with

webapp1.local -> 192.168.1.101  # your local ip address

webapp2.local -> 192.168.1.101  # your local ip address

