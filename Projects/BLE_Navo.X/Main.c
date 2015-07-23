/* 
 */
#define _SUPPRESS_PLIB_WARNING 1
#define LOOP_MAX 4000000

#include <p32xxxx.h>
#include <plib.h>
#include <stdint.h>
#include "HMain.h"
#include <math.h>
//config
#pragma config FPLLMUL = MUL_20, FPLLIDIV = DIV_2, FPLLODIV = DIV_2
#pragma config POSCMOD = HS, FNOSC = PRIPLL, FPBDIV = DIV_1
#pragma config FWDTEN = OFF
#pragma config FSOSCEN = OFF
#pragma config WDTPS = PS4
#pragma config CP=OFF, BWP=OFF
#pragma config FCKSM = CSDCMD
#pragma config ICESEL   = ICS_PGx1      // ICE/ICD Comm Channel Select
#pragma config JTAGEN = OFF
//USB
#pragma config FUSBIDIO = OFF
#pragma config FVBUSONIO = OFF

#define PC_REC_RATE 0.95
#define TW_OUT_RATE 0.045

unsigned char OS_Str_1[64];
int g, Rx1, Rx2;
//#=================================================================================================
//#=================================================================================================
int __attribute__((section("XCodeMain"))) main( void ) {
    Tweeq_Init();

    _TRISB5 = 1;
    U2RXRbits.U2RXR = 1; //
    RPB10Rbits.RPB10R = 2; //
    //U2BRG = (SYS_FREQ/17/(9600));
    UARTSetDataRate(UART2, SYS_FREQ, 9600);
    U2MODE = UART_EN;
    U2STA = (UART_RX_ENABLE | UART_TX_ENABLE);

    mOLED_Init();
    mOLED_Clear();

    mOLED_Print_Str(0, 0, "HELLO WORLD!");

    mOLED_Refresh();
    
    i2c_Init();
    MPU_SetAddr(0x68);
    MPU_Init();
    
    mOLED_Print_Str(0,1, "MPU Init!");
    
    mOLED_Refresh();
    
    Delayms(2000);
    
    int MPU_Transmit = 1;

    g = 0;
    int pos=0;
    int X,Y,Z;
    int count=0, avgcount=0;
    int Xg=0,Yg=0,Zg=0;
    
    int waitperiod = (int)(PC_REC_RATE/TW_OUT_RATE)*4000;
    
    while(1)    
    {
//        
//        Rx1 = COMM1_Rx(); //COMM1 is computer, COMM2 is the BLE Module
//        if (Rx1 >= 0)
//        {
//            COMM2_Tx(Rx1);
//        }
//
//        Rx2 = COMM2_Rx();
//        if (Rx2 >= 0)
//        {
//            COMM1_Tx(Rx2);
//        }
        
        if (g % 100 == 0)
        {
            count++;
            if(g%waitperiod!=0){
                int X2,Y2,Z2,Xg2,Yg2,Zg2;
                
                avgcount++;
                
                X2 = (int16_t) MPU_Read_X();
                Y2 = (int16_t) MPU_Read_Y();
                Z2 = (int16_t) MPU_Read_Z();
                
                if(count==1) {
                    Xg2 = X2;
                    Yg2 = Y2;
                    Zg2 = Z2;
                }
                else if(count<10) {
                    Xg2 = ((Xg2*(count-1))+X2)/count;
                    Yg2 = ((Yg2*(count-1))+Y2)/count;
                    Zg2 = ((Zg2*(count-1))+Z2)/count;                    
                }

                X = ((X*avgcount)+X2)/(avgcount+1);
                Y = ((Y*avgcount)+Y2)/(avgcount+1);
                Z = ((Z*avgcount)+Z2)/(avgcount+1);
                Xg = ((Xg*avgcount)+Xg2)/(avgcount+1);
                Yg = ((Yg*avgcount)+Yg2)/(avgcount+1);
                Zg = ((Zg*avgcount)+Zg2)/(avgcount+1);
                
                if((g+1)%waitperiod==0) {
                    sprintf(OS_Str_1, "ax=%d&ay=%d&az=%d&xg=%d&yg=%d&zg=%dn",X2,Y2,Z2,Xg2,Yg2,Zg2);
                    COMM1_Tx_Str(OS_Str_1);
                    COMM2_Tx_Str(OS_Str_1);
                }
            }
            else
            {
                avgcount=0;
                if(MPU_Transmit!=0)
                {
                    X = (int16_t) MPU_Read_X();
                    Y = (int16_t) MPU_Read_Y();
                    Z = (int16_t) MPU_Read_Z();

                    if(count==1) {
                        Xg = X;
                        Yg = Y;
                        Zg = Z;
                    }
                    else if(count<10) {
                        Xg = ((Xg*(count-1))+X)/count;
                        Yg = ((Yg*(count-1))+Y)/count;
                        Zg = ((Zg*(count-1))+Z)/count;                    
                    }

                    sprintf(OS_Str_1, "ax=%d&ay=%d&az=%d&xg=%d&yg=%d&zg=%dn",X,Y,Z,Xg,Yg,Zg);
                    COMM1_Tx_Str(OS_Str_1);
                    COMM2_Tx_Str(OS_Str_1);
                }
            }
        }
        if (g == LOOP_MAX/2)
        {
            LED_HIGH;
        }
        if (g == LOOP_MAX)
        {
            LED_LOW;
            g = 0;
        }
        g = g + 1;
    }

    return (EXIT_SUCCESS);
}
//#=================================================================================================
//#=================================================================================================
