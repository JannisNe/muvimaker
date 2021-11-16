import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setuptools.setup(
        name="muvimaker",
        version="0.2.7",
        author="Jannis Necker",
        author_email="jannis.necker@gmail.com",
        description="A small package to generate moving pictures from sound",
        long_description=long_description,
        long_description_content_type="text/markdown",
        license="MIT",
        keywords="music video picture generation",
        url="https://github.com/JannisNe/muvimaker",
        project_urls={
            "Bug Tracker": "https://github.com/JannisNe/muvimaker/issues",
        },
        packages=setuptools.find_packages(),
        classifiers=[
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.9",
        ],
        python_requires='>=3.9',
        install_requires=[
            "moviepy==1.0.3",
            "librosa==0.8.1",
            "numpy==1.21.2",
            "matplotlib==3.4.3",
            "jupyterlab==3.1.4",
            "pillow==8.3.2",
            "gizeh==0.1.11",
            "ffmpeg==1.4",
            "coveralls",
            "setuptools==59.1.1",
            "scikit-image==0.18.3"
        ],
        package_data={'muvimaker': [
            'example_data/example_pic.jpg',
            'example_data/example_song.mp3'
        ]},
        include_package_data=True
    )