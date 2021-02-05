import numpy as np

# 参数设计
temperature_low = np.random.normal(loc=20, scale=15, size=50)
temperature_high = temperature_low+np.random.normal(loc=40, scale=3, size=50)
width_low = np.random.normal(loc=20, scale=8, size=50)
width_high = width_low+np.random.normal(loc=30, scale=8, size=50)
extension_rate = np.random.normal(loc=50, scale=15, size=50)

moisture_tolerance = np.random.normal(loc=50, scale=20, size=50)
decomposition_rate = np.random.normal(loc=15, scale=5, size=50)

print(temperature_low, temperature_high, width_low, width_high)

print(moisture_tolerance)
print(decomposition_rate)


#







