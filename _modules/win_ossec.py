import socket
import ssl
import os
import logging

log = logging.getLogger(__name__)

'''
A helper module for working with OSSEC on windows. The feature that motivated
this module was the ability to take advantage of ossec_authd on windows systems.
'''

def authd_enroll(serverIp, port=1515,
  keyFilePath='C:\\Program Files (x86)\\ossec-agent\\client.keys'):
  '''
  Attempt to auto enroll using ossec-authd running on the server and port
  specified.

  Note, this will overwrite the contnets of the specified client.keys file
  '''
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ssl_sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE)

  ssl_sock.connect((serverIp, port))

  agentName = __salt__['grains.get']('id')

  log.info("Connected to "+serverIp+":"+str(port) +\
    ", using agent name "+agentName)

  # Write the agent name over the stream, this is all that;s needed, amazingly
  # enough
  ssl_sock.write("OSSEC A:'"+agentName+"'\n")

  responseData = ssl_sock.read()


  log.info("Received response: "+str(responseData))

  ssl_sock.close()

  responseStr = str(responseData)
  lineStr = responseStr.split("OSSEC K:'")[1]
  keyLine = lineStr.replace("'", "")

  keysFile = open(keyFilePath, 'w')
  keysFile.write(keyLine+"\n")
  keysFile.close()

  return {
    "result": True,
    "key_line": keyLine
  }

def _parsekeyLine(keyLine):
  parts = keyLine.split(" ")

  return {
    "id": parts[0],
    "agentName": parts[1],
    "netRestriction": parts[2],
    "agentKey": parts[3]
  }

def get_agent_id(
  keyFilePath='C:\\Program Files (x86)\\ossec-agent\\client.keys'):
  '''
  Get the agent's id.
  '''

  if not os.path.exists(keyFilePath):
    return None

  keyFile = open(keyFilePath, 'r')
  keyParts = _parsekeyLine(keyFile.read())
  return keyParts["id"]
