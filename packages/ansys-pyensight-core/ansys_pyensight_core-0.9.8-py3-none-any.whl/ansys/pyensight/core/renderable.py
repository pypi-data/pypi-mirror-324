"""Renderable module.

This module provides the interface for creating objects in the EnSight session
that can be displayed via HTML over the websocket server interface.
"""
import hashlib
import os
import shutil
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union, no_type_check
import uuid
import warnings
import webbrowser

import requests

if TYPE_CHECKING:
    from ansys.pyensight.core import Session


def _get_ansysnexus_version(version: Union[int, str]) -> str:
    if int(version) < 242:
        return ""
    return str(version)


class Renderable:
    """Generates HTML pages for renderable entities.

    This class provides the underlying HTML remote webpage generation for
    the :func:`show<ansys.pyensight.core.Session.show>` method. The approach
    is to generate the renderable in the EnSight session and make the
    artifacts available via the websocket server. The artifacts are then
    wrapped with simple HTML pages, which are also served up by the websocket
    server. These HTML pages can then be used to populate iframes.

    Parameters
    ----------
    session :
        PyEnSight session to generate renderables for.
    cell_handle :
        Jupyter notebook cell handle (if any). The default is ``None``.
    width : int, optional
        Width of the renderable. The default is ``None``.
    height : int, optional
        Height of the renderable. The default is ``None``.
    temporal : bool, optional
        Whether to show data for all timesteps in an interactive
        WebGL-based browser viewer. The default is ``False``.
    aa : int, optional
        Number of antialiasing passes to use when rendering images.
        The default is ``1``.
    fps : float, optional
        Number of frames per second to use for animation playback. The
        default is ``30.0``.
    num_frames : int, optional
        Number of frames of static timestep to record for animation playback.
        The default is ``None``.

    """

    def __init__(
        self,
        session: "Session",
        cell_handle: Optional[Any] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        temporal: bool = False,
        aa: int = 1,
        fps: float = 30.0,
        num_frames: Optional[int] = None,
    ) -> None:
        self._session = session
        self._filename_index: int = 0
        self._guid: str = str(uuid.uuid1()).replace("-", "")
        self._download_names: List[str] = []
        # The Jupyter notebook cell handle (if any)
        self._cell_handle = cell_handle
        # the URL to the base HTML file for this entity
        self._url: Optional[str] = None
        # the pathname of the HTML file in the remote EnSight session
        self._url_remote_pathname: Optional[str] = None
        # the name passed to the pyensight session show() string
        self._rendertype: str = ""
        # Common attributes used by various subclasses
        self._width: Optional[int] = width
        self._height: Optional[int] = height
        self._temporal: bool = temporal
        self._aa: int = aa
        self._fps: float = fps
        self._num_frames: Optional[int] = num_frames
        #
        self._using_proxy = False
        # if we're talking directly to WS, then use 'http' otherwise 'https' for the proxy
        self._http_protocol = "http"
        try:
            if self._session.launcher._pim_instance is not None:
                self._using_proxy = True
                self._http_protocol = "https"
        except Exception:
            # the launcher may not be PIM aware; that's ok
            pass

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return f"{name}( url='{self._url}' )"

    @no_type_check
    def _repr_pretty_(self, p: "pretty", cycle: bool) -> None:
        """Support the pretty module for better IPython support.

        Parameters
        ----------
        p : text, optional
            Pretty flag. The default is ``"pretty"``.
        cycle : bool, optional
            Cycle flag. The default is ``None``.

        """
        name = self.__class__.__name__
        p.text(f"{name}( url='{self._url}' )")

    def _get_query_parameters_str(self, params: Optional[Dict[str, str]] = None) -> str:
        """Generate any optional http query parameters.
        Return a string formatted as a URL query to tack on to the
        beginning part of the URL.  The string may be empty if there
        aren't any parameters.  The method takes a dict
        of parameters, possibly empty or None, and combines it with the
        parameters from the launcher, which also may be empty.
        """
        qp_dict = self._session.launcher._get_query_parameters()
        if qp_dict is None:
            # just in case
            qp_dict = {}
        if params:
            qp_dict.update(params)
        query_parameter_str = ""
        symbol = "?"
        for p in qp_dict.items():
            query_parameter_str += f"{symbol}{p[0]}={p[1]}"
            symbol = "&"
        return query_parameter_str

    def _generate_filename(self, suffix: str) -> Tuple[str, str]:
        """Create session-specific files and URLs.

        Every time this method is called, a new filename (on the EnSight host)
        and the associated URL for that file are generated. The caller
        provides the suffix for the names.

        Parameters
        ----------
        suffix: str
            Suffix of the file.

        Returns
        -------
        Tuple[str, str]
            Filename to use on the host system and the URL that accesses the
            file via REST calls to the websocket server.

        """
        filename = f"{self._session.secret_key}_{self._guid}_{self._filename_index}{suffix}"
        # Note: cannot use os.path.join here as the OS of the EnSight session might not match
        # the client OS.
        pathname = f"{self._session.launcher.session_directory}/{filename}"
        self._filename_index += 1
        return pathname, filename

    def _generate_url(self) -> None:
        """Build the remote HTML filename and associated URL.

        On the remote system the, pathname to the HTML file is
        ``{session_directory}/{session}_{guid}_{index}_{type}.html``.
        The URL to the file (through the session HTTP server) is
        ``http://{system}:{websocketserverhtmlport}/{session}_{guid}_{index}_{type}.html``.

        Note that there may be optional http query parameters at the end of the URL.

        After this call, ``_url`` and ``_url_remote_pathname`` reflect these names.

        """
        suffix = f"_{self._rendertype}.html"
        filename_index = self._filename_index
        remote_pathname, _ = self._generate_filename(suffix)
        simple_filename = f"{self._session.secret_key}_{self._guid}_{filename_index}{suffix}"
        url = f"{self._http_protocol}://{self._session.html_hostname}:{self._session.html_port}"
        self._url = f"{url}/{simple_filename}{self._get_query_parameters_str()}"
        self._url_remote_pathname = remote_pathname

    def _save_remote_html_page(self, html: str) -> None:
        """Create an HTML webpage on the remote host.

        Given a snippet of HTML, create a file on the remote server with the
        name generated by the ``_generate_url()`` method.
        The most common use is to generate an "iframe" wrapper around some HTML
        snippet.

        Parameters
        ----------
        html : str
            HTML snippet to wrap remotely.

        """
        # save "html" into a file on the remote server with filename .html
        cmd = f'open(r"""{self._url_remote_pathname}""", "w").write("""{html}""")'
        self._session.grpc.command(cmd, do_eval=False)

    def browser(self) -> None:
        """Open a web browser page to display the renderable content."""
        if self._url:
            webbrowser.open(self._url)

    @property
    def url(self) -> Optional[str]:
        """URL to the renderable content."""
        return self._url

    def _default_size(self, width: int, height: int) -> Tuple[int, int]:
        """Propose and return a size for a rectangle.

        The renderable may have been constructed with user-supplied width and height
        information. If so, that information is returned. If not, the width and
        height values passed to this method are returned.

        Parameters
        ----------
        width : int
            Width value to return if the renderable does not have a width.
        height : int
            Height value to return if the renderable does not have a height.

        Returns
        -------
        Tuple[int, int]
            Tuple (width, height) of the size values to use.

        """
        out_w = self._width
        if out_w is None:
            out_w = width
        out_h = self._height
        if out_h is None:
            out_h = height
        return out_w, out_h

    def update(self) -> None:
        """Update the visualization and display it.

        When this method is called, the graphics content is updated to the
        current EnSight instance state. For example, an image might be re-captured.
        The URL of the content stays the same, but the content that the URL displays is
        updated.

        If the renderable was created in the context of a Jupyter notebook cell,
        the original cell display is updated.

        """
        if self._cell_handle:
            from IPython.display import IFrame

            width, height = self._default_size(800, 600)
            self._cell_handle.update(IFrame(src=self._url, width=width, height=height))

    def delete(self) -> None:
        """Delete all server resources for the renderable.

        A renderable occupies resources in the EnSight :class:`Session<ansys.pyensight.core.Session>`
        instance. This method releases those resources. Once this method is called, the renderable
        can no longer be displayed.

        Notes
        -----
        This method has not yet been implemented.

        """
        pass

    def download(self, dirname: str) -> List[str]:
        """Download the content files for the renderable.

        A renderable saves files (such as images, mpegs, and geometry) in the EnSight instance.
        Normally, these files are accessed via the webpage specified in the URL property.
        This method allows for those files to be downloaded to a local directory so that they
        can be used for other purposes.

        .. note::
           Any previously existing files with the same name are overwritten.

        Parameters
        ----------
        dirname : str
            Name of the existing directory to save the files to.


        Returns
        -------
        list
            List of names for the downloaded files.

        Examples
        --------
        Download the PNG file generated by the image renderable.

        >>> img = session.show('image", width=640, height=480, aa=4)
        >>> names = img.download("/tmp")
        >>> png_pathname = os.path.join("/tmp", names[0])

        """
        for filename in self._download_names:
            url = f"{self._http_protocol}://{self._session.html_hostname}:{self._session.html_port}/{filename}{self._get_query_parameters_str()}"
            outpath = os.path.join(dirname, filename)
            with requests.get(url, stream=True) as r:
                with open(outpath, "wb") as f:
                    shutil.copyfileobj(r.raw, f)
        return self._download_names


