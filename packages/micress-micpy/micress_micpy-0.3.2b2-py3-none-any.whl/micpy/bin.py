"""The `micpy.bin` module provides methods to read and write binary files."""

from dataclasses import dataclass
from typing import Callable, Generator, IO, List, Optional, Tuple, Union

import gzip
import os
import sys
import zlib

import numpy as np

from micpy import geo
from micpy import utils
from micpy.matplotlib import matplotlib, pyplot


__all__ = ["File", "Field", "Series", "plot", "PlotArgs"]


@dataclass
class Chunk:
    """A chunk of uncompressed binary data."""

    DEFAULT_SIZE = 8388608

    data: bytes
    decompressobj: zlib.decompressobj = None

    @staticmethod
    def iterate(
        file: IO[bytes],
        chunk_size: int,
        compressed: bool = True,
        offset: int = 0,
        decompressobj: zlib.decompressobj = None,
    ) -> Generator["Chunk", None, None]:
        """Yield chunks of uncompressed binary data."""
        file.seek(offset)

        if decompressobj:
            decompressobj = decompressobj.copy()
        else:
            decompressobj = (
                zlib.decompressobj(zlib.MAX_WBITS | 32) if compressed else None
            )

        while True:
            data = file.read(chunk_size)
            if data == b"":
                break

            if compressed:
                prev_decompressobj = decompressobj
                decompressobj = prev_decompressobj.copy()
                data = decompressobj.decompress(data)

            yield Chunk(data, prev_decompressobj if compressed else None)


class Footer:
    """A field footer."""

    TYPE = [("length", np.int32)]
    SIZE = np.dtype(TYPE).itemsize

    def __init__(self, length: int = 0):
        data = np.array((length,), dtype=self.TYPE)
        self.body_length = data["length"]

    def to_bytes(self):
        """Convert the footer to bytes."""
        return np.array((self.body_length,), dtype=self.TYPE).tobytes()


class Header:
    """A field header."""

    TYPE = [("size", np.int32), ("time", np.float32), ("length", np.int32)]
    SIZE = np.dtype(TYPE).itemsize

    def __init__(self, size: int, time: float, length: int):
        self.size = size
        self.time = round(float(time), 7)
        self.body_length = length

        self.field_size = Header.SIZE + 4 * self.body_length + Footer.SIZE

        if not self.size == self.field_size - 8:
            raise ValueError("Invalid header")

    @staticmethod
    def from_bytes(data: bytes):
        """Create a new header from bytes."""
        kwargs = np.frombuffer(data[: Header.SIZE], dtype=Header.TYPE)
        return Header(*kwargs[0].item())

    def to_bytes(self):
        """Convert the header to bytes."""
        return np.array(
            (self.size, self.time, self.body_length), dtype=Header.TYPE
        ).tobytes()

    @staticmethod
    def read(filename: str, compressed: bool = True) -> "Header":
        """Read the header of a binary file."""
        file_open = gzip.open if compressed else open

        with file_open(filename, "rb") as file:
            file.seek(0)
            data = file.read(Header.SIZE)
            return Header.from_bytes(data)


