from setuptools import setup, find_packages

setup(
    name='bendis_arm',
    version='0.9',
    packages=find_packages(),
    install_requires=[
        'gym',
        'pybullet',
        'numpy',
        'stable-baselines3',
        'opencv-python',
    ],
    description='A robotic arm environment for reinforcement learning',
    author='Bendis',
    author_email='gargazlucaaleaxndru@gmai.com',
    url='https://huggingface.com/Gargaz',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)