class RenderableImage(Renderable):
    """Renders an image on the EnSight host system and makes it available via a webpage."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize RenderableImage."""
        super().__init__(*args, **kwargs)
        self._rendertype = "image"
        self._generate_url()
        # the HTML serves up a PNG file
        pathname, filename = self._generate_filename(".png")
        self._png_pathname = pathname
        self._png_filename = filename
        # the download is the png file
        self._download_names.append(self._png_filename)
        self.update()

    def update(self):
        """Update the image and display it.

        If the renderable is part of a Jupyter notebook cell, that cell is updated
        as an iframe reference.

        """
        # save the image file on the remote host
        w, h = self._default_size(1920, 1080)
        cmd = f'ensight.render({w},{h},num_samples={self._aa}).save(r"""{self._png_pathname}""")'
        self._session.cmd(cmd)
        # generate HTML page with file references local to the websocket server root
        html = '<body style="margin:0px;padding:0px;">\n'
        html += f'<img src="/{self._png_filename}{self._get_query_parameters_str()}">\n'
        html += "</body>\n"
        # refresh the remote HTML
        self._save_remote_html_page(html)
        super().update()


class RenderableDeepPixel(Renderable):
    """Renders a deep pixel image on the EnSight host system and makes it available via a webpage."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._rendertype = "deep_pixel"
        self._generate_url()
        pathname, filename = self._generate_filename(".tif")
        self._tif_pathname = pathname
        self._tif_filename = filename
        # the download is the tiff file
        self._download_names.append(self._tif_filename)
        self.update()

    def update(self):
        """Update the deep pixel image and display it.

        If the renderable is part of a Jupyter notebook cell, that cell is updated as
        an iframe reference.
        """
        # save the (deep) image file
        # get the optional query parameters which may be an empty string
        # needed for proxy servers like ansys lab
        optional_query = self._get_query_parameters_str()
        w, h = self._default_size(1920, 1080)
        deep = f",num_samples={self._aa},enhanced=1"
        cmd = f'ensight.render({w},{h}{deep}).save(r"""{self._tif_pathname}""")'
        self._session.cmd(cmd)
        html_source = os.path.join(os.path.dirname(__file__), "deep_pixel_view.html")
        with open(html_source, "r") as fp:
            html = fp.read()
        # copy some files from Nexus
        cmd = "import shutil, enve, ceiversion, os.path\n"
        base_name = "os.path.join(enve.home(), f'nexus{ceiversion.nexus_suffix}', 'django', "
        base_name += "'website', 'static', 'website', 'scripts', "
        for script in ["geotiff.js", "geotiff_nexus.js", "bootstrap.min.js"]:
            name = base_name + f"'{script}')"
            cmd += f'shutil.copy({name}, r"""{self._session.launcher.session_directory}""")\n'
        name = "os.path.join(enve.home(), f'nexus{ceiversion.nexus_suffix}', 'django', "
        name += "'website', 'static', 'website', 'content', 'bootstrap.min.css')"
        cmd += f'shutil.copy({name}, r"""{self._session.launcher.session_directory}""")\n'
        self._session.cmd(cmd, do_eval=False)
        # With Bootstrap 5 (2025 R1), class names have '-bs-' in them, e.g. 'data-bs-toggle' vs 'data-toggle'
        bs_prefix = "bs-"
        jquery_version = ""
        if int(self._session._cei_suffix) < 251:
            bs_prefix = ""
            jquery_version = "-3.4.1"
        jquery = f"jquery{jquery_version}.min.js"
        cmd = "import shutil, enve, ceiversion, os.path\n"
        name = base_name + f"'{jquery}')"
        cmd += "try:"
        cmd += f'    shutil.copy({name}, r"""{self._session.launcher.session_directory}""")\n'
        cmd += "except Exception:"
        cmd += "    pass"
        name = "os.path.join(enve.home(), f'nexus{ceiversion.nexus_suffix}', 'django', "
        name += "'website', 'static', 'website', 'content', 'bootstrap.min.css')"
        cmd += f'shutil.copy({name}, r"""{self._session.launcher.session_directory}""")\n'
        self._session.cmd(cmd, do_eval=False)
        url = f"{self._http_protocol}://{self._session.html_hostname}:{self._session.html_port}"
        tiff_url = f"{url}/{self._tif_filename}{optional_query}"
        # replace some bits in the HTML
        html = html.replace("TIFF_URL", tiff_url)
        html = html.replace("ITEMID", self._guid)
        html = html.replace("OPTIONAL_QUERY", optional_query)
        html = html.replace("JQUERY_VERSION", jquery_version)
        html = html.replace("BS_PREFIX", bs_prefix)
        # refresh the remote HTML
        self._save_remote_html_page(html)
        super().update()


class RenderableMP4(Renderable):
    """Renders the timesteps of the current dataset into an MP4 file and displays the results."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._rendertype = "animation"
        self._generate_url()
        # the HTML serves up a PNG file
        pathname, filename = self._generate_filename(".mp4")
        self._mp4_pathname = pathname
        self._mp4_filename = filename
        # the download is the mp4 file
        self._download_names.append(self._mp4_filename)
        self.update()

    def update(self):
        """Update the animation and display it.

        If the renderable is part of a Jupyter notebook cell, that cell is updated as an
        iframe reference.

        """
        # save the image file on the remote host
        w, h = self._default_size(1920, 1080)
        # Assume this is a particle trace animation save...
        num_frames = self._num_frames
        st = 0
        if self._num_frames is None:
            # get the timestep limits, [0,0] is non-time varying
            st, en = self._session.ensight.objs.core.TIMESTEP_LIMITS
            num_frames = en - st + 1
        self._session.ensight.file.animation_rend_offscreen("ON")
        self._session.ensight.file.animation_screen_tiling(1, 1)
        self._session.ensight.file.animation_format("mpeg4")
        self._session.ensight.file.animation_format_options("Quality High Type 1")
        self._session.ensight.file.animation_frame_rate(self._fps)
        self._session.ensight.file.animation_rend_offscreen("ON")
        self._session.ensight.file.animation_numpasses(self._aa)
        self._session.ensight.file.animation_stereo("mono")
        self._session.ensight.file.animation_screen_tiling(1, 1)
        self._session.ensight.file.animation_file(self._mp4_pathname)
        self._session.ensight.file.animation_window_size("user_defined")
        self._session.ensight.file.animation_window_xy(w, h)
        self._session.ensight.file.animation_frames(num_frames)
        self._session.ensight.file.animation_start_number(st)
        self._session.ensight.file.animation_multiple_images("OFF")
        self._session.ensight.file.animation_raytrace_it("OFF")
        self._session.ensight.file.animation_raytrace_ext("OFF")
        self._session.ensight.file.animation_play_flipbook("OFF")
        self._session.ensight.file.animation_play_keyframe("OFF")

        if self._num_frames is None:
            # playing over time
            self._session.ensight.file.animation_play_time("ON")
            self._session.ensight.file.animation_reset_traces("OFF")
            self._session.ensight.file.animation_reset_time("ON")
        else:
            # recording particle traces/etc
            self._session.ensight.file.animation_play_time("OFF")
            self._session.ensight.file.animation_reset_traces("ON")
            self._session.ensight.file.animation_reset_time("OFF")

        self._session.ensight.file.animation_reset_flipbook("OFF")
        self._session.ensight.file.animation_reset_keyframe("OFF")
        self._session.ensight.file.save_animation()

        # generate HTML page with file references local to the websocket server root
        html = '<body style="margin:0px;padding:0px;">\n'
        html += f'<video width="{w}" height="{h}" controls>\n'
        html += f'    <source src="/{self._mp4_filename}{self._get_query_parameters_str()}" type="video/mp4" />\n'
        html += "</video>\n"
        html += "</body>\n"

        # refresh the remote HTML
        self._save_remote_html_page(html)
        super().update()


