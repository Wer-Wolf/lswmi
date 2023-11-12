# lswmi

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
![Tests](https://github.com/Wer-Wolf/lswmi/actions/workflows/Test.yaml/badge.svg)
[![codecov](https://codecov.io/gh/Wer-Wolf/lswmi/graph/badge.svg?token=XIT6Q90IMW)](https://codecov.io/gh/Wer-Wolf/lswmi)

Utility to retrieve information about WMI devices on Linux.

## Requirements

Python >= 3.11 is required to use this utility.

## Installation

```sh
python3 -m pip install lswmi
```

## Examples

Listing all available WMI devices:

```
python3 -m lswmi
05901221-D566-11D1-B2F0-00A0C9062910: Data   (Instances: 1)
ABBC0F6A-8EA1-11D1-00A0-C90629100000: Method (Instances: 1)
05901221-D566-11D1-B2F0-00A0C9062910: Data   (Instances: 1)
ABBC0F72-8EA1-11D1-00A0-C90629100000: Event  (Instances: 1)
97845ED0-4E6D-11DE-8A39-0800200C9A66: Method (Instances: 1)
C3021213-D0BC-41A2-BA17-816CD5ED7744: Method (Instances: 1)
05901221-D566-11D1-B2F0-00A0C9062910: Data   (Instances: 1)
B82BB115-43AE-4B35-B79D-BD6416ABC381: Method (Instances: 1)
05901221-D566-11D1-B2F0-00A0C9062910: Data   (Instances: 1)
A0485619-3E07-4ABE-BE6B-0AB67E2A92E6: Method (Instances: 1)
```

Enable verbose output:

```
python3 -m lswmi -V
05901221-D566-11D1-B2F0-00A0C9062910: Data   (Instances: 1)
    Identification: MO
    Expensive: False
    Setable: False
    Driver: wmi-bmof

ABBC0F6A-8EA1-11D1-00A0-C90629100000: Method (Instances: 1)
    Identification: AA
    Expensive: False

05901221-D566-11D1-B2F0-00A0C9062910: Data   (Instances: 1)
    Identification: MO
    Expensive: False
    Setable: False
    Driver: wmi-bmof

ABBC0F72-8EA1-11D1-00A0-C90629100000: Event  (Instances: 1)
    Identification: D2
    Expensive: False

97845ED0-4E6D-11DE-8A39-0800200C9A66: Method (Instances: 1)
    Identification: BC
    Expensive: False

C3021213-D0BC-41A2-BA17-816CD5ED7744: Method (Instances: 1)
    Identification: BC
    Expensive: False

05901221-D566-11D1-B2F0-00A0C9062910: Data   (Instances: 1)
    Identification: BA
    Expensive: False
    Setable: False
    Driver: wmi-bmof

B82BB115-43AE-4B35-B79D-BD6416ABC381: Method (Instances: 1)
    Identification: BC
    Expensive: False

05901221-D566-11D1-B2F0-00A0C9062910: Data   (Instances: 1)
    Identification: MO
    Expensive: False
    Setable: False
    Driver: wmi-bmof

A0485619-3E07-4ABE-BE6B-0AB67E2A92E6: Method (Instances: 1)
    Identification: BC
    Expensive: False

```