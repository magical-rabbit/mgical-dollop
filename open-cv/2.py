import os
import cv2
def rec(imgpath):
  # 加载预训练的 SSD 模型
  opencv_dnn_model = cv2.dnn.readNetFromCaffe(
        prototxt="models/deploy.prototxt"
        , caffeModel="models/res10_300x300_ssd_iter_140000_fp16.caffemodel")
  image = cv2.imread(imgpath)
  image_height, image_width, _ = image.shape
  preprocessed_image = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(image_width,image_height), mean=(104.0, 117.0, 123.0), swapRB=False, crop=True)
  opencv_dnn_model.setInput(preprocessed_image)
  results = opencv_dnn_model.forward()  
  output_image = image.copy()
  res = 0
  for face in results[0][0]:
    # 置信度
    bbox = face[3:]
    face_confidence = face[2]
    if face_confidence >=0.25:
      x1 = int(bbox[0] * image_width)
      y1 = int(bbox[1] * image_height)
      x2 = int(bbox[2] * image_width)
      y2 = int(bbox[3] * image_height)
      cv2.rectangle(output_image, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=image_width//200)
      cv2.rectangle(output_image, pt1=(x1, y1-image_width//20), pt2=(x1+image_width//16, y1),
                              color=(0, 255, 0), thickness=-1)
      cv2.putText(output_image, text=str(round(face_confidence, 1)), org=(x1, y1-25), 
                            fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=image_width//700,
                            color=(255,255,255), thickness=image_width//200)
      res+=1
  
  
  cv2.imwrite('./outputs/'+os.path.basename(imgpath),output_image)
  return res
  # cv2.imshow('img', output_image)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()




# rec('7c148b2c-7ed7-11ed-967a-70cd0dec807d.jpg')
# rec('8fe41251-7ed8-11ed-b814-70cd0dec807d.jpg')
# rec('1ff671a7-7ed8-11ed-9deb-70cd0dec807d.jpg')

import os
import re
g = os.walk("../data/news_sdust/data/pic/")
f = open('opencv_out_log.txt','w')

for path,dir_list,file_list in g:
  # print(path)
  ls = re.findall(r"\d+\.?\d*",path)
  # print(ls)
  if len(ls)==2:
    ans_head = 0
    for file_name in file_list:
      try:
        ans_head+=rec(os.path.join(path, file_name))
      except:
        print('[dayi-error]头飞了')
      # print(os.path.join(path, file_name) )
    print('{}年{}月 共有{}个头'.format(ls[0],ls[1],ans_head))
    f.write('{}年{}月 共有{}个头\n'.format(ls[0],ls[1],ans_head))