class RenderableWebGL(Renderable):
    """Renders an AVZ file (WebGL renderable) on the EnSight host system and makes it available via
    a webpage.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._rendertype = "webgl"
        self._generate_url()
        pathname, filename = self._generate_filename(".avz")
        self._avz_pathname = pathname
        self._avz_filename = filename
        # the download is the avz file
        self._download_names.append(self._avz_filename)
        self.update()

    def update(self):
        """Update the WebGL geometry and display it.

        If the renderable is part of a Jupyter notebook cell, that cell is updated as
        an iframe reference.
        """
        # save the .avz file
        self._session.ensight.part.select_all()
        self._session.ensight.savegeom.format("avz")
        # current timestep or all of the timesteps
        ts = self._session.ensight.objs.core.TIMESTEP
        st = ts
        en = ts
        if self._temporal:
            st, en = self._session.ensight.objs.core.TIMESTEP_LIMITS
        self._session.ensight.savegeom.begin_step(st)
        self._session.ensight.savegeom.end_step(en)
        self._session.ensight.savegeom.step_by(1)
        # Save the file
        self._session.ensight.savegeom.save_geometric_entities(self._avz_pathname)
        # generate HTML page with file references local to the websocket server root
        version = _get_ansysnexus_version(self._session._cei_suffix)
        if self._using_proxy:
            # if using pim we get the static content from the front end and not
            # where ensight is running, thus we use a specific URI host and not relative.
            html = f"<script src='{self._http_protocol}://{self._session.html_hostname}:{self._session.html_port}/ansys{version}/nexus/viewer-loader.js'></script>\n"
            html += f"<ansys-nexus-viewer src='{self._http_protocol}://{self._session.html_hostname}:{self._session.html_port}/{self._avz_filename}"
            html += f"{self._get_query_parameters_str()}'></ansys-nexus-viewer>\n"
        else:
            html = f"<script src='/ansys{version}/nexus/viewer-loader.js'></script>\n"
            html += f"<ansys-nexus-viewer src='/{self._avz_filename}{self._get_query_parameters_str()}'></ansys-nexus-viewer>\n"
        # refresh the remote HTML
        self._save_remote_html_page(html)
        super().update()


class RenderableVNC(Renderable):
    """Generates an ansys-nexus-viewer component that can be used to connect to the EnSight VNC remote image renderer."""

    def __init__(self, *args, **kwargs) -> None:
        ui = kwargs.get("ui")
        if kwargs.get("ui"):
            kwargs.pop("ui")
        super().__init__(*args, **kwargs)
        self._ui = ui
        self._generate_url()
        self._rendertype = "remote"
        self.update()

    def _update_2023R2_or_less(self):
        """Update the remote rendering widget and display it for
        backend EnSight of version earlier than 2024R1
        """
        query_params = {
            "autoconnect": "true",
            "host": self._session.html_hostname,
            "port": self._session.ws_port,
        }
        url = f"{self._http_protocol}://{self._session.html_hostname}:{self._session.html_port}"
        url += "/ansys/nexus/novnc/vnc_envision.html"
        url += self._get_query_parameters_str(query_params)
        self._url = url

    def update(self):
        """Update the remote rendering widget and display it.

        If the renderable is part of a Jupyter notebook cell, that cell is updated as an
        iframe reference.

        """
        optional_query = self._get_query_parameters_str()
        version = _get_ansysnexus_version(self._session._cei_suffix)
        ui = "simple" if not self._ui else self._ui
        if int(self._session._cei_suffix) < 242:  # pragma: no cover
            version = ""
            self._update_2023R2_or_less()  # pragma: no cover
        else:
            html = (
                f"<script src='/ansys{version}/nexus/viewer-loader.js{optional_query}'></script>\n"
            )
            rest_uri = (
                f"{self._http_protocol}://{self._session.html_hostname}:{self._session.html_port}"
            )
            ws_uri = (
                f"{self._http_protocol}://{self._session.html_hostname}:{self._session.ws_port}"
            )

            query_args = ""
            if self._using_proxy and optional_query:  # pragma: no cover
                query_args = f', "extra_query_args":"{optional_query[1:]}"'  # pragma: no cover

            attributes = ' renderer="envnc"'
            attributes += f" ui={ui}"
            attributes += ' active="true"'
            attributes += (
                " renderer_options='"
                + f'{{ "ws":"{ws_uri}", "http":"{rest_uri}", "security_token":"{self._session.secret_key}", "connect_to_running_ens":true {query_args} }}'
                + "'"
            )

            html += f"<ansys-nexus-viewer {attributes}></ansys-nexus-viewer>\n"

            # refresh the remote HTML
            self._save_remote_html_page(html)
        super().update()


# Undocumented class
class RenderableVNCAngular(Renderable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._generate_url()
        self._rendertype = "remote"
        self.update()

    def update(self):
        optional_query = self._get_query_parameters_str()
        version = _get_ansysnexus_version(self._session._cei_suffix)
        base_content = f"""
