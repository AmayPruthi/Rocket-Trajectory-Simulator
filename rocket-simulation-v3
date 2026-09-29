```python
import math

G = 6.67430e-11
M_E = 5.972e24
R_E = 6371000.0

dry_mass = 20000.0
fuel_mass = 80000.0
initial_mass = dry_mass + fuel_mass

thrust = 1500000.0
fuel_burn_rate = 500.0

dt = 0.1
time = 0.0

x_pos = 0.0
y_pos = R_E

x_vel = 0.0
y_vel = 0.0

print("Liftoff!")
print(f"Initial mass: {initial_mass / 1000:.1f} tonnes")
print(f"Thrust: {thrust / 1000:.0f} kN")

while True:

    mass = dry_mass + fuel_mass

    r = math.sqrt(x_pos**2 + y_pos**2)
    altitude = r - R_E

    gravity = (G * M_E) / (r**2)

    ux = -x_pos / r
    uy = -y_pos / r

    gravity_x = gravity * ux
    gravity_y = gravity * uy

    thrust_x = 0.0
    thrust_y = 0.0

    if fuel_mass > 0:

        if altitude < 10000:
            pitch_angle = 0.0
        else:
            pitch_angle = min(
                (altitude - 10000) / 150000,
                1.0
            ) * math.radians(85)

        thrust_x = math.sin(pitch_angle) * thrust / mass
        thrust_y = math.cos(pitch_angle) * thrust / mass

        fuel_used = fuel_burn_rate * dt
        fuel_mass = max(0.0, fuel_mass - fuel_used)

    speed = math.sqrt(x_vel**2 + y_vel**2)

    if speed > 0:
        density = 1.225 * math.exp(-altitude / 8500)

        drag_coefficient = 0.5
        reference_area = 10.0

        drag_force = (
            0.5
            * density
            * speed**2
            * drag_coefficient
            * reference_area
        )

        drag_x = -drag_force * x_vel / speed / mass
        drag_y = -drag_force * y_vel / speed / mass
    else:
        drag_x = 0.0
        drag_y = 0.0

    acceleration_x = (
        gravity_x
        + thrust_x
        + drag_x
    )

    acceleration_y = (
        gravity_y
        + thrust_y
        + drag_y
    )

    x_vel += acceleration_x * dt
    y_vel += acceleration_y * dt

    x_pos += x_vel * dt
    y_pos += y_vel * dt

    time += dt

    speed = math.sqrt(x_vel**2 + y_vel**2)

    if int(time * 10) % 100 == 0:
        print(
            f"T: {time:6.1f}s | "
            f"Alt: {altitude / 1000:7.2f} km | "
            f"Speed: {speed:7.1f} m/s | "
            f"Mass: {mass / 1000:6.1f} t | "
            f"Fuel: {fuel_mass / 1000:6.1f} t"
        )

    if altitude < 0 and time > 1:
        print("Crash! The rocket hit Earth.")
        break

    orbital_speed = math.sqrt(G * M_E / r)

    if altitude >= 200000 and speed >= orbital_speed * 0.95:
        print()
        print("Orbit achieved!")
        print(f"Time: {time:.1f} s")
        print(f"Altitude: {altitude / 1000:.1f} km")
        print(f"Speed: {speed:.1f} m/s")
        print(f"Remaining fuel: {fuel_mass / 1000:.1f} tonnes")
        break

    if fuel_mass <= 0 and altitude < 200000:
        print()
        print("Fuel exhausted.")
        print(f"Maximum altitude reached so far: {altitude / 1000:.1f} km")
        break

    if time > 2000:
        print("Simulation stopped.")
        break
```
