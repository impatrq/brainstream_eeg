/*
	Arduino Pico Analog Correction
	https://github.com/Phoenix1747/Arduino-Pico-Analog-Correction/
*/

#include "stdlib.h"
#include "stdio.h"
#ifndef PicoAnalogCorrection_H
#define PicoAnalogCorrection_H

#define PS_PIN 23 // Power Save Pin, H to disable, L default
#define PIN_POWER_SAVE 23
typedef enum
{
	PAC_C, // Celsius
	PAC_F, // Fahrenheit
} pactemp_t;

class PicoAnalogCorrection
{
private:
	size_t _max_channel, _gnd_offset, _vcc_offset, _adc_res;
	float _a, _d, _vref;
	const float conversion_factor = 1.23f / (1 << 12);
	void setCorrectionValues();

public:
	PicoAnalogCorrection(size_t adc_res = 12, float vref = 3.3);
	PicoAnalogCorrection(size_t adc_res, size_t gnd_val, size_t vcc_val); // Backwards Compatability
	PicoAnalogCorrection(size_t adc_res, float vref, size_t gnd_val, size_t vcc_val);

	void calibrateAdc(size_t gnd_pin, size_t vcc_pin, size_t avg_size = 100);
	void returnCalibrationValues();
	void ADCinit();
	void analogReadResolution(size_t adc_res);

	int analogRead();
	double analogCRead(size_t pin, size_t avg_size = 1);
	double analogNOCRead(size_t pin, size_t avg_size = 1);
	float analogReadTemp(pactemp_t type = PAC_C);
};
#endif
