# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.sparse namespace
"""

import sys as _sys

from tensorflow.python.framework.sparse_tensor import SparseTensor # line: 48
from tensorflow.python.ops.array_ops import sparse_mask as mask # line: 1598
from tensorflow.python.ops.array_ops import sparse_placeholder as placeholder # line: 3082
from tensorflow.python.ops.data_flow_ops import SparseConditionalAccumulator # line: 1476
from tensorflow.python.ops.math_ops import sparse_segment_mean as segment_mean # line: 5004
from tensorflow.python.ops.math_ops import sparse_segment_sqrt_n as segment_sqrt_n # line: 5116
from tensorflow.python.ops.math_ops import sparse_segment_sum as segment_sum # line: 4638
from tensorflow.python.ops.sparse_ops import sparse_add as add # line: 460
from tensorflow.python.ops.sparse_ops import sparse_bincount as bincount # line: 3205
from tensorflow.python.ops.sparse_ops import sparse_concat as concat # line: 284
from tensorflow.python.ops.sparse_ops import sparse_cross as cross # line: 608
from tensorflow.python.ops.sparse_ops import sparse_cross_hashed as cross_hashed # line: 666
from tensorflow.python.ops.sparse_ops import sparse_expand_dims as expand_dims # line: 143
from tensorflow.python.ops.sparse_ops import sparse_eye as eye # line: 249
from tensorflow.python.ops.sparse_ops import sparse_fill_empty_rows as fill_empty_rows # line: 2109
from tensorflow.python.ops.sparse_ops import from_dense # line: 111
from tensorflow.python.ops.sparse_ops import sparse_tensor_dense_matmul as matmul # line: 2430
from tensorflow.python.ops.sparse_ops import sparse_maximum as maximum # line: 2734
from tensorflow.python.ops.sparse_ops import sparse_merge as merge # line: 1802
from tensorflow.python.ops.sparse_ops import sparse_minimum as minimum # line: 2780
from tensorflow.python.ops.sparse_ops import sparse_reduce_max as reduce_max # line: 1341
from tensorflow.python.ops.sparse_ops import sparse_reduce_max_sparse as reduce_max_sparse # line: 1427
from tensorflow.python.ops.sparse_ops import sparse_reduce_sum as reduce_sum # line: 1559
from tensorflow.python.ops.sparse_ops import sparse_reduce_sum_sparse as reduce_sum_sparse # line: 1628
from tensorflow.python.ops.sparse_ops import sparse_reorder as reorder # line: 821
from tensorflow.python.ops.sparse_ops import sparse_reset_shape as reset_shape # line: 2004
from tensorflow.python.ops.sparse_ops import sparse_reshape as reshape # line: 876
from tensorflow.python.ops.sparse_ops import sparse_retain as retain # line: 1957
from tensorflow.python.ops.sparse_ops import sparse_slice as slice # line: 1136
from tensorflow.python.ops.sparse_ops import sparse_softmax as softmax # line: 2671
from tensorflow.python.ops.sparse_ops import sparse_tensor_dense_matmul as sparse_dense_matmul # line: 2430
from tensorflow.python.ops.sparse_ops import sparse_split as split # line: 991
from tensorflow.python.ops.sparse_ops import sparse_tensor_to_dense as to_dense # line: 1681
from tensorflow.python.ops.sparse_ops import sparse_to_indicator as to_indicator # line: 1737
from tensorflow.python.ops.sparse_ops import sparse_transpose as transpose # line: 2824

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "sparse", public_apis=None, deprecation=True,
      has_lite=False)
