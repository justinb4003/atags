# TriSonics 4003 Apriltag related code

This will be a temporary location for experimenting with Apriltags.

To run the ```main.py``` file in the repository you will need to:

- Install Python (https://www.python.org)
- Create a virtual environment
- Install the packages in ```requirements.txt``
- Execute the script

After you've installed the Python package for your system you will need to open a command terminal and run the following:

```python3 -m venv venv-apr``` This creates a new virtual environment.

```.\venv-apr\Scripts\activate``` on Windows or ```. ./venv-apr/bin/activate``` on Linux or macOS to activate the environment

```pip install -r requirements.txt``` to install the packages listed in that file.

```python main.py``` to execute the script. Press 'q' in the window displaying the image to terminate the script cleanly.

By default the code will open camera ```0``` which is usually a safe bet as that's the first number assigned to the first camera in a system. If you want to use a USB camera on a system that already has a bult in one you might need to change it to ```1``` to find the correct camera.