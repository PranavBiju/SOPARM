#!/bin/bash
 
while true; do
python3 recorder.py
echo "A new file appeared!"
python3 Speech_pipe.py
python3 ans.py
    
done
