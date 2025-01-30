import setuptools

setuptools.setup(
    name="weatherxu",
    version="1.0.1",
    url="https://github.com/weatherxu/weatherxu-python",

    author="WeatherXu",
    author_email="contact@weatherxu.com",

    description="Official Python SDK for weatherxu.com",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),

    license_files=('LICENSE'),

    packages=setuptools.find_packages(),

    install_requires=[],
    keywords=['weather', 'weather data', 'weather forecast', 'weather api'],
)
