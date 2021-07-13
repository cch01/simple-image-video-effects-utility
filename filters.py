from utils import * 
import cv2

class Filters:
  def __init__(self):
    self.functions = {
      1: self.negativeFilter,
      2: self.sepiaFilter,
      3: self.coolerFilter,
      4: self.warmerFilter,
      5: self.paint,
      6: self.reduceNoise,
      7: self.blurFilter,
      8: self.sharpening,
    }

  def negativeFilter(self, frame):
    return cv2.bitwise_not(frame)

  def sepiaFilter(self, frame):
    return applyOverlay(frame, 20, 66, 112, 0.4, 0.6)

  def coolerFilter(self, frame):
    return applyOverlay(frame, 64, 0, 0, 0.25, 1)

  def warmerFilter(self, frame):
    return applyOverlay(frame, 0, 48, 48, 0.25, 1)
   
  def paint(self, frame):
    frame = createAlphaChannel(frame)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(grayFrame, 120, 255, cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blured = cv2.GaussianBlur(frame, (17, 17), 5)
    blended = alphaBlend(frame, blured, mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame

  def reduceNoise(self, frame):
    return cv2.medianBlur(frame, 5)

  def blurFilter(self, frame, level=24):
    return cv2.blur(frame, (level,level))

  def sharpening(self, frame):
    filter = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
    return cv2.filter2D(frame, -1, filter)

