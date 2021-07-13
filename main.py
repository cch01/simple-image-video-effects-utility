import cv2
from filterUtils import resizeDisplayingWindow
from filters import Filters
from enum import Enum
from functools import reduce


filters = Filters()
class SrcType(Enum):
  VIDEO = 0
  IMAGE = 1

def renderVideo(path, filterIdxs):
  vid = cv2.VideoCapture(path)
  if not vid.isOpened():
    print('---Error on opening video file---')
  fps = round(vid.get(cv2.CAP_PROP_FPS))
  while(vid.isOpened()):
    ret, frame = vid.read()
    if ret == True:
      print('Showing preview, press "q" on the preview windows to proceed\n')
      cv2.imshow('video_ori', resizeDisplayingWindow(frame, 480))
      frame = reduce(lambda frame, filterIdx: filters.functions[filterIdx](frame), filterIdxs, frame)
      cv2.imshow('video', resizeDisplayingWindow(frame, 480))
      if cv2.waitKey(fps) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    else:
      break

  vid.release()
  needToSave = askForSaving(path, SrcType.VIDEO)
  if needToSave: outputVideo(path, filterIdxs)


def outputImage(img):
  fileName = input('Please provide output file name:\n')
  try:
    cv2.imwrite(fileName, img)
  except:
    print('---File name invalid---\n')
    return outputImage(img)

def outputVideo(path, filterIdxs):
  vid = cv2.VideoCapture(path)
  fileName = input('Output file name:\n')
  fps = round(vid.get(cv2.CAP_PROP_FPS))
  width  = round(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = round(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  out = cv2.VideoWriter(fileName, fourcc, fps, (width,height))
  print('Encoding video, please wait...')
  while(vid.isOpened()):
    ret, frame = vid.read()
    if ret == True:
      frame = reduce(lambda frame, filterIdx: filters.functions[filterIdx](frame), filterIdxs, frame)
      out.write(frame)
    else:
      break
  print('Finished')
  out.release()
  vid.release()


def askForSaving(path, type):
  isAccepted = input('Do you want to save the results? (1 for Yes; 0 for No and back to previous step)\n')
  if isAccepted != '0' and isAccepted != '1':
    print('---Please enter either "0" or "1"---')
    return askForSaving(path, type)

  if isAccepted == '0':
    print('Reselect filters')
    filtersSelected = askForFilters()
    if type == SrcType.VIDEO:
      return renderVideo(path, filtersSelected)
    else:
      return renderImage(path, filtersSelected)
  
  return True




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
  filters = input('Select filters to be applied:\n1. Inverted Filter\n2. Sepia Filter\n3. Cooler\n4. Warmer\n5. Paint Effect\n6. Noise Reduction\n7. Blur\n8. Sharpening\n9. negative\n\nAdd "," between filters if multiple filters are desired.\n')
  try:
    inputs = [int(f) for f in filters.split(",")]
    isValidInputs = all(val < 10 and val >= 0 for val in inputs)
    if not isValidInputs:
      print('---Please provide correct values---')
      return askForFilters()
    return inputs

  except:
    print('---Please provide correct values---')
    return askForFilters()



def renderImage(path, filterIdxs):
  img = cv2.imread(path)
  cv2.imshow('ori_img', resizeDisplayingWindow(img, 480))
  print('Showing preview, press "q" on the preview windows to proceed\n')
  img = reduce(lambda _img, idx: filters.functions[idx](_img), filterIdxs, img)
  cv2.imshow('img', resizeDisplayingWindow(img, 480))
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  needToSave = askForSaving(path, SrcType.IMAGE)
  if needToSave: outputImage(img)


if __name__ == '__main__':
  path, srcType = openSrcFile()
  filtersSelected = askForFilters()
  if srcType == SrcType.VIDEO:
    renderVideo(path, filtersSelected)
  if srcType == SrcType.IMAGE:
    renderImage(path, filtersSelected)
