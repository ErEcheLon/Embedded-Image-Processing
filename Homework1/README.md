
OpenCV與AVX

Step 1. 任意影像做灰階

Step 2. 將灰階圖進行Threshold，小於128為0、大於等於128為255

Step 3. 進行Morphology 的 Open與Close，各做一百次，Kenrel由3*3至9*9記錄其執行速度。
