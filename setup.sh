sudo apt-get update
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install python2.7-dev python3.5-dev
sudo apt-get install make
sudo apt-get install python-pip
cd ~
mkdir glfwSource
cd glfwSource
wget  glfw.zip https://github.com/glfw/glfw/releases/download/3.2.1/glfw-3.2.1.zip
unzip glfw-3.2.1.zip
cd glfw-3.2.1
mkdir build
cd build
cmake ..
make 
sudo make install

sudo pip install pyrr
sudo pip install pyopengl
sudo pip install glfw

