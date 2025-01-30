from setuptools import setup, find_packages

setup(
    name='pump_q8',
    version='0.2.0',
    description='نظام تداول وتحليل العملات الرقمية المتقدم',
    author='Jaraah',
    author_email='developer@pumpq8.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'python-dotenv==1.0.0',
        'cryptography==41.0.3',
        'ccxt==4.0.84',
        'pandas==2.1.1',
        'numpy==1.26.0',
        'ta-lib==0.4.20',
        'tensorflow==2.14.0',
        'scikit-learn==1.3.1',
        'matplotlib==3.7.2',
        'requests==2.31.0',
        'pyyaml==6.0.1',
        'python-telegram-bot==20.4'
    ],
    extras_require={
        'dev': [
            'pytest==7.4.2',
            'coverage==7.3.1',
            'memory-profiler==0.60.0',
            'bandit==1.7.5'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial :: Investment',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'pump_q8=src.main:main',
        ],
    }
)
