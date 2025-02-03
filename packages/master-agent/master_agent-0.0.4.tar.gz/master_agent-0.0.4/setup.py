from setuptools import setup, find_packages

setup(
    name='master_agent',
    version='0.0.4',
    author='Stevo Huncho',
    author_email='stevo@stevohuncho.com',
    description='A library providing the tools to solve complex environments in Minigrid using LgTS',
    keywords="reinforcement learning, actor-critic, a2c, ppo, multi-processes, gpu, teacher student, ts",
    packages=find_packages(),
    install_requires=[
        'torch',
        'minigrid',
        'numpy',
    ],
)