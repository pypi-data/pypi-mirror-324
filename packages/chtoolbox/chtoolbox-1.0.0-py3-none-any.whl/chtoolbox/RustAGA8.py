import ctypes
from ctypes import c_double, c_uint32, Structure, POINTER
import os
import sys


class AGA8Calc:
    """ """

    def __init__(self, equation = 'GERG-2008'):

        self.Aga8Adapter = aga8(equation)

    def calculate(self, composition, pressure: float, temperature: float, pressure_unit = 'KPa', temperature_unit = 'K', molar_mass = None):
        """

        Parameters
        ----------
        composition : dict
            Composition containing component name as key and mole percent or mole fraction as value.
            
            C1 : methane
            N2 : nitrogen
            CO2 : carbon_dioxide
            C2 : ethane
            C3 : propane
            iC4 : isobutane
            nC4 : n_butane
            iC5 : isopentane
            nC5 : n_pentane
            nC6 : hexane
            nC7 : heptane
            nC8 : octane
            nC9 : nonane
            nC10 : decane
            H2 : hydrogen
            O2 : oxygen
            CO : carbon_monoxide
            H2O : water
            H2S : hydrogen_sulfide
            He : helium
            Ar : argon
            
        pressure : float
            P - Pressure

        temperature : float
            T - Temperature

        pressure_unit : str
            Unit of pressure. The default unit is kilopascal (kPa).

        temperature_unit : str
            Unit of temperature. The default unit is Kelvin (K).

        Returns
        -------
        results : TYPE
            Dictionary with properties from AGA8.
            
            '     P - Pressure [kPa]
            '     T - Temperature [k]
            '     Z - Compressibility factor [-]
            '  dPdD - First derivative of pressure with respect to density at constant temperature [kPa/(mol/l)]
            'd2PdD2 - Second derivative of pressure with respect to density at constant temperature [kPa/(mol/l)^2]
            'd2PdTD - Second derivative of pressure with respect to temperature and density [kPa/(mol/l)/K]
            '  dPdT - First derivative of pressure with respect to temperature at constant density (kPa/K)
            '     U - Internal energy [J/mol]
            '     H - Enthalpy [J/mol]
            '     S - Entropy [J/(mol-K)]
            '    Cv - Isochoric heat capacity [J/(mol-K)]
            '    Cp - Isobaric heat capacity [J/(mol-K)]
            '     W - Speed of sound [m/s]
            '     G - Gibbs energy [J/mol]
            '    JT - Joule-Thomson coefficient [K/kPa]
            ' Kappa - Isentropic Exponent [-]
            '     A - Helmholtz energy [J/mol]
            '     D - Molar density [mol/l]
            '    mm - Molar mass [g/mol]
            '   rho - Mass density [kg/m3]
            
            '   gas_composition - Dictionary containing the composition used in the calculations

        """

        #Convert pressure to kPa
        pressure_kPa = pressure_unit_conversion(
            pressure_value=pressure,
            pressure_unit=pressure_unit
            )

        #Convert temperature to K
        temperature_K = temperature_unit_conversion(
            temperature_value=temperature,
            temperature_unit=temperature_unit
            )

        results = {}

        #Convert composition to aga8 format
        Aga8fluid, AGA8comp = to_aga8_composition(composition)

        #Get Aga8fluid as dictionary. Only used for debug purpose
        Aga8fluidDict = {component : getattr(Aga8fluid,component) for component, _ in Aga8fluid._fields_}

        fluid_sum = sum([getattr(Aga8fluid, field) for field, _ in Aga8fluid._fields_])
        
        # # normalize composition of not already normalized
        if round(fluid_sum,10) != 1.0:
            raise Exception('Fluid composition do not sum to 1')
            # for field, _ in Aga8fluid._fields_:
            #     setattr(Aga8fluid, field, getattr(Aga8fluid, field)/fluid_sum)

        self.Aga8Adapter.set_composition(Aga8fluid)
        self.Aga8Adapter.set_pressure(pressure_kPa)
        self.Aga8Adapter.set_temperature(temperature_K)
        self.Aga8Adapter.calc_density()
        self.Aga8Adapter.calc_properties()  # calculate properties

        Aga8Properties = self.Aga8Adapter.get_properties()  # get properties

        results = {prop : getattr(Aga8Properties,prop) for prop, _ in Aga8Properties._fields_}

        #Calculate mass density
        if molar_mass is None:
            results['rho'] = results['d']*results['mm'] #mol/l * g/mol = g/l = kg/m3
        else:
            results['rho'] = results['d']*molar_mass #mol/l * g/mol = g/l = kg/m3

        #Add gas composition to results
        results['gas_composition'] = Aga8fluidDict

        #Add pressure and temperature to results
        results['pressure_kPa'] = pressure_kPa
        results['temperature_K'] = temperature_K

        return results
    

    
    def calculate_from_T_and_rho(self, composition, mass_density: float, temperature: float, temperature_unit = 'K', molar_mass = None):
        '''
        Calculate speed of sound at a given temperature and mass density (for example used in speed of sound correction in Gas Density Meters)
        This is a temporary implementation using scipy fsolve. This function (without fsolve) is available in the AGA8 Rust dll file and will be implemented. 
        This is why the scipy import is inside the function as well, to avoid dependency to scipy using regular calculations. 
        
        Parameters
        ----------
        gas_composition : TYPE
            Dictionary with component name as key and mole percent or mole fraction as value.
        mass_density : float
            Mass density [kg/m3]
        temperature : float
            Temperature. Unit of measure is defined by pressure_unit.
        temperature_unit : TYPE, optional
            Unit of measure for temperature. The default is 'K'.
        molar_mass : float, optional
            Molar mass can be given as an optional input [kg/kmol]. If this is given, this molar mass will be used to calculate the mass density instead of the AGA8 calculated molar mass. The default is None. In that case the AGA8 calculated molar mass will be used. 
        
        Returns
        -------
        results : TYPE
            Dictionary with properties from AGA8. (same as for the calculate method, with pressure added. Pressure unit is given by the pressure_unit input)
        '''
        
        #Convert temperature to K
        temperature_K = temperature_unit_conversion(
            temperature_value=temperature,
            temperature_unit=temperature_unit
            )

        results = {}

        #Convert composition to aga8 format
        Aga8fluid, AGA8comp = to_aga8_composition(composition)

        #Get Aga8fluid as dictionary. Only used for debug purpose
        Aga8fluidDict = {component : getattr(Aga8fluid,component) for component, _ in Aga8fluid._fields_}

        fluid_sum = sum([getattr(Aga8fluid, field) for field, _ in Aga8fluid._fields_])
        
        # # normalize composition of not already normalized
        if round(fluid_sum,10) != 1.0:
            raise Exception('Fluid composition do not sum to 1')
            # for field, _ in Aga8fluid._fields_:
            #     setattr(Aga8fluid, field, getattr(Aga8fluid, field)/fluid_sum)

        self.Aga8Adapter.set_composition(Aga8fluid)
        
        #Calculate molar mass if the molar mass is not specified
        if molar_mass is None:
            molar_mass = self.Aga8Adapter.calc_molar_mass()
        
        #Calculate molar density (mol/l)
        if molar_mass !=0:
            molar_density = mass_density / molar_mass #kg/m3 / kg/kmol --> kmol/m3 --> mol/l
        else:
            #Return blank dictionary of molar mass is 0, to avoid division by zero error
            return {}
        
        self.Aga8Adapter.set_density(molar_density)
        self.Aga8Adapter.set_temperature(temperature_K)

        pressure_kPa = self.Aga8Adapter.calc_pressure()        
        
        #Set the pressure obtained from the calculation
        self.Aga8Adapter.set_pressure(pressure_kPa)
        
        self.Aga8Adapter.calc_properties()  # calculate properties

        Aga8Properties = self.Aga8Adapter.get_properties()  # get properties

        results = {prop : getattr(Aga8Properties,prop) for prop, _ in Aga8Properties._fields_}

        #Calculate mass density
        if molar_mass is None:
            results['rho'] = results['d']*results['mm'] #mol/l * g/mol = g/l = kg/m3
        else:
            results['rho'] = results['d']*molar_mass #mol/l * g/mol = g/l = kg/m3

        #Add gas composition to results
        results['gas_composition'] = Aga8fluidDict
        
        #Add pressure and temperature to results
        results['pressure_kPa'] = pressure_kPa
        results['temperature_K'] = temperature_K

        return results

