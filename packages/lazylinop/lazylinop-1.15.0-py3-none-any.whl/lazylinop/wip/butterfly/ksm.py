# -*- coding: utf-8 -*-

from lazylinop import LazyLinOp
import numpy as np
from pathlib import Path
import warnings
try:
    import pyopencl as cl
    found_pyopencl = True
except ModuleNotFoundError:
    cl = None
    found_pyopencl = False
    warnings.warn("pyopencl not found.")
try:
    import pycuda.driver as cuda
    import pycuda.autoinit
    from pycuda.compiler import SourceModule
    found_pycuda = True
except:  # ImportError:
    cuda = None
    SourceModule = None
    found_pycuda = False
    warnings.warn("pycuda not found.")
from scipy.sparse import csr_matrix
try:
    import numba as nb
    from numba import njit
except ImportError:
    def njit(f):
        return f
    # def njit(*args, **kwargs):
    #     def dummy(f):
    #         return f
    #     return dummy


def _get_all_platforms() -> list:
    """
    Print all platforms and devices.
    """
    platforms = cl.get_platforms()
    print("List of platforms and devices.")
    tmp = []
    for i, p in enumerate(platforms):
        devices = p.get_devices()
        for d in devices:
            print(i, p.get_info(cl.platform_info.NAME), d)
            print(" ", p.get_info(cl.platform_info.EXTENSIONS))
            tmp.append((p, d))
    return tmp


def _get_platform(platform_name: str, device: str = 'cpu'):
    """
    Return platform and device specified by arguments.

    Args:
        platform_name: ``str``
            Run ``get_all_platforms()`` to list all
            the available platforms and devices.
        device_type: ``str``, optional
            Device type, ``'cpu'`` (default) or ``'gpu'``.

    Returns:
        ``pyopencl.Device``
    """
    platform, device = None, None
    platforms = cl.get_platforms()
    for p in platforms:
        if p.get_info(cl.platform_info.NAME) != platform_name:
            continue
        if device == 'gpu':
            devices = p.get_devices(device_type=cl.device_type.GPU)
        else:
            devices = p.get_devices(device_type=cl.device_type.CPU)
        for d in devices:
            # print('selection', p, d)
            return d
    return platform, device


def _check_hyper_parameters(hp, a: int, b: int, c: int, d: int,
                            batch_size: int, smem: int, nbytes: int) -> bool:
    """
    Check if the given hyper-parameters satisfy the kernel assertions.

    Args:
        hp:
            Tuple of hyper-parameters
            ``(TILEX, TILEK, TILEY, TX, TY, VSIZE)``.
        a, b, c, d: ``int``, ``int``, ``int``, ``int``
            Pattern of the Kronecker-Sparse factor.
        batch_size: ``int``
            Size of the batch ``x.shape[1]`` in ``L @ x``.
        smem: ``int``
            Size of shared memory of your hardware.
        nbytes: ``int``
            Number of bytes of the elements of the
            Kronecker-Sparse factor.

    Returns:
        ``bool``
    """
    n_rows = a * b * d
    n_cols = a * c * d
    tile_x, tile_k, tile_y = hp[0], hp[1], hp[2]
    if tile_k > n_cols or tile_k > c:
        return False
    if tile_y > n_rows or tile_y > b:
        return False
    if batch_size > 0 and (tile_x > batch_size or
                           batch_size % tile_x != 0):
        return False
    if (nbytes * (2 * (tile_y * tile_k + tile_k * tile_x)
                  + tile_y * tile_x)) >= smem:
        return False
    x, y = hp[0] // hp[3], hp[2] // hp[4]
    strideInput = (hp[5] * x * y) / hp[0]
    if (hp[5] * x * y) % hp[0] != 0:
        return False
    strideValues = (hp[5] * x * y) / hp[1]
    if (hp[5] * x * y) % hp[1] != 0:
        return False
    if hp[1] > hp[0] or hp[1] > hp[2]:
        return False
    if (b * d) % (d * hp[2]) != 0:
        return False
    if hp[1] % strideInput != 0:
        return False
    if hp[2] % strideValues != 0:
        return False
    return True


@njit
def _find_hyper_parameters(a, b, c, d, batch_size: int = 0,
                           smem: int = 163000, nbytes: int = 8) -> tuple:
    """
    Nested loops over tile size to find one possible set
    of hyper-parameters for a given pattern.

    Args:
        a, b, c, d: ``int``, ``int``, ``int``, ``int``
            Pattern of the Kronecker-Sparse factor.
        batch_size: ``int``, optional
            Size of the batch ``x.shape[1]`` in ``L @ x``.
            Default value is 0 (skip batch size condition).
        smem: ``int``
            Size of shared memory of your hardware.
            Default size is 163000 bytes.
        nbytes: ``int``
            Number of bytes of the elements of the
            Kronecker-Sparse factor.
            Default value is 8.

    Returns:
        Tuple of hyper-parameters
        ``(TILEX, TILEK, TILEY, TX, TY, VSIZE)``.
    """
    n_rows = a * b * d
    n_cols = a * c * d
    hp = (0, 0, 0, 0, 0, 0)
    tmp = 16
    for vsize in range(4, 0, -1):
        for x in range(tmp, 0, -1):
            for tx in range(16, vsize - 1, -1):
                tile_x = x * tx
                if batch_size > 0 and (tile_x > batch_size or
                                       batch_size % tile_x != 0):
                    continue
                for k in range(16, 0, -1):
                    tile_k = k * vsize
                    if tile_k > n_cols or tile_k > c:
                        continue
                    if tile_k > tile_x:
                        continue
                    for y in range(tmp, 0, -1):
                        strideInput = (vsize * x * y) / tile_x
                        if (vsize * x * y) % tile_x != 0:
                            continue
                        if tile_k % strideInput != 0:
                            continue
                        strideValues = (vsize * x * y) / tile_k
                        if (vsize * x * y) % tile_k != 0:
                            continue
                        for ty in range(16, vsize - 1, -1):
                            tile_y = y * ty
                            if (nbytes * (2 * (tile_y * tile_k
                                               + tile_k * tile_x)
                                          + tile_y * tile_x)) >= smem:
                                continue
                            if tile_y > n_rows or tile_y > b:
                                continue
                            if tile_y % strideValues != 0:
                                continue
                            if tile_k > tile_y:
                                continue
                            if (b * d) % (d * tile_y) != 0:
                                continue
                            return (tile_x, tile_k, tile_y, tx, ty, vsize)
    return hp


