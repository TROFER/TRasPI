#include <IRremote.h>
int IR_RECEIVE_PIN = 11;
const uint8_t NEC_KHZ = 38;

const byte numChars = 32;
char receivedChars[numChars];

boolean newData = false;

void setup() {
    Serial.begin(9600);
    Serial.println("<READY>");
    IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK);
}

void loop() {
    recvWithStartEndMarkers();
    showNewData();
}

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;
 
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

void send(uint16_t* data, const size_t size) {
    IrSender.sendRaw(data, size, NEC_KHZ);
}

void receive() {
    while (true) {
        if (IrReceiver.decode()) {
            IrReceiver.compensateAndPrintIRResultAsCArray(&Serial, true);
            IrReceiver.resume();
            break;
        }
    }
}

void showNewData() {
    if (newData == true) {
        String str = String(receivedChars);
        proc_int(str.toInt());
        newData = false;
    }
}

size_t size = 0;
size_t iindex = 256;
uint16_t ibuffer[256];

void proc_int(int val) {
    if (iindex == 256 && val == 0) {
        receive();
        return;
    }
    if (iindex == 256) {
        iindex = 0;
        size = val;
        return;
    }
    ibuffer[iindex] = val;
    Serial.println(val);
    if (++iindex == (size)) {
        iindex = 256;
        send(ibuffer, size);
        
    }
}