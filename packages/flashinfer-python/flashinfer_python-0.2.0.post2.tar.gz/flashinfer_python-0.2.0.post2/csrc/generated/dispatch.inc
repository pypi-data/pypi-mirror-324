#define _DISPATCH_CASES_head_dim(case_var, ...)         \
  _DISPATCH_CASE(64, case_var, __VA_ARGS__) \
  _DISPATCH_CASE(128, case_var, __VA_ARGS__) \
  _DISPATCH_CASE(256, case_var, __VA_ARGS__) \
// EOL

#define _DISPATCH_CASES_head_dim_sm90(case_var, ...)         \
  _DISPATCH_CASE(64, case_var, __VA_ARGS__) \
  _DISPATCH_CASE(128, case_var, __VA_ARGS__) \
  _DISPATCH_CASE(256, case_var, __VA_ARGS__) \
// EOL

#define _DISPATCH_CASES_pos_encoding_mode(case_var, ...)         \
  _DISPATCH_CASE(PosEncodingMode::kNone, case_var, __VA_ARGS__) \
// EOL

#define _DISPATCH_CASES_use_fp16_qk_reduction(case_var, ...)         \
  _DISPATCH_CASE(false, case_var, __VA_ARGS__) \
// EOL

#define _DISPATCH_CASES_mask_mode(case_var, ...)         \
  _DISPATCH_CASE(MaskMode::kNone, case_var, __VA_ARGS__) \
  _DISPATCH_CASE(MaskMode::kCausal, case_var, __VA_ARGS__) \
  _DISPATCH_CASE(MaskMode::kCustom, case_var, __VA_ARGS__) \
// EOL
