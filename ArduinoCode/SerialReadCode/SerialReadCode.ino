#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUMPIXELS 16
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

/*
Class for the rotatry Indexor
*/

class RotaryIndexor
{
  public:
    RotaryIndexor(int ChipSelect , int Rotationa , int Rotationb , int PushedButton);
    void Update();
    int Rotations();
    bool Button();
  private:
    
    int _PreviousState;
    int _ChipSelectPin;
    int _RotationaPin;
    int _RotationbPin;
    int _PushedButtonPin;
    bool _PushedButtonState;
    int _Rotations;

};

RotaryIndexor::RotaryIndexor(int ChipSelect , int Rotationa , int Rotationb , int PushedButtonPin)
{
  pinMode(ChipSelect , OUTPUT);
  int _ChipSelectPin = ChipSelect;
  int _RotationaPin = Rotationa;
  int _RotationbPin = Rotationb;
  int _PushedButtonPin = PushedButtonPin;
}

void RotaryIndexor::Update()
{
  //Updates all of the varibles. DOES NOT RETURN ANYTHING.
  digitalWrite(_ChipSelectPin , HIGH);
  

  if (digitalRead(_RotationaPin)):
    {
      CurrentScore += 1;
    }
  if (digitalRead(_RotationbPin)):
  {
    CurrentScore += 2;
  }
  if (CurrentScore - _PreviousState == 1 || CurrentScore - _PreviousState == -3):
  {
    _Rotations = _Rotations + 1;
  }
  else if(CurrentScore = _PreviousState):
  {
    ;
  }
  else
  {
    _Rotations = _Rotations - 1
  }

  digitalWrite(_ChipSelectPin , LOW)
  

}

int RotaryIndexor::Rotations()
{
  //Takes the Rotation out of the Rotations varible AND resets it.
  temp = _Rotations
  _Rotations = 0
  return _Rotations
}

bool RotaryIndexor::Button()
{
  //Takes the Button State and prints it.
  return _PushedButtonState
}

String MsgIn = ""; 


bool MessageDecoder(String Msg)
{
  //The code that decodes the message coming from the arduino.
  
  if (Msg.endsWith("$"))
  {
    Serial.println("Message ends wirh $");
    int Length = Msg.length();
    if (Length == 1)
    {
      
      return true;
    }
    if (Length%4 == 0)
    {
      Serial.print("Here");
      int NumberToWriteOut = Length /12 ;
      for(int i = 0; i<NumberToWriteOut; i++)
      {
        String LedString = Msg.substring(i * 12 ,i*12 + 12);
        Serial.print("Led String");
        Serial.println(LedString.substring(0,11));
        int Red = LedString.substring(0,3).toInt();
        int Green = LedString.substring(4,7).toInt();
        int Blue = LedString.substring(8,11).toInt();
        pixels.setPixelColor(i, pixels.Color(Red,Green,Blue));
        Serial.print(Red);
        Serial.print(" ");
        Serial.print(Green);
        Serial.print(" ");
        Serial.println(Blue);
      }
      pixels.show();
      delay(10);
    }
    return true;
  }
  else
  {
    return false;
  }
}


/*
I should put the varibles here



*/

RotorA RotaryIndexor(1,2,3,4);



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  
  RotorA.Update()

}

void loop() {
  RotarA.Update();
  while (Serial.available() > 0) {
    char inChar = Serial.read();
    MsgIn += inChar;
  }
  if (MessageDecoder(MsgIn))
  {
    Serial.println(MsgIn);
    Serial.println("ShouldBeWorking");
    MsgIn = "";
    Serial.flush();
  }
  Serial.flush();
  
  
}
