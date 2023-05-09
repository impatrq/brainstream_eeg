#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "esp_system.h"
#include "esp_task_wdt.h"
#include "driver/gpio.h"
#include "driver/uart.h"
#include "esp_timer.h"
#include "string.h"
#include <stdlib.h>
#include "driver/adc.h"
#include "esp_adc_cal.h"

// static esp_adc_cal_characteristics_t adc2_chars;

#define PIN_ENTRADA GPIO_NUM_4
#define I2C_MASTER_SCL_IO 22 // GPIO22 como SCL
#define I2C_MASTER_SDA_IO 21 // GPIO21 como SDA
#define I2C_MASTER_NUM I2C_NUM_0
#define ADS1115_ADDR 0x48 // Dirección del ADS1115
#define portTICK_RATE_MS ((TickType_t)1000 / configTICK_RATE_HZ)
#define S0_PIN GPIO_NUM_26
#define S1_PIN GPIO_NUM_27
#define S2_PIN GPIO_NUM_14
#define S3_PIN GPIO_NUM_12

#define ADS1115_CONV_REG 0x00
#define ADS1115_CONFIG_REG 0x01
#define ADS1115_THRES_LOW_REG 0x02
#define ADS1115_THRES_HIGH_REG 0x03

esp_err_t i2c_master_init()
{
    i2c_config_t conf;
    conf.mode = I2C_MODE_MASTER;
    conf.sda_io_num = I2C_MASTER_SDA_IO;
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    conf.scl_io_num = I2C_MASTER_SCL_IO;
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    conf.master.clk_speed = 400000;
    conf.clk_flags = 0;
    i2c_param_config(I2C_MASTER_NUM, &conf);
    return i2c_driver_install(I2C_MASTER_NUM, conf.mode, 0, 0, 0);
}

void uart_config()
{
    const uart_port_t uart_num = UART_NUM_0;
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .rx_flow_ctrl_thresh = 122,
        .source_clk = UART_SCLK_DEFAULT};
    uart_param_config(uart_num, &uart_config);
    uart_set_pin(UART_NUM_0, 1, 3, -1, -1);
    const int uart_buffer_size = (1024 * 2);
    QueueHandle_t uart_queue;
    uart_driver_install(UART_NUM_0, uart_buffer_size, uart_buffer_size, 10, &uart_queue, 0);
}

// void gpio_init(){
//     gpio_config_t gpioConfig;
//     gpioConfig.mode = GPIO_MODE_OUTPUT;
//     gpioConfig.pull_down_en = GPIO_PULLDOWN_DISABLE;
//     gpioConfig.pull_up_en = GPIO_PULLDOWN_DISABLE;
//     gpioConfig.intr_type = GPIO_INTR_DISABLE;
//     gpioConfig.pin_bit_mask = 1ULL <<  S2_PIN;
//     gpio_set_level(S0_PIN, 1);
//     gpio_config(&gpioConfig);
// }

void multiplexer_sc(int channel)
{
    gpio_config_t gpioConfig;
    gpioConfig.mode = GPIO_MODE_OUTPUT;
    gpioConfig.pull_down_en = GPIO_PULLDOWN_DISABLE;
    gpioConfig.pull_up_en = GPIO_PULLDOWN_DISABLE;
    gpioConfig.intr_type = GPIO_INTR_DISABLE;

    if (channel < 0 || channel > 15)
    {
        printf("Invalid channel number %d\n", channel);
    }
    gpioConfig.pin_bit_mask = 1ULL << S0_PIN;
    gpio_config(&gpioConfig);
    gpio_set_level(S0_PIN, (channel >> 3) & 0x01); // x000

    gpioConfig.pin_bit_mask = 1ULL << S1_PIN;
    gpio_config(&gpioConfig); // 0x00
    gpio_set_level(S1_PIN, (channel >> 2) & 0x01);

    gpioConfig.pin_bit_mask = 1ULL << S2_PIN;
    gpio_config(&gpioConfig); // 00x0
    gpio_set_level(S2_PIN, (channel >> 1) & 0x01);

    gpioConfig.pin_bit_mask = 1ULL << S3_PIN;
    gpio_config(&gpioConfig); // 000x
    gpio_set_level(S3_PIN, channel & 0x01);
    return;
}

