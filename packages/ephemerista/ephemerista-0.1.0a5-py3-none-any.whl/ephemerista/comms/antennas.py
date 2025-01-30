import abc
import math
from typing import Literal

import branca
import folium
import geojsoncontour
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydantic_numpy.typing as pnd
import scipy
from folium import plugins as folium_plugins
from matplotlib import pyplot as plt
from numpy.typing import ArrayLike
from pydantic import Field
from pydantic.json_schema import SkipJsonSchema
from scipy.interpolate import griddata

from ephemerista import BaseModel, Vec3
from ephemerista.angles import Angle
from ephemerista.comms.utils import to_db, wavelength
from ephemerista.coords.twobody import TwoBody
from ephemerista.form_widget import with_form_widget
from ephemerista.math import cone_vectors
from ephemerista.propagators.orekit.conversions import time_to_abs_date

ANTENNA_DISCRIMINATOR = "antenna_type"
PATTERN_DISCRIMINATOR = "pattern_type"

"""
When dividing by a quantity, if this quantity is lower than this threshold,
an alternate formulation will be used to avoid division by zero
"""
DIV_BY_ZERO_LIMIT = 1e-6

"""
Represents the lowest gain value in linear representation, because zero gain
would lead to an error when converting to dB.
This value represents a signal strength in dB so low that no link will probably be possible.
"""
MINF_GAIN_LINEAR = 1e-12

SHORT_DIPOLE_LIMIT = 0.1  # when length/wavelength lower than this value, it is officially a short dipole


class FieldOfRegard(Angle):
    degrees: float = Field(
        ge=0.0,
        le=90.0,
        default=0.0,
        description="Field of regard half-cone angle in degrees",
    )


@with_form_widget
class Antenna(BaseModel, abc.ABC):
    design_frequency: float | None = Field(
        gt=0.0, default=None, description="The design frequency of the antenna in Hz"
    )
    field_of_regard: FieldOfRegard = Field(
        description=(
            "Defines a cone around the boresight vector in which a movable antenna can operate."
            "The value is the half-angle of the cone in degrees. A value of 0.0 indicates a fixed antenna."
        ),
        default=FieldOfRegard(),
    )
    boresight_vector: Vec3 = Field(
        description="The boresight vector of the antenna in the local reference frame",
        default=(0.0, 0.0, 1.0),
    )

    @abc.abstractmethod
    def gain(self, frequency: float, angle: float) -> float:
        raise NotImplementedError()

    @abc.abstractmethod
    def beamwidth(self, frequency: float) -> float:
        raise NotImplementedError()

    @property
    def boresight_array(self) -> np.ndarray:
        return np.array(self.boresight_vector)

    def viz_cone_3d(
        self,
        frequency: float,
        sc_state: TwoBody,
        beamwidth_deg: float | None = None,
        cone_length: float | None = None,  # cone length in kilometers
        opacity: float = 0.5,
        name: str | None = None,
        **kwargs,
    ) -> go.Surface:
        """
        Plots the antenna's beamwidth as a 3D cone.

        The beamwidth is optional. If None, the antenna's beamwidth will be used.

        All keywords arguments are passed to plotly's go.Surface method to tune the plot

        TODO: make the sc_state param optional. That would require the following:
            - enforcing cone_length is not None
            - use the antenna's boresight vector in LVLH frame without converting it to ECI frame
                (which means the 3D visualization will be in LVLH coordinate system)
        """
        if not beamwidth_deg:
            beamwidth_deg = np.rad2deg(self.beamwidth(frequency))

        sat_pos = sc_state.to_cartesian().position
        if not cone_length:
            cone_length = np.linalg.norm(sat_pos)

        if not name:
            name = "Antenna cone"

        eci_from_lvlh = sc_state.to_cartesian().rotation_lvlh()
        boresight_eci = eci_from_lvlh @ self.boresight_array

        angle_res_deg = 10.0
        cone_dirs, _ = cone_vectors(
            boresight_eci, theta_deg=beamwidth_deg, angle_res_deg=angle_res_deg, include_endpoint=True
        )
        cone_lengths = np.linspace(0, cone_length, 10)
        cone_dirs_3d = np.zeros((len(cone_lengths), cone_dirs.shape[0], cone_dirs.shape[1]))
        for i, cone_len in enumerate(cone_lengths):
            cone_dirs_3d[i, :, :] = cone_len * cone_dirs

        cone_vec_3d = cone_dirs_3d + sat_pos

        viz_cone = go.Surface(
            x=cone_vec_3d[:, :, 0],
            y=cone_vec_3d[:, :, 1],
            z=cone_vec_3d[:, :, 2],
            showscale=False,
            opacity=opacity,
            surfacecolor=np.linalg.norm(cone_dirs_3d, axis=2),
            name=name,
            **kwargs,
        )
        return viz_cone


