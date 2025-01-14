# If not working, first do: sudo rm -rf /tmp/.docker.xauth
# It still not working, try running the script as root.
## Build the image first
### docker build -t r2_path_planning .
## then run this script
xhost local:root



docker run --rm -it \
    -e DISPLAY=$DISPLAY \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v mydata:/app/resultados \
    --net=host \
    --privileged \
    --runtime=nvidia \
    neatsnake


echo "Done."