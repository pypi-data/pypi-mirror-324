import setuptools

# (Optional) Read a long description from a README file
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "pyhaab** is a Python library that automates the process of connecting to Cisco switches (via Netmiko), retrieving interface and VLAN details, and organizing all information into an Excel workbook. It streamlines repetitive network administration tasks, providing:"

setuptools.setup(
    name="pyhaab",              # <-- Must match the name on PyPI
    version="0.2.0",            # <-- IMPORTANT: Increase this version every new release
    author="Your Name",
    author_email="ihaabsaeed@gmail.com",
    description="pyhaab is a Python library that connects to Cisco switches using Netmiko, retrieves interface and VLAN details, and writes them to a fully formatted Excel file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ihaabSaeed12/pyhaab",  # Or another project URL
    packages=setuptools.find_packages(),  # automatically finds "pyhaab" folder
    install_requires=[
        # list your library’s dependencies here
        # e.g. "netmiko", "openpyxl"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
