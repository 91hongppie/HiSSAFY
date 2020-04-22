# face_recogition 에서 CUDA 사용하기

1. 윈도우 CUDA 설치

   1. CUDA Toolkit 다운로드

      1. https://developer.nvidia.com/cuda-toolkit-archive

   2. cuDNN SDK 다운로드

      1. https://developer.nvidia.com/rdp/cudnn-download

   3. CUDA Toolkit 와 cuDNN SDK 는 버전에 맞게 다운

      예) CUDA Toolkit 10.1
      	  Download cuDNN v7.6.2 (July 22, 2019), for CUDA 10.1

   4. CUDA Toolkit 설치

   5. cuDNN SDK 압축을 풀고 bin, include, lib 폴더를 CUDA Toolkit 설치 위치(예)C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1)에 덮어쓰기

   6. 확인 방법

      1. anaconda evn 생성

      2. `conda create -n **env이름** python=3.7`

      3. `activate **env이름**`

      4. `pip install tensorflow-gpu`

      5. ```bash
         import tensorflow as tf
         a = tf.constant(3)
         sess = tf.Session()
         ```

2. Dlib을 git 에서 clone

   1. `git clone https://github.com/davisking/dlib.git`

3. 아래 명령어를 실행해서 Dlib 을 빌드한다.

   1. `cd dlib`

   2. `
      mkdir build; cd build; cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1; cmake --build .`

   3. ```bash
      -- Using CMake version: 3.5.1 
      -- Compiling dlib version: 19.18.99 
      -- Enabling AVX instructions 
      -- Looking for cuDNN install... 
      -- Found cuDNN: /usr/lib/x86_64-linux-gnu/libcudnn.so 
      -- Building a CUDA test project to see if your compiler is compatible with CUDA... 
      -- Checking if you have the right version of cuDNN installed. 
      -- Enabling CUDA support for dlib.  DLIB WILL USE CUDA ******
      -- C++11 activated. 
      -- Configuring done 
      -- Generating done
      ```

   4. \*\*\*\*\*\* 이 들어간 부분의 메세지가 나오지 않는다면 CUDA 설치나 cuDNN 설치에 문제가 있으므로 제대로 설치 후 다시 시도