# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.test namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v2.test import experimental
from tensorflow.python.framework.test_util import TensorFlowTestCase as TestCase # line: 2565
from tensorflow.python.framework.test_util import assert_equal_graph_def_v2 as assert_equal_graph_def # line: 222
from tensorflow.python.framework.test_util import create_local_cluster # line: 4021
from tensorflow.python.framework.test_util import gpu_device_name # line: 171
from tensorflow.python.framework.test_util import is_gpu_available # line: 2075
from tensorflow.python.framework.test_util import with_eager_op_as_function # line: 1305
from tensorflow.python.ops.gradient_checker_v2 import compute_gradient # line: 296
from tensorflow.python.platform.benchmark import TensorFlowBenchmark as Benchmark # line: 287
from tensorflow.python.platform.benchmark import benchmark_config # line: 274
from tensorflow.python.platform.test import disable_with_predicate # line: 131
from tensorflow.python.platform.test import is_built_with_cuda # line: 89
from tensorflow.python.platform.test import is_built_with_gpu_support # line: 149
from tensorflow.python.platform.test import is_built_with_rocm # line: 110
from tensorflow.python.platform.test import is_built_with_xla # line: 170
from tensorflow.python.platform.test import is_cpu_target_available # line: 194
from tensorflow.python.platform.test import main # line: 49
