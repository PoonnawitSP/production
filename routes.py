from flask import Flask,  request, jsonify, render_template
from app import app
from models import user

@app.route('/signIn', methods=['POST'])
def signIn():
    return user().signIn()