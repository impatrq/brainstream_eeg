/*
	Arduino Pico Analog Correction
	https://github.com/Phoenix1747/Arduino-Pico-Analog-Correction/
*/

#include "PicoAnalogCorrection.hpp"
#include "hardware/adc.h"
#include "pico/stdlib.h"
#include <math.h>
#include "pico/time.h"

long map(long x, long in_min, long in_max, long out_min, long out_max)
{
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

PicoAnalogCorrection::PicoAnalogCorrection(size_t adc_res, float vref)
{
	_adc_res = adc_res;
	_max_channel = pow(2, adc_res) - 1;
	_gnd_offset = 0;
	_vcc_offset = 0;
	_vref = vref;
	setCorrectionValues();
}

PicoAnalogCorrection::PicoAnalogCorrection(size_t adc_res, size_t gnd_val, size_t vcc_val)
{
	_adc_res = adc_res;
	_max_channel = pow(2, adc_res) - 1;
	_gnd_offset = gnd_val;
	_vcc_offset = vcc_val;
	_vref = 3.3;
	setCorrectionValues();
}

PicoAnalogCorrection::PicoAnalogCorrection(size_t adc_res, float vref, size_t gnd_val, size_t vcc_val)
{
	_adc_res = adc_res;
	_max_channel = pow(2, adc_res) - 1;
	_vref = vref;
	_gnd_offset = gnd_val;
	_vcc_offset = vcc_val;
	setCorrectionValues();
}

void PicoAnalogCorrection::setCorrectionValues()
{
	if (_vcc_offset == 0)
	{
		_a = 1.0;
	}
	else
	{
		_a = _max_channel / (_vcc_offset - _gnd_offset);
	}
	_d = -_a * _gnd_offset;
	return;
}

void PicoAnalogCorrection::calibrateAdc(size_t gnd_pin, size_t vcc_pin, size_t avg_size)
{
	float gnd_value = .0;
	adc_select_input(gnd_pin);
	for (size_t i = 0; i < avg_size; i++)
	{
		gnd_value += float(analogRead());
	}
	_gnd_offset = gnd_value / avg_size;

	float vcc_value = .0;
	adc_select_input(vcc_pin);
	for (size_t i = 0; i < avg_size; i++)
	{
		vcc_value += float(analogRead());
	}
	_vcc_offset = vcc_value / avg_size;

	setCorrectionValues();
	return;
}

void PicoAnalogCorrection::returnCalibrationValues()
{
	// Serial.println("(" + String(_gnd_offset) + ", " + String(_vcc_offset) + ")");
	return;
}

void PicoAnalogCorrection::analogReadResolution(size_t adc_res)
{
	// _adc_res = adc_res;
	// ::analogReadResolution(adc_res);
}

int PicoAnalogCorrection::analogRead()
{
	gpio_put(23, 1); // Disable power-saving
	sleep_us(2);	 // Cooldown for the converter to stabilize?
	int value = adc_read();
	// printf("%d\n", value);
	gpio_put(23, 0); // Re-enable power-saving

	return value;
}

double PicoAnalogCorrection::analogCRead(size_t pin, size_t avg_size)
{
	double value = .0;
	adc_select_input(pin);
	for (size_t i = 0; i < avg_size; i++)
	{
		// value += float(map(analogRead(), _gnd_offset, _vcc_offset, 0, _max_channel));
		value += float(_a * analogRead() + _d);
	}

	return (value / avg_size);
}

double PicoAnalogCorrection::analogNOCRead(size_t pin, size_t avg_size)
{
	int value = 0;
	adc_select_input(pin);
	for (size_t i = 0; i < avg_size; i++)
	{
		// value += float(map(analogRead(), _gnd_offset, _vcc_offset, 0, _max_channel));
		value += analogRead();
	}

	return (value / avg_size);
}

void PicoAnalogCorrection::ADCinit()
{
	stdio_init_all();
	adc_init();
	adc_gpio_init(26);
	adc_gpio_init(27);
	adc_gpio_init(28);
	adc_set_temp_sensor_enabled(false);

	// Configurar el pin 23(GP22)como entrada
	gpio_init(PIN_POWER_SAVE);
	gpio_set_dir(PIN_POWER_SAVE, GPIO_OUT);
	adc_set_clkdiv(100000);
	sleep_ms(1000);
}

// float PicoAnalogCorrection::analogReadTemp(pactemp_t type) {
//     float t = ::analogReadTemp(_vref);

// 	if (type == PAC_F) {
// 		return t * 1.8f + 32.0f;
// 	} else {
// 		return t;
// 	}
// }
