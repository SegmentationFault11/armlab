#!/bin/bash

# Kill existing session if any and create a new one.
SESSION=$USER
tmux kill-session -t $USER
tmux -2 new-session -d -s $SESSION

# Work session.
tmux new-window -t $SESSION:1 -n 'Work'
tmux select-window -t $SESSION:1
tmux kill-window -t 0
# Set up panels.
tmux split-window -h
tmux select-pane -t 0
tmux split-window -v
tmux select-pane -t 2
tmux split-window -v
# Send commands.
tmux select-pane -t 0
tmux send-keys 'cd bin' C-m
tmux send-keys 'cd ./rexarm_driver' C-m
tmux select-pane -t 1
tmux send-keys 'cd rexarm_python' C-m
tmux send-keys 'python control_station.py' C-m
tmux select-pane -t 2
tmux send-keys 'cd bin' C-m
tmux send-keys './bottle_recognizer' C-m
tmux select-pane -t 3
tmux send-keys 'cd web' C-m
tmux send-keys 'python app.py' C-m
tmux a