<!doctype html>
<html lang="en" class="dark">
<head><base href="/ansys{version}/nexus/angular/">
  <meta charset="utf-8">
  <title>WebEnSight</title>
  <script src="/ansys{version}/nexus/viewer-loader.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="ensight.ico">
<link rel="stylesheet" href="styles.css"></head>
<body>
"""
        module_with_attributes = "\n  <web-en-sight "
        module_with_attributes += f'wsPort="{self._session.ws_port}" '
        module_with_attributes += f'secretKey="{self._session.secret_key}"'
        if self._using_proxy and optional_query:  # pragma: no cover
            module_with_attributes += f' extraQueryArgs="{optional_query[1:]}"'
        module_with_attributes += ">\n"
        script_src = '<script src="runtime.js" type="module"></script><script src="polyfills.js" type="module"></script><script src="main.js" type="module"></script></body>\n</html>'
        content = base_content + module_with_attributes + script_src
        self._save_remote_html_page(content)
        super().update()


class RenderableEVSN(Renderable):
    """Generates a URL that can be used to connect to the EnVision VNC remote image renderer."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._rendertype = "remote_scene"
        self._generate_url()
        pathname, filename = self._generate_filename(".evsn")
        self._evsn_pathname = pathname
        self._evsn_filename = filename
        pathname, filename = self._generate_filename(".png")
        self._proxy_pathname = pathname
        self._proxy_filename = filename
        # the download is the evsn file
        self._download_names.append(self._evsn_filename)
        self.update()

    def update(self):
        """Update the remote rendering widget and display it.

        If the renderable is part of a Jupyter notebook cell, that cell is updated as an
        iframe reference.

        """
        # Save the proxy image
        w, h = self._default_size(1920, 1080)
        cmd = f'ensight.render({w},{h},num_samples={self._aa}).save(r"""{self._proxy_pathname}""")'
        self._session.cmd(cmd)
        # save the .evsn file
        self._session.ensight.file.save_scenario_which_parts("all")
        self._session.ensight.file.scenario_format("envision")
        # current timestep or all of the timesteps
        if self._temporal:
            st, en = self._session.ensight.objs.core.TIMESTEP_LIMITS
            self._session.ensight.file.scenario_steptime_anim(1, st, en, 1.0)
        else:
            self._session.ensight.file.scenario_steptime_anim(0, 1, 1, 1)
        varlist = self._session.ensight.objs.core.VARIABLES.find(True, "ACTIVE")
        vars = [x.DESCRIPTION for x in varlist]
        self._session.ensight.variables.select_byname_begin(vars)
        # Save the file
        self._session.ensight.file.save_scenario_fileslct(self._evsn_pathname)

        # generate HTML page with file references local to the websocketserver root
        optional_query = self._get_query_parameters_str()
        version = _get_ansysnexus_version(self._session._cei_suffix)
        html = f"<script src='/ansys{version}/nexus/viewer-loader.js{optional_query}'></script>\n"
        server = f"{self._http_protocol}://{self._session.html_hostname}:{self._session.html_port}"

        # FIXME: This method doesn't work with Ansys Lab since the viewer seems to require
        # a full pathname to the file being generated by EnSight on a shared file system.
        # The following commented out line should replace the two after that, but that
        # prevents running locally from working since it's not using the full pathname to
        # the shared file. -MFK
        cleanname = self._evsn_filename.replace("\\", "/")
        attributes = f"src='{cleanname}'"
        # attributes = f"src='{cleanname}{optional_query}'"

        attributes += f" proxy_img='/{self._proxy_filename}{optional_query}'"
        attributes += " aspect_ratio='proxy'"
        attributes += " renderer='envnc'"
        http_uri = f'"http":"{server}"'
        ws_uri = (
            f'"ws":"{self._http_protocol}://{self._session.html_hostname}:{self._session.ws_port}"'
        )
        secrets = f'"security_token":"{self._session.secret_key}"'
        if not self._using_proxy or not optional_query:  # pragma: no cover
            attributes += f" renderer_options='{{ {http_uri}, {ws_uri}, {secrets} }}'"
        elif self._using_proxy and optional_query:  # pragma: no cover
            query_args = f'"extra_query_args":"{optional_query[1:]}"'  # pragma: no cover
            attributes += f" renderer_options='{{ {http_uri}, {ws_uri}, {secrets}, {query_args} }}'"  # pragma: no cover
        html += f"<ansys-nexus-viewer {attributes}></ansys-nexus-viewer>\n"
        # refresh the remote HTML
        self._save_remote_html_page(html)
        super().update()


