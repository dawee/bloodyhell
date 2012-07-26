#!/bin/sh

echo "*** Install Swig  ***"
apt-get install swig
echo "*** Downloading PyBox2D ***"
wget http://pybox2d.googlecode.com/files/pybox2d-2.0.2b2.zip
unzip pybox2d-2.0.2b2.zip
echo "*** Build PyBox2D ***"
cd Box2D-2.0.2b2
python setup.py build
python setup.py install
