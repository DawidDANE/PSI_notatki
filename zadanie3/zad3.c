#pragma config POSCMOD = XT
#pragma config OSCIOFNC = ON
#pragma config FCKSM = CSDCMD
#pragma config FNOSC = PRI
#pragma config IESO = ON

#pragma config WDTPS = PS32768
#pragma config FWPSA = PR128
#pragma config WINDIS = ON
#pragma config FWDTEN = ON
#pragma config ICS = PGx2
#pragma config GWRP = OFF
#pragma config GCP = OFF
#pragma config JTAGEN = OFF

#include "xc.h"
#include "libpic30.h"
#include "adc.h"
#include "buttons.h"

#define LEDS        LATA
#define LED_SINGLE  0x01
#define POT_LIMIT   512
#define BLINK_TIME  2000000UL

void init_hardware(void) {
    TRISA = 0x0000;  
    ADC_SetConfiguration(ADC_CONFIGURATION_DEFAULT);
    ADC_ChannelEnable(ADC_CHANNEL_POTENTIOMETER);
    BUTTON_Enable(BUTTON_S3);  
    BUTTON_Enable(BUTTON_S4);  
}

int is_alarm_reset(void) {
    return ADC_Read10bit(ADC_CHANNEL_POTENTIOMETER) <= POT_LIMIT || BUTTON_IsPressed(BUTTON_S3);
}

void warning_blink(void) {
    for (int count = 0; count < 5; count++) {
        if (is_alarm_reset() || BUTTON_IsPressed(BUTTON_S4)) {
            LEDS = 0x00;
            return;
        }
        LEDS = LED_SINGLE;
        __delay32(BLINK_TIME);
        LEDS = 0x00;
        __delay32(BLINK_TIME);
    }
}

int main(void) {
    init_hardware();

    int alarm_active = 0;

    while (1) {
        unsigned int pot_reading = ADC_Read10bit(ADC_CHANNEL_POTENTIOMETER);

        
        if (pot_reading > POT_LIMIT && !alarm_active) {
            warning_blink();  
            pot_reading = ADC_Read10bit(ADC_CHANNEL_POTENTIOMETER);
            if (pot_reading > POT_LIMIT && !BUTTON_IsPressed(BUTTON_S4)) {
                alarm_active = 1;
            }
        }

        
        if (alarm_active) {
            LEDS = 0xFF;
        } else {
            LEDS = 0x00;
        }

        
        if (alarm_active && is_alarm_reset()) {
            __delay32(200000); 
            alarm_active = 0;
            LEDS = 0x00;
        }
    }

    return 0;
}
