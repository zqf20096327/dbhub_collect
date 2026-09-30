# How to run the project

## Installing the core components
We will need Gazebo, PX4, ROS and MAVROS to run this project. 
We need MAVROS to let ROS communicate with Mavlink. Mavlink is the communication link between ROS and PX4. And we need Gazebo for simulation. 

We can follow this guide to install all these components using a single shell script: 
https://docs.px4.io/master/en/dev_setup/dev_env_linux_ubuntu.html#rosgazebo

(In the home folder) It will tell us to run

```bash
wget https://raw.githubusercontent.com/PX4/Devguide/master/build_scripts/ubuntu_sim_ros_melodic.sh
```

and then

```bash
bash ubuntu_sim_ros_melodic.sh
```

to install.

We are using ubuntu 20, so instead we download the file in this guthub repo:

https://gist.github.com/ekaktusz/a1065a2a452567cb04b919b20fdb57c4

and then move it to the home folder and run
```
bash ubuntu_sim_ros_noetic.sh
```


## Installing QGroundControl
This part is not strictly necessary but it is in some cases, so just to be sure, install QGroundControl as per these instructions:
https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html

It will tell us to run
```
sudo usermod -a -G dialout $USER
sudo apt-get remove modemmanager -y
sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y
wget https://d176tv9ibo4jno.cloudfront.net/latest/QGroundControl.AppImage
chmod +x ./QGroundControl.AppImage
```

It can now be launched by running
```bash
./QGroundControl.AppImage
``` 

## Download and build the PX4-Autopilot assets
Following this guide:

https://docs.px4.io/master/en/dev_setup/building_px4.html

It will tell us to run (in the home folder):
```
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh
sudo reboot now
```

If it was installed correctly, we should be able to run 
```
make px4_sitl gazebo
```
to launch gazebo with a drone.

## Using PX4 with ROS
Following this guide:

https://docs.px4.io/master/en/simulation/ros_interface.html

We need to make the px4 package visible. We do so by running the following inside ~/PX4-Autopilot:
```
source Tools/setup_gazebo.bash $(pwd) $(pwd)/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$(pwd)/Tools/sitl_gazebo
```
(This can also be added to ~/.bashrc, to avoid doing this on every new terminal. See the bottom of the README for all the changes made to the ~/.bashrc file)

Now, to launch MAVROS, we can run
```
roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"
```
To launch gazebo with a drone using roslaunch, in a new terminal, we can run:

```
roslaunch px4 posix_sitl.launch
```

## Using these components with our own project
### Preparing the project

Instide the root folder of our catkin workspace (/dm884_car_detection) run:

```
git submodule update --init --recursive
```
to install the necessary submodules (darknet_ros).

Then, still in the root folder, run:
```
catkin_make
```
to build the project.

Now, we need to make the ros packages visible by running:

```
source ./devel/setup.bash 
```
(This can also be added to ~/.bashrc, to avoid doing this in every new terminal. See the bottom of the README for all the changes made to the ~/.bashrc file)

### Running the project
Launch MAVROS by running:
```
roslaunch mavros px4.launch fcu_url:="udp://:14540@127.0.0.1:14557"
```

In a new terminal, launch the project .launch file called car_detection.launch by running:
```
roslaunch car_detection car_detection.launch
```
NOTE: The above command does not work without sourcing px4 as shown earlier. This needs to be done in every terminal using px4. Not just once in any terminal.


In a new terminal, navigate to /dm844_car_detection/src/scripts and run:
```
python3 mission_test.py car_detection_flight.plan
```
It may be necessary to install a few Python modules, such as px4tools before running the mission. Just install them along the way, if the mission fails, and it prompts you to.

This will launch a drone mission which should fly across the parking lot, while pointing at the cars. At the same time, it should launch darknet_ros, which opens a window that shows the detected objects, as well as a terminal that lists the objects and a percentage of how sure it is of its recognition. 

To record the mission, in a new terminal, run:
```
mkdir bagfiles
cd bagfiles
rosbag record /darknet_ros/detection_image
```

When the drone has landed, stop the recording by typing ctrl+C.

# .bashrc additions
To provide an example, my ~/.bashrc looks like this:
```
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
source ~/Documents/Projects/AUAV/dm884_car_detection/devel/setup.bash
source ~/PX4-Autopilot/Tools/setup_gazebo.bash ~/PX4-Autopilot ~/PX4-Autopilot/build/px4_sitl_default
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:~/PX4-Autopilot
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:~/PX4-Autopilot/Tools/sitl_gazebo
```