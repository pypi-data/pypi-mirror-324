import abc
import os
import pathlib
import string
import xml.etree.ElementTree as et
from io import StringIO
from typing import Optional, Union

import fastnumbers
import numpy as np
import numpy.typing as npt
import pandas as pd

from roxieapi.commons.types import (
    BlockGeometry,
    Brick3DGeometry,
    Coil3DGeometry,
    CoilGeometry,
    DesignVariableResult,
    Geometry,
    GraphInfo,
    GraphPlot,
    HarmonicCoil,
    ObjectiveResult,
    Plot2D,
    Plot3D,
    PlotAxis,
    PlotInfo,
    PlotLegend,
    WedgeGeometry,
    WedgeSurface,
)
from roxieapi.output.parser import (
    CoilGeomDfs,
    MeshGeomDfs,
    OptData,
    RoxieOutputParser,
    TransStepData,
)


class _XmlParser(abc.ABC):
    _PLOTINFOS = {
        "coilPlotInfo": "coilPlot",
        "meshPlotInfo": "meshPlot",
        "coilPlot3DInfo": "coilPlot3D",
        "meshPlot3DInfo": "meshPlot3D",
        "matrixPlotInfo": "matrixPlot",
        "irisPlotInfo": "irisPlot",
        "pointPlotInfo": "pointPlot",
    }

    def __init__(self, output: RoxieOutputParser) -> None:
        self.output = output
        self.current_opt: Optional[OptData] = None
        self.current_step: Optional[TransStepData] = None

    def parse_element_start(self, path: pathlib.Path, elem: et.Element) -> None:
        if path.match("/roxieData"):
            self._fill_sim_info(elem)
        elif path.match("/roxieData/loop/step"):
            self._create_opt(elem)
        elif path.match("/roxieData/loop/step/loop/step"):
            self._create_step(elem)
        else:
            pass

    def parse_element_end(self, path: pathlib.Path, elem: et.Element) -> None:
        if path.match("/roxieData/plottingInfos"):
            self._fill_plot_info(elem)
            elem.clear()
        elif path.match("/roxieData/loop/step"):
            self.current_opt = None
            elem.clear()
        elif path.match("/roxieData/loop/graphData"):
            self.output.optimizationGraphs = self._extract_graph_data(elem)
            elem.clear()
        elif path.match("/roxieData/loop/optimizationResults"):
            self._fill_dv_objectives(elem)
            elem.clear()
        elif path.match("/roxieData/loop/step/loop/step"):
            self.current_step = None
            elem.clear()
        elif path.match("/roxieData/loop/step/loop/graphData"):
            if self.current_opt is None:
                raise ValueError("Error in XML file: No active optimization step")
            self.current_opt.transientGraphs = self._extract_graph_data(elem)
            elem.clear()
        elif path.parent.match("/roxieData/loop/step/loop/step"):
            if self.current_step is None:
                raise RuntimeError(
                    "Error while parsing XML file: No current transient step"
                )
            if path.name == "conductorForces":
                self.current_step.conductorForces = self._extract_csv_table(elem)
                elem.clear()
            elif path.name == "coilData":
                self.current_step.coilData = self._extract_csv_table(elem)
                elem.clear()
            elif path.name == "coilData3D":
                self.current_step.coilData3D = self._extract_csv_table(elem)
                elem.clear()
            elif path.name == "brickData3D":
                self.current_step.brickData3D = self._extract_csv_table(elem)
                elem.clear()
            elif path.name == "meshData":
                self.current_step.meshData = self._extract_csv_table(elem)
                elem.clear()
            elif path.name == "meshData3D":
                self.current_step.meshData3D = self._extract_csv_table(elem)
                elem.clear()
            elif path.name == "matrixData":
                self.current_step.matrixData = self._extract_csv_table(elem)
                elem.clear()
            elif path.name == "graphData":
                self.current_step.deviceGraphs = self._extract_graph_data(elem)
                elem.clear()
            elif path.name == "harmonicCoil":
                self.current_step.harmonicCoils.update(
                    [self._extract_harmonic_coil(elem)]
                )
                elem.clear()
        elif path.match("/roxieData/loop/step/coilGeom"):
            self._extract_coils_2D(elem)
            elem.clear()
        elif path.match("/roxieData/loop/step/coilGeom3D"):
            self._extract_coils_3D(elem)
            elem.clear()
        elif path.match("/roxieData/loop/step/meshGeom"):
            self._extract_mesh_2d(elem)
            elem.clear()
        elif path.match("/roxieData/loop/step/meshGeom3D"):
            self._extract_mesh_3d(elem)
            elem.clear()
        elif path.match("/roxieData/loop/step/brickGeom3D"):
            self._extract_bricks_3d(elem)
            elem.clear()

    @abc.abstractmethod
    def _extract_coils_2D(self, elem) -> None:
        pass

    @abc.abstractmethod
    def _extract_coils_3D(self, elem) -> None:
        pass

    @abc.abstractmethod
    def _extract_mesh_2d(self, elem) -> None:
        pass

    @abc.abstractmethod
    def _extract_mesh_3d(self, elem) -> None:
        pass

    @abc.abstractmethod
    def _extract_bricks_3d(self, elem) -> None:
        pass

    def _extract_harmonic_coil(self, elem: et.Element) -> tuple[int, HarmonicCoil]:
        params = {}
        id = None
        measurement_type = None
        main_harmonic = None
        coil_type = None
        for k, v in elem.attrib.items():
            if k == "id":
                id = int(v)
            elif k == "meas_type":
                measurement_type = int(v)
            elif k == "main_harmonic":
                main_harmonic = int(v)
            elif k == "coil_type":
                coil_type = int(v)
            else:
                params[k] = float(v)
        if (harms := elem.find("harmonics")) is not None:
            bn, an = self._extract_harmonic_table(harms)
        else:
            bn = {}
            an = {}
        if (irisData := elem.find("irisData")) is not None:
            iris = self._extract_csv_table(irisData)
        else:
            iris = pd.DataFrame()

        if (sc := elem.find("strandContributions")) is not None:
            strandData = self._extract_csv_table(sc)
        else:
            strandData = pd.DataFrame()

        if id is None:
            raise ValueError("Missing 'id' attribute in harmonic coil element")
        if measurement_type is None:
            raise ValueError("Missing 'meas_type' attribute in harmonic coil element")
        if main_harmonic is None:
            raise ValueError(
                "Missing 'main_harmonic' attribute in harmonic coil element"
            )
        if coil_type is None:
            raise ValueError("Missing 'coil_type' attribute in harmonic coil element")
        return (
            id,
            HarmonicCoil(
                id,
                coil_type,
                measurement_type,
                main_harmonic,
                params,
                bn,
                an,
                strandData,
                iris,
            ),
        )

    @abc.abstractmethod
    def _extract_harmonic_table(
        self, harms
    ) -> tuple[dict[int, float], dict[int, float]]:
        pass

    def _fill_dv_objectives(self, elem: et.Element) -> None:
        for it in elem:
            itId = int(it.attrib["nr"])
            if itId not in self.output.opt:
                raise ValueError(
                    f"Error in XML file: Iteration {itId} is not in optimization steps"
                )
            for obj in it.findall("objectives/objective"):
                objId = int(obj.attrib["nr"])
                self.output.opt[itId].objectiveResults[objId] = ObjectiveResult(
                    nr=objId,
                    value=float(obj.attrib["value"]),
                    raw_value=float(obj.attrib.get("raw_value", obj.attrib["value"])),
                    obj_name=obj.attrib.get("obj_name", ""),
                    obj_p1=int(obj.attrib.get("obj_p1", "0")),
                    obj_p2=int(obj.attrib.get("obj_p2", "0")),
                )
            for dv in it.findall("designVariables/variable"):
                dvId = int(dv.attrib["nr"])
                if "blocks" in dv.attrib:
                    blocks = [int(x) for x in dv.attrib.get("blocks", "").split(" ")]
                else:
                    blocks = []
                self.output.opt[itId].designVariables[dvId] = DesignVariableResult(
                    nr=dvId,
                    value=float(dv.attrib["value"]),
                    name=dv.attrib.get("name", ""),
                    act_on=int(dv.attrib.get("act_on", "0")),
                    blocks=blocks,
                )

    def _extract_graph_data(self, root: et.Element) -> dict[int, pd.DataFrame]:
        target: dict[int, pd.DataFrame] = {}
        for d in root.findall("graph"):
            id = int(d.attrib["id"])
            target[id] = self._extract_csv_table(d)
        return target

    def _extract_csv_table(self, root: et.Element) -> pd.DataFrame:
        df = pd.read_csv(StringIO(root.text), header=0)
        df.rename(columns=lambda x: x.strip(), inplace=True)
        return df

    def _extract_xml_to_csv(self, root: et.Element) -> pd.DataFrame:
        dict = [el.attrib for el in root]
        df = pd.DataFrame(dict)
        return df

    def _create_opt(self, elem: et.Element) -> None:
        runId = int(elem.attrib["id"])
        runname = elem.attrib["label"]
        opt = OptData(runId, runname)
        self.output.opt[runId] = opt
        self.current_opt = opt

    def _create_step(self, elem: et.Element) -> None:
        if self.current_opt is None:
            raise ValueError("Error in XML file: Step without optimization")
        stepId = int(elem.attrib["id"])
        step = TransStepData(stepId, elem.attrib["label"])
        self.current_opt.step[stepId] = step
        self.current_step = step

    def _fill_sim_info(self, elem: et.Element) -> None:
        """Fill the basic information from a simulation"""
        self.output.roxie_version = elem.attrib["version"]
        self.output.roxie_githash = elem.attrib["git_hash"]
        self.output.run_date = elem.attrib["runDate"]
        self.output.comment = elem.attrib["comment"]

    def _fill_plot_info(self, elem: et.Element) -> None:
        # Extract plotInfo objects first:
        plotInfos: list[PlotInfo] = []
        for pi in elem:
            if pi.tag in self._PLOTINFOS.keys():
                plotInfos.append(self._extract_plotinfo(pi))

        for pi in elem:
            if pi.tag == "graphPage":
                self._extract_graph_info(pi)
            elif pi.tag == "pageXsec":
                self._extract_plot2d_info(pi, plotInfos)
            elif pi.tag == "page3D":
                self._extract_plot3d_info(pi, plotInfos)

    def _extract_plotinfo(self, elem: et.Element) -> PlotInfo:
        id = elem.attrib["id"]
        leg = elem.find("legend")
        plotLegend = None
        if leg is not None:
            attr = leg.attrib
            plotLegend = PlotLegend(
                attr.get("pos", "w"),
                attr.get("greyScale") == "true",
                float(attr["min"]) if attr.get("min") else None,
                float(attr["max"]) if attr.get("max") else None,
            )
        dataType = elem.attrib["dataType"]
        lbl = elem.attrib["label"]
        harmCoil = None
        if (hc := elem.attrib.get("harm_coil", "0")) != "0":
            harmCoil = int(hc)

        vector_mappings = {}
        if dataType == "vector":
            if id_x := elem.attrib.get("data_x", None):
                vector_mappings["x"] = int(id_x)
            if id_y := elem.attrib.get("data_y", None):
                vector_mappings["y"] = int(id_y)
            if id_z := elem.attrib.get("data_z", None):
                vector_mappings["z"] = int(id_z)

        return PlotInfo(
            id,
            self._PLOTINFOS[elem.tag],
            dataType,
            lbl,
            plotLegend,
            harmCoil,
            vector_mappings,
        )

    def _extract_plot2d_info(
        self, elem: et.Element, plotInfosAll: list[PlotInfo]
    ) -> None:
        t = elem.find("title")
        id = int(elem.attrib["id"])
        if t:
            title = t.attrib["label"]
        else:
            title = "Plot2D {0}".format(id)
        axes = self._extract_axes_info(elem)

        plotInfos: list[PlotInfo] = []
        for pi in self._PLOTINFOS.values():
            pps = [pp.attrib["id"] for pp in elem.findall(pi)]
            plotInfos.extend(
                filter(lambda x: x.type == pi and x.id in pps, plotInfosAll)
            )
        p2d = Plot2D(title, id, axes, plotInfos.copy())

        self.output.plots2D.append(p2d)

    def _extract_plot3d_info(
        self, elem: et.Element, plotInfosAll: list[PlotInfo]
    ) -> None:
        id = int(elem.attrib["id"])
        if t := elem.find("title"):
            title = t.attrib["label"]
        else:
            title = "Plot3D {0}".format(id)
        axes = self._extract_axes_info(elem)

        plotInfos: list[PlotInfo] = []
        for pi in self._PLOTINFOS.values():
            pps = [pp.attrib["data_id"] for pp in elem.findall(pi)]
            plotInfos.extend(
                filter(lambda x: x.type == pi and x.id in pps, plotInfosAll)
            )
        p3d = Plot3D(title, id, axes, plotInfos.copy())

        self.output.plots3D.append(p3d)

    def _extract_graph_info(self, elem: et.Element) -> None:
        id = int(elem.attrib["id"])
        graphTypes = []
        graphList: list[GraphInfo] = []
        for plot in elem.findall("graphPlot"):
            graphTypes.append(int(plot.attrib["graphType"]))

            graphList.append(
                GraphInfo(
                    int(plot.attrib["id"]),
                    int(plot.attrib["graphType"]),
                    plot.attrib["xval"],
                    plot.attrib["yval"],
                    bool(plot.attrib["logX"]),
                    bool(plot.attrib["logY"]),
                    float(plot.attrib["weight"]),
                    plot.attrib.get("label", None),
                )
            )

        title = elem.attrib.get("title", f"Graph {id}")
        axes = self._extract_axes_info(elem)

        gp = GraphPlot(title, id, axes, graphList.copy())
        if 1 in graphTypes:
            self.output.graphs_device.append(gp)
        if 2 in graphTypes:
            self.output.graphs_transient.append(gp)
        if 3 in graphTypes:
            self.output.graphs_optimization.append(gp)

    def _extract_axes_info(self, elem: et.Element) -> dict[str, PlotAxis]:
        axes: dict[str, PlotAxis] = {}
        for axis in elem:
            if not axis.tag.startswith("axis"):
                continue
            ax = axis.tag[-1]
            lbl = axis.attrib.get("label", "")
            log = axis.attrib.get("log", "false").lower() == "true"
            min = axis.attrib.get("min", None)
            max = axis.attrib.get("max", None)
            bounds = (float(min), float(max)) if min and max else None
            axes[ax] = PlotAxis(lbl, bounds, log)
        return axes

    @staticmethod
    def parse_xml(xml_file: Union[str, os.PathLike], output: RoxieOutputParser) -> None:
        xml_elem_path = pathlib.Path("/")
        parser: _XmlParser
        for event, elem in et.iterparse(xml_file, events=("start", "end")):
            if event == "start":
                xml_elem_path = xml_elem_path / elem.tag
                if xml_elem_path.match("/roxieData"):
                    version = elem.attrib.get("xml_version", -1)
                    if version == "3":
                        parser = _XmlParserV3(output)
                    else:
                        parser = _XmlParserV2(output)
                parser.parse_element_start(xml_elem_path, elem)
            if event == "end":
                if parser is None:
                    raise RuntimeError("Missing parsing of xml version, can't continue")
                parser.parse_element_end(xml_elem_path, elem)
                xml_elem_path = xml_elem_path.parent
            pass


