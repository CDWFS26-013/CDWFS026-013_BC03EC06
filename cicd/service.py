import os
import json

class Water():
    
    @staticmethod
    def _open_load_water(water_path):
        water = {}
        if os.path.isfile(water_path):
            with open(water_path, 'r') as f:
                data = f.read()
                water = json.loads(data)
        return water

    @staticmethod
    def _write_water(water_path, water_content):
        with open(water_path, 'w') as f:
            f.write(water_content)


    @staticmethod
    def read_water(water_path = './water.json'):
        water = Water._open_load_water(water_path)
        return water

    @staticmethod
    def read_water_by_user(user_id, water_prefix = 'water'):
        water_path = f'./{water_prefix}_{user_id}.json'
        water = Water._open_load_water(water_path)
        return water

    @staticmethod
    def save_water(water, water_path='./water.json'):
        water_json = json.dumps(water)
        Water._write_water(water_path, water_json)
        return water

    @staticmethod
    def save_water_by_user(water, user_id, water_prefix='water'):
        water_json = json.dumps(water)
        water_path = f'./{water_prefix}_{user_id}.json'
        Water._write_water(water_path, water_json)
        return water