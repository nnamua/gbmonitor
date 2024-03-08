#!/usr/bin/env python3

import argparse
import time
from dataclasses import dataclass
from typing import Optional, Tuple

import hid


@dataclass
class MonitorProperty:
    """
    A configurable monitor property
    """

    name: str
    value: int
    range: Tuple[int, int]
    abbr: Optional[str] = None
    description: str = ""


class Monitor:
    """
    This class sets configurable monitor properties
    """

    VID = 0x0BDA
    PID = 0x1100

    @property
    def configurable_properties(self):
        return {
            "brightness": MonitorProperty(
                name="brightness",
                abbr="b",
                range=tuple((0, 100)),
                value=0x10,
            ),
            "contrast": MonitorProperty(
                name="contrast",
                abbr="c",
                range=tuple((0, 100)),
                value=0x12,
            ),
            "sharpness": MonitorProperty(
                name="sharpness",
                abbr="s",
                range=tuple((0, 10)),
                value=0x87,
            ),
            "low_blue_light": MonitorProperty(
                name="low-blue-light",
                abbr="lb",
                range=tuple((0, 10)),
                value=0xE00B,
                description="Blue light reduction. 0 means no reduction.",
            ),
            "kvm_switch": MonitorProperty(
                name="kvm-switch",
                abbr="kvm",
                range=tuple((0, 1)),
                value=0xE069,
                description="Switch KVM to device 0 or 1",
            ),
            "color_mode": MonitorProperty(
                name="color-mode",
                abbr="cm",
                range=tuple((0, 3)),
                value=0xE003,
                description="0 is cool, 1 is normal, 2 is warm, 3 is user-defined.",
            ),
            "rgb_red": MonitorProperty(
                name="rgb-red",
                range=tuple((0, 100)),
                value=0xE004,
                description="Red value -- only works if colour-mode is set to 3",
            ),
            "rgb_green": MonitorProperty(
                name="rgb-green",
                range=tuple((0, 100)),
                value=0xE005,
                description="Green value -- only works if colour-mode is set to 3",
            ),
            "rgb_blue": MonitorProperty(
                name="rgb-blue",
                range=tuple((0, 100)),
                value=0xE006,
                description="Blue value -- only works if colour-mode is set to 3",
            ),
        }

    @staticmethod
    def _build_request(monitor_property: MonitorProperty, property_value: int) -> bytes:
        """
        Builds a HID reqeust for setting the property whose name is prop_name to property_value
        :param monitor_property: The property to set
        :param property_value: The value to set the property to
        :return: A byte string representation of the request
        """
        # +1 for Null byte in the header
        request_size = 192 + 1
        header_size = 0x40 + 1

        # Buffer needs to start with a null byte
        buffer = [0x00]
        # Request header
        buffer += [0x40, 0xC6]
        buffer += [0x00] * 4
        buffer += [0x20, 0x00, 0x6E, 0x00, 0x80]

        # preamble needs this to be set up
        msg = [monitor_property.value >> 8] if monitor_property.value > 0xFF else []
        msg += [monitor_property.value & 0xFF, 0x00, property_value]

        preamble = [0x51, 0x81 + len(msg), 0x03]

        # Header padding
        buffer = buffer + [0x00] * (header_size - len(buffer))

        buffer += preamble
        buffer += msg
        buffer += [0x00] * (request_size - len(buffer))
        return bytes(buffer)

    def set_property(self, property_name: str, property_value: int):
        """
        Sets property_name to property_value
        :param property_name: The name of the property to set
        :param property_value: The value to set the property to
        :return: Number of bytes written to the hid device
        """

        prop = self.configurable_properties[property_name]
        with hid.Device(self.VID, self.PID) as device:
            return device.write(Monitor._build_request(prop, property_value))


def ranged_int(min: int, max: int):
    """
    Returns a function, which transforms its argument into an integer
    and checks if the result is in the given bounds.
    :param min: Minimum value
    :param max: Maximum value
    :return: Function to used in ArgumentParser
    """

    def func(arg: str) -> int:
        try:
            x = int(arg)
            if x < min or x > max:
                raise argparse.ArgumentTypeError(f"must be within range [{min}, {max}]")
            return x
        except ValueError:
            raise argparse.ArgumentTypeError(f"must be a valid integer.")

    return func


def main():
    monitor = Monitor()
    parser = argparse.ArgumentParser(description="Set monitor property.")

    # Generate options from configurable properties
    for prop in monitor.configurable_properties.values():
        name = (f"-{prop.abbr}", f"--{prop.name}") if prop.abbr is not None else (f"--{prop.name}",)
        parser.add_argument(*name, type=ranged_int(*prop.range))
    args = parser.parse_args()

    # Set property for each supplied argument
    for name, value in vars(args).items():
        if value is not None:
            monitor.set_property(name, value)

            # Some sort of delay was required in my setup, could maybe be tweaked
            time.sleep(0.2)


if __name__ == "__main__":
    main()
