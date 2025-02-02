import icnsutil

# Load the PNG file
file = "./../App/resources/icon.png"
output = ""

# compose
img = icnsutil.IcnsFile()
img.add_media(file=file)
img.write("./../App/resources/icon.ico")
img.write("./../App/resources/icon.icns")
