from setuptools import setup, find_packages
long_description = """
A powerful yet easy-to-use VISCA over IP utility designed to simplify communication with cameras supporting the VISCA protocol. This library provides everything you need to send commands, manage responses, and handle retries over UDP, ensuring reliable camera control.

Key Features:

    Complete VISCA Support: Supports commands like Set, Inquiry, and more.
    Retry Mechanism: Ensures reliable message delivery over UDP with retransmissions.
    Extensible: Built with Python, easily adaptable for advanced use cases.
    Quick Start: Check example01 for a step-by-step implementation.

Whether you're controlling a physical camera or an emulated one, this utility makes the process seamless. Perfect for developers working on broadcasting, streaming, or robotics projects.

"""

setup(
    name="viscaSmith",
    version="0.4.7",
    author="Alessio Michelassi",
    author_email="alessio.michelassi@gmail.com",
    description="Una libreria per controllare telecamere VISCA tramite UDP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlessioMichelassi/ViscaSmithCore",
    packages=find_packages(include=["visca", "visca.*", "doc"]),
    include_package_data=True,  # Includi file non Python (es. JSON)
    install_requires=["PyQt6"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)