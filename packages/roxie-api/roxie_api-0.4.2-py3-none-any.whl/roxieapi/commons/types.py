from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
import numpy.typing as npt
import pandas as pd

from roxieapi.commons.roxie_constants import PlotLabels


@dataclass
class BrickData:
    """Roxie Brick Data input"""

    current: float
    n1: int
    n2: int
    ncut: int
    nodes: np.ndarray

    def to_table(self) -> str:
        """Return a string representation of the BrickData block .

        Returns:
            str: Brick data as string
        """
        assert len(self.nodes) % 4 == 0, "Node length must be multiple of 4"
        nodelen = len(self.nodes) // 4
        output = (
            f"{self.current:12g}    {self.n1}    {self.n2}    {nodelen}    {self.ncut}"
        )
        nodestr = "\n".join(
            [f"    {n[0]:13g}    {n[1]:13g}    {n[2]:13g}" for n in self.nodes]
        )

        return output + "\n" + nodestr


@dataclass
class IronYokeOptions:
    mesh_scale: int = 0
    mir_inner_radius: float = 0
    mir_rel_perm: float = 0
    sym_yz: int = 0
    sym_zx: int = 0
    sym_xy: int = 0
    rot_mode: int = 0
    rot_div: int = 0
    rot_sym: int = 0


@dataclass
class Geometry:
    """Geometry Information for 2D/3D geometries.

    For 2D geometries, each point is a [x,y] coordinate.
    For 3D geometries, each point is a [x,y,z] coordinate.

    nodes - List of points ([x,y,z]) making up the Geometry
    elements - List of connected points as faces or cells in the form of [<p1>..<pn>]
    boundaries - Dict of boundaries for a Geometry, in the form of {id: [[x,y,z]...[x,y,z]]}
    """

    nodes: npt.NDArray[np.float64]
    elements: Optional[List[List[int]]]
    boundaries: Optional[Dict[int, npt.NDArray[np.float64]]]

    def generate_elements_for_coil_nodes(self) -> None:
        """Generate cells from points.
           points are ordered in z direction, 4 points define one face.
           Once cell is between two sets of 4 points

          7+----+6
          /|   /|
        3+----+2|
         |4+--|-+5
         |/   |/
        0+----+1
        """
        self.elements = [
            list(range(i - 4, i + 4)) for i in range(4, len(self.nodes), 4)
        ]


@dataclass
class CoilGeometry:
    """Geometry information for 2D coils"""

    nr: int
    block_id: int
    layer_id: int
    geometry: npt.NDArray[np.float64]
    strands: Dict[int, npt.NDArray[np.float64]]


@dataclass
class Base3DGeometry:
    """Base geometry for 3D objects"""

    nr: int
    geometry: Geometry


@dataclass
class Brick3DGeometry(Base3DGeometry):
    """Geometry information for 3D bricks"""


@dataclass
class Coil3DGeometry(Base3DGeometry):
    """Geometry information for 3D coils"""

    block_id: int
    layer_id: int


@dataclass
class WedgeSurface:
    """Surface of a wedge"""

    lower_edge: npt.NDArray[np.float64]
    upper_edge: npt.NDArray[np.float64]


@dataclass
class WedgeGeometry:
    """Geometry to store wedge information"""

    layer: int
    nr: int

    inner_surface: Optional[WedgeSurface]
    outer_surface: Optional[WedgeSurface]

    block_inner: int
    block_outer: int


@dataclass
class BlockGeometry:
    nr: int
    inner_surface: WedgeSurface
    outer_surface: WedgeSurface


@dataclass
class BlockTopology:
    """Topology of blocks, conductors and strands"""

    block_nr: int
    block_orig: int
    layer_nr: int
    first_conductor: int
    last_conductor: int
    n_radial: int
    n_azimuthal: int
    first_strand: int
    last_strand: int
    ins_radial: float
    ins_azimuthal: float


@dataclass
class PlotAxis:
    """Plot Axis information (for roxie plots)"""

    label: str
    bounds: Optional[Tuple[float, float]]
    log: bool


