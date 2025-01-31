import logging
import string
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from roxieapi.commons.types import (
    BlockGeometry,
    BlockTopology,
    Brick3DGeometry,
    Coil3DGeometry,
    CoilGeometry,
    DesignVariableResult,
    Geometry,
    GraphPlot,
    HarmonicCoil,
    ObjectiveResult,
    Plot2D,
    Plot3D,
    WedgeGeometry,
)


class EddyCurrentsData:
    """Data for eddy currents calculations for every time_step"""

    def __init__(self, xroot) -> None:
        self._xroot = xroot

    def get_time_step_count(self) -> int:
        """
        Get the number of <time_step> elements in the XML file.

        Returns
        -------
        int
            The number of <time_step> elements found.
        """
        time_steps = self._xroot.findall(".//time_step")
        return len(time_steps)

    def get_info_on_timestep(self, time_step_index: int) -> dict:
        """
        Parse the information for the specified <time_step> to extract step_number and absolute_time.

        Parameters
        ----------
        time_step_index : int
            The index of the <time_step> element to parse.

        Returns
        -------
        dict
            A dictionary containing:
            - "step_number" (int): The time step number.
            - "absolute_time" (float): The absolute time for the present time step.
        """
        # Find all <time_step> elements
        time_steps = self._xroot.findall(".//time_step")

        # Handle the case where no <time_step> elements are found
        if time_steps is None or len(time_steps) == 0:
            raise ValueError("No <time_step> elements found in the XML file.")

        # Check if the time_step_index is within range
        if time_step_index >= len(time_steps) or time_step_index < 0:
            raise IndexError("time_step_index is out of range.")

        # Get the text content of the specified <time_step> element
        time_step_elem = time_steps[time_step_index]
        line = time_step_elem.text.strip() if time_step_elem.text else ""

        # Split the line by whitespace and parse the values
        try:
            _, step_number, absolute_time = line.split()
            step_number = int(step_number)
            absolute_time = float(absolute_time)
        except ValueError as err:
            raise ValueError("The <time_step> line format is incorrect.") from err

        return {"step_number": step_number, "absolute_time": absolute_time}

    def get_elements_info(self) -> dict:
        """
        Parse the <element_data> line to extract tot_ele and max_nodes.

        Returns
        -------
        dict
            A dictionary containing:
            - "tot_ele" (int): The total number of elements.
            - "max_nodes" (int): The maximum number of nodes.
        """
        # Find the <element_data> element
        element_data_elem = self._xroot.find(".//element_data")

        # Check if <element_data> element exists
        if element_data_elem is None or not element_data_elem.text:
            raise ValueError("<element_data> element is missing or empty.")

        # Extract text, strip any surrounding whitespace, and split by whitespace
        try:
            _, _, tot_ele, max_nodes = element_data_elem.text.strip().split()
        except ValueError as err:
            raise ValueError(
                "<element_data> is missing or has the wrong format."
            ) from err

        return {"tot_ele": int(tot_ele), "max_nodes": int(max_nodes)}

    def get_elements(self) -> pd.DataFrame:
        """
        Parse the <elements> data to extract details for each element.

        Returns
        -------
        pd.DataFrame
            A DataFrame with columns:
            - ele_num: Element number
            - hmo_ele: HMO element
            - ele_type: Element type
            - ele_collector: Element collector
            - nodes: List of node numbers (up to max_nodes)
        """
        # Find the <elements> element
        elements_elem = self._xroot.find(".//elements")

        # Handle the case where no <time_step> elements are found
        if elements_elem is None:
            raise ValueError("No <elements> found in the XML file.")

        # Check if <elements> element exists
        if elements_elem is None or not elements_elem.text:
            raise ValueError("<elements> element is missing or empty.")

        # Extract text content, strip whitespace, and split by lines
        lines = elements_elem.text.strip().split("\n")

        # Initialize a list to store element data
        element_data = []

        # Process each line in the <elements> data
        for line in lines[1:]:
            # Split line by whitespace
            columns = line.split()
            print(columns)

            # Parse the main attributes
            try:
                ele_num = int(columns[0])
                hmo_ele = int(columns[1])
                ele_type = int(columns[2])
                ele_collector = int(columns[3])
            except (ValueError, IndexError) as e:
                raise ValueError(
                    f"Wrong formatting of the <elements> line: {line}"
                ) from e

            # The remaining numbers are nodes (with padding zeros to max_nodes)
            nodes = list(map(int, columns[4:]))

            # Append to the data list
            element_data.append(
                {
                    "ele_num": ele_num,
                    "hmo_ele": hmo_ele,
                    "ele_type": ele_type,
                    "ele_collector": ele_collector,
                    "nodes": nodes,
                }
            )

        # Convert the list of dictionaries to a DataFrame
        return pd.DataFrame(element_data)

    def get_eddy_currents_on_timestep(self, time_step_index=0) -> pd.DataFrame:
        """
        Parse the eddy currents data from a specific time_step in the post.xml file.

        Parameters
        ----------
        time_step_index : int, optional
            The index of the <time_step> element from which to retrieve the <eddy_currents_data>.
            Defaults to 0, which is the first time_step.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the eddy currents data. The columns are
            - node: node number
            - elem: element number
            - jx: x component of the current density
            - jy: y component of the current density
            - jz: z component of the current density
            - j2/sigma: squared current density divided by the conductivity
        """
        # Find all <time_step> elements
        time_steps = self._xroot.findall(".//time_step")

        # Check if the time_step_index is within range
        if time_step_index >= len(time_steps) or time_step_index < 0:
            raise IndexError("time_step_index is out of range.")

        # Get the <eddy_currents_data> element for the specified time_step
        eddy_currents_elem = time_steps[time_step_index].find(".//eddy_currents_data")

        if eddy_currents_elem is None or not eddy_currents_elem.text:
            return (
                pd.DataFrame()
            )  # Return an empty DataFrame if the element is missing or empty

        # Extract and parse the text content
        data = eddy_currents_elem.text.strip()
        lines = data.split("\n")
        data_lines = lines[1:]  # Skip the header line

        # Parse the data into rows
        rows = [line.split() for line in data_lines]
        df = pd.DataFrame(rows, columns=["node", "elem", "jx", "jy", "jz", "j2/sigma"])

        # Convert columns to numeric and handle NaN
        df = df.apply(pd.to_numeric, errors="coerce")
        return df

    def get_eddy_currents_all_timesteps(self) -> pd.DataFrame:
        """
        Retrieve eddy currents data for all time steps and store it in a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing eddy currents data for all time steps. The columns are:
            - time_step: index of the time step
            - node: node number
            - elem: element number
            - jx: x component of the current density
            - jy: y component of the current density
            - jz: z component of the current density
            - j2/sigma: squared current density divided by the conductivity
            If no data exists, returns an empty DataFrame with the above columns.
        """
        # Find all <time_step> elements to get the total number of time steps
        time_steps = self._xroot.findall(".//time_step")
        time_steps_num = len(time_steps)

        # Initialize an empty list to store DataFrames for each time step
        all_data = []

        for i in range(time_steps_num):
            # Get the eddy currents data for the current time step
            df = self.get_eddy_currents_on_timestep(time_step_index=i)

            if not df.empty:
                # Add the time_step index as a new column
                df["time_step"] = i

                # Append the data for the current time step
                all_data.append(df)

        if all_data:
            # Concatenate all DataFrames into one
            eddy_currents_df = pd.concat(all_data, ignore_index=True)
        else:
            # Return an empty DataFrame with the appropriate column names
            eddy_currents_df = pd.DataFrame(
                columns=["time_step", "node", "elem", "jx", "jy", "jz", "j2/sigma"]
            )

        return eddy_currents_df

    def get_potential_on_timestep(self, time_step_index: int) -> pd.DataFrame:
        """
        Parse the potential data from a specific time_step in the post.xml file.

        Parameters
        ----------
        time_step_index : int
            The index of the <time_step> element from which to retrieve the <potential_data>.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the potential data. The columns are
            - node: node number
            - az: potential value
            - norm_deriv_az: normalized derivative of az
        """
        # Find all <time_step> elements
        time_steps = self._xroot.findall(".//time_step")

        # Check if the time_step_index is within range
        if time_step_index >= len(time_steps) or time_step_index < 0:
            raise IndexError("time_step_index is out of range.")

        # Get the <potential_data> element for the specified time_step
        potential_data_elem = time_steps[time_step_index].find(".//potential_data")

        if potential_data_elem is None or not potential_data_elem.text:
            return (
                pd.DataFrame()
            )  # Return an empty DataFrame if the element is missing or empty

        # Extract and parse the text content
        data = potential_data_elem.text.strip()
        lines = data.split("\n")
        data_lines = lines[1:]  # Skip the header line

        # Parse the data into rows
        rows = [line.split() for line in data_lines]
        df = pd.DataFrame(rows, columns=["node", "az", "norm_deriv_az"])

        # Convert columns to numeric and handle NaN
        df = df.apply(pd.to_numeric, errors="coerce")
        return df

    def get_potential_all_timesteps(self) -> pd.DataFrame:
        """
        Retrieve potential data for all time steps and store it in a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing potential data for all time steps. The columns are:
            - time_step: index of the time step
            - node: node number
            - az: potential value
            - norm_deriv_az: normalized derivative of az
            If no data exists, returns an empty DataFrame with the above columns.
        """
        # Find all <time_step> elements to get the total number of time steps
        time_steps = self._xroot.findall(".//time_step")
        time_steps_num = len(time_steps)

        # Initialize an empty list to store DataFrames for each time step
        all_data = []

        for i in range(time_steps_num):
            # Get the potential data for the current time step
            df = self.get_potential_on_timestep(time_step_index=i)

            if not df.empty:
                # Add the time_step index as a new column
                df["time_step"] = i

                # Append the data for the current time step
                all_data.append(df)

        if all_data:
            # Concatenate all DataFrames into one
            potential_df = pd.concat(all_data, ignore_index=True)
        else:
            # Return an empty DataFrame with the appropriate column names
            potential_df = pd.DataFrame(
                columns=["time_step", "node", "az", "norm_deriv_az"]
            )

        return potential_df

    def get_mesh_elements(self) -> Optional[pd.DataFrame]:
        """
        Extract mesh elements from the XML root element and return them as a pandas DataFrame.

        Returns
        -------
        Optional[pd.DataFrame]
            A DataFrame with mesh elements. Returns None if the "elements" tag is not found.
        """
        # Check if the "elements" tag is present
        if eData := self._xroot.find(".//meshGeom/elements"):
            results = []
            # Iterate over "fe" elements within "elements"
            for elem in eData.findall("fe"):
                # Collect element data, including 'id' and 'cnt' attributes, and element indices
                data = {
                    "id": int(elem.attrib["id"]),
                    "cnt": int(elem.attrib["cnt"]),
                }
                # Add the attributes a, b, c, ..., h
                for x in string.ascii_lowercase[: data["cnt"]]:
                    data[x] = int(elem.attrib[x])

                results.append(data)

            # Convert the results to a pandas DataFrame and return
            return pd.DataFrame(results)
        else:
            # Return None if "elements" is not found
            return None

    def get_nodal_coords(self) -> Optional[np.ndarray]:
        """
        Extract node data from the XML root element and return it as a NumPy array.

        Returns
        -------
        Optional[np.ndarray]
            A NumPy array of node data. Returns None if the "nodes" tag is not found.
        """
        # Locate the "nodes" element
        nData = self._xroot.find(".//meshGeom/nodes")

        # Raise an exception if "nodes" element is missing
        if nData is None:
            raise Exception("Error in meshGeometry: Nodes missing")

        # Parse node data into a DataFrame
        dicts = [x.attrib for x in nData.findall("p")]
        df = pd.DataFrame(dicts)

        # Convert columns to numeric where possible
        for c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        # Convert the DataFrame to a NumPy array and return
        nodes = df.to_numpy()
        return nodes

    def get_magnetic_induction_on_timestep(self, time_step_index: int) -> pd.DataFrame:
        """
        Parse the magnetic induction data from a specific time_step in the post.xml file.

        Parameters
        ----------
        time_step_index : int
            The index of the <time_step> element from which to retrieve the <magnetic_induction_data>.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the magnetic induction data. The columns are
            - node: node number
            - elem: element number
            - Bx: x component of the magnetic induction
            - By: y component of the magnetic induction
            - Bz: z component of the magnetic induction
        """
        # Find all <time_step> elements
        time_steps = self._xroot.findall(".//time_step")

        # Check if the time_step_index is within range
        if time_step_index >= len(time_steps) or time_step_index < 0:
            raise IndexError("time_step_index is out of range.")

        # Get the <magnetic_induction_data> element for the specified time_step
        magnetic_induction_elem = time_steps[time_step_index].find(
            ".//magnetic_induction_data"
        )

        if magnetic_induction_elem is None or not magnetic_induction_elem.text:
            return (
                pd.DataFrame()
            )  # Return an empty DataFrame if the element is missing or empty

        # Extract and parse the text content
        data = magnetic_induction_elem.text.strip()
        lines = data.split("\n")
        data_lines = lines[1:]  # Skip the header line

        # Parse the data into rows
        rows = [line.split() for line in data_lines]
        df = pd.DataFrame(rows, columns=["node", "elem", "Bx", "By", "Bz"])

        # Convert columns to numeric and handle NaN
        df = df.apply(pd.to_numeric, errors="coerce")
        return df

    def get_magnetic_field_on_timestep(self, time_step_index: int) -> pd.DataFrame:
        """
        Parse the magnetic field data from a specific time_step in the post.xml file.

        Parameters
        ----------
        time_step_index : int
            The index of the <time_step> element from which to retrieve the <magnetic_field_data>.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the magnetic field data. The columns are
            - node: node number
            - elem: element number
            - Hx: x component of the magnetic field
            - Hy: y component of the magnetic field
            - Hz: z component of the magnetic field
        """
        # Find all <time_step> elements
        time_steps = self._xroot.findall(".//time_step")

        # Handle the case where no <time_step> elements are found
        if time_steps is None or len(time_steps) == 0:
            raise ValueError("No <time_step> elements found in the XML file.")

        # Check if the time_step_index is within range
        if time_step_index >= len(time_steps) or time_step_index < 0:
            raise IndexError("time_step_index is out of range.")

        # Get the <magnetic_field_data> element for the specified time_step
        magnetic_field_elem = time_steps[time_step_index].find(".//magnetic_field_data")

        if magnetic_field_elem is None or not magnetic_field_elem.text:
            return (
                pd.DataFrame()
            )  # Return an empty DataFrame if the element is missing or empty

        # Extract and parse the text content
        data = magnetic_field_elem.text.strip()
        lines = data.split("\n")
        data_lines = lines[1:]  # Skip the header line

        # Parse the data into rows
        rows = [line.split() for line in data_lines]
        df = pd.DataFrame(rows, columns=["node", "elem", "Hx", "Hy", "Hz"])

        # Convert columns to numeric and handle NaN
        df = df.apply(pd.to_numeric, errors="coerce")
        return df

    def get_magnetic_induction_all_timesteps(self) -> pd.DataFrame:
        """
        Retrieve magnetic induction data for all time steps and store it in a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing magnetic induction data for all time steps. The columns are:
            - time_step: index of the time step
            - node: node number
            - elem: element number
            - Bx: x component of the magnetic induction
            - By: y component of the magnetic induction
            - Bz: z component of the magnetic induction
            If no data exists, returns an empty DataFrame with the above columns.
        """
        # Find all <time_step> elements to get the total number of time steps
        time_steps = self._xroot.findall(".//time_step")
        time_steps_num = len(time_steps)

        # Initialize an empty list to store DataFrames for each time step
        all_data = []

        for i in range(time_steps_num):
            # Retrieve magnetic induction data for the current time step
            df = self.get_magnetic_induction_on_timestep(time_step_index=i)

            if not df.empty:
                # Add a column for the time_step index
                df["time_step"] = i

                # Append the data for this time step
                all_data.append(df)

        if all_data:
            # Combine all DataFrames into one
            magnetic_induction_df = pd.concat(all_data, ignore_index=True)
        else:
            # Return an empty DataFrame with the appropriate columns
            magnetic_induction_df = pd.DataFrame(
                columns=["time_step", "node", "elem", "Bx", "By", "Bz"]
            )

        return magnetic_induction_df

    def get_magnetic_field_all_timesteps(self) -> pd.DataFrame:
        """
        Retrieve magnetic field data for all time steps and store it in a pandas DataFrame.

        Returns
        -------
        pd.DataFrame
            A DataFrame containing magnetic field data for all time steps. The columns are:
            - time_step: index of the time step
            - node: node number
            - elem: element number
            - Hx: x component of the magnetic field
            - Hy: y component of the magnetic field
            - Hz: z component of the magnetic field
            If no data exists, returns an empty DataFrame with the above columns.
        """
        # Find all <time_step> elements to get the total number of time steps
        time_steps = self._xroot.findall(".//time_step")
        time_steps_num = len(time_steps)

        # Initialize an empty list to store DataFrames for each time step
        all_data = []

        for i in range(time_steps_num):
            # Get the magnetic field data for the current time step
            df = self.get_magnetic_field_on_timestep(time_step_index=i)

            if not df.empty:
                # Add the time_step index as a new column
                df["time_step"] = i

                # Append the data for the current time step
                all_data.append(df)

        if all_data:
            # Concatenate all DataFrames into one
            magnetic_field_df = pd.concat(all_data, ignore_index=True)
        else:
            # Return an empty DataFrame with the appropriate column names
            magnetic_field_df = pd.DataFrame(
                columns=["time_step", "node", "elem", "Hx", "Hy", "Hz"]
            )

        return magnetic_field_df

    def get_iron_nodal_data_info(self) -> dict:
        """
        Parse the <iron_nodal_data> line to extract tot_nodes, nodf, and dim.

        Returns
        -------
        dict
            A dictionary containing:
            - "tot_nodes" (int): Total number of nodes.
            - "nodf" (int): Number of degrees of freedom.
            - "dim" (int): Dimensionality of the nodes.
        """
        # Find the <iron_nodal_data> element
        iron_nodal_data_elem = self._xroot.find(".//iron_nodal_data")

        # Check if <iron_nodal_data> element exists
        if iron_nodal_data_elem is None or not iron_nodal_data_elem.text:
            raise ValueError("<iron_nodal_data> element is missing or empty.")

        # Extract text, strip any surrounding whitespace, and split by whitespace
        try:
            _, _, _, tot_nodes, nodf, dim = iron_nodal_data_elem.text.strip().split()
        except ValueError as err:
            raise ValueError(
                "<iron_nodal_data> is missing or has the wrong format."
            ) from err

        return {"tot_nodes": int(tot_nodes), "nodf": int(nodf), "dim": int(dim)}

    def parse_nodal_coord_info(self) -> pd.DataFrame:
        """
        Parse the <nodal_coord> data to extract details for each node.

        Returns
        -------
        pd.DataFrame
            A DataFrame with columns:
            - node_num: Node number
            - hmo_node: HMO node
            - x: X coordinate
            - y: Y coordinate
            - z: Z coordinate
            - frame: Frame value
            - bound: Boundary condition
            - nodf: Degrees of freedom
        """
        # Find the <nodal_coord> element
        nodal_coord_elem = self._xroot.find(".//nodal_coord")

        # Check if <nodal_coord> element exists
        if nodal_coord_elem is None or not nodal_coord_elem.text:
            raise ValueError("<nodal_coord> element is missing or empty.")

        # Extract text content, strip whitespace, and split by lines
        lines = nodal_coord_elem.text.strip().split("\n")

        # Initialize a list to store node data
        node_data = []

        # Process each line in the <nodal_coord> data
        for line in lines[1:]:
            # Split line by whitespace
            columns = line.split()

            try:
                node_num = int(columns[0])
                hmo_node = int(columns[1])
                x = float(columns[2])
                y = float(columns[3])
                z = float(columns[4])
                frame = int(columns[5])
                bound = int(columns[6])
                nodf = int(columns[7])
            except (ValueError, IndexError) as e:
                raise ValueError(
                    f"Wrong formatting of the <nodal_coord> line: {line}"
                ) from e

            # Append to the data list
            node_data.append(
                {
                    "node_num": node_num,
                    "hmo_node": hmo_node,
                    "x": x,
                    "y": y,
                    "z": z,
                    "frame": frame,
                    "bound": bound,
                    "nodf": nodf,
                }
            )

        # Convert the list of dictionaries to a DataFrame
        return pd.DataFrame(node_data)


