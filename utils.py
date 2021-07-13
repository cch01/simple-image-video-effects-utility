import cv2
import numpy as np
from enum import Enum

class SrcType(Enum):
  VIDEO = 0
  IMAGE = 1

def createAlphaChannel(frame):
  try:
    frame.shape[3]
  except IndexError:
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
  return frame

def resizeDisplayingWindow(frame, height=480):
    dimension = None
    frameHeight, frameWidth = frame.shape[:2]
    outputHeight = height
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

def openSrcFile():
  path = input('Image/Video location:\n')
  if path.endswith('.mp4'):
    try:
      vid = cv2.VideoCapture(path)
      if vid.isOpened():
        vid.release()
        return (path, SrcType.VIDEO)

    except:
      print('---Please provide correct file source path---')
      return openSrcFile()

  if path.endswith('.jpg') or path.endswith('.png'):
    img = cv2.imread(path)
    try:
      img.shape[0]
      return (path, SrcType.IMAGE)
    except:
      print('---Please provide correct file source path---')
      return openSrcFile()
  
  print('---Please provide correct file source path---')
  return openSrcFile()


def askForFilters():
  filters = input('Select filters to be applied:\n1. Negative Filter\n2. Sepia Filter\n3. Cooler\n4. Warmer\n5. Paint Effect\n6. Noise Reduction\n7. Blur\n8. Sharpening\n\nAdd "," between filters if multiple filters are desired.\n')
  try:
    inputs = [int(f) for f in filters.split(",")]
    isValidInputs = all(val < 9 and val >= 0 for val in inputs)
    if not isValidInputs:
      print('---Please provide correct values---')
      return askForFilters()
    return inputs

  except:
    print('---Please provide correct values---')
    return askForFilters()