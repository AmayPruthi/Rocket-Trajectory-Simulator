```python
import math

G = 6.67430e-11
M_E = 5.972e24
R_E = 6371000.0

x_pos = 0.0
y_pos = R_E
x_vel = 0.0
y_vel = 0.0
time = 0.0

thrust = 15.0
fuel_burn_time = 30000.0
dt = 0.5

print("Liftoff! Starting simulation...")

while True:
    r = math.sqrt(x_pos**2 + y_pos**2)
    current_altitude = r - R_E

    g_force = (G * M_E) / (r**2)

    ux = -x_pos / r
    uy = -y_pos / r

    g_acc_x = g_force * ux
    g_acc_y = g_force * uy

    thrust_acc_x = 0.0
    thrust_acc_y = 0.0

    if time < fuel_burn_time:
        if current_altitude < 10000:
            thrust_acc_y = thrust
        else:
            pitch_factor = min(current_altitude / 100000.0, 1.0)
            thrust_acc_x = thrust * pitch_factor
            thrust_acc_y = thrust * (1.0 - pitch_factor * 0.7)

    total_acc_x = g_acc_x + thrust_acc_x
    total_acc_y = g_acc_y + thrust_acc_y

    x_vel += total_acc_x * dt
    y_vel += total_acc_y * dt

    x_pos += x_vel * dt
    y_pos += y_vel * dt

    time += dt

    speed = math.sqrt(x_vel**2 + y_vel**2)

    if int(time * 10) % 100 == 0:
        print(
            f"T: {time:.1f}s | "
            f"Alt: {current_altitude/1000:.2f} km | "
            f"Speed: {speed:.1f} m/s"
        )

    if current_altitude <= 0 and time > 1.0:
        print("Crash! The rocket hit the Earth.")
        break

    if current_altitude >= 200000 and speed > 7000:
        print(
            f"Success! Stable orbit achieved at T: {time:.1f}s! "
            f"Alt: {current_altitude/1000:.1f}km, "
            f"Speed: {speed:.1f}m/s"
        )
        break

    if time > 1000:
        print("Simulation ended.")
        break
```

For GitHub, I'd name this file:

`v2_gravity_orbit_simulation.py`

One thing to fix later: **30,000 seconds of fuel burn is about 8.3 hours**, which is extremely long for this simplified rocket model. We can correct the physics when we build V3.
