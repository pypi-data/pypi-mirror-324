# 📟 Scientific & Electronic Calculator

A Python package for performing **scientific and electronic calculations**, including Ohm's Law, metric conversions, frequency conversions, physics formulas, and more.

## 🚀 Features
- Ohm’s Law & Power Law calculations
- Frequency & metric unit conversions
- Speed, distance, and time calculations
- Newton’s Laws & gravitational force computations
- Electronic component calculations (resistors, capacitors, inductors)
- CMYK to RGB color conversion

## 📦 Installation
You can install this package using `pip`:

```
pip install Fcode_Calculator
```


## 📖 Usage
**Import the package and start using the functions:**

```
import Fcode_Calculator as ps
```

##  Ohm's Law Example
```
voltage = ps.ohms_law("Voltage", I=2, R=10)
print(voltage)  # Output: 20 volts
```

## Frequency Conversion
```
freq_in_ghz = ps.freq_converter(5, "MHz", "GHz")
print(freq_in_ghz)  # Output: 0.005 GHz
```

## Einstein’s Energy Formula
```
energy = ps.einstein_mass_energy(2)
print(energy)  # Output: 1.8e+17
```

## 📚 Available Functions
 - **🔹 Electronics**
```
ohms_law(type, V=None, I=None, R=None): Calculate Ohm’s Law values.
```
```
power_law(type, V=None, I=None, P=None): Calculate power, voltage, or current.
```
```
series_resistor(*resistances): Sum of resistors in series.
```
```
parallel_resistor(*resistances): Total resistance in parallel circuits.
```

 - **🔹 Scientific **
```
speed(distance, time): Calculate speed.
```
```
distance(speed, time): Find distance.
```
```
gravitational_force(G, m1, m2, r): Compute gravitational force.
```
```
einstein_mass_energy(mass): Compute energy from mass.
```
 - **🔹 Conversions**
```
freq_converter(value, from_freq, to_freq): Convert between Hz, kHz, MHz, and GHz.
```
```
metric_converter(value, from_unit, to_unit): Convert metric units (nano, micro, kilo, etc.).
```
```
cmyk_to_rgb(c, m, y, k): Convert CMYK color values to RGB.
```

## 🛠️ Development & Contributions
If you want to improve this package:
Fork the repository on GitHub.
Clone the repository:
```
git clone https://github.com/fcode101/PyScience.git
```
```
cd scientific_calculator
```


## 📜 License
This project is licensed under the MIT License.

- 💡 Created by F-Code-101:
- 📧 Contact: techwbro@gmail.com
- 🎥 https://www.youtube.com/@F-Code101

---
