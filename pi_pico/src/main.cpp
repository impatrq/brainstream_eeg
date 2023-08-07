
#include <PicoAnalogCorrection.hpp>
#include "hardware/adc.h"
#include "stdio.h"
#include "pico/stdlib.h"

const uint8_t GND_PIN = 0;  // GND meas pin
const uint8_t VCC_PIN = 1;  // VCC meas pin
const uint8_t POT_PIN = 2;  // VCC meas pin
const uint8_t ADC_RES = 12; // ADC bits
const float VREF = 1.23;    // Analog reference voltage
const float conversion_factor = 1.23f / (1 << 12);
// En la teoría va a ir conectado una tensión de 1.2V a la VREF, pero por ahora se queda así
void multiInit(uint8_t first, uint8_t last);
void select_channel(uint8_t channel);
int main()
{
    stdio_init_all();
    sleep_ms(2000);
    char userInput;
    gpio_init(2);
    multiInit(2, 5);
    select_channel(6);
    PicoAnalogCorrection pico(ADC_RES, VREF);
    // adc_init();
    // adc_gpio_init(26);
    // adc_gpio_init(27);
    // adc_gpio_init(28);
    // adc_set_temp_sensor_enabled(false);
    pico.ADCinit();
    pico.calibrateAdc(GND_PIN, VCC_PIN, 5000);
    while (true)
    {
        // printf("Offset Values: ");

        // float value = pico.analogCRead(POT_PIN, 500);
        // printf("El valor del número es: %f\n", value);
        // int gola = pico.analogCRead(GND_PIN, 500);
        // int queso = pico.analogCRead(VCC_PIN, 500);
        double startTime = time_us_32();
        double macarron = conversion_factor * pico.analogNOCRead(POT_PIN, 50);
        sleep_ms(2);
        double endTime = time_us_32();
        int sampling_frequency = 1 / ((endTime - startTime) / 1000000);
        printf("%g\t%d\r\n", macarron, sampling_frequency);
    }
    // while (1)
    // {
    //     userInput = getchar();

    //     // printf("22");
    //     // sleep_ms(1000);
    //     while (true)
    //     {
    //         printf("quesooooooooo");
    //         sleep_ms(1000);
    //     }

    //     printf("quesooooooooo", userInput);
    // }
    // delay(1000);
}

void multiInit(uint8_t first, uint8_t last)
{
    for (int i = first; i <= last; i++)
    {
        gpio_init(i);
        gpio_set_dir(i, GPIO_OUT);
        gpio_put(i, 0);
    }
}
void select_channel(uint8_t channel)
{
    gpio_put(5, (channel >> 3) & 0x01);
    gpio_put(4, (channel >> 2) & 0x01);
    gpio_put(3, (channel >> 1) & 0x01);
    gpio_put(2, (channel)&0x01);
}