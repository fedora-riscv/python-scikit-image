#!/bin/sh

VERSION=$1
tar -xzf scikit-image-$VERSION.tar.gz
pushd scikit-image-$VERSION
rm ./skimage/data/lena_RGB_U8.npy
rm ./skimage/data/lena.png
rm ./skimage/data/lena_GRAY_U8.npz
rm ./skimage/data/lenagray.png
rm ./skimage/data/lena_GRAY_U8.npy
rm ./skimage/data/lena_RGB_U8.npz
popd

tar -czf scikit-image-$VERSION-nolena.tar.gz scikit-image-$VERSION
