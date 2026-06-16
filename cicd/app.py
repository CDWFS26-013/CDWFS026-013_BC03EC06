from flask import Flask
import datetime
from service import Water


app = Flask(__name__)


# Ajoute de l'eau
@app.route('/add_water', methods=['PUT'])
def add_water():
    water = Water.read_water()
    if 'water' in water:
        print(water)
        water["water"] += 10
        if "adding" not in water.keys():
            water["adding"] = [{'added_at': str(datetime.datetime.now()), 'quantity': 10}]
            return Water.save_water(water)
        else:
            water["adding"].append({'added_at': str(datetime.datetime.now()), 'quantity': 10})
            return Water.save_water(water)
    return water

# Get water
@app.route('/water', methods=['GET'])
def water():
    app.logger.info(f'getting water at {datetime.datetime.now()}')
    return Water.read_water()


@app.route('/add_water/<user_id>', methods=['PUT'])
def add_water_user(user_id):
    water = Water.read_water_by_user(user_id=user_id)
    if 'water' in water:
        print(water)
        water["water"] += 10
        Water.save_water_by_user(water, user_id)
    return water

@app.route('/check_alert/<user_id>', methods=['GET'])
def check_alert(user_id):
    threshold = 10
    water = Water.read_water_by_user(user_id=user_id)
    if water and 'water' in water:
        if water['water'] < threshold:
            return {'msg': 'alert missing water', 'threshold': threshold}
        else:
            return {'msg': 'everything is ok', 'threshold': threshold}
    return {'msg': 'missing water information', 'threshold': threshold}

if __name__ == '__main__':
    app.run(debug=True)
else:
    print('using as import')
