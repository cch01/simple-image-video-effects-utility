import cv2
import numpy as np

def invertedFilter(frame):
  return cv2.bitwise_not(frame)

def createAlphaChannel(frame):
  try:
    frame.shape[3]
  except IndexError:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
  return frame

def sepiaFilter(frame, intensity=0.4):
  frame = createAlphaChannel(frame)
  frameHeight, frameWidth, frameChannels = frame.shape
  blue = 20
  green = 66
  red = 112
  sepiaParams = (blue, green, red, 1)
  overlay = np.full((frameHeight, frameWidth, 4), sepiaParams, dtype='uint8')
  cv2.addWeighted(overlay, intensity, frame, 0.6, 0, frame)
  return frame


cap = cv2.VideoCapture('video.mp4')

if not cap.isOpened():
  print('Error on opening video file')

while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    frame = sepiaFilter(frame)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
  else:
    break

cap.release()
cv2.destroyAllWindows()