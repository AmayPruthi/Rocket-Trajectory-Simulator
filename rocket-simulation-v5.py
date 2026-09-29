import math
import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. CONSTANTS & ENVIRONMENT SETUP
# ==========================================
G = 6.67430e-11          # Gravitational constant
M_E = 5.972e24           # Mass of Earth in kg
R_E = 6371000.0          # Radius of Earth in meters
rho_0 = 1.225            # Sea-level air density (kg/m^3)
earth_rotation_speed = 465.0 

# ==========================================
# 2. ROCKET CONFIGURATION & STAGING
# ==========================================
s1_dry_mass, s1_fuel_mass, s1_thrust, s1_burn_time = 15000.0, 80000.0, 3500000.0, 90.0
s2_dry_mass, s2_fuel_mass, s2_thrust, s2_burn_time = 4000.0, 25000.0, 800000.0, 1200.0

current_stage = 1
dry_mass = s1_dry_mass
fuel_mass = s1_fuel_mass
max_thrust = s1_thrust
burn_time = s1_burn_time
fuel_burn_rate = fuel_mass / burn_time
stage_timer = 0.0

drag_coefficient = 0.15
cross_section_area = 12.0

# Initial State Vector (2D Coordinates)
x_pos = 0.0
y_pos = R_E
x_vel = earth_rotation_speed  
y_vel = 0.0
time = 0.0
dt = 0.5                  

ambient_temp = 288.15     
rocket_temp = ambient_temp
max_allowed_g = 4.0       

# Data History Logging for 2D Map & Graphs
time_history = []
alt_history = []
vel_history = []
temp_history = []
g_history = []

# 2D Map Tracking Lists
path_x = []
path_y = []

print("🚀 Liftoff! 2D Master Rocket Simulation Initialized...")
print("-" * 75)

