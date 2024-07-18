#!/usr/bin/env python3
import sys
import os

CONFIG_FILE_EXT = ".config"

UNSET = "unset"
DISABLE = "n"
ENABLE = "y"
MODULE = "m"

GENERIC_PATCHES = [
    # kernel-fsync config
    ["I2C_NCT6775", None, MODULE],
    ["ZENIFY", None, ENABLE],
    ["FB_SIMPLE", UNSET, ENABLE],
    ["FB_EFI", UNSET, ENABLE],
    ["FB_VESA", UNSET, ENABLE],
    ["ACPI_EC_DEBUGFS", UNSET, MODULE],
    ["NTSYNC", None, ENABLE],
    ["USER_NS_UNPRIVILEGED", None, ENABLE],
    ["TCP_CONG_BBR2", None, MODULE],
    ["SECURITY_LOCKDOWN_LSM_EARLY", None, UNSET],
    #  scheduler stuff
    ["SCHED_BORE", None, ENABLE],
    ["MIN_BASE_SLICE_NS", None, "1000000"],
    ["SCHED_CLASS_EXT", None, ENABLE],

    # device specific config
    # Microsoft Surface
    ["HID_IPTS", None, MODULE],
    ["HID_ITHC", None, MODULE],
    ["SURFACE_BOOK1_DGPU_SWITCH", None, MODULE],
    ["VIDEO_DW9719", None, MODULE],
    ["IPC_CLASSES", None, ENABLE],
    ["LEDS_TPS68470", None, MODULE],
    ["SENSORS_SURFACE_FAN", None, MODULE],
    ["SENSORS_SURFACE_TEMP", None, MODULE],

    # amdgpu HDR Color management
    ["AMD_PRIVATE_COLOR", None, ENABLE],

    # Rog Ally Gyro Fix
    ["BMI323_I2C", None, MODULE],
    ["BMI323_SPI", None, MODULE],

    # Mac T2 supprot
    ["DRM_APPLETBDRM", None, MODULE],
    ["HID_APPLETB_BL", None, MODULE],
    ["HID_APPLETB_KBD", None, MODULE],
    ["HID_APPLE_MAGIC_BACKLIGHT", None, MODULE],
    ["CONFIG_APPLE_BCE", None, MODULE],
]

ARCH_PATCHES = {
    "x86_64": [
        # Lenovo Legion
        ["LEGION_LAPTOP", None, MODULE],
        ["ACPI_CALL", None, MODULE],

        # Aly & Legion Go Gyro
        ["IIO_SYSFS_TRIGGER", None, MODULE],
        ["IIO_HRTIMER_TRIGGER", None, MODULE],

        # Steam Deck
        ["MFD_STEAMDECK", None, MODULE],
        ["SENSORS_STEAMDECK", None, MODULE],
        ["LEDS_STEAMDECK", None, MODULE],
        ["EXTCON_STEAMDECK", None, MODULE],
        # Required by the Steam Deck for DRD, otherwise USB is borked
        ["USB_DWC3", None, MODULE],
        ["USB_DWC3_ULPI", None, ENABLE],
        ["USB_DWC3_DUAL_ROLE", None, ENABLE],
        ["USB_DWC3_PCI", None, MODULE],
        ["USB_DWC3_HAPS", None, MODULE],
        ["USB_DWC3_HOST", ENABLE, UNSET, "fedora"],
        ["USB_DWC2", None, MODULE],
        ["USB_DWC2_DUAL_ROLE", None, ENABLE],
        ["USB_DWC2_PCI", None, MODULE],
        ["USB_DWC2_DEBUG", None, UNSET],
        ["USB_DWC2_TRACK_MISSED_SOFS", None, UNSET],
        ["USB_CHIPIDEA", None, MODULE],
        ["USB_CHIPIDEA_UDC", None, ENABLE],
        ["USB_CHIPIDEA_HOST", None, ENABLE],
        ["USB_CHIPIDEA_PCI", None, MODULE],
        ["USB_CHIPIDEA_MSM", None, MODULE],
        ["USB_CHIPIDEA_GENERIC", None, MODULE],
        ["USB_ISP1760", None, MODULE],
        ["USB_ISP1760_HCD", None, ENABLE],
        ["USB_ISP1761_UDC", None, ENABLE],
        ["USB_ISP1760_DUAL_ROLE", None, ENABLE],
        ["USB_GADGET", None, MODULE],
        ["USB_GADGET_VBUS_DRAW", None, "2"],
        ["USB_GADGET_STORAGE_NUM_BUFFERS", None, "2"],
        ["USB_GADGET_DEBUG", None, UNSET],
        ["USB_GADGET_DEBUG_FILES", None, UNSET],
        ["USB_GADGET_DEBUG_FS", None, UNSET],
        ["U_SERIAL_CONSOLE", None, UNSET],
        ["USB_R8A66597", None, UNSET],
        ["USB_PXA27X", None, UNSET],
        ["USB_MV_UDC", None, UNSET],
        ["USB_MV_U3D", None, UNSET],
        ["USB_M66592", None, UNSET],
        ["USB_BDC_UDC", None, UNSET],
        ["USB_AMD5536UDC", None, UNSET],
        ["USB_NET2272", None, UNSET],
        ["USB_NET2280", None, UNSET],
        ["USB_GOKU", None, UNSET],
        ["USB_EG20T", None, UNSET],
        ["USB_DUMMY_HCD", None, UNSET],
        ["USB_CONFIGFS", None, UNSET],
        ["PHY_SAMSUNG_USB2", None, UNSET],

        # Steam Deck HDR Color management
        ["DRM_AMD_COLOR_STEAMDECK", None, ENABLE],

        # Deck Sound stuff?
        ["SND_SOC_AMD_ACP_COMMON", None, MODULE],
        ["SND_SPI", None, ENABLE],
        ["SND_SOC_AMD_SOF_MACH", None, MODULE],
        ["SND_SOC_AMD_MACH_COMMON", None, MODULE],
        ["SND_SOC_SOF", None, MODULE],
        ["SND_SOC_SOF_PROBE_WORK_QUEUE", None, ENABLE],
        ["SND_SOC_SOF_IPC3", None, ENABLE],
        ["SND_SOC_SOF_INTEL_IPC4", None, ENABLE],
        ["SND_SOC_SOF_AMD_COMMON", None, MODULE],
        ["SND_SOC_SOF_AMD_ACP63", None, MODULE],
        ["SND_SOC_AMD_ACP_PCI", None, UNSET],
        ["SND_AMD_ASOC_RENOIR", None, UNSET],
        ["SND_AMD_ASOC_REMBRANDT", None, UNSET],
        ["SND_SOC_AMD_LEGACY_MACH", None, UNSET],
        ["SND_SOC_TOPOLOGY", None, ENABLE],

    ],
}