@dataclass
class Position:
    """A field position in a binary file."""

    id: int
    time: float
    chunk_id: int
    chunk_offset: int
    decompressobj: zlib.decompressobj
    chunk_size: int
    field_size: int
    file: IO[bytes]

    @staticmethod
    def _iterate_params(
        file: IO[bytes], position: int, compressed: bool, chunk_size: int
    ):
        if position:
            return (
                position.file,
                position.decompressobj is not None,
                position.chunk_size,
                position.field_size,
                position.id,
                position.chunk_id[0],
                position.chunk_offset[0],
                position.decompressobj.copy() if position.decompressobj else None,
                position.chunk_id[0] * position.chunk_size,
            )

        header = Header.read(file.name, compressed)
        return (file, compressed, chunk_size, header.field_size, 0, 0, 0, None, 0)

    @staticmethod
    def _process_buffer(chunk_buffer: bytes, field_buffer: bytes, field_size: int):
        required_size = field_size - len(field_buffer)
        required_buffer = chunk_buffer[:required_size]
        field_buffer += required_buffer
        chunk_buffer = chunk_buffer[required_size:]
        return field_buffer, chunk_buffer, len(required_buffer)

    @staticmethod
    def iterate(
        file: IO[bytes] = None,
        compressed: bool = True,
        chunk_size: int = Chunk.DEFAULT_SIZE,
        position: "Position" = None,
    ) -> Generator["Position", None, None]:
        """Yield positions of fields in a binary file."""

        # File:   [0100110001110101011010110110000101110011]
        # Chunks: [   0    |   1    |   2    |   3    | 4  ]
        # Fields: [0  |1  |2  |3                   |4  |5  ]

        (
            file,
            compressed,
            chunk_size,
            field_size,
            field_id,
            chunk_id,
            chunk_offset,
            decompressobj,
            offset,
        ) = Position._iterate_params(file, position, compressed, chunk_size)

        field_buffer = b""
        prev_chunk_id = chunk_id
        prev_chunk_offset = chunk_offset

        for chunk in Chunk.iterate(
            file,
            chunk_size=chunk_size,
            compressed=compressed,
            offset=offset,
            decompressobj=decompressobj,
        ):
            chunk_buffer = chunk.data

            if chunk_offset:
                chunk_buffer = chunk_buffer[chunk_offset:]

            while chunk_buffer:
                if len(field_buffer) == 0:
                    decompressobj = chunk.decompressobj
                    prev_chunk_id = chunk_id
                    prev_chunk_offset = chunk_offset

                (field_buffer, chunk_buffer, consumed) = Position._process_buffer(
                    chunk_buffer, field_buffer, field_size
                )
                chunk_offset += consumed

                if len(field_buffer) == field_size:
                    if not (position and position.id == field_id):
                        yield Position(
                            id=field_id,
                            time=Header.from_bytes(field_buffer).time,
                            chunk_id=(prev_chunk_id, chunk_id),
                            chunk_offset=(prev_chunk_offset, chunk_offset),
                            chunk_size=chunk_size,
                            field_size=field_size,
                            decompressobj=decompressobj,
                            file=file,
                        )
                    field_id += 1
                    field_buffer = b""

            chunk_id += 1
            chunk_offset = 0


class Index(List[Position]):
    """An index of fields in a binary file."""

    @staticmethod
    def from_file(
        file: IO[bytes],
        verbose: bool = True,
        chunk_size: int = Chunk.DEFAULT_SIZE,
        compressed: bool = True,
        position: Position = None,
    ):
        """Build an index from a binary file."""
        iterator = Position.iterate(
            file, chunk_size=chunk_size, compressed=compressed, position=position
        )

        if verbose:
            iterator = utils.progress_indicator(
                iterator, description="Indexing", unit="Field"
            )

        return Index(iterator)

    @staticmethod
    def from_filename(
        filename: str,
        verbose: bool = True,
        chunk_size: int = Chunk.DEFAULT_SIZE,
        compressed: bool = True,
    ):
        """Build an index from a binary file."""
        file = open(filename, "rb")
        return Index.from_file(file, verbose, chunk_size, compressed)


class Field(np.ndarray):
    """A field."""

    def __new__(cls, data, time: float, spacing: Tuple[float, float, float]):
        obj = np.asarray(data).view(cls)
        obj.time = time
        obj.spacing = spacing
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

        # pylint: disable=attribute-defined-outside-init
        self.time = getattr(obj, "time", None)
        self.spacing = getattr(obj, "spacing", None)

    @staticmethod
    def from_bytes(data: bytes, shape=None, spacing=None):
        """Create a new time step from bytes."""

        header = Header.from_bytes(data)

        start, end, count = (
            header.SIZE,
            header.field_size,
            header.body_length,
        )

        data = data[start:end]
        data = np.frombuffer(data, count=count, dtype="float32")
        if np.all(np.isclose(data, data.astype("int32"))):
            data = data.astype("int32")

        if shape is not None:
            data = data.reshape(shape)

        return Field(data, time=header.time, spacing=spacing)

    def to_bytes(self):
        """Convert the field to bytes."""
        header = Header(
            size=self.size * self.itemsize + 8,
            time=self.time,
            length=self.size,
        )
        footer = Footer(length=self.size)

        return header.to_bytes() + self.tobytes() + footer.to_bytes()

    @staticmethod
    def dimensions(shape: Tuple[int, int, int]) -> int:
        """Get the number of dimensions of a shape."""
        x, y, _ = shape

        if y == 1:
            if x == 1:
                return 1
            return 2
        return 3

    @staticmethod
    def read(position: Position, shape=None, spacing=None) -> "Field":
        """Read a field from a binary file."""
        file_offset = position.chunk_id[0] * position.chunk_size
        position.file.seek(file_offset)

        decompressobj = (
            position.decompressobj.copy() if position.decompressobj else None
        )

        field_buffer = b""

        while True:
            chunk_data = position.file.read(position.chunk_size)

            if not chunk_data:
                break

            data = decompressobj.decompress(chunk_data) if decompressobj else chunk_data

            if field_buffer == b"":
                field_buffer = data[position.chunk_offset[0] :]
            else:
                field_buffer += data

            if len(field_buffer) >= position.field_size:
                break

        field_data = field_buffer[: position.field_size]

        return Field.from_bytes(field_data, shape=shape, spacing=spacing)

    def to_file(self, file: IO[bytes], geometry: bool = True):
        """Write the field to a binary file.

        Args:
            file (IO[bytes]): Binary file.
            geometry (bool, optional): `True` if geometry should be written, `False`
                otherwise. Defaults to `True`.
        """

        file.write(self.to_bytes())

        if geometry:
            geo_filename, geo_data = geo.build(file.name, self.shape, self.spacing)
            geo.write(geo_filename, geo_data, geo.Type.BASIC)

    def write(
        self,
        filename: str,
        compressed: bool = True,
        geometry: bool = True,
    ):
        """Write the field to a binary file.

        Args:
            filename (str): Filename of the binary file.
            compressed (bool, optional): `True` if file should be compressed, `False`
                otherwise. Defaults to `True`.
            geometry (bool, optional): `True` if geometry should be written, `False`
                otherwise. Defaults to `True`.
        """

        file_open = gzip.open if compressed else open
        with file_open(filename, "wb") as file:
            self.to_file(file, geometry)


