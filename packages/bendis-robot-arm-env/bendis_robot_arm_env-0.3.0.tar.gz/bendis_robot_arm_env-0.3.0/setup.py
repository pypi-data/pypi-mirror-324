from setuptools import setup, find_packages

setup(
    name='bendis-robot-arm-env',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'gym',
        'pybullet',
        'pybullet',
        'numpy',
        'stable-baselines3',
        'opencv-python',
    ],
    description='Robotic Arm Environment for Training RL Agents',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/bendis-robot-arm-env',  # Optional, if you plan to host it on GitHub
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
