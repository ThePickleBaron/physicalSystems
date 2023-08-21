import math

def pressure_drop(diameter, viscosity, flow_rate, pipe_length, specific_gravity, head):
    # Constants for water at nearly room temperature
    rho = specific_gravity * 998.2 # Density
    g = 9.81
    head_loss = head - pipe_length * g * rho

    # The calculation depend on the power-law characteristics.
    n = 0.8  # Flow behavior index - typical value for pseudoplastic fluids
    k = viscosity  # Consistency index

    velocity = flow_rate / (math.pi * (diameter ** 2) / 4)  
    reynolds_no = rho * velocity * diameter / viscosity  
    friction_factor = 16 / reynolds_no  # valid for laminar flow

    if reynolds_no > 2000:  # If not laminar flow, use Churchill correction
        friction_factor = 0.25 * (pow(math.log10((k/diameter) + 5.74 / pow(reynolds_no, 0.9)), -2))

    pressure_drop = friction_factor * (pipe_length / diameter) * 0.5 * rho * (velocity ** 2)

    return pressure_drop

diameter = 0.072
viscosity = 50  # Pa.s
flow_rate = 0.00013  # m^3/s
pipe_length = 100.0  # 1 meter
specific_gravity = 1.0  # for water
head = 3  # in meter

pd = pressure_drop(diameter, viscosity, flow_rate, pipe_length, specific_gravity, head)
print(f"Pressure drop: {pd} Pa")