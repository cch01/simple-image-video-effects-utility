import cv2
import numpy as np


def createAlphaChannel(frame):
  try:
    frame.shape[3]
  except IndexError:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
  return frame

def resizeDisplayingWindow(frame):
    dimension = None
    frameHeight, frameWidth = frame.shape[:2]
    outputHeight = 240
    aspectRatio = outputHeight / float(frameHeight)
    dimension = (int(frameWidth * aspectRatio), outputHeight)
    return cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)


def applyOverlay(frame, blue, green, red, overlayIntensity, frameIntensity):
  frame = createAlphaChannel(frame)
  frameHeight, frameWidth = frame.shape[:2]
  overlayParams = (blue, green, red, 1)
  overlay = np.full((frameHeight, frameWidth, 4), overlayParams, dtype='uint8')
  cv2.addWeighted(overlay, overlayIntensity, frame, frameIntensity, 0, frame)
  return frame

def alphaBlend(frame1, frame2, mask):
  alphaMask = mask/255
  return cv2.convertScaleAbs(frame1*(1-alphaMask) + frame2*alphaMask)