class SimpleAntenna(Antenna):
    antenna_type: Literal["simple"] = Field(default="simple", alias="type", repr=False, frozen=True)
    gain_db: float = Field(ge=0.0, json_schema_extra={"title": "Gain"})
    beamwidth_deg: float = Field(ge=0.0, json_schema_extra={"title": "Beamwidth"})

    def gain(self, _frequency: float, _angle: float) -> float:
        return self.gain_db

    def beamwidth(self, _frequency: float) -> float:
        return np.deg2rad(self.beamwidth_deg)


@with_form_widget
class Pattern(BaseModel, abc.ABC):
    @abc.abstractmethod
    def gain(self, frequency: float, angle: float) -> float:
        raise NotImplementedError()

    @abc.abstractmethod
    def beamwidth(self, frequency: float) -> float:
        raise NotImplementedError()


class ParabolicPattern(Pattern):
    pattern_type: Literal["parabolic"] = Field(default="parabolic")
    diameter: float = Field(gt=0.0)
    efficiency: float = Field(gt=0.0)

    bessel_first_root: float = scipy.special.jn_zeros(1, 1)[0]

    def area(self) -> float:
        return math.pi * self.diameter**2 / 4

    def beamwidth(self, frequency: float) -> float:
        """
        Computes the half-cone angle of the half-power beamwidth in radians
        Source: https://en.wikipedia.org/wiki/Parabolic_antenna
        """
        return np.arcsin(self.bessel_first_root * wavelength(frequency) / np.pi / self.diameter)

    def peak_gain(self, frequency: float) -> float:
        area = self.area()
        lamb = wavelength(frequency)
        g = to_db(4 * math.pi * area / lamb**2)
        return g + to_db(self.efficiency)

    def gain(self, frequency: float, angle: ArrayLike) -> np.ndarray:
        """
        Computes the gain of a parabolic antenna for a direction given by the angle `_angle`
        Assumes an uniform illuminated aperture (i.e. taper parameter $\tau$ = 1.0)
        Source: Equation (17) of https://web.archive.org/web/20160101021857/https://library.nrao.edu/public/memos/alma/memo456.pdf
        """
        u = np.pi * self.diameter / wavelength(frequency) * np.sin(angle)

        with np.testing.suppress_warnings() as sup:
            # Ugly but otherwise we get 'RuntimeWarning: invalid value encountered in scalar divide' warnings,
            # but we actually don't use the values issuing these warnings thanks to the np.where call
            sup.filter(RuntimeWarning)

            pattern_loss_linear = np.where(
                np.abs(u) < DIV_BY_ZERO_LIMIT,  # Preventing division by zero at zero angle
                1.0,  # Maximum gain (relative to peak gain)
                np.square(2 * scipy.special.jv(1, u) / u),
            )
            # Setting very low gain at angles higher than 45 degrees
            # This is because the pattern equation used is symmetrical, that would result in
            # the backlobe having the same gain as the main lobe, which is wrong...

            # Besides, this equation also does not model spillover radation from the feed missing the reflector,
            # so it does not make sense to use it for high angles.
            # For basically any parabolic antenna, if the depointing is higher than 45 degrees,
            # you will barely receive anything...
            pattern_loss_linear = np.where(
                np.cos(angle) < np.cos(np.pi / 2),
                MINF_GAIN_LINEAR,  # very small value otherwise conversion to dB fails
                pattern_loss_linear,
            )

            return self.peak_gain(frequency=frequency) + to_db(pattern_loss_linear)


class CustomPattern(Pattern):
    pattern_type: Literal["custom"] = Field(default="custom")
    # Skipping because it cannot be displayed by the form widget
    angles: SkipJsonSchema[pnd.Np1DArrayFp64]
    # Skipping because it cannot be displayed by the form widget
    gains: SkipJsonSchema[pnd.Np1DArrayFp64]
    symmetrical: bool = Field(default=True)
    beamwidth_: float = Field(default=np.pi)

    def beamwidth(self, _frequency: float) -> float:
        """
        Returns 180 degrees, because the concept of beamwidth is undefined with a custom pattern...
        """
        return self.beamwidth_

    def gain(self, _frequency: float, angle: ArrayLike) -> np.ndarray:
        # TODO: Handle symmetry and out-of-range angles
        return np.interp(angle, self.angles, self.gains)  # type: ignore

    def peak_gain(self, _frequency: float) -> float:
        return np.max(self.gains)


