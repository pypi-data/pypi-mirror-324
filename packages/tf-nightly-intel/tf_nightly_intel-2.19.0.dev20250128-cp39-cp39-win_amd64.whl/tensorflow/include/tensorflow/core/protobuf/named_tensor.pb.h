// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/protobuf/named_tensor.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2fnamed_5ftensor_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2fnamed_5ftensor_2eproto

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
#include "tensorflow/core/framework/tensor.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2fprotobuf_2fnamed_5ftensor_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2fprotobuf_2fnamed_5ftensor_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2fprotobuf_2fnamed_5ftensor_2eproto;
namespace tensorflow {
class NamedTensorProto;
struct NamedTensorProtoDefaultTypeInternal;
extern NamedTensorProtoDefaultTypeInternal _NamedTensorProto_default_instance_;
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::NamedTensorProto* Arena::CreateMaybeMessage<::tensorflow::NamedTensorProto>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {

// ===================================================================

class NamedTensorProto final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.NamedTensorProto) */ {
 public:
  inline NamedTensorProto() : NamedTensorProto(nullptr) {}
  ~NamedTensorProto() override;
  explicit PROTOBUF_CONSTEXPR NamedTensorProto(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  NamedTensorProto(const NamedTensorProto& from);
  NamedTensorProto(NamedTensorProto&& from) noexcept
    : NamedTensorProto() {
    *this = ::std::move(from);
  }

  inline NamedTensorProto& operator=(const NamedTensorProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline NamedTensorProto& operator=(NamedTensorProto&& from) noexcept {
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
  static const NamedTensorProto& default_instance() {
    return *internal_default_instance();
  }
  static inline const NamedTensorProto* internal_default_instance() {
    return reinterpret_cast<const NamedTensorProto*>(
               &_NamedTensorProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(NamedTensorProto& a, NamedTensorProto& b) {
    a.Swap(&b);
  }
  inline void Swap(NamedTensorProto* other) {
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
  void UnsafeArenaSwap(NamedTensorProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  NamedTensorProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<NamedTensorProto>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const NamedTensorProto& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const NamedTensorProto& from) {
    NamedTensorProto::MergeImpl(*this, from);
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
  void InternalSwap(NamedTensorProto* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.NamedTensorProto";
  }
  protected:
  explicit NamedTensorProto(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kNameFieldNumber = 1,
    kTensorFieldNumber = 2,
  };
  // string name = 1;
  void clear_name();
  const std::string& name() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_name(ArgT0&& arg0, ArgT... args);
  std::string* mutable_name();
  PROTOBUF_NODISCARD std::string* release_name();
  void set_allocated_name(std::string* name);
  private:
  const std::string& _internal_name() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_name(const std::string& value);
  std::string* _internal_mutable_name();
  public:

  // .tensorflow.TensorProto tensor = 2;
  bool has_tensor() const;
  private:
  bool _internal_has_tensor() const;
  public:
  void clear_tensor();
  const ::tensorflow::TensorProto& tensor() const;
  PROTOBUF_NODISCARD ::tensorflow::TensorProto* release_tensor();
  ::tensorflow::TensorProto* mutable_tensor();
  void set_allocated_tensor(::tensorflow::TensorProto* tensor);
  private:
  const ::tensorflow::TensorProto& _internal_tensor() const;
  ::tensorflow::TensorProto* _internal_mutable_tensor();
  public:
  void unsafe_arena_set_allocated_tensor(
      ::tensorflow::TensorProto* tensor);
  ::tensorflow::TensorProto* unsafe_arena_release_tensor();

  // @@protoc_insertion_point(class_scope:tensorflow.NamedTensorProto)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr name_;
    ::tensorflow::TensorProto* tensor_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2fprotobuf_2fnamed_5ftensor_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// NamedTensorProto

// string name = 1;
inline void NamedTensorProto::clear_name() {
  _impl_.name_.ClearToEmpty();
}
inline const std::string& NamedTensorProto::name() const {
  // @@protoc_insertion_point(field_get:tensorflow.NamedTensorProto.name)
  return _internal_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void NamedTensorProto::set_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.NamedTensorProto.name)
}
inline std::string* NamedTensorProto::mutable_name() {
  std::string* _s = _internal_mutable_name();
  // @@protoc_insertion_point(field_mutable:tensorflow.NamedTensorProto.name)
  return _s;
}
inline const std::string& NamedTensorProto::_internal_name() const {
  return _impl_.name_.Get();
}
inline void NamedTensorProto::_internal_set_name(const std::string& value) {
  
  _impl_.name_.Set(value, GetArenaForAllocation());
}
inline std::string* NamedTensorProto::_internal_mutable_name() {
  
  return _impl_.name_.Mutable(GetArenaForAllocation());
}
inline std::string* NamedTensorProto::release_name() {
  // @@protoc_insertion_point(field_release:tensorflow.NamedTensorProto.name)
  return _impl_.name_.Release();
}
inline void NamedTensorProto::set_allocated_name(std::string* name) {
  if (name != nullptr) {
    
  } else {
    
  }
  _impl_.name_.SetAllocated(name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.name_.IsDefault()) {
    _impl_.name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.NamedTensorProto.name)
}

// .tensorflow.TensorProto tensor = 2;
inline bool NamedTensorProto::_internal_has_tensor() const {
  return this != internal_default_instance() && _impl_.tensor_ != nullptr;
}
inline bool NamedTensorProto::has_tensor() const {
  return _internal_has_tensor();
}
inline const ::tensorflow::TensorProto& NamedTensorProto::_internal_tensor() const {
  const ::tensorflow::TensorProto* p = _impl_.tensor_;
  return p != nullptr ? *p : reinterpret_cast<const ::tensorflow::TensorProto&>(
      ::tensorflow::_TensorProto_default_instance_);
}
inline const ::tensorflow::TensorProto& NamedTensorProto::tensor() const {
  // @@protoc_insertion_point(field_get:tensorflow.NamedTensorProto.tensor)
  return _internal_tensor();
}
inline void NamedTensorProto::unsafe_arena_set_allocated_tensor(
    ::tensorflow::TensorProto* tensor) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.tensor_);
  }
  _impl_.tensor_ = tensor;
  if (tensor) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.NamedTensorProto.tensor)
}
inline ::tensorflow::TensorProto* NamedTensorProto::release_tensor() {
  
  ::tensorflow::TensorProto* temp = _impl_.tensor_;
  _impl_.tensor_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::tensorflow::TensorProto* NamedTensorProto::unsafe_arena_release_tensor() {
  // @@protoc_insertion_point(field_release:tensorflow.NamedTensorProto.tensor)
  
  ::tensorflow::TensorProto* temp = _impl_.tensor_;
  _impl_.tensor_ = nullptr;
  return temp;
}
inline ::tensorflow::TensorProto* NamedTensorProto::_internal_mutable_tensor() {
  
  if (_impl_.tensor_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::TensorProto>(GetArenaForAllocation());
    _impl_.tensor_ = p;
  }
  return _impl_.tensor_;
}
inline ::tensorflow::TensorProto* NamedTensorProto::mutable_tensor() {
  ::tensorflow::TensorProto* _msg = _internal_mutable_tensor();
  // @@protoc_insertion_point(field_mutable:tensorflow.NamedTensorProto.tensor)
  return _msg;
}
inline void NamedTensorProto::set_allocated_tensor(::tensorflow::TensorProto* tensor) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.tensor_);
  }
  if (tensor) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(tensor));
    if (message_arena != submessage_arena) {
      tensor = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, tensor, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.tensor_ = tensor;
  // @@protoc_insertion_point(field_set_allocated:tensorflow.NamedTensorProto.tensor)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2fprotobuf_2fnamed_5ftensor_2eproto
