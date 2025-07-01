# Start from the base image
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Set the default shell to bash for all subsequent RUN commands to ensure ROS scripts work
SHELL ["/bin/bash", "-c"]

# --- Environment Variables ---
ENV DEBIAN_FRONTEND=noninteractive \
    ROS_DISTRO=humble \
    NB_USER=wellyowo \
    NB_UID=1000 \
    HOME=/home/wellyowo

# --- Set up ROS 2 APT Repository ---
# This ensures the system knows where to find all "ros-humble-*" packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    lsb-release \
    && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2.list && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Install All System & ROS Dependencies ---
# This single RUN command installs everything needed by your workspace
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Basic system tools
    git \
    sudo \
    python3-pip \
    x11-xserver-utils \
    tzdata \
    # Hardware libraries from Kobuki README
    libusb-1.0-0-dev \
    libftdi1-dev \
    libuvc-dev \
    # Essential ROS development tools
    ros-dev-tools \
    python3-rosdep \
    # ---- EXPLICIT LIST OF ROSDEP-DISCOVERED PACKAGES ----
    ros-${ROS_DISTRO}-desktop \
    ros-${ROS_DISTRO}-depth-image-proc \
    ros-${ROS_DISTRO}-diagnostic-updater \
    ros-${ROS_DISTRO}-ecl-build \
    ros-${ROS_DISTRO}-ecl-license \
    ros-${ROS_DISTRO}-gazebo-ros2-control \
    ros-${ROS_DISTRO}-graph-msgs \
    ros-${ROS_DISTRO}-image-publisher \
    ros-${ROS_DISTRO}-joint-state-publisher \
    ros-${ROS_DISTRO}-joint-state-publisher-gui \
    ros-${ROS_DISTRO}-kobuki-ros-interfaces \
    ros-${ROS_DISTRO}-kobuki-velocity-smoother \
    ros-${ROS_DISTRO}-magic-enum \
    ros-${ROS_DISTRO}-moveit-common \
    ros-${ROS_DISTRO}-moveit-core \
    ros-${ROS_DISTRO}-moveit-kinematics \
    ros-${ROS_DISTRO}-moveit-planners-ompl \
    ros-${ROS_DISTRO}-moveit-ros-move-group \
    ros-${ROS_DISTRO}-moveit-ros-planning \
    ros-${ROS_DISTRO}-moveit-ros-visualization \
    ros-${ROS_DISTRO}-moveit-setup-assistant \
    ros-${ROS_DISTRO}-moveit-simple-controller-manager \
    ros-${ROS_DISTRO}-nav2-bringup \
    ros-${ROS_DISTRO}-nav2-msgs \
    ros-${ROS_DISTRO}-navigation2 \
    ros-${ROS_DISTRO}-realsense2-camera \
    ros-${ROS_DISTRO}-rtabmap-ros \
    ros-${ROS_DISTRO}-rviz-visual-tools \
    ros-${ROS_DISTRO}-slam-toolbox \
    ros-${ROS_DISTRO}-tf-transformations \
    ros-${ROS_DISTRO}-xacro \
    #for ament lint cpplint build
    ros-${ROS_DISTRO}-ament-lint-auto \
    ros-${ROS_DISTRO}-ament-cmake-cppcheck \
    ros-${ROS_DISTRO}-ament-cmake-cpplint \
    ros-${ROS_DISTRO}-ament-cmake-flake8 \
    ros-${ROS_DISTRO}-ament-cmake-lint-cmake \
    #for dynamixel drivers
    ros-${ROS_DISTRO}-dynamixel-sdk \ 
    #for joint state control
    ros-${ROS_DISTRO}-ros2-controllers \
    # ---------------------------------------------------
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Install Python Packages ---
# Install Python-specific tools required by the repositories
RUN pip3 install -U \
    vcstool \
    transforms3d

# --- User Setup and Finalization ---
RUN groupadd --gid ${NB_UID} ${NB_USER} && useradd --uid ${NB_UID} --gid ${NB_UID} -m ${NB_USER} && \
    echo "${NB_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Initialize rosdep (still good practice to have in the base image)
RUN rosdep init && rosdep update
WORKDIR ${HOME}

# Set up the shell environment
# Create the workspace directory and set up the shell environment
RUN echo "source /opt/ros/humble/setup.bash" >> ${HOME}/.bashrc && \
    echo "source /usr/share/gazebo/setup.sh" >> ${HOME}/.bashrc && \
    echo "if [ -f ${HOME}/locobot_ws/install/setup.bash ]; then source ${HOME}/locobot_ws/install/setup.bash; fi" >> ${HOME}/.bashrc && \
    echo "export INTERBOTIX_XSLOCOBOT_BASE_TYPE=kobuki" >> ${HOME}/.bashrc