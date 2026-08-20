#!/bin/bash -eu

# Build a go fuzzer binary into $OUT using OSS-Fuzz helpers.
# package_path                fuzz_func_name         output_binary_name
compile_go_fuzzer github.com/abcxyz/terraform-aws-observability-pro/fuzz FuzzHCLParseCFLite hcl_parse_cflite_fuzzer
