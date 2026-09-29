altitude = 0.0
velocity = 0.0
time = 0.0

gravity = -9.8
thrust = 20
fuel = 6.0

dt = 0.1

print("Liftoff!")

while True:

    if time < fuel:
        acceleration = thrust + gravity
    elif altitude >= 100000:
        acceleration = 50.0
    else:
        acceleration = gravity

    time += dt
    velocity += acceleration * dt
    altitude += velocity * dt

    print(
        f"T: {time:.1f}s | "
        f"Alt: {altitude:.1f}m | "
        f"Vel: {velocity:.1f}m/s"
    )

    if altitude < 0:
        print("Crash! The rocket hit the ground.")
        break

    if altitude > 200000:
        print("Success! The rocket has journeyed deep into space.")
        break
