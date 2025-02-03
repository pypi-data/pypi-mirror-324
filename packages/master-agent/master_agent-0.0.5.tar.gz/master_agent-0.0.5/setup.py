from setuptools import setup

setup(
    name='master_agent',
    version='0.0.5',
    author='Stevo Huncho',
    author_email='stevo@stevohuncho.com',
    description='A library providing the tools to solve complex environments in Minigrid using LgTS',
    keywords="reinforcement learning, actor-critic, a2c, ppo, multi-processes, gpu, teacher student, ts",
    packages=["master_agent", "master_agent.llm", "master_agent.envs"],
    install_requires=[
        'torch',
        'minigrid',
        'numpy',
    ],
)