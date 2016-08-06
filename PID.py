class PIDController(object):
  
  Kcrit = 6.5
  # Pu = 2
  Kp = Kcrit / 1.7 #6   
  Ki =  0#1 #  0 # 1                       
  Kd = .25 # .25 # .25 #.3
  K = .5
  GUARD_GAIN = 10

  def __init__ (self):
    self.totalError = 0
    self.lastError = 0

  def calculateSpeed(self, targetPosition, currentPosition):
    error = targetPosition - currentPosition
    proportionalTerm = PIDController.Kp * error
    self.totalError = self.totalError + error     
    integralTerm = PIDController.Ki * max(min(PIDController.GUARD_GAIN, self.totalError), -PIDController.GUARD_GAIN)
    derivativeTerm = PIDController.Kd * (error - self.lastError)                            
    # self.lastError = error
    return max(min(PIDController.K * (proportionalTerm + integralTerm + derivativeTerm), 50), -50)


