all: clean zip

clean:
	rm -rf blender-cem-addon.zip

zip:
	zip -r blender-cem-addon.zip .

