from setuptools import setup

setup(
    name="lecturemd",
    version="0.1.3",
    packages=[
        "lecturemd",
        "lecturemd.new",
        "lecturemd.configure",
        "lecturemd.make",
    ],
    install_requires=[
        "textual",
        "pyyaml",
        "rich",
        "pygmentation",
        "pyndoc",
    ],
    entry_points={"console_scripts": ["lecturemd = lecturemd.__main__:main"]},
    package_data={
        "lecturemd.new": ["templates/*", "styles/*", "templates/latex_packages/*"],
        "lecturemd.configure": ["configure.tcss", "ncl.tcss"],
        "lecturemd.make": ["filters/*", "post/*"],
    },
    include_package_data=True,
)
