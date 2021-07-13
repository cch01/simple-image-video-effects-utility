import cv2
from utils import SrcType, resizeDisplayingWindow, openSrcFile, askForFilters
from filters import Filters
from functools import reduce
import ffmpeg
import subprocess

filters = Filters()

def processVideo(path, filterIdxs):
  vid = cv2.VideoCapture(path)
  if not vid.isOpened():
    print('---Error on opening video file---')
  fps = round(vid.get(cv2.CAP_PROP_FPS))
  print('---Showing preview, press "q" on the preview windows to proceed---\n')
  while(vid.isOpened()):
    ret, frame = vid.read()
    if ret == True:
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


def outputVideo(path, filterIdxs):
  vid = cv2.VideoCapture(path)
  outputFileName = input('Output file name:\n')
  fps = round(vid.get(cv2.CAP_PROP_FPS))
  width  = round(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = round(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  out = cv2.VideoWriter('tmp_'+outputFileName, fourcc, fps, (width,height))
  print('Encoding video, please wait...')
  while(vid.isOpened()):
    ret, frame = vid.read()
    if ret == True:
      frame = reduce(lambda frame, filterIdx: filters.functions[filterIdx](frame), filterIdxs, frame)
      frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
      out.write(frame)
    else:
      break
  print('Finished')
  vid.release()
  out.release()
  srcVideo = ffmpeg.input(path)
  audio = srcVideo.audio
  tmpProduct = ffmpeg.input('tmp_'+outputFileName)
  ffmpeg.output(audio, tmpProduct.video, outputFileName).run(overwrite_output=True)
  subprocess.call('rm tmp_%s' % outputFileName)
  


def askForSaving(path, type):
  isAccepted = input('Do you want to save the results? (1 for Yes; Other for No and back to previous step)\n')
  if isAccepted != '1':
    print('Reselect filters')
    filtersSelected = askForFilters()
    if type == SrcType.VIDEO:
      return processVideo(path, filtersSelected)
    else:
      return processImage(path, filtersSelected)
  
  return True



def processImage(path, filterIdxs):
  img = cv2.imread(path)
  cv2.imshow('ori_img', resizeDisplayingWindow(img, 480))
  print('---Showing preview, press "q" on the preview windows to proceed---\n')
  img = reduce(lambda _img, idx: filters.functions[idx](_img), filterIdxs, img)
  cv2.imshow('img', resizeDisplayingWindow(img, 480))
  cv2.waitKey(0)
  cv2.destroyAllWindows()
  needToSave = askForSaving(path, SrcType.IMAGE)
  if needToSave: outputImage(img)

def outputImage(img):
  fileName = input('Please provide output file name:\n')
  try:
    cv2.imwrite(fileName, img)
  except:
    print('---File name invalid---\n')
    return outputImage(img)


if __name__ == '__main__':
  path, srcType = openSrcFile()
  filtersSelected = askForFilters()
  if srcType == SrcType.VIDEO:
    processVideo(path, filtersSelected)
  if srcType == SrcType.IMAGE:
    processImage(path, filtersSelected)
