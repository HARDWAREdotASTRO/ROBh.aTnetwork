

//#include <Arduino.h>
#include <CmdMessenger.h>
#include <SoftwareSerial.h>

unsigned long thisCycleStart = 0;
const int motorAF_neutral = 9; // motor circuit is connected to pin 5
const int motorAF_hot = 8;
const int motorAR_neutral = 12; // motor circuit is connected to pin 5
const int motorAR_hot = 11;

const int motorBF_neutral = 2; // motor circuit is connected to pin 5
const int motorBF_hot = 3;
const int motorBR_neutral = 6; // motor circuit is connected to pin 5
const int motorBR_hot = 5;

const int buttonAF = 10; // GREEN
const int buttonAR = 13; // ORANGE
const int buttonBF = 4; // BLUE
const int buttonBR = 7; // RED

const int buttons[4] = {
        buttonAF,
        buttonAR,
        buttonBF,
        buttonBR
};
const char * buttonLabels[] = {
        "AF",
        "AR",
        "BF",
        "BR"
};

long iters = 0;

bool * currentState[] = {LOW, LOW, LOW, LOW};

bool buttonState[4] = {HIGH, HIGH, HIGH, HIGH};

const int TIME = 1 * 1000; // testing for how long to keep motors on for
int motorATime = TIME;
int motorBTime = TIME;

void motorOff(const char * motor) {
        if (motor == "A") {
                digitalWrite(motorAF_neutral, LOW);
                digitalWrite(motorAF_hot, LOW);
                digitalWrite(motorAR_neutral, LOW);
                digitalWrite(motorAR_hot, LOW);
        } else if (motor == "B") {
                digitalWrite(motorBF_neutral, LOW);
                digitalWrite(motorBF_hot, LOW);
                digitalWrite(motorBR_neutral, LOW);
                digitalWrite(motorBR_hot, LOW);
        }
}

void motorOn(const char * motor, const char * dir, int delayTime=TIME);

void motorOn(const char * motor,
             const char * dir, int delayTime){
        if (motor == "A") {
                if (dir == "F") {
                        digitalWrite(motorAR_neutral, LOW);
                        digitalWrite(motorAR_hot, LOW);
                        digitalWrite(motorAF_hot, HIGH);
                        digitalWrite(motorAF_neutral, HIGH);
                } else if (dir == "R") {
                        digitalWrite(motorAF_neutral, LOW);
                        digitalWrite(motorAF_hot, LOW);
                        digitalWrite(motorAR_hot, HIGH);
                        digitalWrite(motorAR_neutral, HIGH);
                }
        } else if (motor == "B") {
                if (dir == "F") {
                        digitalWrite(motorBR_neutral, LOW);
                        digitalWrite(motorBR_hot, LOW);
                        digitalWrite(motorBF_hot, HIGH);
                        digitalWrite(motorBF_neutral, HIGH);
                } else if (dir == "R") {
                        digitalWrite(motorBF_neutral, LOW);
                        digitalWrite(motorBF_hot, LOW);
                        digitalWrite(motorBR_hot, HIGH);
                        digitalWrite(motorBR_neutral, HIGH);
                }
        }
        delay(delayTime);
        // motorOff(motor);
}


CmdMessenger cmdMessenger = CmdMessenger(Serial,',',';','/');

enum {
        MotorOn,
        MotorOff,
        Status,
        kAcknowledge,
        kError
};

void attatchCommandCallbacks(){
        cmdMessenger.attach(CommandUnknown);
        cmdMessenger.attach(MotorOff, CommandMotorOff);
        cmdMessenger.attach(MotorOn, CommandMotorOn);
        cmdMessenger.attach(Status, CommandStatus);
}

void CommandUnknown(){
        cmdMessenger.sendCmd(kError, "Command Unknown");
}

void OnReady(){
        cmdMessenger.sendCmd(kAcknowledge, "Ready");
}

void CommandMotorOff(){
        char * motor = cmdMessenger.readStringArg();
        motorOff(motor);
}

void CommandMotorOn(){
        int delayTime = TIME;
        char * motor = cmdMessenger.readStringArg();
        char * dir = cmdMessenger.readStringArg();

        if (cmdMessenger.available()) {delayTime = cmdMessenger.readBinArg<int>();}

        if (motor == "A" and dir =="F") { // turn on A
                buttonState[0] = LOW;
                currentState[0] = LOW;
                currentState[1] = HIGH;
                motorATime = delayTime;
        }
        else{}

        if (motor == "A" and dir =="R") { // turn on A
                buttonState[1] = LOW;
                currentState[1] = LOW;
                currentState[0] = HIGH;
                motorATime = delayTime;
        }

        if (motor =="B" and dir =="F") { // turn on B
                buttonState[2] = LOW;
                currentState[2] = LOW;
                currentState[3] = HIGH;
                motorBTime = delayTime;
        }

        if (motor =="B" and dir =="R") { // turn on B
                buttonState[3] = LOW;
                currentState[2] = HIGH;
                currentState[3] = LOW;
                motorBTime = delayTime;
        }
}


bool * getButtons() {
        bool states[] = {HIGH, HIGH, HIGH, HIGH};
        for (int i = 0; i < 4; i++) {
                states[i] = digitalRead(buttons[i]);
        }
        return states;
}

