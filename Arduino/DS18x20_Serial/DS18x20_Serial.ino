#include <OneWire.h>

// Based on OneWire DS18S20, DS18B20, DS1822 Temperature Example http://www.pjrc.com/teensy/td_libs_OneWire.html
// Used onewire lib (see arduino library manager "OneWire" by Paul Stoffregen

OneWire  ds(10);  // on pin 10 (a 4.7K resistor is necessary)

void setup(void) {
  Serial.begin(9600);
}
bool initDone=false;
int rdelay=1000;
void loop(void) {
  byte i;
  byte present = 0;
  byte type_s;
  byte data[9];
  byte addr[8];
  float celsius, fahrenheit;
  String adr=String();
  
  if ( !ds.search(addr)) {    
    initDone=true;
   // Serial.println("No more addresses.");
    //Serial.println();
    ds.reset_search();
    delay(250);    
    return;
  }

//  Serial.print("R");
  for( i = 0; i < 8; i++) {
     //Serial.write(' ');
     //Serial.print(addr[i], HEX);
     adr += String(addr[i],HEX);
  }
  
  if (OneWire::crc8(addr, 7) != addr[7]) {
      //Serial.println("CRC is not valid!");
      return;
  }  

 
  // the first ROM byte indicates which chip
  switch (addr[0]) {
    case 0x10:
      //Serial.println("  Chip = DS18S20");  // or old DS1820
      type_s = 1;
      break;
    case 0x28:
      //Serial.println("  Chip = DS18B20");
      type_s = 0;
      break;
    case 0x22:
      ///Serial.println("  Chip = DS1822");
      type_s = 0;
      break;
    default:
      //Serial.println("Device is not a DS18x20 family device.");
      return;
  } 

  ds.reset();
  ds.select(addr); 
  ds.write(0x44, 0); //start conversion (transfer temperature into scratchpad memory)        
  
  delay(rdelay); // wait for conversion to happen      
  
  present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);         // Read Scratchpad

  //Serial.print("  Data = ");
  //Serial.print(present, HEX);
  //Serial.print(" ");
  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds.read();
    //Serial.print(data[i], HEX);
    //Serial.print(" ");
  }
  //Serial.print(" CRC=");
  //Serial.print(OneWire::crc8(data, 8), HEX);
  //Serial.println();
  byte cfg;
  // Convert the data to actual temperature
  // because the result is a 16 bit signed integer, it should
  // be stored to an "int16_t" type, which is always 16 bits
  // even when compiled on a 32 bit processor.
  int16_t raw = (data[1] << 8) | data[0];
  if (type_s) {
    raw = raw << 3; // 9 bit resolution default
    if (data[7] == 0x10) {
      // "count remain" gives full 12 bit resolution
      raw = (raw & 0xFFF0) + 12 - data[6];
    }
  } else {
    cfg= (data[4] & 0x60);
    // at lower res, the low bits are undefined, so let's zero them
    if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
    else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
    else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    //// default is 12 bit resolution, 750 ms conversion time
  }
  celsius = (float)raw / 16.0;
  fahrenheit = celsius * 1.8 + 32.0;
  Serial.print(adr);
  Serial.print("R");
  Serial.print(cfg, HEX);
  Serial.print("T");
  Serial.print(celsius);
  Serial.println("C");    
  if(cfg!=0x20 && !initDone){ // if resolution is different (e.g. too high) and also total scan is not finished
     // set resolution of temp sensor to lower value     
     ds.reset();
     ds.select(addr);
     Serial.println("Xconfigure it");    
     ds.write(0x4e); //write scratchpad
     ds.write(0x00); //TH
     ds.write(0x00); //TL
     ds.write(0x3f); //config
     delay(100);   
  }else{     
     rdelay=200; // if every one is configured to lower resolution the read time is faster, so 
  }
}
