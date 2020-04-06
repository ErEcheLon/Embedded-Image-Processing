# 作業一 OpenCV與AVX

Step 1. 任意影像做灰階

Step 2. 將灰階圖進行Threshold，小於128為0、大於等於128為255

Step 3. 進行Morphology 的 Open與Close，各做一百次，Kenrel由3*3至9*9記錄其執行速度。

比對以下項目的差別：

1.沒有使用AVX

2.使用AVX

3.查Multi Thread(Map & Reduce)加速

### 電腦規格

- CPU: i5-9300H 4核 8線
- RAM: 8G

#### Morphology Open Operation Running 1000 time

| Kernel  |   Using AVX (s)   | Without AVX (s)  |
| :---------:  | :-----------------: | :------------------: |
|     3x3      | 0.1959 | 1.3343 |
|     4x4      | 0.2142 | 1.8740 |
|     5x5      | 0.2320 | 2.0366 |
|     6x6      | 0.2541 | 2.5080 |
|     7x7      | 0.2956 | 2.8968 |
|     8x8      | 0.3076 | 3.3848 |
|     9x9      | 0.3398 | 4.7608 |

#### Morphology Close Operation Running 1000 time

| Kernel  |   Using AVX (s)   | Without AVX (s)  |
| :---------:  | :-----------------: | :------------------: |
|     3x3      | 0.2243 | 1.3633 |
|     4x4      | 0.2789 | 1.8207 |
|     5x5      | 0.2670 | 2.1121 |
|     6x6      | 0.3027 | 2.5041 |
|     7x7      | 0.3201 | 2.9857 |
|     8x8      | 0.3386 | 3.4193 |
|     9x9      | 0.3610 | 4.0903 |


#### Morphology with 3x3 Kernel 
####Using Open Operation Running 10000 time

| Kernel  | Threads |   Using AVX (s)   | Without AVX (s)  |
| :---------: |:------: | :-----------------: | :------------------: |
|     3x3     | 1 | 1.7289 | 26.3202 |
|     3x3     | 2 | 0.9922 | 10.7506 |
|     3x3     | 4 | 0.6116 | 10.267 |
|     3x3     | 8 | 0.4101 | 7.3761 |

#### Morphology with 3x3 Kernel 
Using Close Operation Running 10000 time

| Kernel  | Threads |   Using AVX (s)   | Without AVX (s)  |
| :---------: |:------: | :-----------------: | :------------------: |
|     3x3     | 1 | 1.7009 | 29.0328 |
|     3x3     | 2 | 0.9742 | 15.9543 |
|     3x3     | 4 | 0.7200 | 9.5633 |
|     3x3     | 8 | 0.4099 | 7.3906 |

#### Morphology with 5x5 Kernel 
Using Open Operation Running 10000 time

| Kernel  | Threads |   Using AVX (s)   | Without AVX (s)  |
| :---------: |:------: | :-----------------: | :------------------: |
|     5x5     | 1 | 2.2768 | 49.8527 |
|     5x5     | 2 | 1.3582 | 19.0085 |
|     5x5     | 4 | 0.8579 | 11.8064 |
|     5x5     | 8 | 0.9773 | 9.03055 |

#### Morphology with 5x5 Kernel 
Using Close Operation Running 10000 time

| Kernel  | Threads |   Using AVX (s)   | Without AVX (s)  |
| :---------: |:------: | :-----------------: | :------------------: |
|     5x5     | 1 | 2.2150 | 44.0541 |
|     5x5     | 2 | 1.1943 | 17.7407 |
|     5x5     | 4 | 1.3815 | 15.4617 |
|     5x5     | 8 | 1.0184 | 8.5820 |

#### Morphology with 7x7 Kernel 
Using Open Operation Running 10000 time

| Kernel  | Threads |   Using AVX (s)   | Without AVX (s)  |
| :---------: |:------: | :-----------------: | :------------------: |
|     7x7     | 1 | 3.2290 | 69.8255 |
|     7x7     | 2 | 1.6246 | 32.0871 |
|     7x7     | 4 | 1.7974 | 20.3571 |
|     7x7     | 8 | 0.9881 | 12.6327 |

#### Morphology with 7x7 Kernel 
Using Close Operation Running 10000 time

| Kernel  | Threads |   Using AVX (s)   | Without AVX (s)  |
| :---------: |:------: | :-----------------: | :------------------: |
|     7x7     | 1 | 2.8853 | 59.0905 |
|     7x7     | 2 | 1.5402 | 31.5701 |
|     7x7     | 4 | 1.2345 | 21.1487 |
|     7x7     | 8 | 1.2499 | 11.1699 |

#### Morphology with 9x9 Kernel 
Using Open Operation Running 10000 time

| Kernel  | Threads |   Using AVX (s)   | Without AVX (s)  |
| :---------: |:------: | :-----------------: | :------------------: |
|     9x9     | 1 | 5.5313 | 93.0841 |
|     9x9     | 2 | 2.1634 | 42.6421 |
|     9x9     | 4 | 1.7444 | 26.9202 |
|     9x9     | 8 | 1.4716 | 17.2203 |

#### Morphology with 9x9 Kernel 
Using Close Operation Running 10000 time

| Kernel  | Threads |   Using AVX (s)   | Without AVX (s)  |
| :---------: |:------: | :-----------------: | :------------------: |
|     9x9     | 1 | 5.8566 | 71.3977 |
|     9x9     | 2 | 1.9165 | 45.8308 |
|     9x9     | 4 | 1.1975 | 30.0809 |
|     9x9     | 8 | 0.8136 | 20.5664 |