# ==========================================
# 3. 2D SIMULATION MAIN LOOP
# ==========================================
while time < 2500:
    r = math.sqrt(x_pos**2 + y_pos**2)
    current_altitude = r - R_E
    
    # Track 2D positions (converting to kilometers for cleaner plotting)
    path_x.append(x_pos / 1000.0)
    path_y.append(y_pos / 1000.0)
    
    if current_altitude <= 0 and time > 1.0:
        print(f"T: {time:.1f}s | ❌ Crash! The rocket hit the Earth.")
        break
        
    # Stage Management
    if current_stage == 1:
        stage_timer += dt
        fuel_mass -= fuel_burn_rate * dt
        if stage_timer >= burn_time or fuel_mass <= 0:
            print(f"🔄 STAGE 1 SEPARATION at T: {time:.1f}s | Alt: {current_altitude/1000:.1f} km")
            current_stage = 2
            dry_mass = s2_dry_mass
            fuel_mass = s2_fuel_mass
            max_thrust = s2_thrust
            burn_time = s2_burn_time
            fuel_burn_rate = fuel_mass / burn_time
            stage_timer = 0.0
    elif current_stage == 2:
        stage_timer += dt
        fuel_mass -= fuel_burn_rate * dt
        if stage_timer >= burn_time or fuel_mass <= 0:
            max_thrust = 0.0
            fuel_mass = 0.0

    current_mass = dry_mass + fuel_mass

    # 2D Inverse-Square Gravity Vector
    g_force = (G * M_E) / (r**2)
    ux, uy = -x_pos / r, -y_pos / r
    g_acc_x, g_acc_y = g_force * ux, g_force * uy
    
    # Atmosphere & Heating
    air_density = rho_0 * math.exp(-current_altitude / 8500.0) if current_altitude < 100000 else 0.0
    speed = math.sqrt(x_vel**2 + y_vel**2)
    
    heating_factor = 1.8e-8 
    aerodynamic_heating = heating_factor * air_density * (speed**3)
    cooling_rate = 0.02 * (rocket_temp - ambient_temp)
    rocket_temp += (aerodynamic_heating - cooling_rate) * dt

    # Aerodynamic Drag Vector
    drag_force = 0.5 * air_density * (speed**2) * drag_coefficient * cross_section_area
    if speed > 0:
        drag_acc_x = -drag_force * (x_vel / speed) / current_mass
        drag_acc_y = -drag_force * (y_vel / speed) / current_mass
    else:
        drag_acc_x = drag_acc_y = 0.0

    # 2D Steering & Gravity Turn Program
    thrust_acc_x = thrust_acc_y = 0.0
    raw_thrust = max_thrust if fuel_mass > 0 else 0.0
    
    if raw_thrust > 0:
        if current_altitude < 3000:
            pitch_angle = math.pi / 2  
        else:
            fraction = min(current_altitude / 90000.0, 1.0)
            pitch_angle = (math.pi / 2) * (1.0 - fraction)
            
        theoretical_thrust_acc = raw_thrust / current_mass
        
        # G-Force Throttle Governor Check
        current_g = math.sqrt((g_acc_x + theoretical_thrust_acc * math.cos(pitch_angle))**2 + 
                              (g_acc_y + theoretical_thrust_acc * math.sin(pitch_angle))**2) / 9.8
        
        throttle = 1.0
        if current_g > max_allowed_g:
            throttle = max_allowed_g / current_g
            
        active_thrust_acc = (raw_thrust * throttle) / current_mass
        
        # Align thrust vector with 2D orbital orientation
        thrust_acc_x = active_thrust_acc * math.cos(pitch_angle)
        thrust_acc_y = active_thrust_acc * math.sin(pitch_angle)

    # Total 2D Acceleration Integration
    total_acc_x = g_acc_x + thrust_acc_x + drag_acc_x
    total_acc_y = g_acc_y + thrust_acc_y + drag_acc_y
    
    x_vel += total_acc_x * dt
    y_vel += total_acc_y * dt
    x_pos += x_vel * dt
    y_pos += y_vel * dt
    time += dt
    
    current_g_load = math.sqrt(total_acc_x**2 + total_acc_y**2) / 9.8
    
    time_history.append(time)
    alt_history.append(current_altitude / 1000.0)
    vel_history.append(speed)
    temp_history.append(rocket_temp - 273.15)
    g_history.append(current_g_load)
    
    if int(time * 10) % 100 == 0:
        print(f"T: {time:5.1f}s | Stg: {current_stage} | Alt: {current_altitude/1000:6.1f} km | Vel: {speed:6.1f} m/s | G-Load: {current_g_load:4.1f}g")
        
    if current_altitude >= 200000 and speed >= 7500:
        print("-" * 75)
        print(f"🎉 SUCCESS! Stable orbital insertion achieved at T: {time:.1f}s!")
        break

# ==========================================
# 4. 2D SPATIAL & TELEMETRY VISUALIZATION
# ==========================================
fig = plt.figure(figsize=(14, 8))

# Subplot 1: True 2D Orbital Trajectory over Earth's Curvature
ax_map = fig.add_subplot(1, 2, 1)
# Draw Earth's surface as a circle
earth_circle = plt.Circle((0, 0), R_E / 1000.0, color='lightblue', label='Earth Surface')
ax_map.add_patch(earth_circle)
ax_map.plot(path_x, path_y, color='darkblue', linewidth=2, label='Rocket Flight Path')
ax_map.set_title('2D Orbital Trajectory Map')
ax_map.set_xlabel('X Position (km)')
ax_map.set_ylabel('Y Position (km)')
ax_map.axis('equal')
ax_map.legend()
ax_map.grid(True)

# Subplot 2: Stacked Telemetry Graphs (Alt, Vel, Temp)
ax_tel1 = fig.add_subplot(3, 2, 2)
ax_tel1.plot(time_history, alt_history, color='blue')
ax_tel1.set_ylabel('Alt (km)')
ax_tel1.axhline(100, color='red', linestyle='--')
ax_tel1.grid(True)

ax_tel2 = fig.add_subplot(3, 2, 4)
ax_tel2.plot(time_history, vel_history, color='orange')
ax_tel2.set_ylabel('Vel (m/s)')
ax_tel2.grid(True)

ax_tel3 = fig.add_subplot(3, 2, 6)
ax_tel3.plot(time_history, temp_history, color='crimson')
ax_tel3.set_ylabel('Temp (°C)')
ax_tel3.set_xlabel('Time (s)')
ax_tel3.grid(True)

plt.tight_layout()
plt.show()
