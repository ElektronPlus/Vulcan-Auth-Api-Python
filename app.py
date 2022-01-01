from flask import Flask, request, jsonify
from vulcan import Account, Keystore, Vulcan
import json
import asyncio

app = Flask(__name__)

@app.route('/register')
async def main():
    try:
        token = request.args.get('token')
        pin = request.args.get('pin')
        keystore = Keystore.create(device_model="Elektron Discord")
        account = await Account.register(keystore, token, "zielonagora", pin)
        client = Vulcan(keystore, account)
        await client.select_student()
        student = client.student
        if "zielonagora-001250" in student.symbol_code:
            name = student.pupil.first_name + " " + student.pupil.last_name
            klasa = student.class_
            return jsonify(
                name=name,
                klasa=klasa
            )
        else: raise Exception('Nie chodzisz do elektrona')

    except Exception as e:
        return jsonify(error=repr(e))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5555, debug=False)
