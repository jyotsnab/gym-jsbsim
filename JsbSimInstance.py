import jsbsim
import os
from typing import Dict, Union

class JsbSimInstance(object):
    """
    A class which wraps an instance of JSBSim and manages communication with it.
    """
    encoding = 'utf-8'  # encoding of bytes returned by JSBSim Cython funcs

    def __init__(self):
        root_dir = os.path.abspath("/home/gordon/Apps/jsbsim-code")
        self.sim = jsbsim.FGFDMExec(root_dir=root_dir)

    def __getitem__(self, key: str):
        """
        Retrieves specified simulation property.

        Properties are identified by strings. A list can be found in the JSBSim
        reference manual, launching JSBSim with '--catalog' command line arg or
        calling FGFDMExec.get_property_catalog().

        :param key: string, the property to be retrieved
        :return: object?, property value
        """
        return self.sim[key]

    def __setitem__(self, key: str, value):
        """
        Sets simulation property to specified value.

        Properties are identified by strings. A list can be found in the JSBSim
        reference manual, launching JSBSim with '--catalog' command line arg or
        calling FGFDMExec.get_property_catalog().

        Warning: JSBSim will create new properties if the specified one exists.
        If the property you are setting is read-only in JSBSim the operation
        will silently fail.

        :param key: string, the property to be retrieved
        :param value: object?, the value to be set
        """
        self.sim[key] = value

    def load_model(self, model_name: str) -> None:
        """
        Loads the specified aircraft config into the simulation.

        The root JSBSim directory aircraft folder is searched for the aircraft
        XML config file.

        :param model_name: string, the aircraft name
        """
        load_success = self.sim.load_model(model=model_name)

        if not load_success:
            raise RuntimeError('JSBSim could not find specified model_name model: '
                               + model_name)

    def get_model_name(self) -> str:
        """
        Gets the name of the aircraft model currently loaded in JSBSim.

        :return: string, the name of the aircraft model if one is loaded, or
            None if no model is loaded.
        """
        name: str = self.sim.get_model_name().decode(self.encoding)
        if name:
            return name
        else:
            # name is empty string, no model is loaded
            return None

    def initialise(self, model_name: str, init_conditions: Dict[str, Union[int, float]]=None) -> None:
        """
        Loads an aircraft and initialises simulation conditions.

        JSBSim creates an InitialConditions object internally when given an
        XML config file. This method either loads a basic set of ICs, or
        can be passed a dictionary with ICs. In the latter case a minimal IC
        XML file is loaded, and then the dictionary values are specified.

        TODO: investigate whether we can specify ICs without loading XML

        :param model_name: string, name of aircraft to be loaded
        :param init_conditions: dict mapping properties to their initial values
        """
        if init_conditions:
            # if we are specifying conditions, load a minimal file
            ic_file = 'minimal_ic.xml'
        else:
            ic_file = 'basic_ic.xml'

        ic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ic_file)
        self.sim.load_ic(ic_path, useStoredPath=False)
        self.load_model(model_name)

        # now that IC object is created in JSBSim, specify own conditions
        if init_conditions:
            for prop, value in init_conditions.items():
                self[prop] = value

        success = self.sim.run_ic()

        if not success:
            raise RuntimeError('JSBSim failed to init simulation conditions.')