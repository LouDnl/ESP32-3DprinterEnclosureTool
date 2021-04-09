from time import sleep
import gc

try: # import the python socket api
    import usocket as socket
except:
    import socket

#import machine # machine settings
from machine import reset

def web_page():

  html = """
  <!DOCTYPE html>
  <html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="2.5; URL='/'">
        <link rel="icon" href="data:,">
        <title>ESP32 Micropython Web Server</title>
        <style>
            html{
                font-family: Helvetica; 
                display:inline-block; 
                margin: 0px auto; 
                text-align: center;}
            h1{
                color: #344feb; 
                padding: 2vh;}
            p{
                font-size: 1.5rem;}
            .button{
                display: inline-block; 
                background-color: #eb7134; 
                border: none; 
                border-radius: 4px; 
                color: white; p
                adding: 16px 40px; 
                /*text-decoration: none; */
                font-size: 30px; 
                margin: 2px; 
                cursor: pointer;}
            .button2{
                background-color: #349ceb;}
        </style>
    </head>
    <body> 
        <h1>Ender 3 v2 Enclosure</h1>
        <h2>Sensors:</h2>
        <p>Enclosure Temperature: <span class="button">""" + temp + """ &#8451;</span></p>
        <p>Enclosure Humidity: <span class="button button2">""" + humi + """ %rH</span></p>
        <p>Ender 3 v2 CPU Temperature: <span class="button">""" + therm + """ &#8451;</span></p>
    </body>
    </html>"""
  return html

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen(5)
except (Exception, AssertionError) as exc:
    print("Address in use, restarting", exc.args[0])
    sleep(2)
    reset()
    pass  

while True:
  if gc.mem_free() < 54000:
      gc.collect()

  try:
    sleep(1)

    from lcd import myList

    if myList[0] != 0:
      temp = myList[0]
    else:
      temp = 10
    
    if myList[1] != 0:
      humi = myList[1]
    else:
      humi = 10
    
    if myList[2] != 0:
      therm = myList[2]
    else:
      therm = 10
      
  except (Exception, AssertionError) as exc:
    print("Couldn't get information from sensors for web ", exc.args[0])
    temp, humi, therm = 10, 10, 10
    pass

  try:
    conn, addr = s.accept()
  except:
    print("Socket Accept Error ", exc.args[0])
    # reset()
    pass 
  print('Got a connection from %s' % str(addr))

  try:
    request = conn.recv(1024)
  except (Exception, AssertionError) as exc:
    print("recv -------------", exc.args[0])
    # reset()
    pass
 
  try:
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
  except (Exception, AssertionError) as exc:
    print("Connection problem", exc.args[0])
    # reset()
    pass
  conn.close()