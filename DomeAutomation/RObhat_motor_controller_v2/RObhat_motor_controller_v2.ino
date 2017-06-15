#include <Arduino.h>
// #include <stdio.h>

const int motorAF_neutral = 9;     // motor circuit is connected to pin 5
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
        Serial.print("Time: \t\t ");
        Serial.print(iters * TIME / 1000);
        Serial.println("s");

        // Below this is turning on output  based on push buttons
        bool * buttonState = getButtons();
        for (int i = 0; i < 4; i++) {
                Serial.print("Button ");
                Serial.print(buttonLabels[i]);
                Serial.print(":\t ");
                Serial.println(!buttonState[i]);
        }

        // Serial monitor
        if (Serial.available()) {
                String serialText =
                        Serial.readStringUntil('&'); // reads incoming data from the serial port
                if (serialText == "onAF") // turn on A
                {
                        motorOn("A", "F");
                        currentState[0] = LOW;
                        currentState[1] = HIGH;
                        Serial.println("Serial A: \t\t FWD");
                } else if (serialText == "onAR") // turn on A
                {
                        motorOn("A", "R");
                        currentState[1] = LOW;
                        currentState[0] = HIGH;
                        Serial.println("Serial A: \t\t REV");
                } else if (serialText = "offA") {
                        motorOff("A");
                        currentState[0] = HIGH;
                        currentState[1] = HIGH;
                        Serial.println("Serial A: \t\t OFF");
                }
                if (serialText == "onBF") // turn on B
                {
                        motorOn("B", "F");
                        currentState[2] = LOW;
                        currentState[3] = HIGH;
                        Serial.println("Serial B: \t\t FWD");
                } else if (serialText == "onBR") // turn on B
                {
                        motorOn("B", "R");
                        currentState[2] = HIGH;
                        currentState[3] = LOW;
                        Serial.println("Serial B: \t\t REV");
                } else if (serialText = "offB") {
                        motorOff("B");
                        currentState[2] = HIGH;
                        currentState[3] = HIGH;
                        Serial.println("Serial B: \t\t OFF");
                }
        }

        if (buttonState[0] == LOW and not (buttonState[1] == LOW)) // 4
        {
                // Serial.println("A: \t\t FWD");
                motorOn("A", "F");
        } else if (buttonState[1] == LOW and not (buttonState[0] == LOW)) // 4
        {
                // Serial.println("A: \t\t REV");
                motorOn("A", "R");
        } else if (buttonState[0] == LOW and buttonState[1] == LOW and currentState[0] == LOW and not (currentState[1] == LOW)) // 1
        {
                buttonState[1] = HIGH;
                // Serial.println("A: \t\t FWD");
                motorOn("A", "F");
        } else if (buttonState[0] == LOW and buttonState[1] == LOW and currentState[1] == LOW and not (currentState[0] == LOW)) // 1
        {
                buttonState[0] = HIGH;
                // Serial.println("A: \t\t REV");
                motorOn("A", "R");
        } else // 4+1
        {
                // Serial.println("A: \t\t OFF");
                // motorOff("A");
        }

        if (buttonState[2] == LOW and not (buttonState[3] == LOW)) // 4
        {
                // Serial.println("B: \t\t FWD");
                motorOn("B", "F");
        } else if (buttonState[3] == LOW and not (buttonState[2] == LOW)) // 4
        {
                // Serial.println("B: \t\t REV");
                motorOn("B", "R");
        } else if (buttonState[2] == LOW and buttonState[3] == LOW and currentState[2] == LOW and not (currentState[3] == LOW)) // 1
        {
                buttonState[3] = HIGH;
                // Serial.println("B: \t\t FWD");
                motorOn("B", "F");
        } else if (buttonState[2] == LOW and buttonState[3] == LOW and currentState[3] == LOW and not (currentState[2] == LOW)) // 1
        {
                buttonState[2] = HIGH;
                // Serial.println("B: \t\t REV");
                motorOn("B", "R");
        } else // 4+1
        {
                // Serial.println("B: \t\t OFF");
                // motorOff("B");
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

        Serial.println("===========================");
        delay(TIME);
        motorOff("A");
        motorOff("B");
        iters++;
        bool * currentState = buttonState;
}
