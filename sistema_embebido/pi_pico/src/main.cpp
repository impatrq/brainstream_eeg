
#include <PicoAnalogCorrection.hpp>
#include "hardware/adc.h"
#include "stdio.h"
#include "pico/stdlib.h"

const uint8_t GND_PIN = 0;  // GND meas pin
const uint8_t VCC_PIN = 1;  // VCC meas pin
const uint8_t POT_PIN = 2;  // VCC meas pin
const uint8_t ADC_RES = 12; // ADC bits
const float VREF = 23.3;    // Analog reference voltage
const float conversion_factor = 3.3f / (1 << 12);
// En la teoría va a ir conectado una tensión de 1.2V a la VREF, pero por ahora se queda así
void multiInit(uint8_t first, uint8_t last);
void select_channel(uint8_t channel);
int main()
{
    stdio_init_all();
    sleep_ms(2000);
    char userInput;
    // gpio_init(2);
    multiInit(2, 5);
    select_channel(6);
    PicoAnalogCorrection pico(ADC_RES, VREF);
    // adc_init();
    // adc_gpio_init(26);
    // adc_gpio_init(27);
    // adc_gpio_init(28);
    // adc_set_temp_sensor_enabled(false);
    pico.ADCinit();
    // pico.calibrateAdc(GND_PIN, VCC_PIN, 5000);
    double macarron[16];
    while (true)
    {
        // printf("Offset Values: ");

        // float value = pico.analogCRead(POT_PIN, 500);
        // printf("El valor del número es: %f\n", value);
        // int gola = pico.analogCRead(GND_PIN, 500);
        // int queso = pico.analogCRead(VCC_PIN, 500);
        double startTime = time_us_32();
        for(int i = 0; i<=15;i++){
             macarron[i] = conversion_factor * pico.analogNOCRead(POT_PIN, 50);
            select_channel(i);
            // sleep_us(10);
            // if (macarron[i] > 3.3) macarron[i] = 3;
            // if (macarron[i] < 0.09) macarron[i] = 0;
        }
        // sleep_us(500);
        double endTime = time_us_32();
        int sampling_frequency = 1 / ((endTime - startTime) / 1000000);
        printf("%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%d\r\n", macarron[1],macarron[2],macarron[3],macarron[4],macarron[5],macarron[6],macarron[7],macarron[8],macarron[9],macarron[10],macarron[11],macarron[12],macarron[13],macarron[14],macarron[15],macarron[0], sampling_frequency);
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
    gpio_put(2, (channel >> 3) & 0x01);
    gpio_put(3, (channel >> 2) & 0x01);
    gpio_put(4, (channel >> 1) & 0x01);
    gpio_put(5, (channel)&0x01);
}