def pressure_unit_conversion(pressure_value, pressure_unit = 'KPa'):
    # Convert inputs to SI units, i.e. kPa
    if pressure_unit.lower() == 'bara':
        pressure = pressure_value * 100
    elif pressure_unit.lower() == 'pa':
        pressure = pressure_value / 1000
    elif pressure_unit.lower() == 'psi':
        pressure = pressure_value * 6.89476
    elif pressure_unit.lower() == 'psia':
        pressure = (pressure_value + 14.6959488) * 6.89476
    elif pressure_unit.lower() == 'psig':
        pressure = pressure_value * 6.89476 + 101.325
    elif pressure_unit.lower() == 'barg':
        pressure = pressure_value * 100 + 101.325
    elif pressure_unit.lower() == 'mpa':
        pressure = pressure_value * 1000
    elif pressure_unit.lower() == 'kpa':
        pressure = pressure_value
    else:
        raise Exception(f'Pressure unit "{pressure_unit}" not supported!')
    
    return pressure


def temperature_unit_conversion(temperature_value, temperature_unit = 'K'):
    # Convert inputs to SI units, i.e. Kelvin
    if temperature_unit.lower() == 'c':
        temperature = temperature_value + 273.15
    elif temperature_unit.lower() == 'f':
        temperature = (temperature_value - 32) * 5 / 9 + 273.15
    elif temperature_unit.lower() == 'k':
        temperature = temperature_value
    else:
        raise Exception(f'Temperature unit "{temperature_unit}" not supported!')

    return temperature