@dataclass
class PlotLegend:
    """Plot Legend information (for roxie plots)"""

    pos: Optional[str]
    greyScale: Optional[bool]
    min_val: Optional[float]
    max_val: Optional[float]


@dataclass
class PlotInfo:
    """Plot info object, containing all information to create a crossection or 3D plot"""

    id: str
    type: str
    dataType: str
    label: str
    plotLegend: Optional[PlotLegend]
    harmCoil: Optional[int]
    vector_mappings: Optional[Dict[str, int]]


@dataclass
class GraphInfo:
    """GraphInfo object, containing all information for a xy graph"""

    id: int
    graph_type: int
    xval: str
    yval: str
    logx: bool
    logy: bool
    weight: float
    label: Optional[str]


@dataclass
class Plot:
    """Base Plot object, containing all information to create a crossection or 3D plot"""

    title: str
    id: int
    axes: Dict[str, PlotAxis]
    _plotInfos: List[PlotInfo]
    active: Optional[PlotInfo] = field(init=False, default=None)


@dataclass
class GraphPlot:
    """Graph plot information"""

    title: str
    id: int
    axes: Dict[str, PlotAxis]
    graphs: List[GraphInfo]


@dataclass
class Plot2D(Plot):
    """Plot2D object, for crossection plots"""

    @staticmethod
    def create(
        title="New Plot2D",
        xlim: Optional[Tuple[float, float]] = None,
        ylim: Optional[Tuple[float, float]] = None,
    ) -> "Plot2D":
        """
        Creates a new Plot2D object.

        Parameters:
            title (str): The title of the plot. Default is "New Plot2D".
            xlim (Optional[Tuple[float, float]]): The limits for the x-axis. Default is None.
            ylim (Optional[Tuple[float, float]]): The limits for the y-axis. Default is None.

        Returns:
            Plot2D: A new Plot2D object.
        """
        return Plot2D(
            title,
            -1,
            {
                "X": PlotAxis("x in mm", bounds=xlim, log=False),
                "Y": PlotAxis("y in mm", bounds=ylim, log=False),
            },
            [],
        )

    def add_coilPlot(
        self,
        id: str,
        label: str = "",
        legend: Optional[PlotLegend] = None,
        harm_coil: Optional[int] = None,
    ) -> "Plot2D":
        """
        Add a coil plot component to the plot.

        parameters:
            id (str): The data id to be used.
            label (str): Label of the coil plot.
            legend (Optional[PlotLegend]): The legend of the component. Default is None.
            harm_coil (Optional[int]): The harmonic coil number if the plot depends on a harmonic coil. Default is None.
        """
        if not label:
            label = PlotLabels.plot2D_desc.get(id, "")
        self._plotInfos.append(
            PlotInfo(id, "coilPlot", "scalar", label, legend, harm_coil, None)
        )
        return self

    def add_meshPlot(
        self, id: str, label: str = "", legend: Optional[PlotLegend] = None
    ) -> "Plot2D":
        """Add a mesh plot to the plot object

        :param id: The data id to be used.
        :type id: str
        :param label: Label of the mesh plot, defaults to ""
        :type label: str, optional
        :param legend: The legend of the component. Default is None.
        :type legend: Optional[PlotLegend], optional
        :return: _description_
        :rtype: Plot2D
        """
        if not label:
            label = PlotLabels.plotMesh2D_desc.get(id, "")
        self._plotInfos.append(
            PlotInfo(id, "meshPlot", "scalar", label, legend, None, None)
        )
        return self

    @property
    def pointPlots(self) -> List[PlotInfo]:
        """Return all pointPlots defined in the Plot"""
        return list(filter(lambda x: x.type == "pointPlot", self._plotInfos))

    @property
    def coilPlots(self) -> List[PlotInfo]:
        """Return all coilPlots defined in the Plot"""
        return list(filter(lambda x: x.type == "coilPlot", self._plotInfos))

    @property
    def meshPlots(self) -> List[PlotInfo]:
        """Return all meshPlots defined in the Plot"""
        return list(filter(lambda x: x.type == "meshPlot", self._plotInfos))

    @property
    def matrixPlots(self) -> List[PlotInfo]:
        """Return all matrixPlots defined in the Plot"""
        return list(filter(lambda x: x.type == "matrixPlot", self._plotInfos))

    @property
    def irisPlots(self) -> List[PlotInfo]:
        """Return all irisPlots defined in the Plot"""
        return list(filter(lambda x: x.type == "irisPlot", self._plotInfos))


