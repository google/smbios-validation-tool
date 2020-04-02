# Description:
#   Smbios validation tool parses the output of dmidecode, and analyze it
#   to validate our vendors smbios tables conformance to LESS specification.

load("//devtools/python/blaze:strict.bzl", "py_strict_test")

package(default_visibility = ["//visibility:private"])

licenses(["notice"])

exports_files(["LICENSE"])

py_binary(
    name = "smbios_validation",
    srcs = [
        "constants.py",
        "matcher.py",
        "rules.py",
        "smbios_validation.py",
        "validator.py",
    ],
    compatible_with = [
        "//buildenv/target:vendor",
    ],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        "//third_party/py/absl:app",
        "//third_party/py/absl/flags",
        "//third_party/py/dmiparse",
        "//third_party/py/termcolor",
    ],
)

py_strict_test(
    name = "matcher_test",
    size = "small",
    srcs = [
        "matcher_test.py",
    ],
    data = [
        "test_data/less_compliant_smbios_records.txt",
    ],
    python_version = "PY3",
    deps = [
        ":smbios_validation",
        "//pyglib:resources",
        "//testing/pybase",
        "//third_party/py/dmiparse",
    ],
)

py_strict_test(
    name = "rules_test",
    size = "small",
    srcs = [
        "rules_test.py",
    ],
    data = [
        "test_data/less_compliant_smbios_records.txt",
        "test_data/not_less_compliant_smbios_records.txt",
    ],
    python_version = "PY3",
    deps = [
        ":smbios_validation",
        "//pyglib:resources",
        "//testing/pybase",
        "//third_party/py/dmiparse",
    ],
)

py_strict_test(
    name = "validator_test",
    size = "small",
    srcs = [
        "validator_test.py",
    ],
    data = [
        "test_data/less_compliant_smbios_records.txt",
        "test_data/not_less_compliant_smbios_records.txt",
    ],
    python_version = "PY3",
    deps = [
        ":smbios_validation",
        "//pyglib:resources",
        "//testing/pybase",
        "//testing/pybase:parameterized",
        "//third_party/py/dmiparse",
    ],
)