def generate_line(c, v) -> str:
    if v == UNSET:
        v = f"# {c} is not set"
    else:
        v = f"{c}={v}"
    return v

def apply_patches(data: str, patches, flags = None) -> str:
    if flags is None:
        flags = []

    for name, *val in patches:
        if not name.startswith("CONFIG_"):
            name = f"CONFIG_{name}"

        s = f"{name}="
        u = f"# {name} "

        if len(val) == 3 and val[2] not in flags:
            continue

        if any(x in data for x in [s, u]):
            try:
                i = data.index(s)
            except ValueError:
                i = data.index(u)

            try:
                line_start = data.rindex("\n", 0, i)+1
            except ValueError:
                # No newline before the config?
                # Probably the first line in the file
                line_start = 0

            line_end = data.index("\n", line_start)

            line = data[line_start:line_end]

            if val[0] is not None:
                # verify we found what we expect
                l = generate_line(name, val[0])
                if l != line:
                    #print(f"    Could not apply {name}: could not find expected config")
                    continue
            data = data[:line_start] + generate_line(name, val[1]) + data[line_end:]

        elif val[0] is None:
            # relevant entry does not exist yet and we don't want to replace anything specific
            data += generate_line(name, val[1])
            data += "\n"
        else:
            print(f"    Couldn't find {name}")
            exit(1)

    return data

CONFIG_FILES = sys.argv[1:]
if not CONFIG_FILES:
    print("No config files given")
    exit(1)

# Verify all given inputs first before working with them
for file in CONFIG_FILES:
    if not os.path.isfile(file):
        print(f"{file} does not exist")
        exit(1)

    filename = os.path.basename(file)
    if not filename.endswith(CONFIG_FILE_EXT):
        print(f"{file} does not have the right file extension")
        exit(1)

    namesegs = filename[:-len(CONFIG_FILE_EXT)].split("-")
    if len(namesegs) < 3:
        print(f"{file} does not have the right number of segments")
        exit(1)

    if namesegs[0] != "kernel":
        print(f"{file} does not appear to be a kernel config")
        exit(1)

for file in CONFIG_FILES:
    filename = os.path.basename(file)
    print(f"Processing {filename}...")

    namesegs = filename[:-len(CONFIG_FILE_EXT)].split("-")
    namesegs.pop(0)

    arch = namesegs.pop(0)
    flavor = namesegs.pop(-1)
    flags = namesegs

    flags.append(flavor)
    if "debug" not in flags:
        flags.append("release")

    with open(file, "r+") as fd:
        data = fd.read()
        fd.seek(0)

        data = apply_patches(data, GENERIC_PATCHES, flags)
        if arch in ARCH_PATCHES:
            data = apply_patches(data, ARCH_PATCHES[arch], flags)

        fd.write(data)
        fd.truncate()

    data = open(file, "r").read()