@dataclass
class Plot3D(Plot):
    @staticmethod
    def create(
        title="New Plot3D",
        xlim: Optional[Tuple[float, float]] = None,
        ylim: Optional[Tuple[float, float]] = None,
        zlim: Optional[Tuple[float, float]] = None,
    ) -> "Plot3D":
        """
        Creates a new Plot3D object

        :param title: The plot title, defaults to "New Plot3D"
        :type title: str, optional
        :param xlim: Limits of x axis, defaults to None
        :type xlim: Optional[Tuple[float, float]], optional
        :param ylim: Limits of y axis, defaults to None
        :type ylim: Optional[Tuple[float, float]], optional
        :param zlim: Limits of z axis, defaults to None
        :type zlim: Optional[Tuple[float, float]], optional
        :return: The Plot3D description
        :rtype: Plot3D
        """
        return Plot3D(
            title,
            -1,
            {
                "X": PlotAxis("x in mm", bounds=xlim, log=False),
                "Y": PlotAxis("y in mm", bounds=ylim, log=False),
                "Z": PlotAxis("z in mm", bounds=zlim, log=False),
            },
            [],
        )

    def add_coilPlot(
        self,
        id: str,
        label: str = "",
        legend: Optional[PlotLegend] = None,
    ) -> "Plot3D":
        """
        Add a coil plot component to the plot.

        parameters:
            id (str): The data id to be used.
            label (str): Label of the coil plot.
            legend (Optional[PlotLegend]): The legend of the component. Default is None.
            harm_coil (Optional[int]): The harmonic coil number if the plot depends on a harmonic coil. Default is None.
        """
        if not label:
            label = PlotLabels.plot3D_desc.get(id, "")
        self._plotInfos.append(
            PlotInfo(id, "coilPlot3D", "scalar", label, legend, None, None)
        )
        return self

    def add_meshPlot(
        self, id: str, label: str = "", legend: Optional[PlotLegend] = None
    ) -> "Plot3D":
        """Add a mesh plot to the plot object

        :param id: The data id to be used.
        :type id: str
        :param label: Label of the mesh plot, defaults to ""
        :type label: str, optional
        :param legend: The legend of the component. Default is None.
        :type legend: Optional[PlotLegend], optional
        :return: _description_
        :rtype: Plot2D
        """
        if not label:
            label = PlotLabels.plotMesh3D_desc.get(id, "")
        self._plotInfos.append(
            PlotInfo(id, "meshPlot3D", "scalar", label, legend, None, None)
        )
        return self

    @property
    def coilPlots(self) -> List[PlotInfo]:
        """Return all coil plots defined"""
        return list(filter(lambda x: x.type == "coilPlot3D", self._plotInfos))

    @property
    def meshPlots(self) -> List[PlotInfo]:
        """Return all mesh plots defined"""
        return list(filter(lambda x: x.type == "meshPlot3D", self._plotInfos))

    @property
    def showSpacers(self) -> bool:
        """Flag if spacers are shown in the plot"""
        return any((x.type == "spacerPlot3D" for x in self._plotInfos))