// void threshold_register(){

//     i2c_cmd_handle_t cmd = i2c_cmd_link_create();
//     i2c_master_start(cmd);
//     i2c_master_write_byte(cmd, ADS1115_ADDR << 1 | I2C_MASTER_WRITE, true);
//     i2c_master_write_byte(cmd, ADS1115_THRES_HIGH_REG, true);
//     i2c_master_write_byte(cmd, 0xff, true);
//     i2c_master_write_byte(cmd, 0xff, true);
//     i2c_master_stop(cmd);
//     i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, 1 / portTICK_RATE_MS);
//     i2c_cmd_link_delete(cmd);

//     cmd = i2c_cmd_link_create();
//     i2c_master_start(cmd);
//     i2c_master_write_byte(cmd, ADS1115_ADDR << 1 | I2C_MASTER_WRITE, true);
//     i2c_master_write_byte(cmd, ADS1115_THRES_LOW_REG, true);
//     i2c_master_write_byte(cmd, 0x00, true);
//     i2c_master_write_byte(cmd, 0x00, true);
//     i2c_master_stop(cmd);
//     i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, 1 / portTICK_RATE_MS);
//     i2c_cmd_link_delete(cmd);

// }

int16_t read_ads1115(uint8_t channel)
{
    // Config register
    // channel = channel << 4;
    uint8_t data[2]; // Se crean 2 variables de 2 bytes
    // i2c_cmd_handle_t cmd = i2c_cmd_link_create(); // Estructura que configura al i2c
    // i2c_master_start(cmd);                                                  // Se inicia la comunicacion con el ads
    // i2c_master_write_byte(cmd, ADS1115_ADDR << 1 | I2C_MASTER_WRITE, true); // se configura para que el addr sea masa (luego seran los distintos modulos)
    // i2c_master_write_byte(cmd, ADS1115_CONFIG_REG, true);                   // Entrar al registro de configuracion
    // i2c_master_write_byte(cmd, 0b11000101 | channel, true);                 // Configuración: modo de operación continuo, ganancia 1, modo de medición de un solo canal
    // i2c_master_write_byte(cmd, 0b11101010, true);                           // Configurar la entrada analógica y comenzar una conversión 10010000
    // i2c_master_stop(cmd);                                                   // Salir los registros de configuracion
    // i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, 1 / portTICK_RATE_MS);        // Se envia el comando y se espera una respuesta
    // i2c_cmd_link_delete(cmd);                                               // borra el comando para ahorrar espacio y recibir info nueva                                         // Esperar a que la conversión se complete

    // while ((gpio_get_level(GPIO_NUM_4)))
    //     ;
    // for (int i = 0; i < 400; i++)
    // {
    //     vTaskDelay(1 / portTICK_RATE_MS);
    // }
    // do
    // {
    //     i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    //     i2c_master_start(cmd);
    //     i2c_master_write_byte(cmd, ADS1115_ADDR << 1 | I2C_MASTER_READ, true);
    //     i2c_master_write_byte(cmd, ADS1115_CONFIG_REG, true);
    //     i2c_master_read_byte(cmd, &data[1], true);
    //     i2c_master_read_byte(cmd, &data[0], true);
    //     i2c_master_stop(cmd); // Se lee una parte del registro de la medicion y se guarda en la variable Data
    //     i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, 1 / portTICK_RATE_MS);
    //     i2c_cmd_link_delete(cmd);
    // } while (!(data[1] & (1 << 7)));

    i2c_cmd_handle_t cmd = i2c_cmd_link_create();                           // Se crea un nuevo comando para leer los datos
    i2c_master_start(cmd);                                                  // Se inicia la comunicacion con el ads
    i2c_master_write_byte(cmd, ADS1115_ADDR << 1 | I2C_MASTER_WRITE, true); // Se configura para que el addr sea masa (luego seran los distintos modulos)
    i2c_master_write_byte(cmd, ADS1115_CONV_REG, true);                     // Se accede a al registro de lectura
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, ADS1115_ADDR << 1 | I2C_MASTER_READ, true);
    i2c_master_read_byte(cmd, &data[1], true); // Se lee una parte del registro de la medicion y se guarda en la variable Data
    i2c_master_read_byte(cmd, &data[0], true); // ´´´´´´´´´´
    i2c_master_stop(cmd);
    i2c_master_cmd_begin(I2C_MASTER_NUM, cmd, 1 / portTICK_RATE_MS);
    i2c_cmd_link_delete(cmd);
    return (data[1] << 8) | data[0]; // Devuelve la lectura como un entero de 16 bits
}

