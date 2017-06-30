
/*
Serial Test
*/
String inString = ""; //string to hold input
String TimeString = "";
String CommandString = "";
int timeInt = "";

void setup() // initializes the sketch by defining variables and pin modes
{
  pinMode(LED_BUILTIN, OUTPUT); // set the built in LED to turn on and oFF
  Serial.begin(9600);// sets the data rate for the serial monitor tool
//  while (! Serial);
//  Serial.println("Push Button or Type 'onA' or 'onB'");// Prints the phrase on serial monitor
    
}

void loop() //following information will not return information to the function that it was called
{
  //Serial monitor, send a command of the formate "00,000" where the first is a two digit number
  //corresponding to some action the arduino should take, and the third is some additional information
  // in the "01" example it is the length of time to keep the LED on for.
  if(Serial.available()) { //gets the number of bytes available for reading from the serial port
   inString = Serial.readString();//reads incoming data from the serial port sets it as a string
   int commaIndex = inString.indexOf(','); //finds the delimiter postion
   CommandString = inString.substring(0,commaIndex); //splits the string into the command 
   TimeString = inString.substring(commaIndex+1); //splits out the amount of time to stay on, if necessary
   timeInt = TimeString.toInt(); //converts the time string into an integer
   //Serial.print("Input:");
   //Serial.println(inString);
   //Serial.print("Command:");
   //Serial.println(CommandString);
   //Serial.print("Time:");
   //Serial.println(timeInt);
   if (CommandString == "00"){ //command "00" is simpily to turn on LED
     digitalWrite(LED_BUILTIN, LOW);
   }
   if (CommandString == "01"){ //commands the LED to turn on for the amount time in seconds given in serial command
                                //this is a lazy implementation of this though since the entire loop is delayed, it would
                                //be better to implement it as a counter in the main loop and have it shut off after so many main loops
     digitalWrite(LED_BUILTIN, HIGH); 
     delay(timeInt*1000); //delay in milliseconds
     digitalWrite(LED_BUILTIN,LOW);
   }
   if (CommandString == "02"){ //turns the LED off
    digitalWrite(LED_BUILTIN, HIGH);
   }
  }
  //here you should be able to put in your other commands
}
   
  
