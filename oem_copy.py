import re
import subprocess
import os, os.path
import json
import sys

# Path where device.ini exists - will include the vendor information
devicePath = "/flashVolume/flashDisk/HighLink/Config/Odu/device.ini"
imagesPath = "/app/flask/dist/assets/img"
iconPath    =   "/app/flask/dist/assets/icon"
releaseFile =   "/app/flask/dist/assets/files/release.json"

# Filenames that should be referenced and handled
filenames 	= 	["login_background.jpg", "logo.png"]

# Check if device.ini file exists, if not leave the script
if (os.path.exists(devicePath) != True):
    print "Could not find device.ini file, existing OEM script"
    sys.exit(os.EX_OK)

# Initialize vendor name
vendorName = "NA"
release = 'NA'


faviconExists = False
bgExists = False
logoExists = False

# Open device file for reading
deviceFile = open(devicePath)

# Go over all lines in device.ini and find the Vendor name
for line in deviceFile:
    foundOem = re.search("\s?VendorID=(.*);", line)

    foundRelease = re.search('\s?CardSoftwareVersion=(.*);', line)

    # If it does, print it delimited by |
    if foundOem:
        vendorName = foundOem.group(1)

    if foundRelease:
        release = foundRelease.group(1)

# Check that a vendor name and release was found
if vendorName == "NA":
    print "Could not find vendor name in device.ini"
    sys.exit(os.EX_OK)

if release == "NA":
    print "Could not find release in device.ini"
    sys.exit(os.EX_OK)

releaseFileData = {}
releaseFileData['release'] = release.split('_')[0]
releaseFileData['build'] = release.split('_')[1]
releaseFileData['vendor'] = vendorName

try:
    with open(releaseFile, 'w+') as fileToSave:
        json.dump(releaseFileData, fileToSave)

    print 'release.json created'
except:
    print "Count not create release.json\n"
    print sys.exc_info()[0]
    sys.exit(os.EX_OK)


# Go over all files that need to be linked and form the links
try:
    for file in filenames:
        # Delete the current link if exists
        fullPath = "{0}/{1}".format(imagesPath,file)
        if os.path.exists(fullPath):
            subprocess.call(["rm", fullPath])
            
        # Generate the new link
        subprocess.call(["ln", "-s", "{0}/{1}/{2}".format(imagesPath,vendorName,file), fullPath])
        print "OEM recognized. " + file + " copied ..."
except subprocess.CalledProcessError:
    print "Failed creating link to {0}".format(file)
except:
    print sys.exc_info()[0]
    print 'Error occurred'
    sys.exit(os.EX_OK)

try:
    fullPath = "{0}/{1}".format(iconPath, 'favicon.ico')
    if os.path.exists(fullPath):
        print "Full Path: " + fullPath
        subprocess.call(["rm", fullPath])

    subprocess.call(["ln", "-s", "{0}/{1}/{2}".format(iconPath, vendorName, 'favicon.ico'), fullPath])
    print "OEM recognized. favicon.ico copied ..."
except:
    print sys.exc_info()[0]
    print 'Error occurred'
    sys.exit(os.EX_OK)