class TransStepData:
    """Data of a transient step"""

    def __init__(self, id: int, name: str) -> None:
        self.id: int = id
        self.name: str = name
        self.coilData = pd.DataFrame()
        self.meshData = pd.DataFrame()
        self.matrixData = pd.DataFrame()
        # self.irisData = pd.DataFrame()
        self.coilData3D = pd.DataFrame()
        self.brickData3D = pd.DataFrame()
        self.meshData3D = pd.DataFrame()
        self.deviceGraphs: Dict[int, pd.DataFrame] = {}
        self.harmonicCoils: Dict[int, HarmonicCoil] = {}
        self.conductorForces: Optional[pd.DataFrame] = None


@dataclass
class CoilGeomDfs:
    conductors: pd.DataFrame
    strands: pd.DataFrame


@dataclass
class MeshGeomDfs:
    nodes: pd.DataFrame
    elements: pd.DataFrame
    boundaries: pd.DataFrame


class OptData:
    """Data Of an optimization Step"""

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name: str = name

        self.transientGraphs: Dict[int, pd.DataFrame] = {}
        self.step: Dict[int, TransStepData] = {}
        self.designVariables: Dict[int, DesignVariableResult] = {}
        self.objectiveResults: Dict[int, ObjectiveResult] = {}

        self._coilGeometries: Dict[int, CoilGeometry] = {}
        self._coilGeometries3D: Dict[int, Coil3DGeometry] = {}
        self._brickGeometries3D: Dict[int, Brick3DGeometry] = {}
        self._wedgeGeometries3D: Dict[int, WedgeGeometry] = {}
        self._blockGeometries3D: dict[int, BlockGeometry] = {}
        self._meshGeometries: Optional[Geometry] = None
        self._meshGeometries3D: Optional[Geometry] = None

        self._coilGeomdf: CoilGeomDfs = CoilGeomDfs(pd.DataFrame(), pd.DataFrame())
        self._coilGeom3ddf: pd.DataFrame = pd.DataFrame()
        self._brickGeom3ddf: pd.DataFrame = pd.DataFrame()
        self._topologydf: pd.DataFrame = pd.DataFrame()
        self._meshGeomdf: MeshGeomDfs = MeshGeomDfs(
            pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        )
        self._meshGeom3ddf: MeshGeomDfs = MeshGeomDfs(
            pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        )

    @property
    def blockTopologies(self) -> Dict[int, BlockTopology]:
        """
        Get block topologies
        """
        return {
            int(block.block_nr): BlockTopology(
                block_nr=block.block_nr,
                block_orig=block.block_origin,
                layer_nr=block.layer_nr,
                first_conductor=block.first_conductor,
                last_conductor=block.last_conductor,
                n_radial=block.n_radial,
                n_azimuthal=block.n_azimuthal,
                first_strand=block.first_strand,
                last_strand=block.last_strand,
                ins_radial=block.ins_radial,
                ins_azimuthal=block.ins_azimuthal,
            )
            for block in self._topologydf.itertuples()
        }

    @property
    def coilGeometries(self) -> Dict[int, CoilGeometry]:
        if not self._coilGeometries:
            self._create_coils_from_df()
        return self._coilGeometries

    @coilGeometries.setter
    def coilGeometries(self, value: Dict[int, CoilGeometry]):
        self._coilGeometries = value

    @property
    def coilGeometries3D(self) -> Dict[int, Coil3DGeometry]:
        if not self._coilGeometries3D:
            self._create_coils3d_from_df()
        return self._coilGeometries3D

    @coilGeometries3D.setter
    def coilGeometries3D(self, value: Dict[int, Coil3DGeometry]):
        self._coilGeometries3D = value

    @property
    def brickGeometries3D(self) -> Dict[int, Brick3DGeometry]:
        if not self._brickGeometries3D:
            self._create_bricks_from_df()
        return self._brickGeometries3D

    @brickGeometries3D.setter
    def brickGeometries3D(self, value: Dict[int, Brick3DGeometry]):
        self._brickGeometries3D = value

    @property
    def wedgeGeometries3D(self) -> Dict[int, WedgeGeometry]:
        if not self._wedgeGeometries3D:
            self._blocks_to_wedges()
        return self._wedgeGeometries3D

    @wedgeGeometries3D.setter
    def wedgeGeometries3D(self, value: Dict[int, WedgeGeometry]):
        self._wedgeGeometries3D = value

    @property
    def blockGeometries3D(self) -> Dict[int, BlockGeometry]:
        return self._blockGeometries3D

    @blockGeometries3D.setter
    def blockGeometries3D(self, value: Dict[int, BlockGeometry]):
        self._blockGeometries3D = value

    @property
    def meshGeometries(self) -> Optional[Geometry]:
        if not self._meshGeometries:
            self._create_mesh_from_df()
            pass
        return self._meshGeometries

    @meshGeometries.setter
    def meshGeometries(self, value: Optional[Geometry]):
        self._meshGeometries = value

    @property
    def meshGeometries3D(self) -> Optional[Geometry]:
        if self._meshGeometries3D is None:
            self._create_mesh3d_from_df()
            pass
        return self._meshGeometries3D

    @meshGeometries3D.setter
    def meshGeometries3D(self, value: Optional[Geometry]):
        self._meshGeometries3D = value

    def _blocks_to_wedges(self) -> None:
        # From given block geometry, generate wedges
        if self._topologydf.empty:
            return

        # Iterate through blocks to establish the blockorder and nr of grouped blocks (by layerid and original blockid)
        block_order: dict[int, dict[int, list[int]]] = {}
        for _, row in self._topologydf.iterrows():
            layer = int(row["layer_nr"])
            block_orig = int(row["block_origin"])
            block_nr = int(row["block_nr"])
            if layer not in block_order:
                block_order[layer] = {}
            if block_orig not in block_order[layer]:
                block_order[layer][block_orig] = []
            block_order[layer][block_orig].append(block_nr)

        # From the generated order extract the list of unique blocklists (each for generating one set of wedges)
        block_ids: dict[int, list[list[int]]] = {}
        for layer in block_order:
            max_len = max(len(blocks) for blocks in block_order[layer].values())
            block_ids[layer] = [[] for _ in range(max_len)]
            for block_orig in block_order[layer]:
                for idx, block_nr in enumerate(block_order[layer][block_orig]):
                    block_ids[layer][idx].append(block_nr)

        wedge_nr = 1
        wedges: dict[int, WedgeGeometry] = {}
        for layer, block_list_list in block_ids.items():
            for block_list in block_list_list:
                # endspacer
                wedges[wedge_nr] = WedgeGeometry(
                    layer,
                    wedge_nr,
                    self.blockGeometries3D[block_list[0]].outer_surface,
                    None,
                    block_list[0],
                    0,
                )
                wedge_nr += 1
                for bl in range(1, len(block_list)):
                    outer = self.blockGeometries3D[block_list[bl - 1]].inner_surface
                    inner = self.blockGeometries3D[block_list[bl]].outer_surface
                    wedges[wedge_nr] = WedgeGeometry(
                        layer,
                        wedge_nr,
                        inner,
                        outer,
                        block_list[bl],
                        block_list[bl - 1],
                    )
                    wedge_nr += 1
                # inner post
                wedges[wedge_nr] = WedgeGeometry(
                    layer,
                    wedge_nr,
                    None,
                    self.blockGeometries3D[block_list[-1]].inner_surface,
                    0,
                    block_list[-1],
                )
                wedge_nr += 1
        self.wedgeGeometries3D = wedges

    def _create_mesh_from_df(self) -> None:
        if self._meshGeomdf.nodes.empty:
            return
        self._meshGeometries = self._meshdf_to_geom(self._meshGeomdf)

    def _create_mesh3d_from_df(self) -> None:
        if self._meshGeom3ddf.nodes.empty:
            return
        self._meshGeometries3D = self._meshdf_to_geom(self._meshGeom3ddf)

    def _meshdf_to_geom(self, df: MeshGeomDfs) -> Geometry:
        nodes = df.nodes.to_numpy()[:, 1:]
        elements = df.elements.to_numpy()[:, 2:]
        elements -= 1  # translate to 0 based index
        elements_list = elements.tolist()
        for nr_elem, lst in zip(df.elements["n_el"], elements_list):
            del lst[nr_elem:]  # Resize lists to match number of elements
        boundaries = {}
        if not df.boundaries.empty:
            for id, grp in df.boundaries.groupby("boundary_id"):
                if grp.empty:
                    continue
                boundaries[id] = grp.to_numpy()[:, 2:]
        return Geometry(nodes, elements_list, boundaries)

    def _create_bricks_from_df(self):
        if self._brickGeom3ddf.empty:
            return
        for idx, grp in self._brickGeom3ddf.groupby("brick_nr"):
            brick_nr = int(idx)
            if grp.empty:
                continue
            nodes = grp.to_numpy()[:, 2:].reshape((-1, 3))
            geom = Geometry(nodes, None, None)
            geom.generate_elements_for_coil_nodes()
            self._brickGeometries3D[brick_nr] = Brick3DGeometry(brick_nr, geom)

    def _create_coils3d_from_df(self):
        if self._coilGeomdf.conductors.empty:
            return
        for idx, grp in self._coilGeom3ddf.groupby("conductor"):
            cond_nr = int(idx)
            if grp.empty:
                continue
            block_info = self._topologydf[
                (self._topologydf.first_conductor <= cond_nr)
                & (self._topologydf.last_conductor >= cond_nr)
            ].iloc[0]
            block_nr = int(block_info.block_nr)
            layer_nr = int(block_info.layer_nr)

            nodes = grp.to_numpy()[:, 2:].reshape((-1, 3))
            geom = Geometry(nodes, None, None)
            geom.generate_elements_for_coil_nodes()

            self._coilGeometries3D[cond_nr] = Coil3DGeometry(
                cond_nr, geom, block_nr, layer_nr
            )

    def _create_coils_from_df(self):
        if self._coilGeomdf.conductors.empty:
            return

        cables = {}
        for _, cond in self._coilGeomdf.conductors.iterrows():
            cable_nr = int(cond["conductor"])
            geom = cond.to_numpy()[1:].reshape((4, 2))
            block_info = self._topologydf[
                (self._topologydf.first_conductor <= cond["conductor"])
                & (self._topologydf.last_conductor >= cond["conductor"])
            ]
            block_nr = block_info.block_nr
            layer_nr = block_info.layer_nr
            first_cond_strand = int(
                (
                    block_info.first_strand
                    + (cond["conductor"] - block_info.first_conductor)
                    * block_info.n_radial
                    * block_info.n_azimuthal
                ).iloc[0]
            )
            last_cond_strand = int(
                (
                    first_cond_strand
                    + (block_info.n_radial * block_info.n_azimuthal)
                    - 1
                ).iloc[0]
            )
            df_strand = self._coilGeomdf.strands
            strands = df_strand[
                (df_strand["strand"] >= first_cond_strand)
                & (df_strand["strand"] <= last_cond_strand)
            ]
            strands_dict = {
                int(st["strand"]): st.to_numpy()[1:].reshape((4, 2))
                for _, st in strands.iterrows()
            }
            cables[cable_nr] = CoilGeometry(
                cable_nr, block_nr, layer_nr, geom, strands_dict
            )
        self._coilGeometries = cables


