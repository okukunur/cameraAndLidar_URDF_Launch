# Working with the Jackal 

##Team ROSbotics
```
Kalpesh(Team Lead)
Deepak
Om
```

## Tasks:

```
- Sign up for a team and register for Jackal
- Teams should develop a URDF model for the sensor pod that includes approximate mass
- Add the URDF model to the Jackal Description
- Calibrate the PS3 cameras using ROS camera calibration
- Define an appropriate TF in which to publish 'laser scan' data from the Hokuyo
- Use the urg_node (Links to an external site.)Links to an external site. to publish LIDAR data in this reference frame
- Combine the two camera nodes and the urg/LIDAR node into a single launch file that can be launched from the rsestudent account
- Demonstrate operation of the Jackal with LIDARs and calibrated camera images via rviz
- Demonstrate in simulation use your Jackal model to map the Jackal race world using work from previous projects
```

Our team uses Jackal 3 for the project. An URDF file is created to include cameras and sensors similar to the jackal present. Camera calibration is done and the files are saved in catkin_ws/src/lab6_pkg/calibrationdata folder. To connect to jackal login to rsestudent account, source the .sh file located in  catkin_ws/src/lab6_pkg/jackal3-shFile. This gives access to the jackal.


Launch files are created to successfully launch the jackal in environment.

To demonstrate the working of jackal including the sensors in gazebo follow the below steps:

-Install usb_cam package for cameras calibration (now they are calibrated)
```
sudo apt-get install ros-indigo-usb-cam
```

-Install urg-node to connect to the laser
```
sudo apt-get install ros-indigo-urg-node
```

-Clone the repository in any directory and navigate to *rosbotics/catkin_ws*
-Build the files
```
../rosbotics/catkin_ws/$catkin_make
``` 
-Source the new .sh file
```
../rosbotics/catkin_ws/$source devel/setup.sh
```
-Export the variables in the same terminal to jackal to include the sensor.urdf file during launching the jackal
```
../rosbotics/catkin_ws/$export USE_JACKAL_URDF_EXTRAS=1
../rosbotics/catkin_ws/$export JACKAL_URDF_EXTRAS="$(rospack find lab6_pkg)/urdf/sensor.urdf"
```
-run the launch file for the jackal to launch and follow the line and map the world
```
../rosbotics/catkin_ws/$roslaunch lab6_pkg lab6.launch
```
-Gazebo and Rviz are opened. Navigate to Rviz to see the mapping along with images from the left and right cameras.
