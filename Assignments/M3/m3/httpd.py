import socket                
import os.path
import os
from os import path

document_root = "./"

def bind_ip(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   print ("Created the Socket successfully")
   s.bind((ip,port))        
   print ("Binding the socket to %s" %(port))
   return s

def server_Starting(s):
   s.listen(5)      
   print ("socket is listening")            
   while True:
      p, addr = s.accept()      
      print ('Got the connection from', addr)
      request = p.recv(1234).decode()
      http_response = requesting_Process(request)
      p.sendall(http_response)
      p.close()

def requesting_Process(request):
   uri = request.split(" ")
   uri = uri[1]
   print(uri)  
   if(uri=="/"):
      content = directory_listing(document_root,uri)
      content_type = "text/html"
      http_response = prepare_response("200","OK",content_type,content.encode())
      return http_response
   if(path.isdir(document_root+uri) ):
      content = directory_listing(document_root+uri,uri)
      content_type = "text/html"
      http_response = prepare_response("200","OK",content_type,content.encode())
      return http_response
   if(path.isfile("./"+uri)):
      f = open("./"+uri, "rb")
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

def directory_listing(dir_path,uri):
   listOfFiles = os.listdir(dir_path)
   tempuri = uri
   if(uri == "/"):
      uri = ""
   resp = "<html><body>"
   str = tempuri.split("/")
   str.pop();
   u = "/"
   if(len(str)==1 and str[0]==""):
     u = "/"
   else:
     u = u.join(str)
   resp = resp+"<a href='"+u+"' >parent</a></br>"
   for entry in listOfFiles:
      resp = resp+"<a href='"+uri+"/"+entry +"'>"+entry+"</a></br>"
   
   #print("resp : "+resp)
   return resp+"</body></html>"

s = bind_ip("",8888)
server_Starting(s)