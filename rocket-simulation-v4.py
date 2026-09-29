```python
import math

G = 6.67430e-11
M_E = 5.972e24
R_E = 6371000.0
rho_0 = 1.225

dry_mass = 25000.0
fuel_mass = 100000.0
thrust_force = 3500000.0
burn_time = 180.0
fuel_burn_rate = fuel_mass / burn_time
drag_coefficient = 0.2
cross_section_area = 10.0

x_pos = 0.0
y_pos = R_E
x_vel = 0.0
y_vel = 0.0
time = 0.0
dt = 0.5

print("Liftoff! Simulating mass loss, variable gravity, and atmospheric drag...")

while True:
    r = math.sqrt(x_pos**2 + y_pos**2)
    current_altitude = r - R_E

    if current_altitude <= 0 and time > 1.0:
        print("Crash! The rocket hit the Earth.")
        break

    if time < burn_time and fuel_mass > 0:
        current_mass = dry_mass + fuel_mass
        current_thrust = thrust_force

        fuel_used = min(fuel_burn_rate * dt, fuel_mass)
        fuel_mass -= fuel_used
    else:
        current_mass = dry_mass
        current_thrust = 0.0

    g_force = (G * M_E) / (r**2)

    ux = -x_pos / r
    uy = -y_pos / r

    g_acc_x = g_force * ux
    g_acc_y = g_force * uy

    if current_altitude < 100000:
        air_density = rho_0 * math.exp(-current_altitude / 8500.0)
    else:
        air_density = 0.0

    speed = math.sqrt(x_vel**2 + y_vel**2)

    drag_force = (
        0.5
        * drag_coefficient
        * air_density
        * cross_section_area
        * speed**2
    )

    if speed > 0:
        drag_acc_x = -drag_force * (x_vel / speed) / current_mass
        drag_acc_y = -drag_force * (y_vel / speed) / current_mass
    else:
        drag_acc_x = 0.0
        drag_acc_y = 0.0

    thrust_acc_x = 0.0
    thrust_acc_y = 0.0

    if current_thrust > 0:
        if current_altitude < 5000:
            pitch_angle = math.pi / 2
        else:
            fraction = min(current_altitude / 80000.0, 1.0)
            pitch_angle = (math.pi / 2) * (1.0 - fraction)

        thrust_acc_magnitude = current_thrust / current_mass

        thrust_acc_x = (
            thrust_acc_magnitude * math.cos(pitch_angle)
        )

        thrust_acc_y = (
            thrust_acc_magnitude * math.sin(pitch_angle)
        )

    total_acc_x = g_acc_x + thrust_acc_x + drag_acc_x
    total_acc_y = g_acc_y + thrust_acc_y + drag_acc_y

    x_vel += total_acc_x * dt
    y_vel += total_acc_y * dt

    x_pos += x_vel * dt
    y_pos += y_vel * dt

    time += dt

    r = math.sqrt(x_pos**2 + y_pos**2)
    current_altitude = r - R_E
    speed = math.sqrt(x_vel**2 + y_vel**2)

    if int(time * 10) % 100 == 0:
        print(
            f"T: {time:.1f}s | "
            f"Alt: {current_altitude / 1000:.1f}km | "
            f"Speed: {speed:.1f}m/s | "
            f"Mass: {current_mass:.0f}kg"
        )

    if current_altitude >= 200000 and speed > 7500:
        print(
            f"Success! Stable orbital insertion achieved "
            f"at T: {time:.1f}s!"
        )
        print(
            f"Final Altitude: {current_altitude / 1000:.1f} km, "
            f"Orbital Speed: {speed:.1f} m/s"
        )
        break

    if time > 2000:
        print("Simulation timeout.")
        break
```
