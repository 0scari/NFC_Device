// TODO the token needs to be reset when session change
// TODO timeout in the Android app after a scan

#include <SPI.h>
#include "PN532_SPI.h"
#include "PN532.h"
#include "NfcAdapter.h"
#include <LiquidCrystal.h>


String legitToken = "";

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 9, en = 8, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

PN532_SPI interface(SPI, 10); // create a SPI interface for the shield with the SPI CS terminal at digital pin 10
NfcAdapter nfc = NfcAdapter(interface); // create an NFC adapter object

void(* resetFunc) (void) = 0; //declare reset function @ address 0

void lcdPrint (String text, int col, int row)
{
    lcd.begin(16, 2); // set up the LCD's number of columns and rows
    lcd.noDisplay(); // Turn off the display
    delay(500);

    lcd.clear();
    lcd.setCursor(col, row);
    lcd.print(text);
    lcd.setCursor(14, 1);
    lcd.print("CU");

    lcd.display();      // Turn on the display
    delay(1000);
}

String readNDEF()
{
    nfc.begin(); // begin NFC communication
    if (nfc.tagPresent()) { // Do an NFC scan to see if an NFC tag is present
        NfcTag tag = nfc.read(); // read the NFC tag

        if(tag.hasNdefMessage()) {
            NdefMessage message = tag.getNdefMessage();
            for(int i=0;i<message.getRecordCount();i++) {
                NdefRecord record = message.getRecord(i);
                int payloadLength = record.getPayloadLength();
                byte payload[payloadLength];
                record.getPayload(payload);

                String payloadAsString = ""; // Processes the message as a string
                for (int c = 1; c < payloadLength; c++)
                    payloadAsString += (char)payload[c];
                return String(payloadAsString);
            }
        }
    } else
      return legitToken;
}

/*!
 *
 * @param token
 */
void writeNDEF(String token)
{
    bool messageWritten = false;
    nfc.begin(); // begin NFC communication

    while (!messageWritten) {
        if(nfc.tagPresent()) {
            NdefMessage message = NdefMessage();
            message.addUriRecord(token);
            bool success = nfc.write(message);
            if(success) {
                Serial.println("Data was written");
                messageWritten = true;
            } else
                Serial.println("Message write failed.");
        } else
            Serial.println("No NFC Tag");
    }
    nfc.begin(); // resetting NFC communication
}

void setLegitToken()
{
    legitToken = readNDEF();
    Serial.print("legitToken = " + legitToken);
}

void tokenRecoveryProcedure()
{
    lcdPrint("Token recovery", 0, 0);
    writeNDEF(legitToken);
    Serial.println("Token recovered");
    lcdPrint("Tap your phone", 1, 0);
}

void setup(void)
{
    lcdPrint("Setting up...", 0, 0);
    // SERIAL COMM
    Serial.begin(115200); // start serial communication
    Serial.println("Serial communication ON");
    setLegitToken();
    // LCD
    lcdPrint("Tap your phone", 1, 0);
}

void loop(void)
{
    delay(2000);
    if (Serial.available()) {
        String token = Serial.readString();
        Serial.print("received data " + token);
        legitToken = token;
        writeNDEF(token);         // must be completed
    } else {
        String tagToken = readNDEF();
        if (tagToken != legitToken) {
            Serial.println("L: " + legitToken + "C: " + tagToken);
            tokenRecoveryProcedure();
        }
        
    }
    nfc.begin(); // disconnects the tag and antenna
}
