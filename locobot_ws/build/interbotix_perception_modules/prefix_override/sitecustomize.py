import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/wellyowo/locobot_sim/locobot_ws/install/interbotix_perception_modules'