@njit
def _find_all_hyper_parameters(a, b, c, d, batch_size: int = 0,
                               smem: int = 163000, nbytes: int = 8) -> list:
    """
    Nested loops over tile size to find all the possible sets
    of hyper-parameters for a given pattern.

    Args:
        a, b, c, d: ``int``, ``int``, ``int``, ``int``
            Pattern of the Kronecker-Sparse factor.
        batch_size: ``int``, optional
            Size of the batch ``x.shape[1]`` in ``L @ x``.
            Default value is 0 (skip batch size condition).
        smem: ``int``
            Size of shared memory of your hardware.
            Default size is 163000 bytes.
        nbytes: ``int``
            Number of bytes of the elements of the
            Kronecker-Sparse factor.
            Default value is 8.

    Returns:
        Tuple of hyper-parameters
        ``(TILEX, TILEK, TILEY, TX, TY, VSIZE)``.
    """
    n_rows = a * b * d
    n_cols = a * c * d
    hp = []
    tmp = 64
    for vsize in range(4, 0, -1):
        for x in range(tmp, 0, -1):
            for tx in range(16, vsize - 1, -1):
                tile_x = x * tx
                if batch_size > 0 and (tile_x > batch_size or
                                       batch_size % tile_x != 0):
                    continue
                for k in range(16, 0, -1):
                    tile_k = k * vsize
                    if tile_k > n_cols or tile_k > c:
                        continue
                    if tile_k > tile_x:
                        continue
                    for y in range(tmp, 0, -1):
                        strideInput = (vsize * x * y) / tile_x
                        if (vsize * x * y) % tile_x != 0:
                            continue
                        if tile_k % strideInput != 0:
                            continue
                        strideValues = (vsize * x * y) / tile_k
                        if (vsize * x * y) % tile_k != 0:
                            continue
                        for ty in range(16, vsize - 1, -1):
                            tile_y = y * ty
                            if (nbytes * (2 * (tile_y * tile_k
                                               + tile_k * tile_x)
                                          + tile_y * tile_x)) >= smem:
                                continue
                            if tile_y > n_rows or tile_y > b:
                                continue
                            if tile_y % strideValues != 0:
                                continue
                            if tile_k > tile_y:
                                continue
                            if (b * d) % (d * tile_y) != 0:
                                continue
                            hp.append((tile_x, tile_k, tile_y, tx, ty, vsize))
    return hp


