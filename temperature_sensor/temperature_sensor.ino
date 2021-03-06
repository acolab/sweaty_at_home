#include <OneWire.h>
#include <VirtualWire.h>

//#define Debug // Uncomment to debug via serial


OneWire  ds(2);  // Thermal sensor data pin (With a pull_up resistor)
const int transmit_pin = 12; // RF Emitter pin
char msg[2]; /* Char table sent by the Arduino (or
            barebone ATMega) to the Raspberry Pi through RF*/

int ambiante; // Temp that will be sent to the Raspberry Pi

void setup() {
#ifdef Debug
  Serial.begin(9600); // Debug only
#endif
  vw_set_tx_pin(transmit_pin); // RF pin setup
  vw_setup(2000); // RF speed (in bauds per second)
}

void loop() {
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  float celsius/*, fahrenheit*/;
  
  if ( !ds.search(addr)) {
#ifdef Debug
    Serial.println();
#endif
    ds.reset_search();
    delay(250);
    return;
  }
  
  if (OneWire::crc8(addr, 7) != addr[7]) {
#ifdef Debug
    Serial.println("CRC is not valid!");
#endif
      return;
  }
#ifdef Debug
  Serial.println();
 #endif
 
  // the first ROM byte indicates which chip
  switch (addr[0]) {
    case 0x10:
#ifdef Debug
      Serial.println("  Chip = DS18S20");  // or old DS1820
#endif
      type_s = 1;
      break;
    case 0x28:
#ifdef Debug
      Serial.println("  Chip = DS18B20");
#endif
      type_s = 0;
      break;
    case 0x22:
#ifdef Debug
      Serial.println("  Chip = DS1822");
#endif
      type_s = 0;
      break;
    default:
#ifdef Debug
      Serial.println("Device is not a DS18x20 family device.");
#endif
      return;
  } 

  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1);        // start conversion, with parasite power on at the end
  
  delay(1000);     // maybe 750ms is enough, maybe not
  // we might do a ds.depower() here, but the reset will take care of it.
  
  present = ds.reset();
  ds.select(addr);    
  ds.write(0xBE);         // Read Scratchpad

  for ( i = 0; i < 9; i++) {           // we need 9 bytes
    data[i] = ds.read();
  }

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
    byte cfg = (data[4] & 0x60);
    // at lower res, the low bits are undefined, so let's zero them
    if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
    else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
    else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
    //// default is 12 bit resolution, 750 ms conversion time
  }
  celsius = (float)raw / 16.0;

#ifdef Debug
  Serial.print("  Temperature = ");
  Serial.print(celsius);
  Serial.print(" Celsius, ");
#endif
  
//  Modify the temperature value to make it sendable through VirtualWire
  ambiante = (int)(100*celsius);

  msg[0] = ambiante >> 8; // Higher byte
  msg[1] = ambiante & 0xFF; // Lower byte
  
  vw_send((uint8_t *)msg, 2);
  vw_wait_tx(); // Wait until the whole message is gone
  
  delay(2000);
}
