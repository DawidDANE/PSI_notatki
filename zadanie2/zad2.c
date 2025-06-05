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

void konfiguracjaSystemu(void) {
    ADC_SetConfiguration(ADC_CONFIGURATION_DEFAULT);
    ADC_ChannelEnable(ADC_CHANNEL_POTENTIOMETER);
    TRISA = 0x0000;
    BUTTON_Enable(BUTTON_S3);
    BUTTON_Enable(BUTTON_S4);
}

int main(void) {
    konfiguracjaSystemu();

    unsigned char licznik = 0x00;
    unsigned char tryb = 1;
    unsigned long wartoscADC;
    unsigned long opoznienie_ms;
    unsigned char zakres;
    const unsigned char wzorzec[] = {
        0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,
        0x81,0x82,0x84,0x88,0x90,0xA0,0xC0,0xC1,
        0xC2,0xC4,0xC8,0xD0,0xE0,0xE1,0xE2,0xE4,
        0xE8,0xF0,0xF1,0xF2,0xF4,0xF8,0xF9,0xFA,
        0xFC,0xFD,0xFE,0xFF
    };
    int indeks = 0;

    while (1) {
        wartoscADC = ADC_Read10bit(ADC_CHANNEL_POTENTIOMETER);

        zakres = wartoscADC / 204;

        switch (zakres) {
            case 0: opoznienie_ms = 130000; break;
            case 1: opoznienie_ms = 400000; break;
            case 2: opoznienie_ms = 1200000; break;
            case 3: opoznienie_ms = 1700000; break;
            case 4: opoznienie_ms = 2800000; break;
        }

        switch (tryb) {
            case 1:
                LATA = licznik;
                licznik++;
                break;
            case 2:
                LATA = wzorzec[indeks % (sizeof(wzorzec) / sizeof(wzorzec[0]))];
                indeks++;
                break;
        }

        __delay32(opoznienie_ms);

        if (BUTTON_IsPressed(BUTTON_S3)) {
            __delay32(1000);
            tryb = 1;
        }

        if (BUTTON_IsPressed(BUTTON_S4)) {
            __delay32(1000);
            tryb = 2;
        }
    }

    return 0;
}
