# Digital Twin

This repository helps you easily create a digital twin of your robot.

## Getting Started

First, you need to authenticate with the kscale api by running
```
pip install kscale
kscale user key
```

To list all the robots you can use as puppets, run
```
kscale robots list
```

## Digital Twin Structure

### Puppets

These are your digital twin robots. They receive actions from the actors and mirror their behavior. Currently, we support the following puppet types:

- [Mujoco](digital_twin/puppet/mujoco.py)
- [PyBullet](digital_twin/puppet/pybullet.py)

### Actors

These are the sources of actions for your puppet robots. Essentially your input sources. Currently, we support the following actor types:

- [Keyboard](digital_twin/actor/keyboard.py)
- [Sinusoid](digital_twin/actor/sinusoid.py)
- [PyKOS](digital_twin/actor/pykos.py)
    - gRPC client for KOS-compatible robots

## Examples

See the [examples](examples) directory for a few examples.

