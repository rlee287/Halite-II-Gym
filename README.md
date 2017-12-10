# Halite II Gym

This is an improved version of the gym that ships with the hlt client tool. This tool does not have a dependency on the `zstd` module.

## Usage

Change directory into the `hlt_gym` folder and run the `hlt_gym.py` file.
If you would like to run the gym from any directory, you can add this directory into the PATH environmental variable.

Example usage:

```
./hlt_gym.py -r "python3 MyBotA.py" -r "python3 MyBotB.py" # Minimal usage
./hlt_gym.py -b /halite/path -r "python3 MyBotA.py" -r "python3 MyBotB.py" #Manually specify path to halite executable
```

Run `./hlt_gym.py --help` for a full list of options.
