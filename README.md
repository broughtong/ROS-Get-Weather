# ROS Get Weather
ROS node for getting the current weather forecast.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This node will intermittently poll for the current weather forecast and continually publish on a topic.

Set the geographical location in the launch file (eg. "Prague"), build, source, do `rostopic echo /weather`.

Example of the published message:

    location: "Prague"
    forecastTime: "Sunday 21:00"
    description: "Cloudy"
    celsius: 4
    precipitation: "7%"
    humidity: "87%"
    wind: "14 km/h"

Requires BeautifulSoup4, ie. `pip install beautifulsoup4`.
    
Tested on Ubuntu 18.04 LTS with ROS Melodic and Ubuntu 20.04 LTS with ROS Noetic.

#### Acknowledgments

This work was supported by the EU-H2020-FET-Open (RIA) project RoboRoyale, with reference number 964492.

