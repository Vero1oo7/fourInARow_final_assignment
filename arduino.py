import serial


class Arduino:

    def __init__(self):
        self.arduino = serial.Serial("COM6", 9600) # establish serial communication

    def arduino_com_AI(self, r, c): # send data to arduino to turn on the AI LEDs
        self.arduino.write(b'Z')
        self.arduino.write(chr(r).encode())
        self.arduino.write(b'L')
        self.arduino.write(chr(c).encode())

    def arduino_com_PLAYER(self, r, c):# send data to arduino to turn on the player LEDs
        self.arduino.write(b'A')
        self.arduino.write(chr(r).encode())
        self.arduino.write(b'L')
        self.arduino.write(chr(c).encode())

    def arduino_receive(self): # receive data from arduino ( for button)
        if self.arduino.inWaiting() > 0:
            my_data = self.arduino.readline().decode("utf-8")
            my_data = int(my_data)
            return my_data



#/////////////ARDUINO CODE///////////////////
"""//7 LED strips with 6 LEDs turning on the LED for the move send from python
#include <FastLED.h>
#define NUM_LEDS_PER_STRIP 6

CRGB leds1[NUM_LEDS_PER_STRIP];
CRGB leds2[NUM_LEDS_PER_STRIP];
CRGB leds3[NUM_LEDS_PER_STRIP];
CRGB leds4[NUM_LEDS_PER_STRIP];
CRGB leds5[NUM_LEDS_PER_STRIP];
CRGB leds6[NUM_LEDS_PER_STRIP];
CRGB leds7[NUM_LEDS_PER_STRIP];
int i;
int r;
int buttonState = 0;

//values for the colours
int blueR = 0;
int blueG = 0;
int blueB = 50;
int greenR = 0;
int greenG = 50;
int greenB = 0;
int color1;
int color2;
int color3;

const int buttonPin = 2;

void setup() {
  Serial.begin(9600);
  //
  FastLED.addLeds<WS2812, 3, GRB>(leds1, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812, 4, GRB>(leds2, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812, 5, GRB>(leds3, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812, 6, GRB>(leds4, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812, 7, GRB>(leds5, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812, 8, GRB>(leds6, NUM_LEDS_PER_STRIP);
  FastLED.addLeds<WS2812, 9, GRB>(leds7, NUM_LEDS_PER_STRIP);
  
  pinMode(buttonPin, INPUT);
  
  for (int i = 0; i < 6; i++) {
    //turn all LEDs off at the beginning
    color1 = 0;
    color2 = 0;
    color3 = 0;
    leds1[i] = CRGB(color1, color2, color3);
    leds2[i] = CRGB(color1, color2, color3);
    leds3[i] = CRGB(color1, color2, color3);
    leds4[i] = CRGB(color1, color2, color3);
    leds5[i] = CRGB(color1, color2, color3);
    leds6[i] = CRGB(color1, color2, color3);
    leds7[i] = CRGB(color1, color2, color3);
    FastLED.show();
  }
}

void loop() {
  if (Serial.available() > 0) {
    uint8_t  serialdata = Serial.read();
    if (serialdata == 'Z' || serialdata == 'A') { 
      if (serialdata == 'Z') { //the AI colour
        color1 = blueR;
        color2 = blueG;
        color3 = blueB;
      }
      else {  //the player colour
        color1 = greenR;
        color2 = greenG;
        color3 = greenB;
      }
      int i = getNextInput(); //the row 
      if (getNextInput() == 'L') { 
        int c = getNextInput(); //the column
        //show for the combination of row and column the correct colour of LED
        if (c == 0) {
          leds1[i] = CRGB(color1, color2, color3);
          FastLED.show();
          delay(50);
        }
        if (c == 1) {
          leds2[i] = CRGB(color1, color2, color3);
          FastLED.show();
          delay(50);
        }
        if (c == 2) {
          leds3[i] = CRGB(color1, color2, color3);
          FastLED.show();
          delay(50);
        }
        if (c == 3) {
          leds4[i] = CRGB(color1, color2, color3);
          FastLED.show();
          delay(50);
        }
        if (c == 4) {
          leds5[i] = CRGB(color1, color2, color3);
          FastLED.show();
          delay(50);
        }
        if (c == 5) {
          leds6[i] = CRGB(color1, color2, color3);
          FastLED.show();
          delay(50);
        }
        if (c == 6) {
          leds7[i] = CRGB(color1, color2, color3);
          FastLED.show();
          delay(50);
        }
        if (c == 10) { //in case of win
          delay(1000); //show winning move
          //show entire board in colour of the winner
          for (int i = 0; i < 6; i++) {
            leds1[i] = CRGB(color1, color2, color3);
            FastLED.show();
            delay(50);
            leds2[i] = CRGB(color1, color2, color3);
            FastLED.show();
            delay(50);
            leds3[i] = CRGB(color1, color2, color3);
            FastLED.show();
            delay(50);
            leds4[i] = CRGB(color1, color2, color3);
            FastLED.show();
            delay(50);
            leds5[i] = CRGB(color1, color2, color3);
            FastLED.show();
            delay(50);
            leds6[i] = CRGB(color1, color2, color3);
            FastLED.show();
            delay(50);
            leds7[i] = CRGB(color1, color2, color3);
            FastLED.show();
            delay(50);
          }
        }
      }
    }
  }
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    //send value to python
    Serial.println(String(buttonState));
    delay(1000);
    Serial.flush();
  }
}
uint8_t getNextInput() {
  while (!Serial.available()); // wait for a character
  return Serial.read();
}"""