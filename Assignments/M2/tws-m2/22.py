import socket                
import os.path
from os import path


def bind_ip(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   print ("Created the socket Successfully")
   sock.bind((ip,port))        
   print ("Binded the socket to %s" %(port))
   return s

def server_Starting(s):
   s.listen(5)      
   print ("Socket is listening")            

   while True:
      p, addr = s.accept()      
      print ('Got connection from', addr)
      request = p.recv(1234).decode()
      
      response = requesting_Process(request)
      p.sendall(response)
      p.close()

def requesting_Process(request):
   uri = request.split(" ")
   uri = uri[1]
   

   if(uri.find("favicon")!=-1):
      return "".encode()
   if(uri == "/"):
      http_response = "HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n"
      content = "<h1>Webserver Under construction</h1>"  
      http_response = http_response+"Content-Length:"+str(len(content))+"\r\n\r\n"
      http_response = http_response+content
      return http_response.encode()
      
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
      
      http_response = prepare_response("200","OK",content_type,content)
  
      return http_response

   http_response = prepare_response("404","Not Found","text/html","<h1>File Not Found</h1>".encode())
   return http_response


def prepare_response(code, message, content_type, content):
   http_response = "HTTP/1.1 "+code+" "+message+"\r\n"
   http_response = http_response+"Content-Type is:"+content_type+"\r\n"
   http_response = http_response+"Content-Length is:"+str(len(content))+"\r\n\r\n"
   http_response = http_response.encode()+content
   return http_response


s = bind_ip("",8888)
server_Starting(sock)