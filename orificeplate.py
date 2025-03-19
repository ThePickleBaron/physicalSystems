import math

# Define our known values
Q_original = 120  # gpm
Q_target = 18  # cubic meters per hour

# Convert original flow to cubic meters per hour
gpmToCubicMetersPerHour = 0.00378541 * 60
Q_original_m3h = Q_original * gpmToCubicMetersPerHour
print(f"Original flow: {Q_original} gpm = {Q_original_m3h:.2f} cubic meters/hour")
print(f"Target flow: {Q_target} cubic meters/hour")

# Using a 3-inch ID pipe = 3 inches = 76.2 mm = 0.0762 m
D_pipe = 0.0762  # meters
A_pipe = math.pi * (D_pipe/2)**2
print(f"Pipe diameter: {D_pipe} m (3-inch ID), Area: {A_pipe:.6f} m²")

# Calculate the flow ratio (beta)
flow_ratio = Q_target / Q_original_m3h
print(f"Flow ratio (target/original): {flow_ratio:.4f}")

# Assume a discharge coefficient Cd for a sharp-edged orifice
Cd = 0.62


# Solve iteratively for beta = d/D (orifice diameter / pipe diameter)
def calculateBeta(flowRatio, initialGuess=0.5):
    # Beta = d/D (orifice diameter / pipe diameter)
    beta = initialGuess
    tolerance = 0.0001
    maxIterations = 100
    iterations = 0
    delta = 1

    while abs(delta) > tolerance and iterations < maxIterations:
        # Calculate flow ratio based on current beta value
        # For an orifice, the flow equation gives us:
        # flowRatio = (beta²)/√(1-beta⁴)
        calculatedFlowRatio = (beta**2) / math.sqrt(1 - beta**4)

        delta = calculatedFlowRatio - flowRatio

        # Adjust beta based on the error
        beta = beta - delta * 0.1  # Damping factor to prevent overshooting

        iterations += 1

    print(f"Converged after {iterations} iterations")
    return beta


# Calculate the beta (d/D) value
beta = calculateBeta(flow_ratio)
print(f"Beta (d/D): {beta:.4f}")

# Calculate the orifice diameter
D_orifice = beta * D_pipe
print(f"Orifice diameter: {D_orifice:.4f} m = {D_orifice*1000:.1f} mm")

# Calculate pressure drop (approximate)
# Assuming water at room temperature, ρ = 1000 kg/m³
rho = 1000  # kg/m³
g = 9.81  # m/s²

# Convert flow rates to m³/s
Q_original_m3s = Q_original_m3h / 3600
Q_target_m3s = Q_target / 3600

# Calculate velocity in pipe
V_pipe = Q_original_m3s / A_pipe
print(f"Flow velocity in pipe: {V_pipe:.2f} m/s")

# Calculate the orifice area
A_orifice = math.pi * (D_orifice/2)**2

# Calculate pressure drop using the orifice equation
# ΔP = (ρ/2) * (Q/(Cd*A_orifice))²
delta_P = (rho/2) * (Q_target_m3s/(Cd*A_orifice))**2
print(f"Pressure drop across orifice: {delta_P/1000:.2f} kPa ({delta_P/6894.76:.2f} psi)")

# Calculate Reynolds number for the pipe flow (to check if flow is turbulent)
# Assuming water at 20°C, kinematic viscosity ν = 1.004 × 10^-6 m²/s
nu = 1.004e-6  # m²/s
Re_pipe = V_pipe * D_pipe / nu
print(f"Reynolds number in pipe: {Re_pipe:.0f}")