import paramiko
import pandas as pd
import time

class Device:
  def __init__(self, ip, user, password):
    self.ip = ip
    self.user = user
    self.password = password

def getDevices():
  df = pd.read_csv('devices.csv')
  df = df.reset_index()
  return df


def sendCommand(command, timeout=1):
  remote_conn.settimeout(1)
  if remote_conn.recv_ready():
    while True:
      try:
        temp_output = str(remote_conn.recv(1024), "utf-8")
      except Exception as e:
        break
  remote_conn.settimeout(timeout)
  remote_conn.send(command)
  time.sleep(timeout)
  output = ""
  while True:
    try:
      temp_output = str(remote_conn.recv(1024), "utf-8")
    except Exception as e:
      #print("timeout")
      break
    output += temp_output
    print(temp_output, end="")
  return output

if __name__ == "__main__":
  devices = []
  for index, d in getDevices().iterrows():
    devices.append(Device(d['ip'], d['user'], d['password']))
  for i in devices:
    print(i.ip, i.user, i.password)
    router_ip = i.ip
    router_username = str(i.user)
    router_password = str(i.password)


    ssh = paramiko.SSHClient()

    # Load SSH host keys.
    ssh.load_system_host_keys()
    # Add SSH host key automatically if needed.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to router using username/password authentication.
    try:
      ssh.connect(router_ip, 
                  username=router_username, 
                  password=router_password,
                  look_for_keys=True )
      remote_conn = ssh.invoke_shell()
    except Exception as e:
      print("Error en connection")
      print(e)
      break

    
    print(ssh)
    # Run command.
    
    sendCommand("enable\n")
    sendCommand("admin\n\n")
    sendCommand("terminal lengt 0\n")
    output = sendCommand("\n")
    hostname = output.split('#')[0].replace("\r", "").replace("\n", "")
    ospfstatus = sendCommand("show ip ospf\n", 4)
    f = open("./OSPFStatus/" + hostname + ".ios", "w")
    f.write(ospfstatus)
    f.close()
    ssh.close()

