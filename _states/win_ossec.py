import os
import logging

log = logging.getLogger(__name__)


def autoenrolled(name, port=1515,
  keyFilePath='C:\\Program Files (x86)\\ossec-agent\\client.keys',
  confFilePath='C:\\Program Files (x86)\\ossec-agent\ossec.conf'):
  '''
  Ensures that the minion is enrolled with the server and attempts to enroll
  automatically, via ossec-authd, if not.

  State validity checking is not terribly smart at the moment. It cannot
  determine if a minion is registered to the specified server, only if it is
  registered at all.

  Simple remove the client.keys file on the minion to re-register via this state.
  '''
  if os.path.exists(keyFilePath):
    return {
      'name': name,
      'result': True,
      'comment': keyFilePath+' already exists ',
      'changes':{}
    }
  else:
    try:
      modOutput = __salt__['win_ossec.authd_enroll'](name, port,
        keyFilePath=keyFilePath)
      return {
        'name': name,
        'result': True,
        'comment': "Successfully enrolled with "+name,
        'changes': modOutput
      }
    except Exception as e:
      return {
        'name': name,
        'result': False,
        'comment': "Unable to register with "+ name+", "+str(e),
        'changes':{}
      }
