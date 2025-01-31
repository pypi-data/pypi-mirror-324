import math
from py_atmosphere.py_atmosphere import py_atmosphere

def mach_number(altitude, alt_units, speed):
    """
    Calculate the Mach number of an object moving at a given altitude.

    Given an altitude, and assumptions of air composition, this function calculates the speed of sound in m/s in 
    specific altitude using the formula: speed of sound = c = sqrt(gamma * R * T), where `gamma` and `R` are 
    standard air properties, and `T` is the temperature at the given altitude. Then it calculates the Mach number 
    of an object moving in said environment.
    The ratio of specific heats, gamma is 1.4.
    The gas constant R is 287.1 J/kg/K.
    Celsius to Kevin: Celsius + 273.15.

    Parameters:
    ------------
    altitude : float
        A numeric value that represents the altitude of interest. This value is the reference to extract air properties, specifically, temperature, pressure and density.
    alt_units : str
        Units of the altitude input to function. Valid units are: m (meters), km (kilometers), ft (feet), miles (miles).
    speed: float
        Speed of the object in m/s.

    Returns:
    ---------
    float
        The Mach number (adimensional) in specific altitude, calculated as: speed / speed of sound as calculated in speed_of_sound function.

    Examples
    ----------
    >>> mach_number(0.0, "ft", 340.4)
    1.0
    """
    # Check the validation for speed
    if not isinstance(speed, (int, float)):
        raise TypeError("Speed must be a numeric value (int or float)")
    if speed < 0:
        raise ValueError("Speed must be a non-negative value")
    
    # Constants for the speed of sound calculation
    gamma = 1.4  # Ratio of specific heats
    R = 287.05  # The gas constant in J/(kg·K)
    
    # Get temperature from py_atmosphere
    temp = py_atmosphere(altitude, alt_units)[1]  # Temperature in Celsius
    temp_k = temp + 273.15  # Convert Celsius to Kelvin
    
    # Calculate speed of sound
    speed_of_sound = math.sqrt(gamma * R * temp_k)
    
    # Calculate Mach number
    mach = speed / speed_of_sound
    
    return mach