# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.saved_model.signature_def_utils namespace
"""

import sys as _sys

from tensorflow.python.saved_model.method_name_updater import MethodNameUpdater # line: 30
from tensorflow.python.saved_model.signature_def_utils_impl import build_signature_def # line: 30
from tensorflow.python.saved_model.signature_def_utils_impl import classification_signature_def # line: 133
from tensorflow.python.saved_model.signature_def_utils_impl import is_valid_signature # line: 293
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def # line: 196
from tensorflow.python.saved_model.signature_def_utils_impl import regression_signature_def # line: 82

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "saved_model.signature_def_utils", public_apis=None, deprecation=True,
      has_lite=False)
