# discordBot
Playing youtube and spotify links<br>
Add token to config.py
#error
<b>
"Task exception was never retrieved
future: <Task finished name='Task-14' coro=<VoiceClient._create_socket() done, defined at C:\Users\tugru\AppData\Local\Programs\Python\Python38-32\lib\site-packages\discord\voice_client.py:172> exception=gaierror(11001, 'getaddrinfo failed')>
Traceback (most recent call last):
  File "C:\-----\------\AppData\Local\Programs\Python\Python38-32\lib\site-packages\discord\voice_client.py", line 191, in _create_socket
    self.endpoint_ip = socket.gethostbyname(self.endpoint)
socket.gaierror: [Errno 11001] getaddrinfo failed"
 </b>
 
 uptade your 
    File "C:\----\----\AppData\Local\Programs\Python\Python38-32\lib\site-packages\discord\voice_client.py", line 191, in _create_socket
  <b>line 190 </b>--   (self.endpoint, _, _) = endpoint.rpartition(':')
