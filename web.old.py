        <meta http-equiv="refresh" content="2.5; URL='/'">

        <p></p>
        <h2>GPIO manipulation</h2>
        <p>GPIO state: <strong>""" + gpio_state + """</strong></p>
        <p><a href="/?led=on"><button class="button">ON</button></a></p>
        <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
        
            <script>
      window.onload = function (){
        var temp = '""" + temp + """';
        document.getElementById('temp').innerHTML = temp;
      }
    </script>
    
    
  <body> 
        <h1>ESP32 Micropython Web Server</h1> 
        <h2>Sensor</h2>
        <p>Enclosure Temperature: """ + temp + """%</p>
        <style class="button" id="temp"></style>
        <p>Enclosure Humidity: """ + humi + """%</p>
        <p>Ender 3 v2 CPU Temperature: """ + therm + """c</p>
    </body>
    <script>
      function getTemp() {
        var temp = '""" + temp + """';
        document.getElementById('temp').innerHTML = temp;
      };
      setInterval(function() {
        getTemp();
      }, 100);
    </script>    
    

  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  hardreset = request.find('/?reset')
  if led_on == 6:
    print('LED ON')
    led.value(1)
  if led_off == 6:
    print('LED OFF')
    led.value(0)
        