class Series(np.ndarray):
    def __new__(cls, fields: List[Field]):
        obj = np.asarray(fields).view(cls)
        obj.times = [field.time for field in fields]
        obj.spacings = [field.spacing for field in fields]
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

        # pylint: disable=attribute-defined-outside-init
        self.times = getattr(obj, "times", None)
        self.spacings = getattr(obj, "spacings", None)

    def iter_field(self):
        """Iterate over fields in the series.

        Yields:
            Field.
        """
        for item, time, spacing in zip(self, self.times, self.spacings):
            yield Field(item, time, spacing)

    def get_field(self, index: int) -> Field:
        """Get a field from the series.

        Args:
            index (int): Index of the field.

        Returns:
            Field.
        """
        return Field(self[index], self.times[index], self.spacings[index])

    def get_series(self, key: Union[int, slice, list]) -> "Series":
        """Get a series of fields.

        Args:
            key (Union[int, slice, list]): Key to list of field IDs, a slice object, or a
                list of field IDs.

        Returns:
            Series of fields.
        """
        if isinstance(key, int):
            return Series([self.get_field(key)])
        if isinstance(key, slice):
            return Series([self.get_field(i) for i in range(*key.indices(len(self)))])
        if isinstance(key, list):
            return Series([self.get_field(i) for i in key])
        raise TypeError("Invalid argument type")

    def write(self, filename: str, compressed: bool = True, geometry: bool = True):
        """Write the series to a binary file.

        Args:
            filename (str): Filename of the binary file.
            compressed (bool, optional): `True` if file should be compressed, `False`
                otherwise. Defaults to `True`.
            geometry (bool, optional): `True` if geometry should be written, `False`
                otherwise. Defaults to `True`.
        """

        file_open = gzip.open if compressed else open
        with file_open(filename, "wb") as file:
            for field in self.iter_field():
                field.to_file(file, geometry)
                geometry = False


