import math

def py_atmosphere(altitude, alt_units):
    """
    Display Glenn Research Center Earth Atmosphere Model air properties for a given altitude.

    This function calculates standard air properties (temperature, pressure, and density) based on NASA's Glenn Research Center Earth Atmosphere Model. 
    The input altitude, provided in a specified unit, is first converted to a standard unit (kilometers) for processing. 
    The resulting air properties are returned in degrees Celsius (temperature) and KiloPascals (pressure).

    Basic equations used: https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html#:~:text=In%20the%20troposphere%2C%20the%20temperature,atmosphere%20model%20is%20also%20available.
    
    Parameters:
    ------------
    altitude : float
        A numeric value that represents the altitude of interest. This value is the reference to extract air properties, specifically, temperature and pressure.
    alt_units : str
        The unit of the input altitude. Valid units are: m (meters), km (kilometers), ft (feet), miles (miles)

    Returns:
    ---------
    list
        A list containing four elements that describes the inputed altitude (m), along with the temperature (Celsius) and pressure (KiloPascal).

    Examples
    ----------
    >>> py_atmosphere(0.0, "ft")
    [0.0, 15.04, 101.29]
    >>> py_atmosphere(11000.0, "m")
    [11000.0, -56.35, 22.734909933285515]
    """

    if not isinstance(altitude, (int, float)):
        raise TypeError("Altitude must be a numeric value (int or float)")
    if altitude < 0:
        raise ValueError("Altitude must be a non-negative value")
    
    ### Manage units for altitude input
    if alt_units == "m":
        alt = altitude
    elif alt_units == "ft":
        alt = altitude * 0.3048
    elif alt_units == "km":
        alt = altitude * 1000
    elif alt_units == "miles":
        alt = altitude * 1000 * 1.60934
    else:
        raise ValueError("Invalid altitude unit. Valid units are: 'm', 'km', 'ft', 'miles'.")
    
    ### Calculate Temperature and Pressure as a function of Altitude
    if alt == 0.0:
        temp = 15.04
        press = 101.29
    elif (alt > 0.0 and alt <=11000):
        temp = 15.04 - 6.49*(alt/1000)
        press = 101.29 * ((temp + 273.15)/288.08) ** 5.256
    elif (alt > 11000.0 and alt <=25000):
        temp = -56.46
        press = 22.65 * math.exp(1.73-0.000157*(alt))
    else:
        raise ValueError("Invalid altitude value. Model maximum value is 25,000 m.")
    
    return [alt, temp, press]
        
