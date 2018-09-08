rm -rf ./dist/
rm -rf ./gym_hearts.egg-info/
python3 setup.py sdist --formats=zip
python3 setup.py sdist --formats=zip upload