class File:
    """A binary file."""

    def __init__(
        self,
        filename: str,
        chunk_size: int = Chunk.DEFAULT_SIZE,
        verbose: bool = True,
    ):
        """Initialize a binary file.

        Args:
            filename (str): File name.
            chunk_size (int, optional): Chunk size in bytes. Defaults to `8388608`
                (8 MiB).
            verbose (bool, optional): Verbose output. Defaults to `True`.

        Raises:
            `FileNotFoundError`: If file is not found.
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        self._filename: str = filename
        self._chunk_size: int = chunk_size
        self._verbose: bool = verbose

        self._file: IO[bytes] = None
        self._compressed: bool = None
        self._created: float = None
        self._modified: float = None
        self._index: Index = None

        self.shape: np.ndarray[(3,), np.int32] = None
        self.spacing: np.ndarray[(3,), np.float32] = None

        try:
            self.find_geometry()
        except (geo.GeometryFileNotFoundError, geo.MultipleGeometryFilesError):
            if self._verbose:
                self._warn("Caution: A geometry file was not found.")

    def __getitem__(self, key: Union[int, slice, list, Callable[[Field], bool]]):
        return self.read(key)

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __iter__(self):
        return self.iterate()

    def _info(self, *args):
        if self._verbose:
            print(*args)

    def _warn(self, *args):
        if self._verbose:
            print(*args, file=sys.stderr)

    def _open_file(self):
        self._file = open(self._filename, "rb")
        self._compressed = utils.is_compressed(self._filename)

    def _close_file(self):
        if self._file:
            self._file.close()
        self._reset()

    def _reset(self):
        self._file = None
        self._compressed = None
        self._created = None
        self._modified = None
        self._index = None

    def _update_timestamps(self):
        self._created = os.path.getctime(self._filename)
        self._modified = os.path.getmtime(self._filename)

    def open(self):
        """Open the file."""
        if not self._file:
            self.create_index()
        return self

    def close(self):
        """Close the file."""
        self._close_file()

    def index(self):
        """Get the index of the file."""
        if self._created != os.path.getctime(self._filename):
            self.create_index()
        elif self._modified != os.path.getmtime(self._filename):
            self.update_index()
        return self._index

    def create_index(self):
        """Create an index of the file."""
        self._close_file()
        self._open_file()
        self._update_timestamps()
        self._index = Index.from_file(
            self._file,
            verbose=self._verbose,
            chunk_size=self._chunk_size,
            compressed=self._compressed,
        )

    def update_index(self):
        """Update the index of the file."""
        self._update_timestamps()
        index = Index.from_file(
            self._file,
            verbose=self._verbose,
            chunk_size=self._chunk_size,
            compressed=self._compressed,
            position=self._index[-1],
        )
        self._index.extend(index)

    def times(self) -> List[float]:
        """Get the times of the fields in the file.

        Returns:
            List of times.
        """
        return [position.time for position in self.index()]

    def set_geometry(
        self, shape: Tuple[int, int, int], spacing: Tuple[float, float, float]
    ):
        """Set the geometry.

        Args:
            shape (Tuple[int, int, int]): Shape of the geometry (z, y, x).
            spacing (Tuple[float, float, float]): Spacing of the geometry (dz, dy, dx) in μm.
        """

        self.shape = np.array(shape)
        self.spacing = np.array(spacing)

        self.print_geometry()

    def read_geometry(self, filename: str, compressed: Optional[bool] = None):
        """Read geometry from a file.

        Args:
            filename (str): Filename of a geometry file.
            compressed (bool, optional): `True` if file is compressed, `False`
                otherwise. Defaults to `None` (auto).
        """
        if compressed is None:
            compressed = utils.is_compressed(filename)

        geometry = geo.read(filename, type=geo.Type.BASIC, compressed=compressed)

        shape = geometry["shape"][::-1]
        spacing = geometry["spacing"][::-1]

        self.set_geometry(shape, spacing)

    def find_geometry(self, compressed: Optional[bool] = None):
        """Find geometry file and read it.

        Args:
            compressed (bool, optional): True if file is compressed, False otherwise.
                Defaults to `None` (auto).

        Raises:
            `GeometryFileNotFoundError`: If no geometry file is found.
            `MultipleGeometryFilesError`: If multiple geometry files are found.
        """
        filename = geo.find(self._filename)

        self.read_geometry(filename, compressed=compressed)

    def print_geometry(self):
        """Get a string representation of the geometry."""

        if self.shape is None or self.spacing is None:
            self._info("Geometry: None")
            return

        dimensions = Field.dimensions(self.shape)
        cells = self.shape
        spacing = 1e4 * np.round(self.spacing.astype(float), 7)
        size = cells * spacing

        self._info(f"Geometry: {dimensions}-Dimensional Grid")
        self._info(f"Grid Size [μm]: {tuple(size)}")
        self._info(f"Grid Shape (Cell Count): {tuple(cells)}")
        self._info(f"Grid Spacing (Cell Size) [μm]: {tuple(spacing)}")

    def iterate(self) -> Generator[Field, None, None]:
        """Iterate over fields in the file.

        Returns:
            A generator of fields.
        """
        for position in self.index():
            yield Field.read(position, shape=self.shape, spacing=self.spacing)

    def read_field(self, field_id: int) -> Field:
        """Read a field from the file.

        Args:
            field_id (int): Field ID.

        Returns:
            Field.
        """
        self.index()

        position = self._index[field_id]
        return Field.read(position, shape=self.shape, spacing=self.spacing)

    def read(
        self, key: Optional[Union[int, slice, list, Callable[[Field], bool]]] = None
    ) -> Series:
        """Read a series of fields from the file.

        Args:
            key (Union[int, slice, list, Callable[[Field], bool]]): Key to list of
            field IDs, a slice object, a list of field IDs, or a function that filters
            fields. Defaults to `None`.

        Returns:
            Series of fields.
        """

        def iterable(iterable):
            if self._verbose:
                return utils.progress_indicator(
                    iterable, description="Reading", unit="Field"
                )
            return iterable

        self.index()

        if key is None:
            fields = list(field for field in iterable(self.iterate()))
        elif isinstance(key, int):
            fields = [self.read_field(key)]
        elif isinstance(key, slice):
            indices = range(*key.indices(len(self._index)))
            fields = [self.read_field(i) for i in iterable(indices)]
        elif isinstance(key, list):
            fields = [self.read_field(i) for i in iterable(key)]
        elif isinstance(key, Callable):
            fields = [field for field in iterable(self.iterate()) if key(field)]
        else:
            raise TypeError("Invalid argument type")
        return Series(fields)


@dataclass
class PlotArgs:
    """Arguments for plotting a field.

    Args:
        title (str, optional): Title of the plot. Defaults to `None`.
        xlabel (str, optional): Label of the x-axis. Defaults to `None`.
        ylabel (str, optional): Label of the y-axis. Defaults to `None`.
        figsize (Tuple[float, float], optional): Figure size. Defaults to `None`.
        dpi (int, optional): Figure DPI. Defaults to `None`.
        aspect (str, optional): Aspect ratio. Defaults to `equal`.
        ax (matplotlib.Axes, optional): Axes of the plot. Defaults to `None`.
        cax (matplotlib.Axes, optional): Axes of the color bar. Defaults to `None`.
        vmin (float, optional): Minimum value of the color bar. Defaults to `None`.
        vmax (float, optional): Maximum value of the color bar. Defaults to `None`.
        cmap (str, optional): Colormap. Defaults to `micpy`.
        alpha (float, optional): Transparency of the plot. Defaults to `1.0`.
        interpolation (str, optional): Interpolation method. Defaults to `none`.
    """

    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    figsize: Optional[Tuple[float, float]] = None
    dpi: Optional[int] = None
    aspect: str = "equal"
    ax: "matplotlib.Axes" = None
    cax: "matplotlib.Axes" = None
    vmin: Optional[float] = None
    vmax: Optional[float] = None
    cmap: str = "micpy"
    alpha: float = 1.0
    interpolation: str = "none"


def plot(
    field: Field,
    axis: str = "y",
    index: int = 0,
    args: Optional[PlotArgs] = None,
) -> Tuple["matplotlib.Figure", "matplotlib.Axes"]:
    """Plot a slice of the field.

    Args:
        field (Field): Field to plot.
        axis (str, optional): Axis to plot. Possible values are `x`, `y`, and `z`.
            Defaults to `y`.
        index (int, optional): Index of the slice. Defaults to `0`.
        args (PlotArgs, optional): Arguments for plotting. Defaults to `None`.

    Returns:
        Matplotlib figure, axes, and color bar.
    """

    if matplotlib is None:
        raise ImportError("matplotlib is not installed")

    if axis not in ["x", "y", "z"]:
        raise ValueError("Invalid axis")

    if field.ndim != 3:
        raise ValueError("Invalid field shape")

    if args is None:
        args = PlotArgs()

    if axis == "z":
        x, y = "x", "y"
        slice_2d = field[index, :, :]
    elif axis == "y":
        x, y = "x", "z"
        slice_2d = field[:, index, :]
    elif axis == "x":
        x, y = "y", "z"
        slice_2d = field[:, :, index]

    fig, ax = (
        pyplot.subplots(figsize=args.figsize, dpi=args.dpi)
        if args.ax is None
        else (args.ax.get_figure(), args.ax)
    )

    if args.title is not None:
        ax.set_title(args.title)
    else:
        if isinstance(field, Field):
            ax.set_title(f"t={np.round(field.time, 7)}s")
    if args.xlabel is not None:
        ax.set_xlabel(args.xlabel)
    else:
        ax.set_xlabel(x)
    if args.ylabel is not None:
        ax.set_ylabel(args.ylabel)
    else:
        ax.set_ylabel(y)
    if args.aspect is not None:
        ax.set_aspect(args.aspect)
    ax.set_frame_on(False)

    image = ax.imshow(
        slice_2d,
        cmap=args.cmap,
        vmin=args.vmin,
        vmax=args.vmax,
        interpolation=args.interpolation,
        alpha=args.alpha,
        origin="lower",
    )

    bar = pyplot.colorbar(image, ax=ax, cax=args.cax)
    bar.locator = matplotlib.ticker.MaxNLocator(
        integer=np.issubdtype(slice_2d.dtype, np.integer)
    )
    bar.outline.set_visible(False)
    bar.update_ticks()

    return fig, ax, bar
