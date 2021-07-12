from filterUtils import * 
import cv2

class Filters:
  def invertedFilter(frame):
    return cv2.bitwise_not(frame)
  def sepiaFilter(frame):
    return applyOverlay(frame, 20, 66, 112, 0.4, 0.6)

  def coolerFilter(frame):
    return applyOverlay(frame, 64, 0, 0, 0.25, 1)

  def warmerFilter(frame):
    return applyOverlay(frame, 0, 48, 48, 0.25, 1)
   
  def portraitMode(frame):
    frame = createAlphaChannel(frame)
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(grayFrame, 160, 255, cv2.THRESH_BINARY)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    blured = cv2.GaussianBlur(frame, (35, 35), 2)
    blended = alphaBlend(frame, blured, mask)
    frame = cv2.cvtColor(blended, cv2.COLOR_BGRA2BGR)
    return frame

