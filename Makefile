all: clean zip

clean:
	rm -rf blender-cem-addon.zip
	rm -rf ./addon/__pycache__

zip:
	zip -r blender-cem-addon.zip ./addon
install:
	pip install -r requirements.txt
lint:
	autopep8 --in-place --aggressive --recursive -v ./addon