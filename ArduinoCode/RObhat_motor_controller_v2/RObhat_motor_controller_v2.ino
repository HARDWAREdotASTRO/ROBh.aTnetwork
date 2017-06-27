#include <Arduino.h>
// #include <stdio.h>

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

const int TIME = 1 * 1000; // testing for how long to keep motors on for

void setup(void) // initializes the sketch by defining variables and pin modes
{
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
        Serial.begin(9600); // sets the data rate for the serial monitor tool
        motorOff("A");
        motorOff("B");
}

bool *
getButtons(void) {
        bool states[4];
        for (int i = 0; i < 4; i++) {
                states[i] = digitalRead(buttons[i]);
        }
        return states;
}

void
motorOff(const char * motor) {
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

void
motorOn(const char * motor,
        const char * dir) {
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
}

long iters = 0;
bool * currentState[4] = {
        HIGH,
        HIGH,
        HIGH,
        HIGH
};

void
loop(void) {
        // Serial.print("Time: \t\t ");
        // Serial.print(iters * TIME / 1000);
        // Serial.println("s");

        // Below this is turning on output  based on push buttons
        bool * buttonState = getButtons();
        for (int i = 0; i < 4; i++) {
                Serial.print("Button ");
                Serial.print(buttonLabels[i]);
                Serial.print(":\t ");
                Serial.println(!buttonState[i]);
        }

        // Serial monitor
        if (Serial.available())
        {
                String serialText =
                        Serial.readStringUntil('&'); // reads incoming data from the serial port
                if (serialText == "onAF") { // turn on A
                        // motorOn("A", "F");
                        buttonState[0] = LOW;
                        currentState[0] = LOW;
                        currentState[1] = HIGH;
                        // Serial.println("Serial A: \t\t FWD");
                } else if (serialText == "onAR") { // turn on A

                        // motorOn("A", "R");
                        buttonState[1] = LOW;
                        currentState[1] = LOW;
                        currentState[0] = HIGH;
                        // Serial.println("Serial A: \t\t REV");
                } else if (serialText = "offA") {
                        motorOff("A");
                        currentState[0] = HIGH;
                        currentState[1] = HIGH;
                        // Serial.println("Serial A: \t\t OFF");
                } else{
                        // Serial.println("Serial A: \t\t N/A");
                }

                if (serialText == "onBF") { // turn on B
                        // motorOn("B", "F");
                        buttonState[2] = LOW;
                        currentState[2] = LOW;
                        currentState[3] = HIGH;
                        // Serial.println("Serial B: \t\t FWD");
                } else if (serialText == "onBR") { // turn on B

                        // motorOn("B", "R");
                        buttonState[3] = LOW;
                        currentState[2] = HIGH;
                        currentState[3] = LOW;
                        // Serial.println("Serial B: \t\t REV");
                } else if (serialText = "offB") {
                        motorOff("B");
                        currentState[2] = HIGH;
                        currentState[3] = HIGH;
                        // Serial.println("Serial B: \t\t OFF");
                }else{
                        // Serial.println("Serial B: \t\t N/A");
                }
        }

        if (buttonState[0] == LOW) {
                if (not (digitalRead(motorAR_hot) == HIGH or currentState[1] == LOW) or buttonState[1] == HIGH) {
                        motorOn("A", "F");
                }
        }

        if (buttonState[1] == LOW) {
                if (not (digitalRead(motorAF_hot) == HIGH or currentState[0] == LOW) or buttonState[0] == HIGH ) {
                        motorOn("A", "R");
                }

        }
        if (buttonState[0] == HIGH and buttonState[1] == HIGH) {
                motorOff("A");
        }
        if (buttonState[2] == LOW) {
                if (not (digitalRead(motorBR_hot) == HIGH or currentState[3] == LOW) or buttonState[3] == HIGH) {
                        motorOn("B", "F");
                }
        }

        if (buttonState[3] == LOW) {
                if (not (digitalRead(motorBF_hot) == HIGH or currentState[2] == LOW) or buttonState[2] == HIGH ) {
                        motorOn("B", "R");
                }

        }
        if (buttonState[2] == HIGH and buttonState[3] == HIGH) {
                motorOff("B");
        }


        if (digitalRead(motorAF_hot) == HIGH) {
                Serial.println("A: \t\t FWD");
        } else if (digitalRead(motorAR_hot) == HIGH) {
                Serial.println("A: \t\t REV");
        } else {
                Serial.println("A: \t\t OFF");
        }

        if (digitalRead(motorBF_hot) == HIGH) {
                Serial.println("B: \t\t FWD");
        } else if (digitalRead(motorBR_hot) == HIGH) {
                Serial.println("B: \t\t REV");
        } else {
                Serial.println("B: \t\t OFF");
        }

        // Serial.println("===========================");
        delay(TIME);
        // motorOff("A");
        // motorOff("B");
        iters++;
        bool * currentState = buttonState;
}
