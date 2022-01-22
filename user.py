from enum import Enum

class St(Enum):
  UNKNOWN = -3  # this is the state of a new user.
  ANONYMOUS = -2  # ראה תרשים זרימה
  NAMED = -1
  S0_NOT_EXPOSED = 0
  S1_EXPOSED = 1
  S2_NOT_IMMUNE = 2
  S3_IMMUNE = 3
  S4_POS_AM_IM = 4  # ראה תרשים זרימה
  S5_NEG_AM_IM = 5
  S6_POS_PCR_IM = 6
  S7_NEG_PCR_IM = 7
  S8_NEG_PCR_NI = 8
  S9_POS_PCR_NI = 9
  Sx10_OTHER = 10 #cancelled
  Sx11_SIXTY = 11
  Sx12_OTHER = 12
  Sx13_SIXTY = 13
  S14_OTHER = 14
  S15_SIXTY = 15
  S16_OTHER = 16
  S17_SIXTY = 17
  S18_ = 18
  S19_ = 19
  S20_ = 20
  S21_ = 21
  S22_ = 22
  S23_ = 23
  S24_ = 24
  S25_ = 25
  S26_ = 26
  S27_ = 27
  S28_ = 28

class User():
  def __init__(self, chat_id):
    self.chat_id = chat_id
    self.name = ''
    #state variable
    self.state = St.UNKNOWN