// void time(void)
// {
//     uint64_t start_time = esp_timer_get_time();
//     int16_t value = read_ads1115(0);
//     int16_t value_1 = read_ads1115(1);
//     int16_t value_2 = read_ads1115(2);
//     int16_t value_3 = read_ads1115(3);
//     uint64_t end_time = esp_timer_get_time();
//     printf("Tiempo de ejecución: %lld uS\t", (end_time - start_time));
//         printf("Valor 0: %d\t",  value);
//         printf("Valor 1: %d\t",  value_1);
//         printf("Valor 2: %d\t",  value_2);
//         printf("Valor 3: %d\n",  value_3);
// }

void app_main()
{
    // uint32_t values;
    uint32_t voltage[3];
    static esp_adc_cal_characteristics_t adc1_chars;
    esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_DEFAULT, 0, &adc1_chars);
    ESP_ERROR_CHECK(adc1_config_width(ADC_WIDTH_BIT_DEFAULT));
    ESP_ERROR_CHECK(adc1_config_channel_atten(ADC1_CHANNEL_4, ADC_ATTEN_DB_11));
    // i2c_master_init();
    uart_config();
    // threshold_register();
    esp_task_wdt_delete(xTaskGetIdleTaskHandleForCPU(0));
    // gpio_init();
    //  char* test_str = "This is a test string.\n";

    // multiplexer_sc(0);
    while (1)
    {

        uint64_t start_time = esp_timer_get_time();
        for (int y = 0; y < 3; y++)
        {
            uint32_t average[50];
            multiplexer_sc(y);
            average[0] = adc1_get_raw(ADC1_CHANNEL_4);

            for (int i = 1; i < 50; i++)
            {
                // multiplexer_sc(i);
                // vTaskDelay(1 / portTICK_RATE_MS);

                average[i] = average[i - 1] + esp_adc_cal_raw_to_voltage(adc1_get_raw(ADC1_CHANNEL_4), &adc1_chars);
                //     // adc2_get_raw(ADC2_CHANNEL_0, ADC_WIDTH_BIT_12, &array[i]);
                //     // vTaskDelay(1 / portTICK_RATE_MS);
            }
            voltage[y] = average[49] / 50;
        }
        uint64_t end_time = esp_timer_get_time();
        //printf("Tiempo de ejecución: %lld uS\t", (end_time - start_time));
        // //  uint64_t start_time = esp_timer_get_time();
        // // int16_t value = read_ads1115(0);
        // // // int16_t value_1 = read_ads1115(1);
        // // // int16_t value_2 = read_ads1115(2);
        // // // int16_t value_3 = read_ads1115(3);
        // uint64_t end_time = esp_timer_get_time();
        // uint64_t dif_time = end_time - start_time;
        char str[5];
        sprintf(str, "%d\t", voltage[0]);
        uart_write_bytes(UART_NUM_0, str, sizeof(str));
        sprintf(str, "%d\t", voltage[1]);
        uart_write_bytes(UART_NUM_0, str, sizeof(str));
        sprintf(str, "%d\n\r", voltage[2]);
        uart_write_bytes(UART_NUM_0, str, sizeof(str));
        // printf("Valor 1: %d\t", voltage[1]);
        // printf("Valor 2: %d\t", voltage[2]);
        // printf("Valor 3: %d\n", voltage[3]);
        // printf("Tiempo de ejecución: %lld uS\t\n", (end_time - start_time));
        // // time();                                    // Leer del canal 0 0 = y 1 = x
        // float voltage = (((float)value+128)* 5) / 128;
    }
}