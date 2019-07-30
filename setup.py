from setuptools import setup, find_packages

setup(
    name="DistributedOscilloscope",
    version="1.0.0",
    packages=['DistributedOscilloscope.server',
              'DistributedOscilloscope.utilities',
              'DistributedOscilloscope.applications.pyqt_app',
              'DistributedOscilloscope.applications.tests',
              'DistributedOscilloscope.nodes.adc_lib_node',
              ],
    package_dir={'':'software'},
    entry_points={
        'console_scripts':[
            'dist_osc_server = DistributedOscilloscope.server.main_server:main',
            'dist_osc_adc_node = DistributedOscilloscope.nodes.adc_lib_node.main:main',
            'dist_osc_gui= DistributedOscilloscope.applications.pyqt_app.main:main'
            ]
    },
)