def _modify_template(a: int, b: int, c: int, d: int, batch_size: int = 0,
                     smem: int = 163000,
                     params: tuple = (None, None),
                     dtype: np.dtype = np.float32, ext: str = 'clh'):
    r"""
    Add explicit values of the hyper-parameters to the kernel.

    Args:
        a, b, c, d: ``int``, ``int``, ``int``, ``int``
            Pattern of the Kronecker-Sparse factor.
        batch_size: ``int``, optional
            Size of the batch ``x.shape[1]`` in ``L @ x``.
            Default value is 0 (skip batch size condition).
        smem: ``int``
            Size of shared memory of your hardware.
            Default size is 163000 bytes.
        params: ``tuple``, optional
            ``params[0]`` and ``params[1]`` expect a tuple of six elements
            ``(TILEX, TILEK, TILEY, TX, TY, VSIZE)`` (see ref.[1]
            for more details).
            If ``(None, None)`` (default), the choice of
            hyper-parameters for multiplication ``L @ X`` and the
            multiplication ``L.H @ X`` is automatic.
            Because we did not run a fine-tuning for all the
            possible $\left(a,~b,~c,~d\right)$ and $\left(a,~c,~b,~d\right)$
            tuples, automatic does not always correspond to the best choice.
        dtype: ``np.dtype``, optional
            dtype of the Kronecker-Sparse factor.
        ext: ``str``, optional

            - ``'clh'`` uses OpenCL kernel template.
            - ``'cuh'`` uses CUDA kernel template.

    References:
        [1] Fast inference with Kronecker-sparse matrices.
        Antoine Gonon and L\0xA9 on Zheng and Pascal Carrivain and Quoc-Tung Le
        https://arxiv.org/abs/2405.15013
    """
    for f in ["ksmm", "rksmm"]:
        with open(
                Path(__file__).parent.joinpath(
                    f"kernels/{f}.{ext}"), 'w') as out_file:
            with open(
                    Path(__file__).parent.joinpath(
                        f"kernels/template_ksmm.{ext}"), 'r') as in_file:
                if f == 'ksmm':
                    if params[0] is None:
                        hp = _find_hyper_parameters(a, b, c, d, batch_size,
                                                    smem=smem,
                                                    nbytes=dtype.itemsize)
                        if hp == tuple([0] * 6):
                            raise Exception("matmat: Did not find" +
                                            " hyper-parameters.")
                    else:
                        if len(params[0]) != 6:
                            raise Exception(
                                "matmat: hyper-parameters must be "
                                + "a tuple of six elements.")
                        else:
                            hp = params[0]
                            if not _check_hyper_parameters(
                                    hp, a, b, c, d,
                                    batch_size,
                                    smem=smem, nbytes=dtype.itemsize):
                                raise Exception(
                                    "matmat: hyper-parameters do not" +
                                    " satisfy the kernel assertions.")
                else:
                    if params[1] is None:
                        rhp = _find_hyper_parameters(a, c, b, d, batch_size,
                                                     smem=smem,
                                                     nbytes=dtype.itemsize)
                        if rhp == tuple([0] * 6):
                            raise Exception("rmatmat: Did not find"
                                            + " hyper-parameters.")
                    else:
                        if len(params[1]) != 6:
                            raise Exception(
                                "rmatmat: hyper-parameters must be "
                                + "a tuple of six elements.")
                        else:
                            rhp = params[1]
                            if not _check_hyper_parameters(
                                    rhp, a, c, b, d,
                                    batch_size,
                                    smem=smem, nbytes=dtype.itemsize):
                                raise Exception(
                                    "rmatmat: hyper-parameters do not" +
                                    " satisfy the kernel assertions.")

                p = hp if f == "ksmm" else rhp

                # Number of threads.
                nthreads = (p[0] // p[3]) * (p[2] // p[4])
                # Define floating point precision.
                if 'float16' in str(dtype):
                    out_file.write("#define USE_FLOAT16\n")
                elif 'float32' in str(dtype):
                    out_file.write("#define USE_FLOAT32\n")
                elif 'float64' in str(dtype):
                    out_file.write("#define USE_FLOAT64\n")
                elif 'complex64' in str(dtype):
                    out_file.write("#define USE_CFLOAT32\n")
                elif 'complex128' in str(dtype):
                    out_file.write("#define USE_CFLOAT64\n")
                else:
                    pass
                # vloadn and vstoren depend on the values of b and c.
                out_file.write("#define V" + str(p[5]) + "\n")
                out_file.write("#define xTILEXx " + str(p[0]) + "\n")
                out_file.write("#define xTILEKx " + str(p[1]) + "\n")
                out_file.write("#define xTILEYx " + str(p[2]) + "\n")
                out_file.write("#define xTXx " + str(p[3]) + "\n")
                out_file.write("#define xTYx " + str(p[4]) + "\n")
                out_file.write(
                    "#define xNTHREADSx " + str(nthreads) + "\n\n")
                lines = in_file.readlines()
                for line in lines:
                    out_file.write(line)

    return hp, rhp


class Ksm_data():
    """
    This class keeps track of the last batch size.
    """
    def __init__(self, batch_size: int = None):
        self.batch_size = batch_size
        self.hp = None
        self.rhp = None
        self.program = None
        self.rprogram = None
        self.d_values = None
        self.d_rvalues = None


def ksm(ks_values: np.ndarray,
        params: tuple = (None, None),
        backend: str = 'opencl-cpu'):
    r"""
    Returns a :class:`.LazyLinOp` ``L`` for the
    Kronecker Sparse Matrix Multiplication (KSMM).
    The sparsity pattern (or support) of a Kronecker-Sparse factor
    is defined as $I_a\otimes 1_{b,c}\otimes I_d$
    while its values are given by a 4D ``np.ndarray``
    of shape ``(a, b, c, d)``.

   The shape of ``L`` is $\left(abd,~acd\right)$.

    :octicon:`megaphone;1em;sd-text-danger` The product ``L @ X`` only
    works for input ``X`` of type ``'float16'``, ``'float32'``,
    ``'float64'``, ``'complex64'`` or ``'complex128'``.
    The ``dtype`` of ``X`` must match that of ``ks_values``.
    Convert it to ``dtype=ks_values.dtype`` otherwise.

    The current ``cpu`` implementation of a ``ksm`` relies on OpenCL.

    The current ``gpu`` implementation of a ``ksm`` relies on
    both CUDA and OpenCL.

    To fill a ``ks_values`` and its Kronecker-Sparse factor ``M``:

    .. code-block:: python3

        M = np.zeros((a * b * d, a * c * d), dtype=np.float32)
        ks_values = np.empty((a, b, c, d), dtype=M.dtype)
        for i in range(a):
            for j in range(b):
                for k in range(c):
                    for l in range(d):
                        tmp = np.random.randn()
                        ks_values[i, j, k, l] = tmp
                        M[i * b * d + j * d + l,
                          i * c * d + k * d + l] = tmp

    Args:
        ks_values: ``np.ndarray``
            List of values of the Kronecker-Sparse factor.
            ``ks_values`` expects a 4D ``np.ndarray``.
        params: ``tuple``, optional
            ``params[0]`` and ``params[1]`` expect a tuple of six elements
            ``(TILEX, TILEK, TILEY, TX, TY, VSIZE)`` (see ref.[1]
            for more details).
            If ``(None, None)`` (default), the choice of
            hyper-parameters for multiplication ``L @ X`` and the
            multiplication ``L.H @ X`` is automatic.
            Because we did not run a fine-tuning for all the
            possible $\left(a,~b,~c,~d\right)$ and $\left(a,~c,~b,~d\right)$
            tuples, automatic does not always correspond to the best choice.

            List of assertions the tuple
            ``(TILEX, TILEK, TILEY, TX, TY, VSIZE)`` must satisfy:

            - ``TILEX = X * TX``
            - ``TILEY = Y * TY``
            - ``batch size % TILEX == 0`` for performance reason.
            - ``TILEK > c``
            - ``TILEX > TILEK and TILEY > TILEK``
            - ``(VSIZE * X * Y) % TILEX == 0``
            - ``TILEK % strideInput == 0``
            - ``(VSIZE * X * Y) % TILEK == 0``
            - ``TILEY % strideValues == 0``
            - ``TILEY > b``
            - `` (b * d) % (d * TILEY) == 0``
            - ``ks_values.dtype.itemsize * (2 * (TILEY * TILEK + TILEK * TILEX) + TILEY * TILEX) < smem``

            where ``smem`` is the shared memory of the hardware used to compute,
            ``VSIZE`` ranges from $1$ to $4$, ``strideValues = VSIZE * X * Y / TILEK``
            and ``strideInput = VSIZE * X * Y / TILEX``.

         backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            Paramaters passed to determine the device
            and detailed implementation.

            - ``'opencl-cpu'`` use the first platform and CPU device
              returned by PyOpenCL (default).
            - ``'opencl-gpu'`` use the first platform and GPU device
              returned by PyOpenCL.
            - ``'cuda-gpu'`` use device id=0.
            - ``'lazylinop'`` (wip).
            - ``'scipy'`` use ``scipy.sparse.block_diag``
              and ``scipy.sparse.csr_matrix`` to compute ``L @ x``.
            - ``(cl.Platform, cl.Device)`` a tuple of OpenCL platform
              and device.
            - ``pycuda.driver.Device`` a CUDA device.

    Examples:
        >>> from lazylinop.wip.butterfly.ksm import ksm
        >>> import numpy as np
        >>> a, b, c, d = 2, 4, 4, 2
        >>> ks_values = np.full((a, b, c, d), 1.0, dtype=np.float32)
        >>> L = ksm(ks_values)
        >>> L.toarray()
        array([[1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
               [0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
               [1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
               [0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
               [1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
               [0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
               [1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
               [0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1., 0.],
               [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1.],
               [0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1., 0.],
               [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1.],
               [0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1., 0.],
               [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1.],
               [0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1., 0.],
               [0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1., 0., 1., 0., 1.]],
              dtype=float32)

    References:
        [1] Fast inference with Kronecker-sparse matrices.
        Antoine Gonon and L\0xA9 on Zheng and Pascal Carrivain and Quoc-Tung Le
        https://arxiv.org/abs/2405.15013
    """

    # Ask for CUDA backend but pyCUDA is not installed.
    if cuda is None and 'cuda' in backend:
        warnings.warn("pyCUDA is not installed, switch to 'scipy' backend.")
        backend = 'scipy'
    elif cl is None and 'cl' in backend:
        warnings.warn("pyOpenCL is not installed, switch to 'scipy' backend.")
        backend = 'scipy'

    if ks_values.ndim != 4:
        raise Exception("ks_values must be a 4D NumPy array.")
    if ks_values.dtype != np.float16 and ks_values.dtype != np.float32 and \
       ks_values.dtype != np.float64 and \
       ks_values.dtype != np.complex64 and ks_values.dtype != np.complex128:
        raise TypeError("dtype of ks_values must be either np.float16,"
                        + " np.float32, np.float64,"
                        + " np.complex64 or np.complex128.")

    if isinstance(backend, str):
        if backend == 'opencl-cpu' or backend == 'opencl-gpu':
            return _ksm(ks_values, params, backend)
        elif backend == 'cuda-gpu':
            return _ksm(ks_values, params, backend)
        elif 'lazylinop' in backend:
            return _ksm_lazylinop(ks_values)
        elif 'scipy' in backend:
            return _ksm_scipy(ks_values)
        else:
            raise ValueError("backend must be either 'opencl-cpu'," +
                             " 'opencl-gpu', 'cuda-gpu'." +
                             " 'lazylinop' or 'scipy'.")
    elif (
            isinstance(backend, tuple) and
            len(backend) == 2 and
            isinstance(backend[0], cl.Platform) and
            isinstance(backend[1], cl.Device)
    ):
        return _ksm(ks_values, params, backend)
    elif isinstance(backend, cuda.Device):
        return _ksm(ks_values, params, backend)
    else:
        raise Exception("No backend found.")


def _context(backend):
    """
    Return either PyOpenCL, PyCUDA context or ``None`` if ``backend='scipy'``.

    Args:
        backend: ``str``, ``tuple[cl.Platform, cl.Device]`` or ``pycuda.driver.Device``

    Returns:
        ``cl.Context``, ``pycuda.driver.Context`` or ``None`` if ``backend='scipy'``.
    """
    context = None
    # OpenCL variables declaration.
    if isinstance(backend, tuple) and len(backend) == 2 and \
       isinstance(backend[0], cl.Platform) and \
       isinstance(backend[1], cl.Device):
        context = cl.Context(devices=[backend[1]])
    elif isinstance(backend, str) and 'opencl' in backend:
        platforms = cl.get_platforms()
        context, ndevices = None, 0
        for platform in platforms:
            if 'gpu' in backend:
                devices = platform.get_devices(
                    device_type=cl.device_type.GPU)
            else:
                devices = platform.get_devices(
                    device_type=cl.device_type.CPU)
            ndevices += len(devices)
            if len(devices) == 0:
                continue
            name = platform.get_info(cl.platform_info.NAME)
            if 'gpu' in backend:
                context = cl.Context(devices=[devices[0]])
                break
            else:
                if 'Portable Computing Language' in name or \
                   'AMD Accelerated Parallel Processing' in name or \
                   'OpenCL' in name:
                    context = cl.Context(devices=[devices[0]])
                    break
        if context is None:
            raise Exception("No context found.")
        if ndevices == 0:
            raise Exception("No device found.")
    elif cuda is not None and isinstance(backend, cuda.Device):
        context = backend.make_context()
    elif isinstance(backend, str) and 'cuda' in backend:
        cuda.init()
        for i in range(10):
            try:
                context = cuda.Device(i).make_context()
                break
            except pycuda._driver.LogicError:
                break
    elif backend == 'scipy':
        context = None
    else:
        raise Exception("backend not found.")
    return context


def _read_kernel(name: str):
    """
    Read and return both ``matmat`` and ``rmatmat`` kernels.

    Args:
        name: ``str``
            Name of the kernel.
    """
    with open(
            Path(__file__).parent.joinpath(
                f"kernels/{name}"), 'r') as in_file:
        kernels = ''.join(in_file.readlines())
    with open(
            Path(__file__).parent.joinpath(
                f"kernels/r{name}"), 'r') as in_file:
        rkernels = ''.join(in_file.readlines())
    return kernels, rkernels


def _ksm(ks_values: np.ndarray,
         params: tuple = (None, None),
         backend='opencl-cpu'):
    """
    pyopencl and pycuda versions of ``ksm()``.
    """

    context = _context(backend)
    is_opencl = isinstance(context, cl.Context)

    # Use this instance to keep track of the last batch size.
    # If batch size changes, we need to compute new hyper-parameters.
    ksm_data = Ksm_data()

    if is_opencl:
        # Create command queue
        queue = cl.CommandQueue(
            context,
            properties=cl.command_queue_properties.PROFILING_ENABLE)

    # Transform ks_values from 4D to 2d array once and for all.
    a, b, c, d = ks_values.shape
    values = np.ascontiguousarray(
        np.swapaxes(ks_values, 2, 3).reshape(a * d * b, c))
    # Host to device.
    if is_opencl:
        d_values = cl.Buffer(
            context,
            cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
            hostbuf=values)
    else:
        d_values = cuda.mem_alloc(values.nbytes)
        cuda.memcpy_htod(d_values, values)

    # Transform acbd from 4D to 2d array once and for all.
    # The transpose of the support Id_{a,a}\otimes 1_{b,c}\otimes Id_{d,d}
    # is given by Id_{a,a}\otimes 1_{c,b}\otimes Id_{d,d}.
    acbd = np.swapaxes(ks_values, 1, 2)
    rvalues = np.ascontiguousarray(
        np.swapaxes(acbd, 2, 3).reshape(a * d * c, b))
    # Host to device.
    if is_opencl:
        d_rvalues = cl.Buffer(
            context,
            cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
            hostbuf=rvalues)
    else:
        d_rvalues = cuda.mem_alloc(rvalues.nbytes)
        cuda.memcpy_htod(d_rvalues, rvalues)

    def _kx(x, a, b, c, d, buf_val, context, adjoint):

        if ksm_data.batch_size is None or ksm_data.batch_size != x.shape[1]:
            # Because of new batch size ...
            if is_opencl:
                smem = context.devices[0].get_info(cl.device_info.LOCAL_MEM_SIZE)
            else:
                smem = context.get_device().get_attribute(
                    pycuda._driver.device_attribute.MAX_SHARED_MEMORY_PER_BLOCK)
            hp, rhp = _modify_template(
                a, b, c, d, x.shape[1],
                smem, params, ks_values.dtype, 'clh' if is_opencl else 'cuh')

            ksm_data.batch_size = x.shape[1]

            if is_opencl:
                # Read kernel from source file.
                kernel, rkernel = _read_kernel("ksmm.clh")
                # Compile kernel
                program = cl.Program(context, kernel).build()
                rprogram = cl.Program(context, rkernel).build()
            else:
                # Read kernel from source file.
                kernel, rkernel = _read_kernel("ksmm.cuh")
                # Compile kernel.
                # Because of overloading function no_extern_c=True.
                # Use extern "C" { __global__ void ksmm(...) {...} }.
                program = SourceModule(kernel, no_extern_c=True)
                rprogram = SourceModule(rkernel, no_extern_c=True)
            ksm_data.hp = hp
            ksm_data.rhp = rhp
            ksm_data.program = program
            ksm_data.rprogram = rprogram
            ksm_data.d_values = d_values
            ksm_data.d_rvalues = d_rvalues
        else:
            hp = ksm_data.hp
            rhp = ksm_data.rhp
            program = ksm_data.program
            rprogram = ksm_data.rprogram

        if ks_values.dtype != x.dtype:
            x = x.astype(ks_values.dtype)
            # raise TypeError("dtype of x must 'float32' or 'float64'.")

        batch_size = x.shape[1]

        # Define the grid.
        if adjoint:
            output_size = a * c * d
            rntx, rnty = rhp[0] // rhp[3], rhp[2] // rhp[4]
        else:
            output_size = a * b * d
            ntx, nty = hp[0] // hp[3], hp[2] // hp[4]
        if is_opencl:
            if adjoint:
                local_work_size = (rntx, rnty)
                global_work_size = (((batch_size + rhp[0] - 1) // rhp[0]) * rntx,
                                    ((output_size + rhp[2] - 1) // rhp[2]) * rnty)
            else:
                local_work_size = (ntx, nty)
                global_work_size = (((batch_size + hp[0] - 1) // hp[0]) * ntx,
                                    ((output_size + hp[2] - 1) // hp[2]) * nty)
        else:
            # Define the grid.
            if adjoint:
                block = (rntx, rnty, 1)
                grid = ((batch_size + rhp[0] - 1) // rhp[0],
                        (output_size + rhp[2] - 1) // rhp[2], 1)
            else:
                block = (ntx, nty, 1)
                grid = ((batch_size + hp[0] - 1) // hp[0],
                        (output_size + hp[2] - 1) // hp[2], 1)

        # The kernel computes K @ X where the input K and X
        # are in row-major format.
        # The output y of the computation is in row-major format.
        # Host to device.
        y = np.empty((output_size, batch_size), dtype=ks_values.dtype)
        if is_opencl:
            d_x = cl.Buffer(
                context,
                cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                hostbuf=x
            )
            d_y = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, y.nbytes)
            # d_y = cl.Buffer(context,
            #                 cl.mem_flags.WRITE_ONLY | cl.mem_flags.COPY_HOST_PTR,
            #                 hostbuf=y)
        else:
            d_x = cuda.mem_alloc(x.nbytes)
            cuda.memcpy_htod(d_x, x)
            d_y = cuda.mem_alloc(y.nbytes)
        # Run the kernel.
        bb = np.int32(c) if adjoint else np.int32(b)
        cc = np.int32(b) if adjoint else np.int32(c)
        if is_opencl:
            knl = rprogram.ksmm if adjoint else program.ksmm
            knl.set_args(buf_val, d_x, d_y,
                         np.int32(a), bb, cc, np.int32(d),
                         np.int32(batch_size))
            event = cl.enqueue_nd_range_kernel(
                queue, knl, global_work_size, local_work_size)
            event.wait()
            complete = cl.command_execution_status.COMPLETE
            if event.command_execution_status != complete:
                raise Exception("OpenCL command execution status is not complete.")
            d_x.release()
        else:
            knl = (rprogram if adjoint else program).get_function('ksmm')
            knl(buf_val, d_x, d_y,
                np.int32(a), bb, cc, np.int32(d),
                np.int32(batch_size), block=block, grid=grid)
            context.synchronize()
            d_x.free()
        # print(f"elapsed={1e-9 * (event.profile.end - event.profile.start)}")
        # Get the output.
        if is_opencl:
            event = cl.enqueue_copy(queue, y, d_y)
            event.wait()
            complete = cl.command_execution_status.COMPLETE
            if event.command_execution_status != complete:
                raise Exception("OpenCL command execution status is not complete.")
            d_y.release()
        else:
            cuda.memcpy_dtoh(y, d_y)
            context.synchronize()
            d_y.free()
        return y

    L = LazyLinOp(
        shape=(a * b * d, a * c * d),
        matmat=lambda x: _kx(x, a, b, c, d, d_values, context, False),
        rmatmat=lambda x: _kx(x, a, b, c, d, d_rvalues, context, True)
    )

    L.context = context

    return L


def multiple_ksm(ks_values: list,
                 params: list = None, backend: str = 'opencl-cpu'):
    r"""
    Returns a :class:`.LazyLinOp` ``L`` for the
    Kronecker Sparse Matrix Multiplication (KSMM).
    The sparsity pattern (or support) of a Kronecker-Sparse factor
    is defined as $I_a\otimes 1_{b,c}\otimes I_d$
    while its values are given by a 4D ``np.ndarray``
    of shape ``(a, b, c, d)``.

   The shape of ``L`` is $\left(abd,~acd\right)$.

    :octicon:`megaphone;1em;sd-text-danger` The product ``L @ X`` only
    works for input ``X`` of type ``'float16'``, ``'float32'``,
    ``'float64'``, ``'complex64'`` or ``'complex128'``.
    The ``dtype`` of ``X`` must match that of ``ks_values``.
    Convert it to ``dtype=ks_values.dtype`` otherwise.

    The current ``cpu`` implementation of a ``ksm`` relies on OpenCL.

    The current ``gpu`` implementation of a ``ksm`` relies on
    both CUDA and OpenCL.

    Args:
        ks_values: ``list`` of ``np.ndarray``
            List of values of the Kronecker-Sparse factors.
            Each element of the list ``ks_values`` expects
            a 4D ``np.ndarray``.
            The length of the list corresponds to the number
            of Kronecker-Sparse factors.
        params: ``list`` of ``tuple``, optional
            List of tuple of length the number of factors.
            ``params[i][0]`` and ``params[i][1]`` expect a tuple
            of six elements ``(TILEX, TILEK, TILEY, TX, TY, VSIZE)``
            (see ref.[1] for more details).
            If ``None`` (default), the choice of
            hyper-parameters for multiplication ``L @ X`` and the
            multiplication ``L.H @ X`` is automatic.
            Because we did not run a fine-tuning for all the
            possible $\left(a,~b,~c,~d\right)$ and $\left(a,~c,~b,~d\right)$
            tuples, automatic does not always correspond to the best choice.

            List of assertions the tuple
            ``(TILEX, TILEK, TILEY, TX, TY, VSIZE)`` must satisfy:

            - ``TILEX = X * TX``
            - ``TILEY = Y * TY``
            - ``batch size % TILEX == 0`` for performance reason.
            - ``TILEK > c``
            - ``TILEX > TILEK and TILEY > TILEK``
            - ``(VSIZE * X * Y) % TILEX == 0``
            - ``TILEK % strideInput == 0``
            - ``(VSIZE * X * Y) % TILEK == 0``
            - ``TILEY % strideValues == 0``
            - ``TILEY > b``
            - `` (b * d) % (d * TILEY) == 0``
            - ``ks_values.dtype.itemsize * (2 * (TILEY * TILEK + TILEK * TILEX) + TILEY * TILEX) < smem``

            where ``smem`` is the shared memory of the hardware used to compute,
            ``VSIZE`` ranges from $1$ to $4$, ``strideValues = VSIZE * X * Y / TILEK``
            and ``strideInput = VSIZE * X * Y / TILEX``.

         backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            Paramaters passed to determine the device
            and detailed implementation.

            - ``'opencl-cpu'`` use the first platform and CPU device
              returned by PyOpenCL (default).
            - ``'opencl-gpu'`` use the first platform and GPU device
              returned by PyOpenCL.
            - ``'cuda-gpu'`` use device id=0.
            - ``'lazylinop'`` (wip).
            - ``'scipy'`` use ``scipy.sparse.block_diag``
              and ``scipy.sparse.csr_matrix`` to compute ``L @ x``.
            - ``(cl.Platform, cl.Device)`` a tuple of OpenCL platform
              and device.
            - ``pycuda.driver.Device`` a CUDA device.

    Returns:
        :class:`LazyLinOp`

    Examples:
        >>> from lazylinop.wip.butterfly.ksm import ksm
        >>> from lazylinop.wip.butterfly.ksm import multiple_ksm
        >>> a1, b1, c1, d1 = 2, 4, 3, 3
        >>> ks_values1 = np.full((a1, b1, c1, d1), 1.0, dtype=np.float32)
        >>> a2, b2, c2, d2 = 3, 3, 5, 2
        >>> ks_values2 = np.full((a2, b2, c2, d2), 1.0, dtype=np.float32)
        >>> L = ksm(ks_values1) @ ksm(ks_values2)
        >>> M = multiple_ksm([ks_values1, ks_values2])
        >>> np.allclose(L.toarray(), M.toarray())
        True

    References:
        [1] Fast inference with Kronecker-sparse matrices.
        Antoine Gonon and L\0xA9 on Zheng and Pascal Carrivain and Quoc-Tung Le
        https://arxiv.org/abs/2405.15013
    """

    # Ask for CUDA backend but pyCUDA is not installed.
    if cuda is None and 'cuda' in backend:
        warnings.warn("pyCUDA is not installed, switch to 'scipy' backend.")
        backend = 'scipy'
    elif cl is None and 'cl' in backend:
        warnings.warn("pyOpenCL is not installed, switch to 'scipy' backend.")
        backend = 'scipy'

    n_factors = len(ks_values)
    for i in range(n_factors):
        if ks_values[i].ndim != 4 or not isinstance(ks_values[i], np.ndarray):
            raise Exception("ks_values elements must be a 4D NumPy array.")
        if (
                ks_values[i].dtype != np.float16 and
                ks_values[i].dtype != np.float32 and
                ks_values[i].dtype != np.float64 and
                ks_values[i].dtype != np.complex64 and
                ks_values[i].dtype != np.complex128
        ):
            raise TypeError("dtype of ks_values must be either np.float16,"
                            + " np.float32, np.float64,"
                            + " np.complex64 or np.complex128.")

    if isinstance(backend, str):
        if backend == 'opencl-cpu' or backend == 'opencl-gpu':
            return _multiple_ksm(ks_values, params, backend)
        elif backend == 'cuda-gpu':
            return _multiple_ksm(ks_values, params, backend)
        elif 'lazylinop' in backend:
            L = _ksm_lazylinop(ks_values[0])
            for i in range(1, n_factors):
                L = L @ _ksm_lazylinop(ks_values[i])
            L.context = None
        elif 'scipy' in backend:
            L = _ksm_scipy(ks_values[0])
            for i in range(1, n_factors):
                L = L @ _ksm_scipy(ks_values[i])
            L.context = None
            return L
        else:
            raise ValueError("backend must be either 'opencl-cpu'," +
                             " 'opencl-gpu', 'cuda-gpu'." +
                             " 'lazylinop' or 'scipy'.")
    elif (
            isinstance(backend, tuple) and
            len(backend) == 2 and
            isinstance(backend[0], cl.Platform) and
            isinstance(backend[1], cl.Device)
    ):
        return _multiple_ksm(ks_values, params, backend)
    elif isinstance(backend, cuda.Device):
        return _multiple_ksm(ks_values, params, backend)
    else:
        raise Exception("No backend found.")


def _multiple_ksm(ks_values: list,
                  params: list = None, backend='opencl-cpu'):
    """
    pyopencl and pycuda versions of ``multiple_ksm()``.
    """

    n_factors = len(ks_values)
    dtype = ks_values[0].dtype
    for i in range(1, n_factors):
        if dtype != ks_values[i].dtype:
            raise TypeError("All elements of ks_values" +
                            " must have the same dtype.")

    context = _context(backend)
    is_opencl = isinstance(context, cl.Context)

    # Use this instance to keep track of the last batch size.
    # If batch size changes, we need to compute new hyper-parameters.
    ksm_data = Ksm_data()

    if is_opencl:
        # Create command queue
        queue = cl.CommandQueue(
            context,
            properties=cl.command_queue_properties.PROFILING_ENABLE)

    # Input and output sizes.
    a, b, c, d = ks_values[n_factors - 1].shape
    input_size = a * c * d
    a, b, c, d = ks_values[0].shape
    output_size = a * b * d

    d_values, d_rvalues, patterns = [], [], []
    for f in range(n_factors):
        # Transform ks_values from 4D to 2d array once and for all.
        if len(ks_values[f].shape) != 4:
            raise Exception("Element of ks_values must be a" +
                            " np.ndarray with four dimensions.")
        a, b, c, d = ks_values[f].shape
        patterns.append((a, b, c, d))
        values = np.ascontiguousarray(
            np.swapaxes(ks_values[f], 2, 3).reshape(a * d * b, c))
        # Host to device.
        if is_opencl:
            d_values.append(
                cl.Buffer(
                    context,
                    cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                    hostbuf=values))
        else:
            d_values.append(cuda.mem_alloc(values.nbytes))
            cuda.memcpy_htod(d_values[f], values)

        # Transform acbd from 4D to 2d array once and for all.
        # The transpose of the support I_a\otimes 1_{b,c}\otimes I_d
        # is given by I_a\otimes 1_{c,b}\otimes I_d.
        acbd = np.swapaxes(ks_values[f], 1, 2)
        rvalues = np.ascontiguousarray(
            np.swapaxes(acbd, 2, 3).reshape(a * d * c, b))
        # Host to device.
        if is_opencl:
            d_rvalues.append(
                cl.Buffer(
                    context,
                    cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                    hostbuf=rvalues))
        else:
            d_rvalues.append(cuda.mem_alloc(rvalues.nbytes))
            cuda.memcpy_htod(d_rvalues[f], rvalues)

    def _kx(x, patterns, buf_val, context, adjoint):

        if is_opencl:
            smem = context.devices[0].get_info(cl.device_info.LOCAL_MEM_SIZE)
        else:
            smem = context.get_device().get_attribute(
                pycuda._driver.device_attribute.MAX_SHARED_MEMORY_PER_BLOCK)

        if ksm_data.batch_size is None or ksm_data.batch_size != x.shape[1]:
            # Because of new batch size, reset data.
            # batch_size = None corresponds to the first call.
            new_batch_size = True
            ksm_data.batch_size = x.shape[1]
            ksm_data.hp = [None] * n_factors
            ksm_data.rhp = [None] * n_factors
            ksm_data.kernels = [None] * n_factors
            ksm_data.rkernels = [None] * n_factors
            ksm_data.program = [None] * n_factors
            ksm_data.rprogram = [None] * n_factors
        else:
            new_batch_size = False

        batch_size = x.shape[1]

        # Max output size.
        max_out_size = 0
        for i in range(n_factors):
            a, b, c, d = patterns[i]
            max_out_size = max(max_out_size,
                               a * c * d if adjoint else a * b * d)
        y = np.empty((max_out_size, batch_size),
                     dtype=ks_values[0].dtype)

        # Loop over the factors (from right to left).
        d_y, idx = [], 0
        for i in range(n_factors - 1, -1, -1):
            if ks_values[i].dtype != x.dtype:
                x = x.astype(ks_values[i].dtype)
                # raise TypeError("dtype of x must 'float32' or 'float64'.")
            a, b, c, d = patterns[i]
            if new_batch_size:
                # Because of new batch size ...
                hp, rhp = _modify_template(
                    a, b, c, d, x.shape[1],
                    smem, (None, None) if params is None else params[i],
                    ks_values[i].dtype, 'clh' if is_opencl else 'cuh')

                # Read kernel from source file.
                kernel, rkernel = _read_kernel(
                    "ksmm." + ("clh" if is_opencl else "cuh"))

                # Compile kernel.
                if is_opencl:
                    program = cl.Program(context, kernel).build()
                    rprogram = cl.Program(context, rkernel).build()
                else:
                    # Because of overloading function no_extern_c=True.
                    # Use extern "C" { __global__ void ksmm(...) {...} }.
                    program = SourceModule(kernel, no_extern_c=True)
                    rprogram = SourceModule(rkernel, no_extern_c=True)
                ksm_data.hp[n_factors - 1 - i] = hp
                ksm_data.rhp[n_factors - 1 - i] = rhp
                ksm_data.program[n_factors - 1 - i] = program
                ksm_data.rprogram[n_factors - 1 - i] = rprogram
                ksm_data.kernels[n_factors - 1 - i] = kernel
                ksm_data.rkernels[n_factors - 1 - i] = rkernel
            else:
                hp = ksm_data.hp[n_factors - 1 - i]
                rhp = ksm_data.rhp[n_factors - 1 - i]
                program = ksm_data.program[n_factors - 1 - i]
                rprogram = ksm_data.rprogram[n_factors - 1 - i]
                kernel = ksm_data.kernels[n_factors - 1 - i]
                rkernel = ksm_data.rkernels[n_factors - 1 - i]

            # Define the grid.
            if adjoint:
                out_size = a * c * d
                rntx, rnty = rhp[0] // rhp[3], rhp[2] // rhp[4]
                if is_opencl:
                    local_work_size = (rntx, rnty)
                    global_work_size = (
                        ((batch_size + rhp[0] - 1) // rhp[0]) * rntx,
                        ((out_size + rhp[2] - 1) // rhp[2]) * rnty)
                else:
                    block = (rntx, rnty, 1)
                    grid = ((batch_size + rhp[0] - 1) // rhp[0],
                            (out_size + rhp[2] - 1) // rhp[2], 1)
            else:
                out_size = a * b * d
                ntx, nty = hp[0] // hp[3], hp[2] // hp[4]
                if is_opencl:
                    local_work_size = (ntx, nty)
                    global_work_size = (
                        ((batch_size + hp[0] - 1) // hp[0]) * ntx,
                        ((out_size + hp[2] - 1) // hp[2]) * nty)
                else:
                    block = (ntx, nty, 1)
                    grid = ((batch_size + hp[0] - 1) // hp[0],
                            (out_size + hp[2] - 1) // hp[2], 1)

            # print("local work size",
            #       local_work_size if is_opencl else block)
            # print("global work size",
            #       global_work_size if is_opencl else grid)

            # The kernel computes K @ X where the input K and X
            # are in row-major format.
            # The output y of the computation is in row-major format.
            # Host to device.
            if i == (n_factors - 1):
                # Multiply most right factor with x.
                if is_opencl:
                    d_x = cl.Buffer(
                        context,
                        cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                        hostbuf=x
                    )
                else:
                    d_x = cuda.mem_alloc(x.nbytes)
                    cuda.memcpy_htod(d_x, x)
                if is_opencl:
                    for _ in range(2):
                        d_y.append(
                            cl.Buffer(context, cl.mem_flags.READ_WRITE, y.nbytes))
                        # d_y.append(
                        #     cl.Buffer(
                        #         context,
                        #         cl.mem_flags.WRITE_ONLY | cl.mem_flags.COPY_HOST_PTR,
                        #         hostbuf=y))
                else:
                    for _ in range(2):
                        d_y.append(cuda.mem_alloc(y.nbytes))
            # Run the kernel.
            bb = np.int32(c) if adjoint else np.int32(b)
            cc = np.int32(b) if adjoint else np.int32(c)
            if is_opencl:
                knl = rprogram.ksmm if adjoint else program.ksmm
                knl.set_args(
                    buf_val[i],
                    d_x if i == (n_factors - 1) else d_y[idx], d_y[1 - idx],
                    np.int32(a), bb, cc, np.int32(d),
                    np.int32(batch_size))
                event = cl.enqueue_nd_range_kernel(
                    queue, knl, global_work_size, local_work_size)
                event.wait()
                complete = cl.command_execution_status.COMPLETE
                if event.command_execution_status != complete:
                    raise Exception("OpenCL command execution" +
                                    " status is not complete.")
            else:
                knl = (rprogram if adjoint else program).get_function('ksmm')
                knl(buf_val[i],
                    d_x if i == (n_factors - 1) else d_y[idx],
                    d_y[1 - idx],
                    np.int32(a), bb, cc, np.int32(d),
                    np.int32(batch_size),
                    block=block,
                    grid=grid)
                context.synchronize()
            # Get the output after multiplication
            # with the most left factor.
            if i == 0:
                if is_opencl:
                    event = cl.enqueue_copy(queue, y, d_y[1 - idx])
                    event.wait()
                    complete = cl.command_execution_status.COMPLETE
                    if event.command_execution_status != complete:
                        raise Exception("OpenCL command execution" +
                                        " status is not complete.")
                else:
                    cuda.memcpy_dtoh(y, d_y[1 - idx])
                    context.synchronize()
            idx = 1 - idx % 2
        if is_opencl:
            d_x.release()
            for i in range(2):
                d_y[i].release()
        else:
            d_x.free()
            for i in range(2):
                d_y[i].free()
        return y[:output_size, :]

    L = LazyLinOp(
        shape=(output_size, input_size),
        matmat=lambda x: _kx(x, patterns, d_values, context, False),
        rmatmat=lambda x: _kx(x, patterns, d_rvalues, context, True)
    )

    L.context = context

    return L


def _ksm_lazylinop(ks_values: np.ndarray):
    # FIXME
    return None


def _ksm_scipy(ks_values: np.ndarray):
    """
    SciPy version of ``ksm()``.
    """

    from scipy.sparse import block_diag, csr_matrix

    a, b, c, d = ks_values.shape

    rows = np.arange(b * d)
    indices = np.array([])
    for i in rows:
        indices = np.append(indices, np.arange(i % d, c * d, d))
    indptr = np.array([0] + [(i + 1) * c for i in range(b * d)])

    B = block_diag([
        csr_matrix(
            (
                ks_values[i, :, :, :].swapaxes(1, 2).reshape(b * d, c).ravel(),
                indices,
                indptr
            ), shape=(b * d, c * d)) for i in range(a)])

    L = LazyLinOp(
        shape=(a * b * d, a * c * d),
        matmat=lambda x: B @ x,
        rmatmat=lambda x: B.T.conj() @ x
    )

    L.context = None

    return L


def del_context(L: LazyLinOp):
    """
    Delete pyCUDA context of the instance ``L``
    of the :class:`.LazyLinOp`.
    Once you compute ``y = L @ x`` and you do not
    need ``L`` anymore, use ``del_context(L)``
    to clean memory.

    Args:
        L: ``LazyLinOp``
            Delete pyCUDA context of ``L``
    """
    if hasattr(L, 'context') and \
       L.context is not None and \
       getattr(L.context, 'pop', None) is not None:
        L.context.pop()
        L.context.detach()
        del L.context
