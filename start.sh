#!/bin/bash
export GROQ_API_KEY=$(cat .env | cut -d'=' -f2)
python app.py