void CommandStatus(){
        cmdMessenger.sendCmdStart("Status");

        cmdMessenger.sendCmdArg("A");
        if (digitalRead(motorAF_hot) == HIGH) {
                cmdMessenger.sendCmdArg("FWD");
        } else if (digitalRead(motorAR_hot) == HIGH) {
                cmdMessenger.sendCmdArg("REV");
        } else {
                cmdMessenger.sendCmdArg("OFF");
        }

        cmdMessenger.sendCmdArg("B");
        if (digitalRead(motorBF_hot) == HIGH) {
                cmdMessenger.sendCmdArg("FWD");
        } else if (digitalRead(motorBR_hot) == HIGH) {
                cmdMessenger.sendCmdArg("REV");
        } else {
                cmdMessenger.sendCmdArg("OFF");
        }

        cmdMessenger.sendCmdEnd();
}

bool cycleTimer(unsigned long &prevTime, unsigned long interval){
        if (millis() - prevTime >= interval) {return true;}
        else {return false;}
}


void setup(){// initializes the sketch by defining variables and pin modes

        Serial.begin(9600); // sets the data rate for the serial monitor tool
        // while (!Serial) ;
        cmdMessenger.printLfCr();
        attatchCommandCallbacks();
        pinMode(motorAF_neutral, OUTPUT);
        pinMode(motorAF_hot, OUTPUT);
        pinMode(motorAR_neutral, OUTPUT);
        pinMode(motorAR_hot, OUTPUT);
        pinMode(motorBF_neutral, OUTPUT);
        pinMode(motorBF_hot, OUTPUT);
        pinMode(motorBR_neutral, OUTPUT);
        pinMode(motorBR_hot, OUTPUT);
        pinMode(buttonAF, INPUT_PULLUP); // input, shorting to ground pulls input
        // low, so "LOW" state is on
        pinMode(buttonAR, INPUT_PULLUP); // input, shorting to ground pulls input
        // low, so "LOW" state is on
        pinMode(buttonBF, INPUT_PULLUP); // input, shorting to ground pulls input
        // low, so "LOW" state is on
        pinMode(buttonBR, INPUT_PULLUP); // input, shorting to ground pulls input
        // low, so "LOW" state is on
        //
        // motorOff("A");
        // motorOff("B");
        cmdMessenger.sendCmd(kAcknowledge, "Arduino Started");
}

void loop() {
        // Serial.print("Time: \t\t ");
        // Serial.print(iters * TIME / 1000);
        // Serial.println("s");
        thisCycleStart = millis();
        // Below this is turning on output  based on push buttons
        bool * buttonState = getButtons();
        // for (int i = 0; i < 4; i++) {
        //         Serial.print("Button ");
        //         Serial.print(buttonLabels[i]);
        //         Serial.print(":\t ");
        //         Serial.println(!buttonState[i]);
        // }

        // cmdMessenger.sendCmd(kAcknowledge, "Start Reading");
        cmdMessenger.feedinSerialData();
        // cmdMessenger.sendCmd(kAcknowledge, "Done Reading");
        for (int i = 0; i < 4; i++) {
                Serial.print("Button ");
                Serial.print(buttonLabels[i]);
                Serial.print(":\t ");
                Serial.println(!buttonState[i]);
                // !buttonState[i];
        }

        if (buttonState[0] == LOW) {
                if (not (digitalRead(motorAR_hot) == HIGH or currentState[1] == LOW) or buttonState[1] == HIGH) {
                        motorOn("A", "F", motorATime);
                }
        }

        if (buttonState[1] == LOW) {
                if (not (digitalRead(motorAF_hot) == HIGH or currentState[0] == LOW) or buttonState[0] == HIGH ) {
                        motorOn("A", "R", motorATime);
                }

        }
        if (buttonState[0] == HIGH and buttonState[1] == HIGH) {
                motorOff("A");
        }
        if (buttonState[2] == LOW) {
                if (not (digitalRead(motorBR_hot) == HIGH or currentState[3] == LOW) or buttonState[3] == HIGH) {
                        motorOn("B", "F", motorBTime);
                }
        }

        if (buttonState[3] == LOW) {
                if (not (digitalRead(motorBF_hot) == HIGH or currentState[2] == LOW) or buttonState[2] == HIGH ) {
                        motorOn("B", "R", motorBTime);
                }

        }
        if (buttonState[2] == HIGH and buttonState[3] == HIGH) {
                motorOff("B");
        }
        CommandStatus();
        //
        // if (digitalRead(motorAF_hot) == HIGH) {
        //         Serial.println("A: \t\t FWD");
        // } else if (digitalRead(motorAR_hot) == HIGH) {
        //         Serial.println("A: \t\t REV");
        // } else {
        //         Serial.println("A: \t\t OFF");
        // }
        //
        // if (digitalRead(motorBF_hot) == HIGH) {
        //         Serial.println("B: \t\t FWD");
        // } else if (digitalRead(motorBR_hot) == HIGH) {
        //         Serial.println("B: \t\t REV");
        // } else {
        //         Serial.println("B: \t\t OFF");
        // }

        // Serial.println("===========================");
        // delay(TIME);
        // motorOff("A");
        // motorOff("B");

        if (cycleTimer(thisCycleStart, TIME)) {
                // Serial.println("End of Loop (regular timings)");
                iters++;
                bool * currentState = buttonState;
        } else{
                int j = 0;
                do {j++; delay(1);} while (!cycleTimer(thisCycleStart, TIME));
                // Serial.print("End of Loop (had to wait for ");
                // Serial.print(j);
                // Serial.println(" ms)");
                iters++;
                bool * currentState = buttonState;
        }
        // Serial.println("End of Loop");
        // iters++;
        // bool * currentState = buttonState;

        // motorOff("A");
        // motorOff("B");

}
