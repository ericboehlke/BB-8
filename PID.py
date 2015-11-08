class PIDController(object):
  
  Kp = .6 
  Ki = .2                       
  Kd = 1
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