class RoxieOutputParser:
    """Roxie output parser class.

    Takes all different Roxie outputs, parses them, and provides a structured output of the results.
    """

    def __init__(self, xml_file: str) -> None:
        from roxieapi.output.xml_parse import _XmlParser

        self.logger = logging.getLogger("RoxieOutputParser")

        self.optimizationGraphs: Dict[
            int, pd.DataFrame
        ] = {}  # Result values on optimization graphs, (id)
        self.opt: Dict[int, OptData] = {}

        self.plots2D: List[Plot2D] = []  # 2D Plots information for device
        self.plots3D: List[Plot3D] = []  # 3D Plots information for device
        self.graphs_device: List[GraphPlot] = []  # Graph information for device
        self.graphs_transient: List[
            GraphPlot
        ] = []  # Plot information for transient plots
        self.graphs_optimization: List[
            GraphPlot
        ] = []  # Plot information for optimization plots

        # General information
        self.roxie_version = ""
        self.roxie_githash = ""
        self.run_date = ""
        self.comment = ""

        # Add once parsing is aligned with rest of parser code
        # xtree = et.parse(xml_file)
        # self.xroot = xtree.getroot()
        # self.eddy_currents = EddyCurrentsData(self.xroot)
        _XmlParser.parse_xml(xml_file, self)

    def find_transstep(self, opt_step: int, trans_step: int) -> Optional[TransStepData]:
        """
        Find the transient step data for a given optimization step and transient step

        :param opt_step: The optimization step number
        :param trans_step: The transient step number
        :return: The TransStepData object or None if not found
        """
        if opt_step in self.opt and trans_step in self.opt[opt_step].step:
            return self.opt[opt_step].step[trans_step]
        return None

    def find_optstep(self, opt_step) -> Optional[OptData]:
        """
        Find the optimization step data for a given optimization step

        :param opt_step: The optimization step number
        :return: The OptData object or None if not found
        """
        return self.opt.get(opt_step, None)

    def get_harmonic_coil(
        self,
        coil_nr: int = 1,
        opt_step: int = 1,
        trans_step: int = 1,
    ) -> Optional[HarmonicCoil]:
        """Return the harmonic coil for given step and coil id, or None if not present

        :param coil_nr: Harmonic Coil Nr, defaults to 1
        :param opt_step: The Optimization Step Nr, defaults to 1
        :param trans_step: The Transient Step Nr, defaults to 1
        :return: The Harmonic coil, or None
        """
        if trans := self.find_transstep(opt_step, trans_step):
            return trans.harmonicCoils.get(coil_nr, None)
        return None

    def get_conductor_forces(
        self, opt_step: int = 1, trans_step: int = 1
    ) -> Optional[pd.DataFrame]:
        """Return Conductor forces for given Step, or None if not present

        :param opt_step: The Optimization step, defaults to 1
        :param trans_step: Transient step, defaults to 1
        :return: The Conductor forces as Dataframe
        """
        if trans := self.find_transstep(opt_step, trans_step):
            return trans.conductorForces
        else:
            return None

    def get_crosssection_plot(self, plot_nr: int = 1) -> Optional[Plot2D]:
        """Return the Crossection 2D plot with number i

        :param plot_nr: The plot_number, defaults to 1
        :return: The Plot2D object, or None
        """
        for pl in self.plots2D:
            if isinstance(pl, Plot2D) and pl.id == plot_nr:
                return pl
        return None

    def get_3d_plot(self, plot_nr: int = 1) -> Optional[Plot3D]:
        """Return the 3D plot with number i
        :param plon_nr: The plot number, defaults to 1
        :return: The Plot3D definition, or None
        """
        for pl in self.plots3D:
            if isinstance(pl, Plot3D) and pl.id == plot_nr:
                return pl
        return None
