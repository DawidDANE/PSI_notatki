#define FCY 16000000UL
#include <libpic30.h>
#include "lcd.h"

void reklama_startowa() {
    LCD_ClearScreen();
    LCD_PutString("Pizzeria tanio@", 16);
    __delay_ms(200);  
}

void przewijaj_napis() {
    const char* tekst = " % Mega rabaty na wszystko!";
    char bufor[17];
    int dl = strlen(tekst);

    while (1) {
        for (int i = 0; i < dl; i++) {
            for (int j = 0; j < 16; j++) {
                bufor[j] = tekst[(i + j) % dl];
            }
            bufor[16] = '\0';
            LCD_ClearScreen();
            LCD_PutString(bufor, 16);
            __delay_ms(250);  
        }
    }
}

int main(void) {
    LCD_Initialize();
    reklama_startowa();
    przewijaj_napis();
    while (1);
    return 0;
}
