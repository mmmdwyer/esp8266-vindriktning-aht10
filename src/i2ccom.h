#pragma once

#include "Types.h"



namespace i2ccom {

    Adafruit_AHT10 aht;
    
    void setup() {
      if (! aht.begin()) {
        Serial.println("Could not find temperature sensor. Halting.");
        while (1) delay(10);
      }
    Serial.println("AHT10 found");
    }

    void handlei2c(floatSensorState_t& temperature, floatSensorState_t& humidity) {

        // Rate-limit checking the sensors
        if ((millis()%10000)) { return; }
      
        sensors_event_t humisens;
        sensors_event_t tempsens;
        
        aht.getEvent(&humisens, &tempsens);// populate temp and humidity objects with fresh data

        // Serial.print("Temperature: "); Serial.print(tempsens.temperature); Serial.println(" degrees C");
        // Serial.print("Humidity: "); Serial.print(humisens.relative_humidity); Serial.println("% rH");

        // Put the current measurement into the current slot
        temperature.measurements[temperature.measurementIdx] = tempsens.temperature;
        humidity.measurements[humidity.measurementIdx] = humisens.relative_humidity;

        // Advance the current measurement pointer with wrap
        temperature.measurementIdx = (temperature.measurementIdx + 1) % 5;
        humidity.measurementIdx = (humidity.measurementIdx + 1) % 5;

        // Update the average when we loop
        if (temperature.measurementIdx == 0) {
            float average = 0.0f;

            for (uint8_t i = 0; i < 5; ++i) {
                average += temperature.measurements[i] / 5.0f;
            }

            temperature.average = average;
            temperature.valid = true;

            Serial.printf("New Avg temperature: %.2f\n", temperature.average);
        }
        if (humidity.measurementIdx == 0) {
            float average = 0.0f;

            for (uint8_t i = 0; i < 5; ++i) {
                average += humidity.measurements[i] / 5.0f;
            }

            humidity.average = average;
            humidity.valid = true;

            Serial.printf("New Avg humidity: %2.f\n", humidity.average);
        }

        // Show the state
        Serial.printf(
                "Current temperature: %.2f, %.2f, %.2f, %.2f, %.2f (%.2f)\n",
                temperature.measurements[0],
                temperature.measurements[1],
                temperature.measurements[2],
                temperature.measurements[3],
                temperature.measurements[4],
                temperature.average
            );
        Serial.printf(
                "Current humidity: %.2f, %.2f, %.2f, %.2f, %.2f, (%.2f)\n",
                humidity.measurements[0],
                humidity.measurements[1],
                humidity.measurements[2],
                humidity.measurements[3],
                humidity.measurements[4],
                humidity.average
            );
    }
} // namespace i2cxom
