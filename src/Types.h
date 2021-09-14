#pragma once

struct genericSensorState_t {
    uint16_t average = 0;
    uint16_t measurements[5] = {0, 0, 0, 0, 0};
    uint8_t measurementIdx = 0;
    boolean valid = false;
};

struct floatSensorState_t {
    float average = 0;
    float measurements[5] = {0, 0, 0, 0, 0};
    uint8_t measurementIdx = 0;
    boolean valid = false;
};
