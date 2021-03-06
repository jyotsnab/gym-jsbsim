# Gym-Jsbsim

Gym-JSBSim provides reinforcement learning environments for the control of fixed-wing aircraft using the JSBSim flight dynamics model. Gym-JSBSim requires a Unix-like OS and Python 3.6.

The package's environments implement the OpenAI Gym interface allowing environments to be created and interacted with in the usual way, e.g.:

```
import gym
import gym_jsbsim

env = gym.make(ENV_ID)
env.reset()
state, reward, done, info = env.step(action)
```

Gym-JSBSim optionally provides 3D visualisation of controlled aircraft using the FlightGear simulator.

## Dependencies

* [JSBSim](https://github.com/JSBSim-Team/jsbsim) flight dynamics model, including the C++ and Python libraries
* FlightGear simulator (optional for visualisation)
* gym, numpy, matplotlib

## Installation
Firstly, follow the instructions on the [JSBSim](https://github.com/JSBSim-Team/jsbsim) repository to install JSBSim and its libraries.

Confirm that JSBSim is installed from the terminal:

```
$ JSBSim --version
JSBSim Version: 1.0.0 Jul 16 2018 09:14:35
```

and confirm that its Python library is correctly installed from a Python interpreter or IDE:

```
import jsbsim
```

Gym-JSBSim is pip installable using its GitHub:

```
pip install git+https://github.com/Gor-Ren/gym-jsbsim
```

## Environments

Gym-JSBSim implements two tasks for controlling the altitude and heading of aircraft:

* **HeadingControl**: aircraft must fly in a straight line, maintaining its initial altitude and direction of travel (heading)
* **TurnHeadingChangeLevelControlTask**: aircraft must make a turn and change its altitude

The environment can be configured to use one of three aircraft:

* **Cessna172P** light aircraft
* **F15** fighter jet
* **A320** airliner



Environment ID strings are constructed as follows:
```
f'JSBSim-{task}-{aircraft}-SHAPING_STANDARD-NoFG-v0'
```

For example, to fly a Cessna on the TurnHeadingControl task,

```
env = gym.make('JSBSim-TurnHeadingControl-Cessna172P-SHAPING.STANDARD-NoFG-v0')
```


## Visualisation

### 2D

A basic plot of agent actions and current state information can be using `human` render mode by calling `env.render(mode='human')`.


### 3D

3D visualisation requires installation of the FlightGear simulator. Confirm it is runnable from terminal with:

```
fgfs --version
```

Visualising with FlightGear requires the Gym to be created with a FlightGear-enabled environment ID by changing 'NoFG' -> 'FG'. For example,
```
env = gym.make('JSBSim-TurnHeadingControl-Cessna172P-SHAPING.STANDARD-FG-v0')
```
Then, the first call to `env.render(mode='flightgear')` will launch FlightGear and begin visualisation. 

## State and Action Space

Gym-JSBSim's environments have a continuous state and action space. The state depends on the task and is composed of properties declared in gym-jsbsim/properties.py.

```
(name='position/h-sl-ft', description='altitude above mean sea level [ft]', min=-1400, max=85000)
(name='attitude/pitch-rad', description='pitch [rad]', min=-1.5707963267948966, max=1.5707963267948966)
(name='attitude/roll-rad', description='roll [rad]', min=-3.141592653589793, max=3.141592653589793)
(name='attitude/psi-deg', description='heading [deg]', 0, 360)
(name='aero/beta-deg', description='sideslip [deg]', -180, +180)
(name='position/lat-geod-deg', description='geocentric latitude [deg]', -90, 90)
(name='position/long-gc-deg', description='geodesic longitude [deg]', -180, 180)
(name='velocities/u-fps', description='body frame x-axis velocity [ft/s]', min=-2200, max=2200)
(name='velocities/v-fps', description='body frame y-axis velocity [ft/s]', min=-2200, max=2200)
(name='velocities/w-fps', description='body frame z-axis velocity [ft/s]', min=-2200, max=2200)
(name='velocities/v-north-fps', description='velocity true north [ft/s]', float('-inf'), float('+inf'))
(name='velocities/v-east-fps', description='velocity east [ft/s]', float('-inf'), float('+inf'))
(name='velocities/v-down-fps', description='velocity downwards [ft/s]', float('-inf'), float('+inf'))
(name='velocities/p-rad_sec', description='roll rate [rad/s]', min=-6.283185307179586, max=6.283185307179586)
(name='velocities/q-rad_sec', description='pitch rate [rad/s]', min=-6.283185307179586, max=6.283185307179586)
(name='velocities/r-rad_sec', description='yaw rate [rad/s]', min=-6.283185307179586, max=6.283185307179586)
(name='fcs/left-aileron-pos-norm', description='left aileron position, normalised', min=-1, max=1)
(name='fcs/right-aileron-pos-norm', description='right aileron position, normalised', min=-1, max=1)
(name='fcs/elevator-pos-norm', description='elevator position, normalised', min=-1, max=1)
(name='fcs/rudder-pos-norm', description='rudder position, normalised', min=-1, max=1)
(name='fcs/throttle-pos-norm', description='throttle position, normalised', 0, 1)
(name='gear/gear-pos-norm', description='landing gear position, normalised', 0, 1)
 ```
 Actions tuples of floats in the range [-1,+1] describing commands to move the aircraft's control surfaces (ailerons, elevator, rudder) and to control the engines and the gears:
 ```
(name='fcs/aileron-cmd-norm', description='aileron commanded position, normalised', min=-1.0, max=1.0)
(name='fcs/elevator-cmd-norm', description='elevator commanded position, normalised', min=-1.0, max=1.0)
(name='fcs/rudder-cmd-norm', description='rudder commanded position, normalised', min=-1.0, max=1.0)
(name='fcs/throttle-cmd-norm', description='throttle commanded position, normalised', 0., 1.)
(name='fcs/mixture-cmd-norm', description='engine mixture setting, normalised', 0., 1.)
(name='fcs/throttle-cmd-norm[1]', description='throttle 1 commanded position, normalised', 0., 1.)
(name='fcs/mixture-cmd-norm[1]', description='engine mixture 1 setting, normalised', 0., 1.)
(name='gear/gear-cmd-norm', description='all landing gear commanded position, normalised', 0, 1)
 ```
