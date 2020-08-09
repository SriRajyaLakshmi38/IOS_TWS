import socket                
import os.path
from os import path

def bind_ip(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   print ("Created the Socket successfully")
   s.bind((ip,port))        
   print ("socket binded to %s" %(port))
   return s  

def server_Starting(s):
   s.listen(5)      
   print ("socket is listening")            

   while True:
      p, addr = s.accept()      
      print ('Got connection from', addr)
      http_request = p.recv(1234).decode()
      
      response = request_Processing(http_request)
      p.sendall(response)
      p.close()

def request_Processing(http_request):
   uri = http_request.split(" ")
   uri = uri[1]
   
   if(uri == "/"):
      response = "HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n"
      content = "<h1>Webserver Under construction</h1>"  
      response = response+"Content-Length is:"+str(len(content))+"\r\n\r\n"
      response = response+content
      return response.encode()
      
   print("is File : "+str(path.isfile("./www"+uri)))
   print(uri)
   if(path.isfile("./www"+uri)):
      f = open("./www"+uri, "rb")
      content = f.read()
      f.close()
      content_type = "text/html"
      if(uri.find(".png") != -1):
         content_type = "image/png"
      if(uri.find(".gif") != -1):
         content_type = "image/gif"
      
      response = prepare_response("200","OK",content_type,content)
  
      return response

   response = prepare_response("404","Not Found","text/html","<h1>File Not Found</h1>".encode())
   return response


def prepare_response(code, message, content_type, content):
   response = "HTTP/1.1 "+code+" "+message+"\r\n"
   response = response+"Content-Type is:"+content_type+"\r\n"
   response = response+"Content-Length is:"+str(len(content))+"\r\n\r\n"
   response = response.encode()+content
   return response


s = bind_ip("",8888)
server_Starting(s)
