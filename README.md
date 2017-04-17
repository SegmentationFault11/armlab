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
lcm-gen -p lcmtypes/* --ppath lcm_python/
```

To compile the C code,

```
make
```

## Setup

To run everything,

```
./up.sh
```

## [Important](https://askubuntu.com/questions/391564/how-do-you-use-chirp)

That error means you are not allowed to access /dev/ttyS0 on your computer. Only root and users in the dialout group may access that device.

If you are running chirp as a normal user (I assume you are), the problem is probably quite simply that your user does not belong to the dialout group. Try the following command:

```
sudo usermod -aG dialout USERNAME
```

where you replace USERNAME with your own username, of course. Log out and in again, fire up chirp, it should now work.


