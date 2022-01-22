from enum import Enum

class State(Enum):
  UNKNOWN = -3  # this is the state of a new user.
  NAMELESS = -2  # ראה תרשים זרימה
  NAMED = -1
  NOT_ESPOSED = 0
  ESPOSED = 1
  NOT_IMMUNE = 2
  IMMUNE = 3
  POS_AM_IM = 4  # ראה תרשים זרימה
  NEG_AM_IM = 5
  POS_PCR_IM = 6
  NEG_PCR_IM = 7
  NEG_PCR_NI = 8
  POS_PCR_NI = 9


class User():
  def __init__(self, chat_id):
    self.chat_id = chat_id
    self.name = ''
    self.state = State.UNKNOWN


