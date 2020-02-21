apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
wget https://www.python.org/ftp/python/3.8.1/Python-3.8.1.tar.xz
tar xf Python-3.8.1.tar.xz
cd Python-3.8.1
./configure
make -j 4
make install
cd ..
rm Python-3.8.1.tar.xz
pip3 install --upgrade pip
pip3 install smbus
apt-get install libtiff4
apt-get install libjpeg62
apt-get install libjpeg-dev zlib1g-dev
pip3 install spidev
pip3 install gpiozero
pip3 install psutil
pip3 install cap1xxx
pip3 install sn3218
pip3 install Pillow
apt install libsdl2-dev libfreetype6-dev libsdl2-mixer-dev libsdl2-image-dev libsdl2-ttf-dev libjpeg-dev libpng-dev libportmidi-dev -y
apt install libsdl1.2-dev -y
apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev -y
pip3 install pygame 
systemctl enable rc-local
apt-get install git -y
cd /home
git clone https://github.com/TWoolhouse/TRasPI.git
mkdir traspi 
mv /home/TRasPI/ /home/traspi
mkdir /home/traspi/user