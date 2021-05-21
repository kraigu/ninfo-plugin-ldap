from setuptools import setup, find_packages

setup(name='ninfo-plugin-ldap',
    version='0.0.1',
    zip_safe=False,
    packages = find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "ninfo>=0.1.11",
        "ldap3",
    ],
    entry_points = {
        'ninfo.plugin': [
            'ldap      = ninfo_plugin_ldap',
        ]
    }
) 
