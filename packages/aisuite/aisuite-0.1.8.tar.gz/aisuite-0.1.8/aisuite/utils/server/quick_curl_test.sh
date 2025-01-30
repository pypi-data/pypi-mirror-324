#!/bin/bash

PORT=7000

# Test /tool-spec endpoint
SPEC_RESPONSE=$(curl -s -X GET "http://localhost:${PORT}/tool-spec?tool_name=get_weather&tool_name=get_coordinates_for_city")
EXPECTED_SPEC_RESPONSE='"errorString":""'
if [[ $SPEC_RESPONSE == *$EXPECTED_SPEC_RESPONSE* ]]; then
  echo "GET /tool-spec passed"
else
  echo "GET /tool-spec failed"
  echo "Received response: $SPEC_RESPONSE"
  exit 1
fi

# Test /execute endpoint for get_weather
EXECUTE_WEATHER_RESPONSE=$(curl -s -X POST http://localhost:${PORT}/execute \
  -H "Content-Type: application/json" \
  -d '{"tool_id": "1", "tool_name": "get_weather", "args": {"latitude": 37.7749, "longitude": -122.4194}}')
EXPECTED_EXECUTE_WEATHER_RESPONSE='"errorString":""'
if [[ $EXECUTE_WEATHER_RESPONSE == *$EXPECTED_EXECUTE_WEATHER_RESPONSE* ]]; then
  echo "POST /execute (get_weather) passed"
else
  echo "POST /execute (get_weather) failed"
  echo "Received response: $EXECUTE_WEATHER_RESPONSE"
  exit 1
fi

# Test /execute endpoint for get_coordinates_for_city
EXECUTE_COORDS_RESPONSE=$(curl -s -X POST http://localhost:${PORT}/execute \
  -H "Content-Type: application/json" \
  -d '{"tool_id": "2", "tool_name": "get_coordinates_for_city", "args": {"city_name": "San Francisco"}}')
EXPECTED_EXECUTE_COORDS_RESPONSE='"errorString":""'
if [[ $EXECUTE_COORDS_RESPONSE == *$EXPECTED_EXECUTE_COORDS_RESPONSE* ]]; then
  echo "POST /execute (get_coordinates_for_city) passed"
else
  echo "POST /execute (get_coordinates_for_city) failed"
  echo "Received response: $EXECUTE_COORDS_RESPONSE"
  exit 1
fi

# If all tests pass
echo "WORKING"
