import math

# ==========================================
# 1. EARTH
# ==========================================

G = 6.67430e-11
M_E = 5.972e24
R_E = 6371000.0
MU = G * M_E

rho_0 = 1.225
scale_height = 8500.0

earth_rotation_speed = 465.0


# ==========================================
# 2. ROCKET STAGES
# ==========================================

stage1 = {
    "dry_mass": 15000.0,
    "fuel_mass": 80000.0,
    "thrust": 3500000.0,
    "burn_time": 90.0
}

stage2 = {
    "dry_mass": 4000.0,
    "fuel_mass": 25000.0,
    "thrust": 800000.0,
    "burn_time": 1200.0
}

current_stage = 1

fuel_mass = stage1["fuel_mass"]
stage_time = 0.0

dry_mass = stage1["dry_mass"]

# Upper stage is carried by stage 1
upper_stage_mass = (
    stage2["dry_mass"] +
    stage2["fuel_mass"]
)


# ==========================================
# 3. ROCKET AERODYNAMICS
# ==========================================

Cd = 0.15
cross_section_area = 12.0

max_g = 4.0

ambient_temperature = 288.15
rocket_temperature = ambient_temperature

heating_factor = 1.8e-8


# ==========================================
# 4. INITIAL STATE
# ==========================================

x = 0.0
y = R_E

vx = earth_rotation_speed
vy = 0.0

time = 0.0

dt = 0.5


# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================

def magnitude(a, b):
    return math.sqrt(a * a + b * b)


def gravity(x, y):

    r = magnitude(x, y)

    gx = -MU * x / (r ** 3)
    gy = -MU * y / (r ** 3)

    return gx, gy


def atmosphere(altitude):

    if altitude <= 0:
        return rho_0

    if altitude >= 120000:
        return 0.0

    return rho_0 * math.exp(
        -altitude / scale_height
    )


def orbital_velocity(altitude):

    r = R_E + altitude

    return math.sqrt(MU / r)


def orbital_energy(r, speed):

    return (speed ** 2 / 2) - (MU / r)


def eccentricity(x, y, vx, vy):

    r = magnitude(x, y)
    v = magnitude(vx, vy)

    radial_velocity = (
        x * vx +
        y * vy
    )

    ex = (
        ((v ** 2 - MU / r) * x)
        - radial_velocity * vx
    ) / MU

    ey = (
        ((v ** 2 - MU / r) * y)
        - radial_velocity * vy
    ) / MU

    return magnitude(ex, ey)


def orbital_parameters(x, y, vx, vy):

    r = magnitude(x, y)
    v = magnitude(vx, vy)

    energy = orbital_energy(r, v)

    e = eccentricity(
        x, y, vx, vy
    )

    if energy < 0:

        semi_major_axis = -MU / (2 * energy)

        perigee = (
            semi_major_axis *
            (1 - e)
            - R_E
        )

        apogee = (
            semi_major_axis *
            (1 + e)
            - R_E
        )

    else:

        perigee = None
        apogee = None

    return energy, e, perigee, apogee


# ==========================================
# 6. START SIMULATION
# ==========================================

print("=" * 70)
print("V6 FULL 2D ORBITAL ROCKET SIMULATOR")
print("=" * 70)

