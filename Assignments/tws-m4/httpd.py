import socket                
import os.path
import os,sys,time
from os import path

document_root = "./"

def bind_ip(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   s.bind((ip, port))
   print (" Created the Socket successfully")
   print ("Binding socket to %s" %(port))
   return s  

def start_server(s):
   s.listen(5)      
   print ("socket is listening")            

   while True:
      p, addr = s.accept()     
      # print ('Got connection from', addr)
      request = p.recv(1234).decode().split(" ")
      if("/bin/" in request[1] or "/tws-bin/" in request[1]):
          re = url_execution(request[1])
          http_response = b""
          if(re is not None):
              http_response = b"""\
HTTP/1.1 200 OK
Content-Type: html;


<html>
<head>
<title> Tiny Web Server </title>
</head>
<body>
""" + re[3] + b"""
</body>
</html>
"""
      else:
        http_response = process_request(request[1])
      p.sendall(http_response)
      p.close()

def process_request(http_request):
   uri = http_request  
   if("favicon" in uri ):
      return "".encode()
   if(uri=="/"):
      content = directory_listing(document_root,uri)
      content_type = "text/html"
      http_response = response_Preparation("200","OK",content_type,content.encode())
      return http_response
   
   if(path.isdir(document_root+uri) ):
      content = directory_listing(document_root+uri,uri)
      content_type = "text/html"
      http_response = response_Preparation("200","OK",content_type,content.encode())
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
      http_response = response_Preparation("200","OK",content_type,content)
      return http_response
   

   http_response = response_Preparation("404","Not Found","text/html","<h1>File Not Found</h1>".encode())
   return http_response


def response_Preparation(code, message, content_type, content):
   http_response = "HTTP/1.1 "+code+" "+message+"\r\n"
   http_response = http_response+"Content-Type:"+content_type+"\r\n"
   http_response = http_response+"Content-Length:"+str(len(content))+"\r\n\r\n"
   http_response = http_response.encode()+content
   return http_response

def directory_listing(dir_path,uri):
   listOfFiles = os.listdir(dir_path)
   rs = ""
   tempuri = uri
   if(uri == "/"):
      uri = ""
   rs = rs + "<html><body>"
   str = tempuri.split("/")
   str.pop();
   u = "/"
   if(len(str)==1 and str[0]==""):
     u = "/"
   else:
     u = u.join(str)
   rs = rs+"<a href='"+u+"' >parent</a></br>"
   for e in listOfFiles:
      rs = rs+"<a href='"+uri+"/"+e +"'>"+e+"</a></br>"
   
   return rs+"</body></html>"

def url_execution(url):
    print(url)
    stdin = sys.stdin.fileno()
    stdout = sys.stdout.fileno()
    parentStdin, childStdout = os.pipe()
    pid = os.fork()
    if pid:
        os.close(childStdout)
        os.dup2(parentStdin,stdin)
        stdin = os.fdopen(parentStdin)

        inp = ""
        for line in sys.stdin:
            inp = inp +line
        ack = inp
        return 200, "text/html", len(ack), ack.encode()
    else:

        os.close(parentStdin)
        os.dup2(childStdout,stdout)
        if("bin/ls" in url):
            args = ["/bin/ls"]
            os.execvp(args[0],args)
        elif("du" in url):
            args = ["du"]
            os.execvp(args[0], args)
        
        else:
            exec(open(os.getcwd() + url).read())

s = bind_ip("",8188)
start_server(s)