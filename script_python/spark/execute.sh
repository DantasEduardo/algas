#!/bin/bash
python raw_staged.py
python staged_consumed.py
python send_data.py