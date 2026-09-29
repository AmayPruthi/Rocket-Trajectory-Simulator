# 🚀 Rocket Trajectory Simulator

A beginner Python project that simulates the vertical flight of a rocket.

The program calculates the rocket's:

* 🚀 Altitude
* 💨 Velocity
* 📐 Acceleration
* ⏱️ Flight time

It uses a simple numerical simulation with small time steps.

## 🧠 Physics Used

The simulation uses basic kinematics:

* Gravity = `-9.8 m/s²`
* Thrust acceleration = `20 m/s²`
* Fuel duration = `6 seconds`
* Time step = `0.1 seconds`

At every time step, the program updates velocity and then altitude.

## 💻 How to Run

Make sure Python is installed.

Run:

```bash
python rocket_simulator.py
```

The program will print the rocket's time, altitude and velocity during the simulation.

## 📊 Example Output

```text
Liftoff!
T: 0.1s | Alt: 0.1m | Vel: 1.0m/s
T: 0.2s | Alt: 0.3m | Vel: 2.0m/s
...
```

## 🎯 What I Learned

This project helped me practise:

* Python variables
* `while` loops
* `if/elif/else`
* Numerical simulation
* Velocity and acceleration
* Basic rocket-flight physics
* Time-step calculations

## 🔭 Future Improvements

I plan to improve the simulator by adding:

* Rocket mass
* Real thrust as a force
* Fuel mass decreasing over time
* Air resistance
* Variable gravity
* Maximum altitude
* Graphs of altitude and velocity
* Multiple rocket stages
* More realistic orbital calculations

## ⚠️ Important Note

This is an educational simulation, not a realistic rocket-flight model. Real rocket trajectories require many additional factors such as changing mass, atmospheric drag, varying gravity, thrust curves and guidance.
