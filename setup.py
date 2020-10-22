from setuptools import setup

setup(
    name = "smbios_validation_tool",
    author = "Xu Han",
    author_email = "",
    license = "Apache",
    url = "https://github.com/google/smbios-validation-tool",
    packages=['smbios_validation_tool', 'dmiparse'],
    scripts=['smbios_validation'],
)
