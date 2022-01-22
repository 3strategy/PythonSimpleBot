from enum import Enum

class State(Enum):
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
  S11 = 11
  S12 = 12
  S13 = 13
  S14 = 14
  S15 = 15
  S16 = 16
  S17 = 17
  S18 = 18
  S19 = 19
  S20 = 20
  S21 = 21
  S22 = 22
  S23 = 23
  S24 = 24
  S25 = 25
  S26 = 26
  S27 = 27

class User():
  def __init__(self, chat_id):
    self.chat_id = chat_id
    self.name = ''
    self.state = State.UNKNOWN


