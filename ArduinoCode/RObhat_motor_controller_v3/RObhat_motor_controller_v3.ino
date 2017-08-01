#include <Arduino.h>
#include <CmdMessenger.h>

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

unsigned long iters = 0;

bool* currentState[] = {LOW, LOW, LOW, LOW};

bool* buttonState[] = {HIGH, HIGH, HIGH, HIGH};

const int TIME = 1 * 1000; // testing for how long to keep motors on for
int motorATime = TIME;
int motorBTime = TIME;

void motorOff(char motor) {
        if (motor == 'A') {
                digitalWrite(motorAF_neutral, LOW);
                digitalWrite(motorAF_hot, LOW);
                digitalWrite(motorAR_neutral, LOW);
                digitalWrite(motorAR_hot, LOW);
        } else if (motor == 'B') {
                digitalWrite(motorBF_neutral, LOW);
                digitalWrite(motorBF_hot, LOW);
                digitalWrite(motorBR_neutral, LOW);
                digitalWrite(motorBR_hot, LOW);
        }
}

void motorOn(char motor, char dir, int delayTime=TIME);

void motorOn(char motor,
             char dir, int delayTime){
        if (motor == 'A') {
                if (dir == 'F') {
                        digitalWrite(motorAR_neutral, LOW);
                        digitalWrite(motorAR_hot, LOW);
                        digitalWrite(motorAF_hot, HIGH);
                        digitalWrite(motorAF_neutral, HIGH);
                } else if (dir == 'R') {
                        digitalWrite(motorAF_neutral, LOW);
                        digitalWrite(motorAF_hot, LOW);
                        digitalWrite(motorAR_hot, HIGH);
                        digitalWrite(motorAR_neutral, HIGH);
                }
        } else if (motor == 'B') {
                if (dir == 'F') {
                        digitalWrite(motorBR_neutral, LOW);
                        digitalWrite(motorBR_hot, LOW);
                        digitalWrite(motorBF_hot, HIGH);
                        digitalWrite(motorBF_neutral, HIGH);
                } else if (dir == 'R') {
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
        kMotorOn,
        kMotorStayOn,
        kMotorOff,
        kStatus,
        kAck,
        kError,
        kLogging
};



void CommandUnknown(){
        cmdMessenger.sendCmd(kError, "Command Unknown");
}

void OnReady(){
        cmdMessenger.sendCmd(kLogging, "Ready");
}

void CommandMotorOff(){
        char motor = cmdMessenger.readBinArg<char>();
        motorOff(motor);
        cmdMessenger.sendCmdStart(kAck);
        cmdMessenger.sendCmdArg(motor);
        cmdMessenger.sendCmdArg("OFF");
        cmdMessenger.sendCmdEnd();
}

void CommandMotorStayOn(){
        char motor = cmdMessenger.readBinArg<char>();
        char dir = cmdMessenger.readBinArg<char>();
        if (motor == 'A') {
                if (dir == 'F') {
                        digitalWrite(motorAR_neutral, LOW);
                        digitalWrite(motorAR_hot, LOW);
                        digitalWrite(motorAF_hot, HIGH);
                        digitalWrite(motorAF_neutral, HIGH);
                } else if (dir == 'R') {
                        digitalWrite(motorAF_neutral, LOW);
                        digitalWrite(motorAF_hot, LOW);
                        digitalWrite(motorAR_hot, HIGH);
                        digitalWrite(motorAR_neutral, HIGH);
                }
        } else if (motor == 'B') {
                if (dir == 'F') {
                        digitalWrite(motorBR_neutral, LOW);
                        digitalWrite(motorBR_hot, LOW);
                        digitalWrite(motorBF_hot, HIGH);
                        digitalWrite(motorBF_neutral, HIGH);
                } else if (dir == 'R') {
                        digitalWrite(motorBF_neutral, LOW);
                        digitalWrite(motorBF_hot, LOW);
                        digitalWrite(motorBR_hot, HIGH);
                        digitalWrite(motorBR_neutral, HIGH);
                }
        }
        cmdMessenger.sendCmdStart(kAck);
        cmdMessenger.sendCmdArg("FORCED");
        cmdMessenger.sendCmdArg(motor);
        cmdMessenger.sendCmdArg(dir);
        cmdMessenger.sendCmdEnd();

}

void CommandMotorOn(){
        //Must send the following information:
        // Motor: 'A' or 'B'
        // Direction: 'F' or 'R'
        // Time: int > 0
        char motor = cmdMessenger.readBinArg<char>();
        char dir = cmdMessenger.readBinArg<char>();
        int delayTime = cmdMessenger.readBinArg<int>();
        if (delayTime <= 0) {int delayTime = 1;}
        // if (motor == 'A' and dir =='F') { // turn on A
        //         buttonState[0] = LOW;
        //         currentState[0] = LOW;
        //         currentState[1] = HIGH;
        //         motorATime = delayTime;
        // }
        //
        // if (motor == 'A' and dir =='R') { // turn on A
        //         buttonState[1] = LOW;
        //         currentState[1] = LOW;
        //         currentState[0] = HIGH;
        //         motorATime = delayTime;
        // }
        //
        // if (motor =='B' and dir =='F') { // turn on B
        //         buttonState[2] = LOW;
        //         currentState[2] = LOW;
        //         currentState[3] = HIGH;
        //         motorBTime = delayTime;
        // }
        //
        // if (motor =='B' and dir =='R') { // turn on B
        //         buttonState[3] = LOW;
        //         currentState[2] = HIGH;
        //         currentState[3] = LOW;
        //         motorBTime = delayTime;
        // }
        motorOn(motor, dir, delayTime);
        cmdMessenger.sendCmdStart(kAck);
        cmdMessenger.sendCmdArg(motor);
        cmdMessenger.sendCmdArg(dir);
        cmdMessenger.sendCmdArg(String(delayTime));
        cmdMessenger.sendCmdEnd();
}


void CommandStatus(){
        cmdMessenger.sendCmdStart(kAck);

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

void attatchCommandCallbacks(){
        cmdMessenger.attach(CommandUnknown);
        cmdMessenger.attach(kMotorOff, CommandMotorOff);
        cmdMessenger.attach(kMotorStayOn, CommandMotorStayOn);
        cmdMessenger.attach(kMotorOn, CommandMotorOn);
        cmdMessenger.attach(kStatus, CommandStatus);
}

void setup(){// initializes the sketch by defining variables and pin modes

        Serial.begin(115200); // sets the data rate for the serial monitor tool
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
        // motorOff('A');
        // motorOff('B');
        cmdMessenger.sendCmd(kLogging, "Arduino Initialized");
}

void buttonLog(){
        cmdMessenger.sendCmdStart(kLogging);
        for (int i = 0; i < 4; i++) {
                cmdMessenger.sendCmdArg(buttonLabels[i]);
                cmdMessenger.sendCmdArg(String(!buttonState[i]));
        }
        cmdMessenger.sendCmdEnd();
}

void loop() {
        // Serial.print("Time: \t\t ");
        // Serial.print(iters * TIME / 1000);
        // Serial.println("s");
        thisCycleStart = millis();
        // Below this is turning on output  based on push buttons

        for (int i = 0; i < 4; i++) {
                buttonState[i] = digitalRead(buttons[i]);
        }


        // cmdMessenger.sendCmd(kLogging, "Start Reading");
        cmdMessenger.feedinSerialData();
        delay(10);
        // cmdMessenger.sendCmd(kLogging, "Done Reading");

        // for (int i = 0; i < 4; i++) {
        //         Serial.print("Button ");
        //         Serial.print(buttonLabels[i]);
        //         Serial.print(":\t ");
        //         Serial.println(!buttonState[i]);
        //         // !buttonState[i];
        // }

        // buttonLog();

        if (buttonState[0] == LOW) {
                if (not (digitalRead(motorAR_hot) == HIGH or currentState[1] == LOW) or buttonState[1] == HIGH) {
                        motorOn('A', 'F', motorATime);
                }
        }

        if (buttonState[1] == LOW) {
                if (not (digitalRead(motorAF_hot) == HIGH or currentState[0] == LOW) or buttonState[0] == HIGH ) {
                        motorOn('A', 'R', motorATime);
                }

        }
        if (buttonState[0] == HIGH and buttonState[1] == HIGH) {
                motorOff('A');
        }
        if (buttonState[2] == LOW) {
                if (not (digitalRead(motorBR_hot) == HIGH or currentState[3] == LOW) or buttonState[3] == HIGH) {
                        motorOn('B', 'F', motorBTime);
                }
        }

        if (buttonState[3] == LOW) {
                if (not (digitalRead(motorBF_hot) == HIGH or currentState[2] == LOW) or buttonState[2] == HIGH ) {
                        motorOn('B', 'R', motorBTime);
                }

        }
        if (buttonState[2] == HIGH and buttonState[3] == HIGH) {
                motorOff('B');
        }

        // CommandStatus();

        // delay(TIME);

        if (cycleTimer(thisCycleStart, TIME)) {
                // cmdMessenger.sendCmd(kLogging, "End of Loop (regular timings)");
                iters++;
                for (int i=0; i<4; i++) {
                        *currentState[i] = buttonState[i];
                }
        } else{
                int j = 0;
                do {j++; delay(1);} while (!cycleTimer(thisCycleStart, TIME));
                // cmdMessenger.sendCmdStart(kLogging);
                // cmdMessenger.sendCmdArg("End of Loop, had to wait");
                // cmdMessenger.sendCmdArg(String(j));
                // cmdMessenger.sendCmdArg("ms");
                // cmdMessenger.sendCmdEnd();
                iters++;
                for (int i=0; i<4; i++) {
                        *currentState[i] = buttonState[i];
                }
        }

        // motorOff('A');
        // motorOff('B');
        motorATime = TIME;
        motorBTime = TIME;

}