def to_aga8_composition(composition: dict):
    """

    Parameters
    ----------
    composition: Composition :
        

    Returns
    -------

    """

    AGA8fluid = AGA8_composition()

    comp_name_mapping = {}
    comp_name_mapping['C1'] = 'methane'
    comp_name_mapping['N2'] = 'nitrogen'
    comp_name_mapping['CO2'] = 'carbon_dioxide'
    comp_name_mapping['C2'] = 'ethane'
    comp_name_mapping['C3'] = 'propane'
    comp_name_mapping['iC4'] = 'isobutane'
    comp_name_mapping['nC4'] = 'n_butane'
    comp_name_mapping['iC5'] = 'isopentane'
    comp_name_mapping['nC5'] = 'n_pentane'
    comp_name_mapping['nC6'] = 'hexane'
    comp_name_mapping['nC7'] = 'heptane'
    comp_name_mapping['nC8'] = 'octane'
    comp_name_mapping['nC9'] = 'nonane'
    comp_name_mapping['nC10'] = 'decane'
    comp_name_mapping['H2'] = 'hydrogen'
    comp_name_mapping['O2'] = 'oxygen'
    comp_name_mapping['CO'] = 'carbon_monoxide'
    comp_name_mapping['H2O'] = 'water'
    comp_name_mapping['H2S'] = 'hydrogen_sulfide'
    comp_name_mapping['He'] = 'helium'
    comp_name_mapping['Ar'] = 'argon'

    composition_sum = sum(composition.values())

    #normalize composition within the for loop. Store it in a individual dictionary
    composition_normalized = {}
    
    #{key : value/sum(composition.values()) for key, value in composition.items()}


    for component, mole_percent in composition.items():
        
        #normalize each component
        composition_normalized[component] = mole_percent/composition_sum

        mole_fraction = composition_normalized[component]

        comp_name = component.split(sep='-')[0]

        if comp_name[0] == 'C' and comp_name[1].isnumeric():

            Cn = int(comp_name[1:])

            #Components with carbon numbers from C6 to C9 are assigned to the corresponding normal alkane
            if Cn in [6,7,8,9]:
                setattr(AGA8fluid, comp_name_mapping[f'nC{Cn}'], mole_fraction)
            
            #Components with carbon number equal or greater than 10, is assigned to nC10
            elif Cn >= 10:
                setattr(AGA8fluid, comp_name_mapping['nC10'], mole_fraction)
            
            #Components with carbon numbers below C6 is assigned to the appropriate AGA8 component. For example C3 or iC4
            else:
                setattr(AGA8fluid, comp_name_mapping[comp_name], mole_fraction)
                
                
                # if comp_name in list(comp_name_mapping.keys()):  #if the carbon number is not found, for example for C3, the
                #     # function looks for the component in the AGA8 fluid and adds the component
                #     setattr(AGA8fluid, comp_name_mapping[comp_name], composition.Components[comp].MoleFraction)

        else:
            if comp_name in list(comp_name_mapping.keys()):  # if the carbon number is not found, for example for C3, the
                # function looks for the component in the AGA8 fluid and adds the component
                setattr(AGA8fluid, comp_name_mapping[comp_name], mole_fraction)
            else:
                raise Exception(f'Illegal component: {comp_name}')

    return AGA8fluid, list(composition_normalized.values())


