# ROS-Get-Weather
ROS node for getting the current weather forecast.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This node will intermittently poll for the current weather forecast and continually publish on a topic.

Set the geographical location in the launch file, build, do `rostopic echo /weather`.

Example of the published message:

    location: "Prague"
    forecastTime: "Sunday 21:00"
    description: "Cloudy"
    celsius: 4
    precipitation: "7%"
    humidity: "87%"
    wind: "14 km/h"
    
Tested on Ubuntu 18.04 LTS with ROS Melodic and Ubuntu 20.04 LTS with ROS Noetic.