class DipolePattern(Pattern):
    pattern_type: Literal["dipole"] = Field(default="dipole")
    length: float = Field(gt=0.0)

    def beamwidth(self, _frequency: float) -> float:
        """
        Returns 180 degrees, because the concept of beamwidth is undefined with dipole antennas:
          a dipole antennas has several main lobes of sometimes different widths
        """
        return np.pi

    def gain_pattern(self, frequency: float, angle: ArrayLike) -> np.ndarray:
        """
        Returns the gain relative to the peak gain, in linear units, between 0 and 1
        Source 1: Slide 17 of https://www.brown.edu/research/labs/mittleman/sites/brown.edu.research.labs.mittleman/files/uploads/lecture25.pdf
        Source 2: https://www.antenna-theory.com/antennas/dipole.php
        Source 3: https://en.wikipedia.org/wiki/Dipole_antenna#Short_dipole
        Source 4: https://www.antenna-theory.com/antennas/shortdipole.php
        """
        with np.testing.suppress_warnings() as sup:
            # TODO: Ugly but otherwise we get 'RuntimeWarning: divide by zero encountered in scalar divide' warnings,
            # but we actually don't use the values issuing these warnings thanks to the np.where call
            sup.filter(RuntimeWarning)

            k = 2 * np.pi / wavelength(frequency=frequency)
            kl2 = k * self.length / 2

            return np.where(
                np.abs(np.sin(angle)) < DIV_BY_ZERO_LIMIT,  # Avoid division by zero when np.sin(angle) is small
                MINF_GAIN_LINEAR,  # very small value otherwise the conversion to dB is not happy
                np.where(
                    self.length / wavelength(frequency=frequency) < SHORT_DIPOLE_LIMIT,
                    np.square(np.sin(angle)),  # Alternative formulation for short dipole
                    np.square((np.cos(kl2 * np.cos(angle)) - np.cos(kl2)) / np.sin(angle)),  # General dipole
                ),
            )

    def directivity(self, frequency: float) -> float:
        integral, err = scipy.integrate.quad(
            lambda angle, frequency: self.gain_pattern(frequency=frequency, angle=angle) * np.sin(angle),
            0,
            np.pi,
            args=(frequency,),
        )
        return 2 / integral

    def peak_gain(self, frequency: float) -> float:
        optimum = scipy.optimize.minimize_scalar(lambda x: -to_db(self.gain_pattern(frequency=frequency, angle=x)))
        return -optimum.fun + to_db(self.directivity(frequency=frequency))

    def gain(self, frequency: float, angle: ArrayLike) -> np.ndarray:
        return to_db(self.directivity(frequency=frequency)) + to_db(self.gain_pattern(frequency=frequency, angle=angle))


type PatternType = ParabolicPattern | CustomPattern | DipolePattern


