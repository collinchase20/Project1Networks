To start this project, I read up on the socket library for python. This was fairly straightforward and 
provided examples for how to set up a basic TCP connection and how to specify the port it runs on. Upon reading
about this library I also learned how to send messages to a server with a connected socket and how to read responses
from the server. With this knowledge it was easy to establish a TCP connection to port 27995 and send the starting HELLO message.
Once here I simply had to iterate through the responses from the server. If the server sent a FIND response I counted the occurances of
the symbol in the character string and sent a COUNT message. I then read the response from the server and start the loop again. If the server
responded with a BYE message I terminated the loop and returned the secret flag contained in the message. I will say the biggest challenge
here was figuring out how to know if the message was truly over. It clearly stated in the project that we need to look for a new
line at the end of the response but I was initially looking for a new line within the last 2 characters of the response when in reality
you only need to look at the last character of the response to see if it is the "\n" character.

I then had to read up on pythons argparse library. I have never wrote a program that uses command line arguments before
so this was a new process for me. Again, the documentation on the library is straightforward and this was simple to
implement and set up before establishing a connection with the socket. 

I also implemented the SSL connection. This was not very difficult after completing the project. Python has an SSL library
that was easy to implement and I only had to add a few if statements throughout my code to determine if I was connecting regularly
or with an SSL connection. When connecting with SSL there was a slightly different way to send and recieve messages from there server.

Finally, to test my code, I would often raise a lot of exceptions throughout my code and run it on the server provided.
The exceptions would hit and clearly tell me what responses I was getting from the server, if any at all, and make it clear
where I was going wrong. This was how I discovered I was not getting the full response from the server when my responses were
not ending with a new line.