@dataclass
class HarmonicCoil:
    id: int
    _coil_type: int
    _measurement_type: int
    _main_harmonic: int
    params: Dict[str, float] = field(default_factory=dict)
    bn: Dict[int, float] = field(default_factory=dict)
    an: Dict[int, float] = field(default_factory=dict)
    strandData: pd.DataFrame = field(default_factory=pd.DataFrame)
    iris: pd.DataFrame = field(default_factory=pd.DataFrame)

    @property
    def main_harmonic(self) -> str:
        if self._main_harmonic == 0:
            return "None"
        else:
            ab = "A" if self.skew else "B"
            return f"{ab}{self.order}"

    @property
    def order(self) -> int:
        return self._main_harmonic // 2

    @property
    def skew(self) -> bool:
        return self._main_harmonic % 2 == 1

    @property
    def absolute(self) -> bool:
        return self._main_harmonic == 0

    @property
    def coil_type(self) -> str:
        if self._coil_type == 1:
            return "Cylindrical"
        if self._coil_type == 2:
            return "Wiggler"
        if self._coil_type == 3:
            return "Zonal"
        if self._coil_type == 4:
            return "Elliptical"
        if self._coil_type == 5:
            return "Cartx"
        if self._coil_type == 6:
            return "Carty"
        if self._coil_type == 7:
            return "Torus"
        if self._coil_type == 8:
            return "Fourier curve"
        return f"unknown coil type {self._coil_type}"

    @property
    def bref(self) -> str:
        nr = self._measurement_type
        if nr == 0:
            return "all"
        if nr == 2:
            return "Bcoil"
        if nr == 1:
            return "Biron"
        if nr == 4:
            return "Bmagn"
        if nr == 3:
            return "Biscc"
        if nr == 5:
            return "{Bcoil+Biron}"
        if nr == 6:
            return "{Bcoil+Biron+Bmagn}"
        if nr == 7:
            return "{Bcoil+Biron+Biscc}"
        return "Unknown Meas type: {0}".format(nr)

    def get_coil_info(self) -> OrderedDict[str, str]:
        d = OrderedDict()
        d["type"] = self.coil_type
        if self._coil_type == 1:
            d["reference radius (mm)"] = str(self.params["rref"])
            d["x position (mm)"] = str(self.params["xpos"])
            d["y position (mm)"] = str(self.params["ypos"])
        if self._coil_type == 2:
            d["period length (mm)"] = str(self.params["period_length"])
            d["x0 (mm)"] = str(self.params["x0"])
            d["y0 (mm)"] = str(self.params["y0"])
        if self._coil_type == 4:
            d["semi minor axis (mm)"] = str(self.params["semi_minor_axis"])
            d["semi major axis (mm)"] = str(self.params["semi_major_axis"])
        if "nr_z" in self.params:
            d["number of coils in Z direction"] = str(self.params["nr_z"])
            d["coil length (mm)"] = str(self.params["coil_length"])
            d["reference position"] = str(self.params["ref_pos"])
        return d

    def get_field_info(self) -> OrderedDict[str, str]:
        d = OrderedDict()
        if not self.absolute:
            d["main field (T)"] = str(self.params["main_field"])
            mh = self._main_harmonic // 2 - 1
            if mh == 0:
                mhs = "T"
            elif mh == 1:
                mhs = "$\\frac{T}{m}$"
            else:
                mhs = f"$\\frac{{T}}{{m^{mh}}}$"
            d[f"reference magnet strength ({mhs})"] = str(self.params["mag_strength"])
            if "nr_z" in self.params:
                d["MAGNETIC LENGTH (mm)"] = str(self.params["mag_length"])
        d["error of harmonic analysis of br"] = str(self.params["error_br"])

        return d

    def get_table(self) -> pd.DataFrame:
        vals = [(i, self.bn[i], self.an[i]) for i in self.bn]
        if self.absolute:
            cols = ["Order", "Bn", "An"]
        else:
            cols = ["Order", "bn", "an"]
        return pd.DataFrame(vals, columns=cols)


@dataclass
class ObjectiveResult:
    nr: int
    value: float
    raw_value: float
    obj_name: str
    obj_p1: int
    obj_p2: int


@dataclass
class DesignVariableResult:
    nr: int
    value: float
    name: str
    act_on: int
    blocks: list[int]
