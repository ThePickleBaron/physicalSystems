import matplotlib.pyplot as plt

def calculate_conductivity(diameter_mm, length_mm, resistivity_megaohms, probe_resistance_megaohms):
    corrected_resistivity_megaohms = resistivity_megaohms - probe_resistance_megaohms
    radius_mm = diameter_mm / 2
    area_mm2 = 3.14159265 * radius_mm ** 2
    length_m = length_mm / 1000
    area_m2 = area_mm2 / 1000000
    conductance_siemens = 1 / (corrected_resistivity_megaohms * 10**6)
    conductivity = (conductance_siemens * area_m2) / length_m
    return conductivity

# Get tube diameter, length, probe resistance, and temperature
diameter_mm = float(input("Enter the diameter of the tube in mm: "))
length_mm = float(input("Enter the length of the tube in mm: "))
probe_resistance_megaohms = float(input("Enter the probe resistance in megaohms: "))
temperature = float(input("Enter the temperature: "))

# Data to hold site information
site_data = {}

# Repeatedly ask for site location and resistivity
while True:
    site_location = input("Enter site location or type 'done': ")
    if site_location.lower() == 'done':
        break
    site_data[site_location] = []
    for i in range(4): # Require 4 resistivity tests per site
        resistivity_megaohms = float(input(f"Enter resistivity for test {i + 1} in megaohms: "))
        conductivity = calculate_conductivity(diameter_mm, length_mm, resistivity_megaohms, probe_resistance_megaohms)
        site_data[site_location].append(conductivity)

# Print comparison chart
print("\nComparison Chart:")
print("Site Location | Resistivity (MΩ) | Temperature | Conductivity (S/m)")
print("-" * 60)
for site, conductivities in site_data.items():
    for conductivity in conductivities:
        print(f"{site:<15} | {'-':<17} | {temperature:<12} | {conductivity}")

# Line graph with all readings
plt.figure(figsize=(10, 6))
for site, conductivities in site_data.items():
    plt.plot(conductivities, label=site)
plt.xlabel('Test Number')
plt.ylabel('Conductivity (S/m)')
plt.title('Conductivity Readings by Site Location')
plt.legend()
plt.show()

# Bar graph with the average for each site
plt.figure(figsize=(10, 6))
plt.bar(site_data.keys(), [sum(conductivities)/len(conductivities) for conductivities in site_data.values()])
plt.xlabel('Site Location')
plt.ylabel('Average Conductivity (S/m)')
plt.title('Average Conductivity Comparison by Site Location')
plt.show()