class AGA8_Equation(Structure):
    """ """
    pass

class AGA8_composition(Structure):
    """ """
    _fields_ = [("methane", c_double),
                ("nitrogen", c_double),
                ("carbon_dioxide", c_double),
                ("ethane", c_double),
                ("propane", c_double),
                ("isobutane", c_double),
                ("n_butane", c_double),
                ("isopentane", c_double),
                ("n_pentane", c_double),
                ("hexane", c_double),
                ("heptane", c_double),
                ("octane", c_double),
                ("nonane", c_double),
                ("decane", c_double),
                ("hydrogen", c_double),
                ("oxygen", c_double),
                ("carbon_monoxide", c_double),
                ("water", c_double),
                ("hydrogen_sulfide", c_double),
                ("helium", c_double),
                ("argon", c_double)]

class Properties(Structure):
    """ """
    _fields_ = [("d", c_double),
                ("mm", c_double),
                ("z", c_double),
                ("dp_dd", c_double),
                ("d2p_dd2", c_double),
                ("dp_dt", c_double),
                ("u", c_double),
                ("h", c_double),
                ("s", c_double),
                ("cv", c_double),
                ("cp", c_double),
                ("w", c_double),
                ("g", c_double),
                ("jt", c_double),
                ("kappa", c_double)]

class Aga8Lib:
    """ """

    def __init__(self, equation):
        self.equation = equation

        lib_path = os.path.dirname(os.path.realpath(__file__)) + '/aga8' + {'darwin': '.dylib', 'win32': '.dll'}.get(
            sys.platform, '.so')
        self.lib = ctypes.cdll.LoadLibrary(lib_path)

        if self.equation.upper() == 'GERG-2008':
            self.lib.gerg_new.restype = POINTER(AGA8_Equation)
            self.lib.gerg_free.argtypes = (POINTER(AGA8_Equation),)
            self.lib.gerg_set_composition.argtypes = (POINTER(AGA8_Equation), POINTER(AGA8_composition), POINTER(c_uint32))
            self.lib.gerg_set_pressure.argtypes = (POINTER(AGA8_Equation), c_double)
            self.lib.gerg_set_temperature.argtypes = (POINTER(AGA8_Equation), c_double)
            self.lib.gerg_calculate_density.argtypes = (POINTER(AGA8_Equation), POINTER(c_uint32))
            self.lib.gerg_calculate_properties.argtypes = (POINTER(AGA8_Equation),)
            self.lib.gerg_get_properties.argtypes = (POINTER(AGA8_Equation),)
            self.lib.gerg_get_properties.restype = Properties
            self.lib.gerg_calculate_pressure.argtypes = (POINTER(AGA8_Equation),)
            self.lib.gerg_calculate_pressure.restype = c_double
            self.lib.gerg_set_density.argtypes = (POINTER(AGA8_Equation), c_double)
            self.lib.gerg_calculate_molar_mass.argtypes = (POINTER(AGA8_Equation),)
            self.lib.gerg_calculate_molar_mass.restype = c_double
            
        elif self.equation.upper() == 'DETAIL':
            self.lib.aga8_new.restype = POINTER(AGA8_Equation)
            self.lib.aga8_free.argtypes = (POINTER(AGA8_Equation),)
            self.lib.aga8_set_composition.argtypes = (POINTER(AGA8_Equation), POINTER(AGA8_composition), POINTER(c_uint32))
            self.lib.aga8_set_pressure.argtypes = (POINTER(AGA8_Equation), c_double)
            self.lib.aga8_set_temperature.argtypes = (POINTER(AGA8_Equation), c_double)
            self.lib.aga8_calculate_density.argtypes = (POINTER(AGA8_Equation), POINTER(c_uint32))
            self.lib.aga8_calculate_properties.argtypes = (POINTER(AGA8_Equation),)
            self.lib.aga8_get_properties.argtypes = (POINTER(AGA8_Equation),)
            self.lib.aga8_get_properties.restype = Properties
            self.lib.aga8_calculate_pressure.argtypes = (POINTER(AGA8_Equation),)
            self.lib.aga8_calculate_pressure.restype = c_double
            self.lib.aga8_set_density.argtypes = (POINTER(AGA8_Equation), c_double)
            self.lib.aga8_calculate_molar_mass.argtypes = (POINTER(AGA8_Equation),)
            self.lib.aga8_calculate_molar_mass.restype = c_double

        else:
            raise Exception('Invalid equation selected. Must be either GERG-2008 or DETAIL')

