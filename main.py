import cv2
from filterUtils import resizeDisplayingWindow
from filters import Filters
from enum import Enum

# import argparse

filterMapper = {
  1: Filters.invertedFilter,
  2: Filters.sepiaFilter,
  3: Filters.coolerFilter,
  4: Filters.warmerFilter,
  5: Filters.paint,
  6: Filters.reduceNoise,
  7: Filters.blurFilter,
  8: Filters.sharpening,
  9: Filters.negative
}
class SrcType(Enum):
  VIDEO = 0
  IMAGE = 1

def renderVideo(vid, filters):
  if not vid.isOpened():
    print('Error on opening video file')
  fps = round(vid.get(cv2.CAP_PROP_FPS))
  while(vid.isOpened()):
    ret, frame = vid.read()
    if ret == True:
      cv2.imshow('video_ori', resizeDisplayingWindow(frame, 480))
      cv2.imshow('video', resizeDisplayingWindow(frame, 480))
      if cv2.waitKey(fps) & 0xFF == ord('q'):
        break
    else:
      break

  vid.release()
  cv2.destroyAllWindows()

def renderPhoto(img, filters):
  cv2.imshow('ori_img', resizeDisplayingWindow(img, 480))

  cv2.imshow('img', resizeDisplayingWindow(img, 480))
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  cv2.imwrite('img.jpg', img)

def openSrcFile():
  path = input('Image/Video location:\n')
  if path.endswith('.mp4'):
    try:
      vid = cv2.VideoCapture(path)
      if vid.isOpened():
        return (vid, SrcType.VIDEO)

    except:
      print('Please provide correct file source path')
      return openSrcFile()

  if path.endswith('.jpg') or path.endswith('.png'):
    img = cv2.imread(path)
    try:
      img.shape[0]
      return (img, SrcType.IMAGE)
    except:
      print('Please provide correct file source path')
      return openSrcFile()
  
  print('Please provide correct file source path')
  return openSrcFile()


def askForFilters():
  filters = input('Select filters to be applied:\n1. Inverted Filter\n2. Sepia Filter\n3. Cooler\n4. Warmer\n5. Paint Effect\n6. Noise Reduction\n7. Blur\n8. Sharpening\n9. negative\n\nAdd "," between filters if multiple filters are desired.\n')
  try:
    inputs = [int(f) for f in filters.split(",")]
    isValidInputs = all(val < 10 and val >= 0 for val in inputs)
    if not isValidInputs:
      print('Please provide correct values')
      return askForFilters()
    return inputs

  except:
    print('Please provide correct values')
    return askForFilters()

if __name__ == '__main__':
  file, srcType = openSrcFile()
  filtersSelected = askForFilters()
  if srcType == SrcType.VIDEO:
    renderVideo(file, filtersSelected)
  if srcType == SrcType.IMAGE:
    renderPhoto(file, filtersSelected)

  
# TODO make CLI, LOGIC for saving modified outputs