class RenderableSGEO(Renderable):  # pragma: no cover
    """Generates a WebGL-based renderable that leverages the SGEO format/viewer interface for progressive geometry transport."""

    def __init__(self, *args, **kwargs) -> None:  # pragma: no cover
        super().__init__(*args, **kwargs)
        self._generate_url()
        pathname, filename = self._generate_filename("")
        # on the server, a JSON block can be accessed via:
        # {_sgeo_base_pathname}/geometry.sgeo
        # and the update files:
        # {_sgeo_base_pathname}/{names}.bin
        self._sgeo_base_pathname = pathname
        self._sgeo_base_filename = filename
        # Create the directory where the sgeo files will go '/{filename}/' URL base
        cmd = f'import os\nos.mkdir(r"""{self._sgeo_base_pathname}""")\n'
        self._session.cmd(cmd, do_eval=False)
        # get a stream ID
        self._stream_id = self._session.ensight.dsg_new_stream(sgeo=1)
        #
        self._revision = 0
        self.update()

    def update(self):  # pragma: no cover
        """Generate a SGEO geometry file.

        This method causes the EnSight session to generate an updated geometry SGEO
        file and content and then display the results in any attached WebGL viewer.

        If the renderable is part of a Jupyter notebook cell, that cell is updated as an
        iframe reference.

        """
        # Ask for an update to be generated
        remote_filename = f"{self._sgeo_base_pathname}/geometry.sgeo"
        self._session.ensight.dsg_save_update(
            remote_filename,
            urlprefix=f"/{self._sgeo_base_filename}/",
            stream=self._stream_id,
        )

        # Update the proxy image
        self._update_proxy()

        # If the first update, generate the HTML
        if self._revision == 0:
            # generate HTML page with file references local to the websocketserver root
            attributes = (
                f"src='/{self._sgeo_base_filename}/geometry.sgeo{self._get_query_parameters_str()}'"
            )
            attributes += f" proxy_img='/{self._sgeo_base_filename}/proxy.png{self._get_query_parameters_str()}'"
            attributes += " aspect_ratio='proxy'"
            attributes += " renderer='sgeo'"
            version = _get_ansysnexus_version(self._session._cei_suffix)
            html = f"<script src='/ansys{version}/nexus/viewer-loader.js{self._get_query_parameters_str()}'></script>\n"
            html += f"<ansys-nexus-viewer id='{self._guid}' {attributes}></ansys-nexus-viewer>\n"
            html += self._periodic_script()
            # refresh the remote HTML
            self._save_remote_html_page(html)
            # Subsequent updates are handled by the component itself
            super().update()

        # update the revision file
        rev_filename = f"{self._sgeo_base_pathname}/geometry.rev"
        cmd = f'with open(r"""{rev_filename}""", "w") as fp:\n'
        cmd += f'    fp.write("{self._revision}")\n'
        self._session.cmd(cmd, do_eval=False)

        self._revision += 1

    def _update_proxy(self):
        """Replace the current proxy image with the current view."""
        # save a proxy image
        w, h = self._default_size(1920, 1080)
        remote_filename = f"{self._sgeo_base_pathname}/proxy.png"
        cmd = f'ensight.render({w},{h},num_samples={self._aa}).save(r"""{remote_filename}""")'
        self._session.cmd(cmd, do_eval=False)

    def delete(self) -> None:
        try:
            _ = self._session.ensight.dsg_close_stream(self._stream_id)
        except Exception:
            pass
        super().delete()

    def _periodic_script(self) -> str:
        html_source = os.path.join(os.path.dirname(__file__), "sgeo_poll.html")
        with open(html_source, "r") as fp:
            html = fp.read()
        revision_uri = f"/{self._sgeo_base_filename}/geometry.rev{self._get_query_parameters_str()}"
        html = html.replace("REVURL_ITEMID", revision_uri)
        html = html.replace("ITEMID", self._guid)
        return html


class RenderableFluidsWebUI(Renderable):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._session.ensight_version_check("2025 R1")
        warnings.warn("The webUI is still under active development and should be considered beta.")
        self._rendertype = "webui"
        self._generate_url()
        self.update()

    def _generate_url(self) -> None:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(self._session._secret_key.encode())
        token = sha256_hash.hexdigest()
        optional_query = self._get_query_parameters_str()
        port = self._session._webui_port
        if "instance_name" in self._session._launcher._get_query_parameters():
            instance_name = self._session._launcher._get_query_parameters()["instance_name"]
            # If using PIM, the port needs to be the 443 HTTPS Port;
            port = self._session.html_port
            # In the webUI code there's already a workflow to pass down the query parameter
            # ans_instance_id, just use it
            instance_name = self._session._launcher._get_query_parameters()["instance_name"]
            optional_query = f"?ans_instance_id={instance_name}"
        url = f"{self._http_protocol}://{self._session.html_hostname}:{port}"
        url += f"{optional_query}#{token}"
        self._url = url