class ComplexAntenna(Antenna):
    antenna_type: Literal["complex"] = Field(default="complex", alias="type", repr=False, frozen=True)
    pattern: PatternType = Field(discriminator=PATTERN_DISCRIMINATOR)

    def gain(self, frequency: float, angle: ArrayLike) -> np.ndarray:
        return self.pattern.gain(frequency, angle)

    def beamwidth(self, frequency: float) -> float:
        return self.pattern.beamwidth(frequency)

    def peak_gain(self, frequency: float) -> float:
        return self.pattern.peak_gain(frequency=frequency)

    def plot_pattern(
        self,
        frequency: float,
        fig_style: str = "polar",
        trace_name: str | None = None,
        *,
        relative_to_peak: bool = False,
    ) -> go.Scatterpolar | go.Scatter | None:
        theta_array = np.arange(-np.pi, np.pi, 1e-3)
        gain_array = self.gain(frequency=frequency, angle=theta_array)
        if relative_to_peak:
            gain_array = gain_array - self.peak_gain(frequency=frequency)

        if fig_style == "polar":
            return go.Scatterpolar(
                r=gain_array,
                theta=np.rad2deg(theta_array),
                mode="lines",
                name=trace_name,
            )

        elif fig_style == "linear":
            return go.Scatter(y=gain_array, x=np.rad2deg(theta_array), mode="lines", name=trace_name)

    def plot_contour_2d(self, frequency: float, sc_state: TwoBody, gain_dynamic: float = 75) -> folium.Map:
        """
        Creates a folium interactive map with the antenna beam contour
        Largely inspired from https://github.com/python-visualization/folium/issues/958#issuecomment-427156672
        """
        gain_coords_df = self.to_geo_df(frequency, sc_state)

        # Setup colormap
        colors = ["#f0f921", "#febd2a", "#f48849", "#db5c68", "#b83289", "#8b0aa5", "#5302a3"]
        vmax = gain_coords_df["gain"].max()
        gain_coords_df = gain_coords_df.loc[gain_coords_df["gain"] >= vmax - gain_dynamic]
        vmin = gain_coords_df["gain"].min()
        levels = len(colors)

        # Make a grid
        x_arr = np.linspace(gain_coords_df["lon_deg"].min(), gain_coords_df["lon_deg"].max(), 800)
        y_arr = np.linspace(gain_coords_df["lat_deg"].min(), gain_coords_df["lat_deg"].max(), 800)
        x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)

        # Grid the values
        z_mesh = griddata(
            (gain_coords_df["lon_deg"], gain_coords_df["lat_deg"]),
            gain_coords_df["gain"],
            (x_mesh, y_mesh),
            method="linear",
        )

        # Gaussian filter the grid to make it smoother
        sigma = [5, 5]

        # Set up the folium plot
        geomap = folium.Map(
            [gain_coords_df["lat_deg"].mean(), gain_coords_df["lon_deg"].mean()], zoom_start=4, tiles="cartodbpositron"
        )

        # Plot the contour plot on folium
        folium.GeoJson(
            geojsoncontour.contourf_to_geojson(
                contourf=plt.contourf(
                    x_mesh,
                    y_mesh,
                    scipy.ndimage.gaussian_filter(z_mesh, sigma, mode="constant"),
                    levels - 1,
                    alpha=0.9,
                    colors=colors,
                    linestyles="None",
                    vmin=vmin,
                    vmax=vmax,
                ),
                min_angle_deg=3.0,
                ndigits=5,
                stroke_width=1,
                fill_opacity=0.8,
            ),
            style_function=lambda x: {
                "color": x["properties"]["stroke"],
                "weight": x["properties"]["stroke-width"],
                "fillColor": x["properties"]["fill"],
                "opacity": 0.6,
            },
        ).add_to(geomap)

        # Add the colormap to the folium map
        geomap.add_child(
            branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax, caption="Gain [dB]").to_step(levels)
        )

        # Fullscreen mode
        folium_plugins.Fullscreen(position="topright", force_separate_button=True).add_to(geomap)

        if plt.get_backend() == "module://matplotlib_inline.backend_inline" and len(plt.get_fignums()) > 0:
            # Close matplotlib plot opened by plt.contourf, annoying when working in a jupyter notebook
            plt.close("all")

        return geomap

    def to_geo_df(self, frequency: float, sc_state: TwoBody) -> pd.DataFrame:
        """
        Returns a dataframe containing the ground coordinates of the antenna beam (i.e. gain)
        as a function of the theta and phi angles
        TODO: project the vectors onto the Earth spheroid without resorting to Orekit
        """
        from ephemerista.propagators.orekit import start_orekit

        start_orekit()

        from org.hipparchus.geometry.euclidean.threed import Line, Vector3D
        from org.orekit.frames import FramesFactory  # type: ignore
        from org.orekit.models.earth import ReferenceEllipsoid  # type: ignore
        from org.orekit.utils import IERSConventions  # type: ignore

        icrf = FramesFactory.getGCRF()  # Earth-centered ICRF

        itrf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)

        wgs84_ellipsoid = ReferenceEllipsoid.getWgs84(itrf)
        orekit_date = time_to_abs_date(sc_state.time)

        theta_res_deg = 0.5
        phi_res_deg = 1.0
        theta_array = np.arange(0, np.pi / 2, np.deg2rad(theta_res_deg))
        gain_array = self.gain(frequency=frequency, angle=theta_array)

        eci_from_lvlh = sc_state.to_cartesian().rotation_lvlh()
        sc_pos_eci = 1e3 * sc_state.to_cartesian().position
        sc_pos_orekit = Vector3D(sc_pos_eci)
        boresight_eci = eci_from_lvlh @ self.boresight_array

        records = []
        # Convert theta array to boresight vectors
        for theta_deg, gain in zip(np.rad2deg(theta_array), gain_array, strict=False):
            if theta_deg > 90:  # noqa: PLR2004
                continue

            # Because antennas as of now are phi-invariant and only depend on theta, we generate a cone and a phi array
            cone_vecs_eci, phi_array = cone_vectors(v1=boresight_eci, theta_deg=theta_deg, angle_res_deg=phi_res_deg)

            for phi_deg, cone_vec_eci in zip(np.rad2deg(phi_array), cone_vecs_eci, strict=False):
                cone_line = Line.fromDirection(sc_pos_orekit, Vector3D(cone_vec_eci), 1.0)
                geodetic_point = wgs84_ellipsoid.getIntersectionPoint(cone_line, sc_pos_orekit, icrf, orekit_date)
                if not geodetic_point:
                    #  No intersection point was found
                    continue

                records.append(
                    {
                        "theta_deg": theta_deg,
                        "phi_deg": phi_deg,
                        "gain": gain,
                        "lat_deg": np.rad2deg(geodetic_point.getLatitude()),
                        "lon_deg": np.rad2deg(geodetic_point.getLongitude()),
                    }
                )

        gain_coords_df = pd.DataFrame.from_records(records)

        return gain_coords_df


type AntennaType = SimpleAntenna | ComplexAntenna
