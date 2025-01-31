from tmlt.private_pgm.domain import Domain
from tmlt.private_pgm.dataset import Dataset
from tmlt.private_pgm.factor import Factor
from tmlt.private_pgm.clique_vector import CliqueVector
from tmlt.private_pgm.graphical_model import GraphicalModel
from tmlt.private_pgm.factor_graph import FactorGraph
from tmlt.private_pgm.region_graph import RegionGraph
from tmlt.private_pgm.inference import FactoredInference
from tmlt.private_pgm.local_inference import LocalInference
from tmlt.private_pgm.public_inference import PublicInference

try:
    from tmlt.private_pgm.mixture_inference import MixtureInference
except:
    import warnings

    warnings.warn("MixtureInference disabled, please install jax and jaxlib")

# These gets automatically replaced by the version number during the release process
# by poetry-dynamic-versioning.
__version__ = "0.1.1-alpha.2"
__version_tuple__ = (0, 1, 1, "alpha", 2)
