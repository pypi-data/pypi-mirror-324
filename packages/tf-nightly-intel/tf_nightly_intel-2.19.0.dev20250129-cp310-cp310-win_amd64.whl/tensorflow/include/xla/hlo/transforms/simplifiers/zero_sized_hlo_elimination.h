/* Copyright 2017 The OpenXLA Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef XLA_HLO_TRANSFORMS_SIMPLIFIERS_ZERO_SIZED_HLO_ELIMINATION_H_
#define XLA_HLO_TRANSFORMS_SIMPLIFIERS_ZERO_SIZED_HLO_ELIMINATION_H_

#include "absl/container/flat_hash_set.h"
#include "absl/status/statusor.h"
#include "absl/strings/string_view.h"
#include "xla/hlo/ir/hlo_module.h"
#include "xla/hlo/pass/hlo_pass_interface.h"

// HLO pass that replaces zero sized Hlos with a zero sized constant literal.
namespace xla {
class ZeroSizedHloElimination : public HloModulePass {
 public:
  using HloPassInterface::Run;
  absl::StatusOr<bool> Run(
      HloModule* module,
      const absl::flat_hash_set<absl::string_view>& execution_threads) override;
  absl::string_view name() const override {
    return "zero_sized_hlo_elimination";
  }
};
}  // namespace xla
#endif  // XLA_HLO_TRANSFORMS_SIMPLIFIERS_ZERO_SIZED_HLO_ELIMINATION_H_
