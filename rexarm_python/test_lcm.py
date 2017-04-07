import lcm, os, sys, inspect

# import LCM packages
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from lcm_python import arm_command_t

msg = arm_command_t.arm_command_t()
msg.size = 9
msg.hole_indices = [0,1,2,3,4,5,6,7,8]
msg.stop_times = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]

lc = lcm.LCM()
lc.publish("ARM", msg.encode())