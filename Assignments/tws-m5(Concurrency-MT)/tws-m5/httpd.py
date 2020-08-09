import socket 
from threading import Thread 
import os,sys,time, signal
from os import path

# from SocketServer import ThreadingMixIn 

class ClientThread(Thread):

    document_root = "./"
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port))
    
    def process_request(self, http_request):
        uri = http_request  
        if("favicon" in uri ):
           return "".encode()
        if(uri=="/"):
           content = self.directory_listing(self.document_root,uri)
           content_type = "text/html"
           http_response = self.prepare_response("200","OK",content_type,content.encode())
           return http_response
       
        if(path.isdir(self.document_root+uri) ):
           content = self.directory_listing(self.document_root+uri,uri)
           content_type = "text/html"
           http_response = self.prepare_response("200","OK",content_type,content.encode())
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
           http_response = self.prepare_response("200","OK",content_type,content)
           return http_response
       

        http_response = self.prepare_response("404","Not Found","text/html","<h1>File Not Found</h1>".encode())
        return http_response


    def prepare_response(self, code, message, content_type, content):
       http_response = "HTTP/1.1 "+code+" "+message+"\r\n"
       http_response = http_response+"Content-Type:"+content_type+"\r\n"
       http_response = http_response+"Content-Length:"+str(len(content))+"\r\n\r\n"
       http_response = http_response.encode()+content
       return http_response

    def directory_listing(self, dir_path,uri):
       listOfFiles = os.listdir(dir_path)
       resp = ""
       tempuri = uri
       if(uri == "/"):
          uri = ""
       resp = resp + "<html><body>"
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
       
       return resp+"</body></html>"

    def execute(self, url):
        print("URL is :"+ url)
        stdin = sys.stdin.fileno()
        stdout = sys.stdout.fileno()
        parentStdin, childStdout = os.pipe()
        pid = os.fork()
        if pid:
            time.sleep(3)
            r, status = os.waitpid(0, os.WNOHANG)
            os.close(childStdout)
            os.dup2(parentStdin,stdin)
            stdin = os.fdopen(parentStdin)

            if(r == 0):
              res_text = "Terminated"
              os.kill(pid, signal.SIGSTOP)
              return 200, "text/html", len(res_text), res_text.encode()  

            iput = ""
            for line in sys.stdin:
                iput = iput +line
            ack = iput
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
            elif("bin/forever" in url):
                args = ["sh","./tws-bin/forever.sh"]
                os.execvp(args[0],args)

            else:
                exec(open(os.getcwd() + url).read())
            os._exit(0)


    def run(self): 
        while True : 
            http_request = conn.recv(2048).decode().split(" ")
            http_response = ""
            if("/bin/" in http_request[1] or "/tws-bin/" in http_request[1]):
                re = self.execute(http_request[1])
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

                http_response = self.process_request(http_request[1])
            print(http_response)
            conn.sendall(http_response)
            conn.close()

# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '127.0.0.1' 
TCP_PORT = 8188 
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
 
while True: 
    tcpServer.listen(4) 
    print("Multithreaded Python server : Waiting for connections from TCP clients..." )
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start()
    threads.append(newthread)