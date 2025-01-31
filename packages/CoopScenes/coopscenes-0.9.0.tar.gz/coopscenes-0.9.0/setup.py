from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='CoopScenes',
    version='0.9.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.7',
    url='https://github.com/MarcelVSHNS/coopscenes.git',
    license='Apache License 2.0',
    author='Marcel und Alex',
    author_email='marcel.vosshans@hs-esslingen.de',
    description='Dev-Kit for CoopScenes',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
