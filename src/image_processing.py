#encoding:utf-8
import cv2
import numpy as np

#画像をぼかす関数
def BlurImage(img, times):
  for i in range(0, times):
    img = cv2.pyrDown(img)
    img = cv2.pyrUp(img)

  return img

#画像のネガポジ反転用関数
def ReverseBW(img):
  img = 255 - img

  return img

#線をモザイクに変換する関数
def LineToMosaic(img, box_size, zero_rate):
  y_length = (int)(len(img) / box_size)
  x_length = (int)(len(img[0]) / box_size)
  mosaic = np.zeros(shape = (y_length, x_length))

  for y in range(0, y_length):
    for x in range(0, x_length):
      div = img[y * box_size : (y + 1) * box_size, x * box_size : (x + 1) * box_size]
      #divの中に0(白)がzero_rate以上の割合で存在する場合0(白)に変換
      zero_count = 0
      for div_y in range(0,box_size):
        for div_x in range(0, box_size):
          if div[div_y][div_x] < 1:
            zero_count += 1
      if zero_count / (box_size * box_size) > zero_rate:
        mosaic[y][x] = 0
      else:
        mosaic[y][x] = 255

  return mosaic

#入力された画像のパスからピクロス用のモザイクデータを出力する関数
## img_path:画像のファイルパス
## blur_times:ぼかし処理の回数
## box_size:一つのマスが対応する画像の範囲
## zero_rate:黒マスと判断するための閾値
def ConvertMosaic(img_path, blur_times, box_size, zero_rate):
  img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
  #画像を二値化
  img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

  #画像のぼかし処理
  img = BlurImage(img, blur_times)
  #画像のエッジを抽出
  img = cv2.Canny(img, 50, 120)
  #画像のネガポジを反転
  img = ReverseBW(img)
  #画像のモザイク処理
  img = LineToMosaic(img, box_size, zero_rate)

  return img