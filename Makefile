all: clean zip

clean:
	rm -rf blender-cem-addon.zip

zip:
	zip -r blender-cem-addon.zip .
install:
	pip install -r requirements.txt
lint:
	autopep8 --in-place --aggressive --recursive -v ./addon