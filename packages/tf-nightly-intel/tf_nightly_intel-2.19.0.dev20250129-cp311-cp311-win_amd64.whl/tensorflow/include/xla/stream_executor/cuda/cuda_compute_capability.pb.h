// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: xla/stream_executor/cuda/cuda_compute_capability.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_xla_2fstream_5fexecutor_2fcuda_2fcuda_5fcompute_5fcapability_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_xla_2fstream_5fexecutor_2fcuda_2fcuda_5fcompute_5fcapability_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_xla_2fstream_5fexecutor_2fcuda_2fcuda_5fcompute_5fcapability_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_xla_2fstream_5fexecutor_2fcuda_2fcuda_5fcompute_5fcapability_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_xla_2fstream_5fexecutor_2fcuda_2fcuda_5fcompute_5fcapability_2eproto;
namespace stream_executor {
class CudaComputeCapabilityProto;
struct CudaComputeCapabilityProtoDefaultTypeInternal;
extern CudaComputeCapabilityProtoDefaultTypeInternal _CudaComputeCapabilityProto_default_instance_;
}  // namespace stream_executor
PROTOBUF_NAMESPACE_OPEN
template<> ::stream_executor::CudaComputeCapabilityProto* Arena::CreateMaybeMessage<::stream_executor::CudaComputeCapabilityProto>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace stream_executor {

// ===================================================================

class CudaComputeCapabilityProto final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:stream_executor.CudaComputeCapabilityProto) */ {
 public:
  inline CudaComputeCapabilityProto() : CudaComputeCapabilityProto(nullptr) {}
  ~CudaComputeCapabilityProto() override;
  explicit PROTOBUF_CONSTEXPR CudaComputeCapabilityProto(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  CudaComputeCapabilityProto(const CudaComputeCapabilityProto& from);
  CudaComputeCapabilityProto(CudaComputeCapabilityProto&& from) noexcept
    : CudaComputeCapabilityProto() {
    *this = ::std::move(from);
  }

  inline CudaComputeCapabilityProto& operator=(const CudaComputeCapabilityProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline CudaComputeCapabilityProto& operator=(CudaComputeCapabilityProto&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const CudaComputeCapabilityProto& default_instance() {
    return *internal_default_instance();
  }
  static inline const CudaComputeCapabilityProto* internal_default_instance() {
    return reinterpret_cast<const CudaComputeCapabilityProto*>(
               &_CudaComputeCapabilityProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(CudaComputeCapabilityProto& a, CudaComputeCapabilityProto& b) {
    a.Swap(&b);
  }
  inline void Swap(CudaComputeCapabilityProto* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(CudaComputeCapabilityProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  CudaComputeCapabilityProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<CudaComputeCapabilityProto>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const CudaComputeCapabilityProto& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const CudaComputeCapabilityProto& from) {
    CudaComputeCapabilityProto::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(CudaComputeCapabilityProto* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "stream_executor.CudaComputeCapabilityProto";
  }
  protected:
  explicit CudaComputeCapabilityProto(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kMajorFieldNumber = 1,
    kMinorFieldNumber = 2,
  };
  // int32 major = 1;
  void clear_major();
  int32_t major() const;
  void set_major(int32_t value);
  private:
  int32_t _internal_major() const;
  void _internal_set_major(int32_t value);
  public:

  // int32 minor = 2;
  void clear_minor();
  int32_t minor() const;
  void set_minor(int32_t value);
  private:
  int32_t _internal_minor() const;
  void _internal_set_minor(int32_t value);
  public:

  // @@protoc_insertion_point(class_scope:stream_executor.CudaComputeCapabilityProto)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    int32_t major_;
    int32_t minor_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_xla_2fstream_5fexecutor_2fcuda_2fcuda_5fcompute_5fcapability_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// CudaComputeCapabilityProto

// int32 major = 1;
inline void CudaComputeCapabilityProto::clear_major() {
  _impl_.major_ = 0;
}
inline int32_t CudaComputeCapabilityProto::_internal_major() const {
  return _impl_.major_;
}
inline int32_t CudaComputeCapabilityProto::major() const {
  // @@protoc_insertion_point(field_get:stream_executor.CudaComputeCapabilityProto.major)
  return _internal_major();
}
inline void CudaComputeCapabilityProto::_internal_set_major(int32_t value) {
  
  _impl_.major_ = value;
}
inline void CudaComputeCapabilityProto::set_major(int32_t value) {
  _internal_set_major(value);
  // @@protoc_insertion_point(field_set:stream_executor.CudaComputeCapabilityProto.major)
}

// int32 minor = 2;
inline void CudaComputeCapabilityProto::clear_minor() {
  _impl_.minor_ = 0;
}
inline int32_t CudaComputeCapabilityProto::_internal_minor() const {
  return _impl_.minor_;
}
inline int32_t CudaComputeCapabilityProto::minor() const {
  // @@protoc_insertion_point(field_get:stream_executor.CudaComputeCapabilityProto.minor)
  return _internal_minor();
}
inline void CudaComputeCapabilityProto::_internal_set_minor(int32_t value) {
  
  _impl_.minor_ = value;
}
inline void CudaComputeCapabilityProto::set_minor(int32_t value) {
  _internal_set_minor(value);
  // @@protoc_insertion_point(field_set:stream_executor.CudaComputeCapabilityProto.minor)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace stream_executor

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_xla_2fstream_5fexecutor_2fcuda_2fcuda_5fcompute_5fcapability_2eproto