class _XmlParserV2(_XmlParser):
    def parse_element_start(self, path: pathlib.Path, elem: et.Element) -> None:
        # Custom parsing here
        super().parse_element_start(path, elem)

    def parse_element_end(self, path: pathlib.Path, elem: et.Element) -> None:
        if path.match("/roxieData/loop/step/wedgeGeom3D"):
            self._extract_wedges_3D(elem)
            elem.clear()  # Custom parsing here
        else:
            super().parse_element_end(path, elem)

    def _extract_mesh_2d(self, root: et.Element) -> None:
        if self.current_opt is None:
            raise Exception("Error in meshGeometry: No open optimization tag found")
        self.current_opt.meshGeometries = self._extract_mesh(root)

    def _extract_mesh_3d(self, root: et.Element) -> None:
        if self.current_opt is None:
            raise Exception("Error in meshGeometry: No open optimization tag found")
        self.current_opt.meshGeometries3D = self._extract_mesh(root)

    def _extract_mesh(self, root: et.Element) -> Geometry:
        nData = root.find("nodes")
        if nData is None:
            raise Exception("Error in meshGeometry: Nodes missing")
        df = self._xml_to_df(nData, "p")
        nodes = df.to_numpy()[:, 1:]  # drop id column
        elements = None
        if eData := root.find("elements"):
            elements = self._extract_mesh_elements(eData)
        boundaries = None
        if bData := root.find("boundaries"):
            boundaries = self._extract_mesh_boundaries(bData)

        return Geometry(nodes, elements, boundaries)

    def _extract_coils_2D(self, root: et.Element) -> None:
        if self.current_opt is None:
            raise Exception("Error in meshGeometry: No open optimization tag found")
        cables = {}
        for cable in root.findall("cable"):
            cable_nr = int(cable.attrib.get("nr", 0))
            block_nr = int(cable.attrib.get("block_nr", 0))
            layer_nr = int(cable.attrib.get("layer_nr", 0))
            df = self._xml_to_df(cable)
            cable_points = df[["x", "y"]].to_numpy(dtype=np.float64)
            strands = {}
            for strand in cable.findall("strands/strand"):
                strand_nr = int(strand.attrib["nr"])
                df = self._xml_to_df(strand)
                strands[strand_nr] = df[["x", "y"]].to_numpy(dtype=np.float64)
            cables[cable_nr] = CoilGeometry(
                cable_nr, block_nr, layer_nr, cable_points, strands
            )

        self.current_opt.coilGeometries = cables

    def _extract_bricks_3d(self, root: et.Element) -> None:
        if self.current_opt is None:
            raise Exception("Error in meshGeometry: No open optimization tag found")
        geoms = {}
        for brick in root.findall("brick"):
            df = self._xml_to_df(brick)
            id = int(brick.get("nr", 0))
            nodes = df[["x", "y", "z"]].to_numpy(dtype=np.float64)
            geoms[id] = Brick3DGeometry(id, Geometry(nodes, None, None))
            geoms[id].geometry.generate_elements_for_coil_nodes()
        self.current_opt.brickGeometries3D = geoms

    def _extract_coils_3D(self, root: et.Element) -> None:
        if self.current_opt is None:
            raise Exception("Error in meshGeometry: No open optimization tag found")
        geoms = {}
        for cable in root.findall("cable"):
            cableId = int(cable.attrib.get("nr", 0))
            df = self._xml_to_df(cable)
            nodes = df[["x", "y", "z"]].to_numpy(dtype=np.float64)
            geoms[cableId] = Coil3DGeometry(
                nr=cableId,
                block_id=int(cable.attrib.get("block_nr", 0)),
                layer_id=int(cable.attrib.get("layer_nr", 0)),
                geometry=Geometry(
                    nodes,
                    None,
                    None,
                ),
            )
            geoms[cableId].geometry.generate_elements_for_coil_nodes()

        self.current_opt.coilGeometries3D = geoms

    def _extract_wedges_3D(self, root: et.Element) -> None:
        if self.current_opt is None:
            raise Exception("Error in meshGeometry: No open optimization tag found")
        wedges: dict[int, WedgeGeometry] = {}
        for spacer in root.findall("spacer"):
            spacer_id = int(spacer.attrib["nr"])
            layer_id = int(spacer.attrib["layer_nr"])
            block_inner = int(spacer.attrib.get("block_inner", "0"))
            block_outer = int(spacer.attrib.get("block_outer", "0"))

            surfaces: dict[str, Optional[WedgeSurface]] = {}
            place = ["inner", "outer"]
            pos = ["lower", "upper"]
            for p in place:
                edges: dict[str, npt.NDArray[np.float64]] = {}
                for pp in pos:
                    spacer_el = spacer.find(f"{p}/{pp}")
                    if spacer_el:
                        df = self._xml_to_df(spacer_el)
                        edges[pp] = df[["x", "y", "z"]].to_numpy(dtype=np.float64)
                if all(pp in edges for pp in pos):
                    surfaces[p] = WedgeSurface(edges["lower"], edges["upper"])
                else:
                    surfaces[p] = None

            if surfaces["inner"] and surfaces["outer"]:
                surfaces["inner"], surfaces["outer"] = (
                    surfaces["outer"],
                    surfaces["inner"],
                )

            wedges[spacer_id] = WedgeGeometry(
                layer_id,
                spacer_id,
                surfaces["inner"],
                surfaces["outer"],
                block_inner,
                block_outer,
            )

        self.current_opt.wedgeGeometries3D = wedges

    def _extract_mesh_elements(self, root: et.Element) -> Optional[list[list[int]]]:
        results = []
        for elem in root.findall("fe"):
            cnt = int(elem.attrib["cnt"])
            entry = []
            for x in string.ascii_lowercase[0:cnt]:
                entry.append(int(elem.attrib[x]) - 1)
            results.append(entry)
        return results

    def _extract_mesh_boundaries(
        self, root: et.Element, elements: list[str] = ["x", "y"]
    ) -> dict[int, npt.NDArray[np.float64]]:
        df: Optional[pd.DataFrame] = self._xml_to_df(root)
        boundaries: dict[int, npt.NDArray[np.float64]] = {}
        if df is not None:
            for f, vals in df.groupby("f"):
                boundaries[f] = vals[elements].to_numpy(dtype=np.float64)  # type: ignore
        return boundaries

    def _xml_to_df(self, root: et.Element, nodenames: str = "p") -> pd.DataFrame:
        def convert(k: str):
            return fastnumbers.try_int(
                k, on_fail=lambda x: fastnumbers.try_float(x, on_fail=lambda x: x)
            )

        data_dicts = [
            {k: convert(v) for k, v in x.attrib.items()}
            for x in root.findall(nodenames)
        ]
        return pd.DataFrame(data_dicts)

    def _extract_harmonic_table(
        self, harms
    ) -> tuple[dict[int, float], dict[int, float]]:
        bn: dict[int, float] = {}
        an: dict[int, float] = {}
        for harm in harms.findall("harmonic"):
            order = int(harm.attrib["order"])
            bn[order] = float(harm.attrib["b"])
            an[order] = float(harm.attrib["a"])
        return bn, an


