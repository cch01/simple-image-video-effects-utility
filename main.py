import cv2
from filterUtils import resizeDisplayingWindow
from filters import Filters

def renderVideo(path):
  vid = cv2.VideoCapture(path)
  fps = round(vid.get(cv2.CAP_PROP_FPS))
  if not vid.isOpened():
    print('Error on opening video file')

  while(vid.isOpened()):
    ret, frame = vid.read()
    if ret == True:
      frame = Filters.portraitMode(resizeDisplayingWindow(frame))
      cv2.imshow('video', resizeDisplayingWindow(frame))
      if cv2.waitKey(fps) & 0xFF == ord('q'):
        break
    else:
      break

  vid.release()
  cv2.destroyAllWindows()

def renderPhoto(path):
  img = cv2.imread(path)
  cv2.imshow('ori_img', resizeDisplayingWindow(img))
  img = Filters.portraitMode(img)
  cv2.imshow('img', resizeDisplayingWindow(img))
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  # renderPhoto('portraitTest.jpg')
  # renderPhoto('photo.jpg')
  renderVideo('video.mp4')
  
# TODO make CLI, LOGIC for saving modified outputs