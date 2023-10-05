from setuptools import setup
setup(
    name='smtp_bcc_client',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'smtp_bcc_client=main:main'
        ]
    }
)