class _XmlParserV3(_XmlParser):
    def parse_element_start(self, path: pathlib.Path, elem: et.Element) -> None:
        # Custom parsing here
        super().parse_element_start(path, elem)

    def parse_element_end(self, path: pathlib.Path, elem: et.Element) -> None:
        if elem.tag == "topology":
            self._extract_topology(elem)
            elem.clear()
        elif path.match("/roxieData/loop/step/blockGeom3D"):
            self._extract_coilblocks_3D(elem)
            elem.clear()  # Custom parsing here        else:
        else:
            super().parse_element_end(path, elem)

    def _extract_topology(self, elem: et.Element) -> None:
        if self.current_opt is None:
            raise Exception("Error in meshGeometry: No open optimization tag found")
        self.current_opt._topologydf = self._extract_csv_table(elem)

    def _extract_harmonic_table(
        self, harms
    ) -> tuple[dict[int, float], dict[int, float]]:
        df = self._extract_csv_table(harms)
        bn = dict(zip(df[df.columns[0]], df[df.columns[1]]))
        an = dict(zip(df[df.columns[0]], df[df.columns[2]]))
        return bn, an

    def _extract_coils_2D(self, elem: et.Element) -> None:
        if self.current_opt is None:
            raise Exception("Error in coilGeometry: No open optimization tag found")
        if (cond := elem.find("conductors")) is not None:
            conductors = self._extract_csv_table(cond)
        else:
            raise ValueError("No Conductors found in coilGeom")
        if (strand := elem.find("strands")) is not None:
            strands = self._extract_csv_table(strand)
        else:
            raise ValueError("No Strands found in coilGeom")
        self.current_opt._coilGeomdf = CoilGeomDfs(conductors, strands)

    def _extract_coils_3D(self, elem) -> None:
        if self.current_opt is None:
            raise Exception(
                "Error in geometry extraction: No open optimization tag found"
            )
        self.current_opt._coilGeom3ddf = self._extract_csv_table(elem)

    def _extract_mesh_2d(self, elem) -> None:
        if self.current_opt is None:
            raise Exception("Error in mesh2dGeometry: No open optimization tag found")
        self.current_opt._meshGeomdf = self._extract_mesh(elem)

    def _extract_mesh(self, elem):
        if (node := elem.find("nodes")) is not None:
            nodes = self._extract_csv_table(node)
        else:
            raise ValueError("No nodes found in meshGeom")
        if (ele := elem.find("elements")) is not None:
            elements = self._extract_csv_table(ele)
        else:
            raise ValueError("No elements found in meshGeom")
        if (bound := elem.find("boundaries")) is not None:
            boundaries = self._extract_csv_table(bound)
        else:
            boundaries = pd.DataFrame()
        result = MeshGeomDfs(nodes, elements, boundaries)
        return result

    def _extract_mesh_3d(self, elem) -> None:
        if self.current_opt is None:
            raise Exception("Error in mesh2dGeometry: No open optimization tag found")
        self.current_opt._meshGeom3ddf = self._extract_mesh(elem)

    def _extract_bricks_3d(self, elem) -> None:
        if self.current_opt is None:
            raise Exception(
                "Error in geometry extraction: No open optimization tag found"
            )
        self.current_opt._brickGeom3ddf = self._extract_csv_table(elem)

    def _extract_coilblocks_3D(self, elem) -> None:
        if self.current_opt is None:
            raise Exception("Error in meshGeometry: No open optimization tag found")
        wedges: dict[int, BlockGeometry] = {}
        edge_dict: dict[tuple[int, bool, bool], npt.NDArray] = {}
        blocks = set()
        for bl in elem.findall("block"):
            block_id = int(bl.attrib["nr"])
            outer = bl.attrib["outer"] == "true"
            upper = bl.attrib["upper"] == "true"
            df = self._extract_csv_table(bl)
            coords = df.to_numpy()[:, 1:4]
            blocks.add(block_id)
            edge_dict[(block_id, outer, upper)] = coords
        for bl in blocks:
            iu = edge_dict[(bl, False, True)]
            il = edge_dict[(bl, False, False)]
            ou = edge_dict[(bl, True, True)]
            ol = edge_dict[(bl, True, False)]
            wedges[bl] = BlockGeometry(bl, WedgeSurface(il, iu), WedgeSurface(ol, ou))

        self.current_opt.blockGeometries3D = wedges