while time < 2500:

    # --------------------------------------
    # POSITION
    # --------------------------------------

    r = magnitude(x, y)

    altitude = r - R_E

    speed = magnitude(vx, vy)


    # --------------------------------------
    # CRASH CHECK
    # --------------------------------------

    if altitude <= 0 and time > 2:

        print()
        print("CRASH: Rocket impacted Earth.")
        break


    # ======================================
    # STAGE SYSTEM
    # ======================================

    if current_stage == 1:

        thrust = stage1["thrust"]

        fuel_burn_rate = (
            stage1["fuel_mass"] /
            stage1["burn_time"]
        )

        fuel_used = (
            fuel_burn_rate * dt
        )

        fuel_used = min(
            fuel_used,
            fuel_mass
        )

        fuel_mass -= fuel_used

        stage_time += dt

        if (
            fuel_mass <= 0
            or stage_time >= stage1["burn_time"]
        ):

            fuel_mass = 0.0

            print()
            print(
                f"STAGE 1 SEPARATION"
            )

            print(
                f"Time: {time:.1f} s"
            )

            print(
                f"Altitude: "
                f"{altitude / 1000:.1f} km"
            )

            current_stage = 2

            dry_mass = stage2["dry_mass"]

            fuel_mass = stage2["fuel_mass"]

            stage_time = 0.0


    elif current_stage == 2:

        thrust = stage2["thrust"]

        fuel_burn_rate = (
            stage2["fuel_mass"] /
            stage2["burn_time"]
        )

        fuel_used = (
            fuel_burn_rate * dt
        )

        fuel_used = min(
            fuel_used,
            fuel_mass
        )

        fuel_mass -= fuel_used

        stage_time += dt

        if (
            fuel_mass <= 0
            or stage_time >= stage2["burn_time"]
        ):

            fuel_mass = 0.0
            thrust = 0.0

            print()
            print(
                f"STAGE 2 ENGINE CUTOFF"
            )

            print(
                f"Time: {time:.1f} s"
            )


    # ======================================
    # MASS
    # ======================================

    if current_stage == 1:

        current_mass = (
            dry_mass +
            fuel_mass +
            upper_stage_mass
        )

    else:

        current_mass = (
            dry_mass +
            fuel_mass
        )


    # ======================================
    # GRAVITY
    # ======================================

    gx, gy = gravity(x, y)


    # ======================================
    # ATMOSPHERE
    # ======================================

    air_density = atmosphere(
        altitude
    )


    # ======================================
    # DRAG
    # ======================================

    drag_force = (
        0.5 *
        air_density *
        speed ** 2 *
        Cd *
        cross_section_area
    )

    if speed > 0:

        drag_ax = (
            -drag_force *
            vx /
            speed /
            current_mass
        )

        drag_ay = (
            -drag_force *
            vy /
            speed /
            current_mass
        )

    else:

        drag_ax = 0.0
        drag_ay = 0.0


    # ======================================
    # THRUST DIRECTION
    # ======================================

    thrust_ax = 0.0
    thrust_ay = 0.0

    if thrust > 0:

        # Vertical launch

        if altitude < 3000:

            tx = -x / r
            ty = -y / r

        else:

            # Direction perpendicular to
            # Earth's radius

            horizontal_x = -y / r
            horizontal_y = x / r

            # Velocity direction

            if speed > 10:

                velocity_x = vx / speed
                velocity_y = vy / speed

            else:

                velocity_x = horizontal_x
                velocity_y = horizontal_y


            # Gravity turn

            turn = min(
                max(
                    (altitude - 3000)
                    / 70000,
                    0.0
                ),
                1.0
            )

            tx = (
                (1 - turn) *
                velocity_x
                +
                turn *
                horizontal_x
            )

            ty = (
                (1 - turn) *
                velocity_y
                +
                turn *
                horizontal_y
            )

            direction = magnitude(
                tx,
                ty
            )

            tx /= direction
            ty /= direction


        # ==================================
        # G LIMITER
        # ==================================

        raw_acceleration = (
            thrust /
            current_mass
        )

        predicted_ax = (
            gx +
            raw_acceleration * tx
        )

        predicted_ay = (
            gy +
            raw_acceleration * ty
        )

        predicted_g = (
            magnitude(
                predicted_ax,
                predicted_ay
            ) / 9.80665
        )

        throttle = 1.0

        if predicted_g > max_g:

            throttle = (
                max_g /
                predicted_g
            )

        active_thrust = (
            thrust *
            throttle
        )

        thrust_acceleration = (
            active_thrust /
            current_mass
        )

        thrust_ax = (
            thrust_acceleration *
            tx
        )

        thrust_ay = (
            thrust_acceleration *
            ty
        )


    # ======================================
    # ATMOSPHERIC HEATING
    # ======================================

    aerodynamic_heating = (
        heating_factor *
        air_density *
        speed ** 3
    )

    cooling = (
        0.02 *
        (
            rocket_temperature -
            ambient_temperature
        )
    )

    rocket_temperature += (
        aerodynamic_heating -
        cooling
    ) * dt


    # ======================================
    # TOTAL ACCELERATION
    # ======================================

    ax = (
        gx +
        drag_ax +
        thrust_ax
    )

    ay = (
        gy +
        drag_ay +
        thrust_ay
    )


    # ======================================
    # UPDATE VELOCITY
    # ======================================

    vx += ax * dt
    vy += ay * dt


    # ======================================
    # UPDATE POSITION
    # ======================================

    x += vx * dt
    y += vy * dt

    time += dt


    # ======================================
    # TELEMETRY
    # ======================================

    r = magnitude(x, y)

    altitude = r - R_E

    speed = magnitude(vx, vy)

    g_load = (
        magnitude(ax, ay) /
        9.80665
    )

    energy, e, perigee, apogee = (
        orbital_parameters(
            x,
            y,
            vx,
            vy
        )
    )


    # ======================================
    # TERMINAL OUTPUT
    # ======================================

    if int(time * 10) % 100 == 0:

        print(
            f"T={time:6.1f}s | "
            f"Stage={current_stage} | "
            f"Alt={altitude / 1000:7.1f} km | "
            f"V={speed:7.1f} m/s | "
            f"Fuel={fuel_mass:7.0f} kg | "
            f"G={g_load:4.1f}"
        )


    # ======================================
    # ORBIT DETECTION
    # ======================================

    circular_speed = orbital_velocity(
        max(altitude, 0)
    )

    if (
        altitude >= 200000
        and speed >= circular_speed * 0.97
        and energy < 0
        and e < 0.2
    ):

        print()
        print("=" * 70)
        print("ORBITAL INSERTION DETECTED")
        print("=" * 70)

        print(
            f"Time:       {time:.1f} s"
        )

        print(
            f"Altitude:   {altitude / 1000:.1f} km"
        )

        print(
            f"Velocity:   {speed:.1f} m/s"
        )

        print(
            f"Circular V: {circular_speed:.1f} m/s"
        )

        print(
            f"Eccentricity: {e:.4f}"
        )

        if perigee is not None:

            print(
                f"Perigee:    "
                f"{perigee / 1000:.1f} km"
            )

            print(
                f"Apogee:     "
                f"{apogee / 1000:.1f} km"
            )

        print("=" * 70)

        break


# ==========================================
# 7. END
# ==========================================

print()
print("Simulation finished.")