class aga8:
    """ """
    def __init__(self, equation):
        self.equation = equation
        self.Aga8Lib = Aga8Lib(equation)
        
        if self.equation.upper() == 'GERG-2008':
            self.obj = self.Aga8Lib.lib.gerg_new()
        elif self.equation.upper() == 'DETAIL':
            self.obj = self.Aga8Lib.lib.aga8_new()

    def __enter__(self):
        return self

    def __del__(self):
        
        if self.equation.upper() == 'GERG-2008':
            self.Aga8Lib.lib.gerg_free(self.obj)
        elif self.equation.upper() == 'DETAIL':
            self.Aga8Lib.lib.aga8_free(self.obj)            

    def __exit__(self, exc_type, exc_value, traceback):        
        if self.equation.upper() == 'GERG-2008':
            self.Aga8Lib.lib.gerg_free(self.obj)
        elif self.equation.upper() == 'DETAIL':
            self.Aga8Lib.lib.aga8_free(self.obj)
        

    def set_composition(self, comp):
        """

        Parameters
        ----------
        comp :
            

        Returns
        -------

        """
        
        status = c_uint32(0)
        
        if self.equation.upper() == 'GERG-2008':
            self.Aga8Lib.lib.gerg_set_composition(self.obj, comp, status)
        elif self.equation.upper() == 'DETAIL':
            self.Aga8Lib.lib.aga8_set_composition(self.obj, comp, status)
        
        if status.value != 0:
            raise Exception()
        
        
    def set_pressure(self, P):
        """

        Parameters
        ----------
        P : Pressure [kPa]
            

        Returns
        -------

        """
        if self.equation.upper() == 'GERG-2008':
            self.Aga8Lib.lib.gerg_set_pressure(self.obj, P)
        elif self.equation.upper() == 'DETAIL':
            self.Aga8Lib.lib.aga8_set_pressure(self.obj, P)
            
        
    def set_temperature(self, T):
        """

        Parameters
        ----------
        T : Temperature [K]
            

        Returns
        -------

        """
        if self.equation.upper() == 'GERG-2008':
            self.Aga8Lib.lib.gerg_set_temperature(self.obj, T)
        elif self.equation.upper() == 'DETAIL':
            self.Aga8Lib.lib.aga8_set_temperature(self.obj, T)


    def set_density(self, d):
        """

        Parameters
        ----------
        d : Molar density [mol/l]
            

        Returns
        -------

        """
        if self.equation.upper() == 'GERG-2008':
            self.Aga8Lib.lib.gerg_set_density(self.obj, d)
        elif self.equation.upper() == 'DETAIL':
            self.Aga8Lib.lib.aga8_set_density(self.obj, d)
        
        
    def calc_density(self):
        """ """
        if self.equation.upper() == 'GERG-2008':
            self.Aga8Lib.lib.gerg_calculate_density(self.obj, c_uint32(0))
        elif self.equation.upper() == 'DETAIL':
            self.Aga8Lib.lib.aga8_calculate_density(self.obj, c_uint32(0))
        
    def calc_properties(self):
        """ """        
        if self.equation.upper() == 'GERG-2008':
            self.Aga8Lib.lib.gerg_calculate_properties(self.obj)
        elif self.equation.upper() == 'DETAIL':
            self.Aga8Lib.lib.aga8_calculate_properties(self.obj)
        
    def calc_pressure(self):
        """ """
        if self.equation.upper() == 'GERG-2008':
            return self.Aga8Lib.lib.gerg_calculate_pressure(self.obj, c_uint32(0))
        elif self.equation.upper() == 'DETAIL':
            return self.Aga8Lib.lib.aga8_calculate_pressure(self.obj, c_uint32(0))

    def calc_molar_mass(self):
        """ """
        if self.equation.upper() == 'GERG-2008':
            return self.Aga8Lib.lib.gerg_calculate_molar_mass(self.obj, c_uint32(0))
        elif self.equation.upper() == 'DETAIL':
            return self.Aga8Lib.lib.aga8_calculate_molar_mass(self.obj, c_uint32(0))
    
    def get_properties(self):
        """ """
        
        if self.equation.upper() == 'GERG-2008':
            return self.Aga8Lib.lib.gerg_get_properties(self.obj)
        elif self.equation.upper() == 'DETAIL':
            return self.Aga8Lib.lib.aga8_get_properties(self.obj)
        