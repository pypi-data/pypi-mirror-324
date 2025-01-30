# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.experimental.dtensor namespace
"""

import sys as _sys

from tensorflow.dtensor.python.accelerator_util import initialize_accelerator_system # line: 114
from tensorflow.dtensor.python.accelerator_util import initialize_accelerator_system as initialize_multi_client # line: 114
from tensorflow.dtensor.python.accelerator_util import initialize_accelerator_system as initialize_tpu_system # line: 114
from tensorflow.dtensor.python.accelerator_util import shutdown_accelerator_system # line: 270
from tensorflow.dtensor.python.accelerator_util import shutdown_accelerator_system as shutdown_tpu_system # line: 270
from tensorflow.dtensor.python.api import reset_dtensor_device as _reset_dtensor_device # line: 505
from tensorflow.dtensor.python.api import call_with_layout # line: 37
from tensorflow.dtensor.python.api import check_layout # line: 395
from tensorflow.dtensor.python.api import copy_to_mesh # line: 167
from tensorflow.dtensor.python.api import default_mesh # line: 89
from tensorflow.dtensor.python.api import device_name # line: 131
from tensorflow.dtensor.python.api import fetch_layout # line: 379
from tensorflow.dtensor.python.api import get_default_mesh # line: 115
from tensorflow.dtensor.python.api import is_dtensor # line: 147
from tensorflow.dtensor.python.api import pack # line: 191
from tensorflow.dtensor.python.api import relayout # line: 411
from tensorflow.dtensor.python.api import relayout_like # line: 452
from tensorflow.dtensor.python.api import run_on # line: 67
from tensorflow.dtensor.python.api import unpack # line: 342
from tensorflow.dtensor.python.config import client_id # line: 86
from tensorflow.dtensor.python.config import full_job_name # line: 117
from tensorflow.dtensor.python.config import heartbeat_enabled # line: 168
from tensorflow.dtensor.python.config import job_name # line: 108
from tensorflow.dtensor.python.config import jobs # line: 148
from tensorflow.dtensor.python.config import local_devices # line: 46
from tensorflow.dtensor.python.config import num_clients # line: 100
from tensorflow.dtensor.python.config import num_global_devices # line: 80
from tensorflow.dtensor.python.config import num_local_devices # line: 68
from tensorflow.dtensor.python.config import preferred_device_type # line: 192
from tensorflow.dtensor.python.d_checkpoint import DTensorCheckpoint # line: 412
from tensorflow.dtensor.python.d_variable import DVariable # line: 143
from tensorflow.dtensor.python.input_util import DTensorDataset # line: 384
from tensorflow.dtensor.python.layout import Layout # line: 351
from tensorflow.dtensor.python.layout import MATCH # line: 39
from tensorflow.dtensor.python.layout import Mesh # line: 53
from tensorflow.dtensor.python.layout import UNSHARDED # line: 36
from tensorflow.dtensor.python.mesh_util import barrier # line: 243
from tensorflow.dtensor.python.mesh_util import create_distributed_mesh # line: 138
from tensorflow.dtensor.python.mesh_util import create_mesh # line: 70
from tensorflow.dtensor.python.save_restore import enable_save_as_bf16 # line: 83
from tensorflow.dtensor.python.save_restore import name_based_restore # line: 100
from tensorflow.dtensor.python.save_restore import name_based_save # line: 176
from tensorflow.dtensor.python.save_restore import sharded_save # line: 34
from tensorflow.dtensor.python.tpu_util import create_tpu_mesh # line: 585
