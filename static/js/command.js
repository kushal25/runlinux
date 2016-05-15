 function onSubmit(){
      var xmlhttp = new XMLHttpRequest();
      var url = "http://localhost:5000/command";

      var json = {"linuxCommand" : document.forms["myForm"]["linuxCommand"].value}

      
      xmlhttp.onreadystatechange = function() {
          if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
              var myArr = JSON.parse(xmlhttp.responseText);
              myFunction(myArr);
          }
      };
      xmlhttp.open("POST", url, true);
      xmlhttp.setRequestHeader("Content-type", "application/json");
        xmlhttp.send(JSON.stringify(json));

      function myFunction(arr) {               
          document.getElementById("resp").innerHTML = arr.commandResponse;
      }
    }
      function logout()
      {
        var xmlhttp = new XMLHttpRequest();
        var url = "http://localhost:5000/logout";            
        xmlhttp.open("GET", url, true);              
      }