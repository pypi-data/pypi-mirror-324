/* Copyright 2024 The OpenXLA Authors.

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

#ifndef XLA_SERVICE_CPU_RUNTIME_SYMBOL_GENERATOR_H_
#define XLA_SERVICE_CPU_RUNTIME_SYMBOL_GENERATOR_H_

#include <optional>

#include "llvm/ADT/StringRef.h"
#include "llvm/ExecutionEngine/Orc/Core.h"
#include "llvm/ExecutionEngine/Orc/Shared/ExecutorSymbolDef.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/Support/Error.h"

namespace xla::cpu {

// Generates symbol definitions for XLA runtime symbols, which are linked into
// the compiled XLA kernels.
class RuntimeSymbolGenerator : public llvm::orc::DefinitionGenerator {
 public:
  explicit RuntimeSymbolGenerator(llvm::DataLayout data_layout);

  llvm::Error tryToGenerate(llvm::orc::LookupState&, llvm::orc::LookupKind,
                            llvm::orc::JITDylib& jit_dylib,
                            llvm::orc::JITDylibLookupFlags,
                            const llvm::orc::SymbolLookupSet& names) final;

 private:
  std::optional<llvm::orc::ExecutorSymbolDef> ResolveRuntimeSymbol(
      llvm::StringRef name);

  llvm::DataLayout data_layout_;
};

}  // namespace xla::cpu

#endif  // XLA_SERVICE_CPU_RUNTIME_SYMBOL_GENERATOR_H_
