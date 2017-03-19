# ArmLab

## Dependency

### LCM

Follow [this](http://lcm-proj.github.io/build_instructions.html). 
Basically, clone the repo and compile, 
but the last step should be `sudo make install` rather than `make install`.
After that, run `python` followed by `import lcm` to ensure lcm is installed.

## Compile

To generate LCM python code,

```
lcm-gen -p lcmtypes/* --ppath lcm/
```

To compile the arm driver C code,

```
make
```

## Setup

To run everything,

```
./up.sh
```
