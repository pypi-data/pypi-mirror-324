# StemHat Python Package Documentation

The **StemHat** Python package provides an easy-to-use interface for controlling the **StemHat** hardware. It includes functions for managing **LEDs, motors, servos, buzzers**, and reading sensor data like **temperature, humidity, light, and analog inputs**. It also supports controlling an **OLED display**.

---

## Installation

Install the package using pip:

```bash
pip install StemHat
```

---

## Usage

### Importing the Package

```python
import StemHat
```

---

## Functions

### LED Control

#### `SetLED(led, red, blue, green)`
Sets the color of the specified LED.

**Parameters:**
- `led` (*int*): The LED to control (0 or 1).
- `red` (*int*): The red component (0-255).
- `blue` (*int*): The blue component (0-255).
- `green` (*int*): The green component (0-255).

---

### Buzzer Control

#### `SetBuzzer(frequency)`
Sets the buzzer frequency.

**Parameters:**
- `frequency` (*int*): The frequency in Hz (0-2550).

---

### Motor Control

#### `SetMotors(LeftMotorSpeed, RightMotorSpeed)`
Sets the speed of the left and right motors.

**Parameters:**
- `LeftMotorSpeed` (*int*): Speed of the left motor (-100 to 100).
- `RightMotorSpeed` (*int*): Speed of the right motor (-100 to 100).

---

### Servo Control

#### `SetServo(servo, angle)`
Sets the angle of the specified servo.

**Parameters:**
- `servo` (*int*): The servo to control (1, 2, 3, or 4).
- `angle` (*int*): The angle to set (0-180).

---

### Sensor Readings

#### `GetAnalog(analog)`
Reads the analog value from the specified analog input.

**Parameters:**
- `analog` (*int*): The analog input to read (0 or 1).

**Returns:**
- (*int*): The analog value.

#### `GetLightSensor()`
Reads the light sensor value.

**Returns:**
- (*int*): The light sensor value.

#### `GetVoltage()`
Reads the input voltage.

**Returns:**
- (*int*): The voltage value.

#### `GetButton(button)`
Reads the state of the specified button.

**Parameters:**
- `button` (*int*): The button to read (5 or 6).

**Returns:**
- (*bool*): The button state (True if pressed, False otherwise).

#### `GetUltrasonic()`
Reads the ultrasonic sensor value.

**Returns:**
- (*int*): The ultrasonic sensor value.

#### `GetTemperature()`
Reads the temperature from the AHT20 sensor.

**Returns:**
- (*float*): The temperature in Celsius.

#### `GetHumidity()`ne_width` (*int*): The width of the outline.

#### `OledLine(x1, y1, x2, y2)`
Draws a line on the OLED display.

**Parameters:**
- `x1` (*int*): The x-coordinate of the start point.
- `y1` (*int*): The y-coordinate of the start point.
- `x2` (*int*): The x-coordinate of the end point.
- `y2` (*int*): The y-coordinate of the end point.

#### `OledPoint(x, y, color)`
Draws a point on the OLED display.

**Parameters:**
- `x` (*int*): The x-coordinate of the point.
- `y` (*int*): The y-coordinate of the point.
- `color` (*int*): The color of the point (0 for black, 1 for white).

#### `OledCircles(x, y, radius, outline, outline_width)`
Draws a circle on the OLED display.

**Parameters:**
- `x` (*int*): The x-coordinate of the center.
- `y` (*int*): The y-coordinate of the center.
- `radius` (*int*): The radius of the circle.
- `outline` (*int*): Outline mode (0 for outline, 1 for solid).
- `outline_width` (*int*): The width of the outline.

#### `OledText(x, y, text, size, color)`
Draws text on the OLED display.

**Parameters:**
- `x` (*int*): The x-coordinate of the text.
- `y` (*int*): The y-coordinate of the text.
- `text` (*str*): The text to display.
- `size` (*int*): The font size.
- `color` (*int*): The text color (0 for black, 1 for white).

#### `OledImage(x, y, img_path, scale, invert)`
Draws an image on the OLED display.

**Parameters:**
- `x` (*int*): The x-coordinate of the image.
- `y` (*int*): The y-coordinate of the image.
- `img_path` (*str*): The path to the image file.
- `scale` (*int*): Scale mode (0 for no scaling, 1 for scaling).
- `invert` (*int*): Invert mode (0 for no inversion, 1 for inversion).

#### `OledClear()`
Clears the OLED display.

#### `OledUpdate()`
Updates the OLED display with the current drawing.

---

### 🎉 Now you're ready to use **StemHat** with Python! 🚀
