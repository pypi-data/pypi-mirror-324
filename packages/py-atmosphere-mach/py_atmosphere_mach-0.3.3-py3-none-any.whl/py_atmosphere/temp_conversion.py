def temp_conversion(properties, property_to_change, desired_unit):
    """
    Convert the units of a selected atmospheric property.

    Parameters:
    ------------
    properties : List
        A three-element list that describes the inputed altitude (km), along with the temperature (Celsius) and pressure (KiloPascal) of the air. 
        This is typically the output of `py_atmosphere` function.
    property_to_change : str
        Selected property for which units need to be changed. Valid inputs are: "altitude", "temperature", "pressure"
    desired_unit : str
        The desired units for the selected property.
        Valid units for temperature: C (Celsius), F (Fahrenheit), K (Kelvin), R (Rankine)
        Valid units for altitude: m (meters), km (kilometers), ft (feet), miles (miles)
        Valid units for pressure: bar (bar), kPa (KiloPascal), psia (Pounds over square inch)
        

    Returns:
    ---------
    list
        A three-element list with the selected property converted to the specified units.

    Examples
    ----------
    >>> temp_conversion([0.0, 15.04, 101325], "temperature", "K")
    [0.0, 288.19, 101325]
    """
    #Initialize list
    output_temp = properties[1]
    output_alt = properties[0]
    output_p = properties[2]
    
    # Check if property is 'temperature'
    if property_to_change == "temperature":
        temp_celsius = properties[1]  # Temperature in Celsius
        if desired_unit == "F":
            output_temp = (temp_celsius * 9/5) + 32  # Convert Celsius to Fahrenheit
        elif desired_unit == "K":
            output_temp = temp_celsius + 273.15  # Convert Celsius to Kelvin
        elif desired_unit == "R":
            output_temp = (temp_celsius + 273.15) * 9/5  # Convert Celsius to Rankine
        elif desired_unit == "C":
            # If the desired unit is Celsius, no change needed
            pass
        else:
            raise ValueError("Invalid desired unit for temperature. Valid units are: 'C', 'F', 'K', 'R'.")
    
    # Check if property is 'altitude'
    elif property_to_change == "altitude":
        altitude_m = properties[0]  # Altitude in meters
        if desired_unit == "m":
            # If the desired unit is meters, no change needed
            pass
        elif desired_unit == "km":
            output_alt = altitude_m / 1000  # Convert meters to kilometers
        elif desired_unit == "ft":
            output_alt = altitude_m * 3.28084  # Convert meters to feet
        elif desired_unit == "miles":
            output_alt = altitude_m * 0.000621371  # Convert meters to miles
        else:
            raise ValueError("Invalid desired unit for altitude. Valid units are: 'm', 'km', 'ft', 'miles'.")
    
    # Check if property is 'pressure'
    elif property_to_change == "pressure":
        pressure_pa = properties[2]  # Pressure in Pascal
        if desired_unit == "kPa":
            # If the desired unit is KiloPascal, no change needed
            pass
        elif desired_unit == "bar":
            output_p = pressure_pa / 100  # Convert KiloPascal to bar
        elif desired_unit == "psia":
            output_p = pressure_pa * 0.1450377  # Convert KiloPascal to psia
        else:
            raise ValueError("Invalid desired unit for pressure. Valid units are: 'kPa', 'bar', 'psia'.")
    
    else:
        raise ValueError("Invalid property. Valid properties are: 'altitude', 'temperature', 'pressure'.")
    
    return [output_alt, output_temp, output_p]