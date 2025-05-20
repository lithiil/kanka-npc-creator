import os
import requests
from dotenv import load_dotenv
import json
import sys
import random
from faker import Faker
fake = Faker()


class NpcGenerator:
    """
    Generates random NPCs and creates them in a specified Kanka campaign.
    """

    def __init__(self):
        load_dotenv()


        self.apiToken = f"Bearer {os.getenv('APITOKEN')}"
        self.dataPath = os.getenv("DATA_PATH")
        self.apiBaseUrl = os.getenv("API_URL")
        self.headers = {
            'Authorization': f"{self.apiToken}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.campaign_id = None

    def get_campaigns(self):
        response = requests.get(f"{self.apiBaseUrl}campaigns", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def set_campaign_id(self, campaign_name: str):
        campaigns = self.get_campaigns()
        for campaign in campaigns.get('data', []):
            if campaign.get('name') == campaign_name:
                print(f"Found the campaign that you are looking for with id: {campaign['id']}")
                self.campaign_id = campaign['id']
                return
        sys.exit("ERROR: No campaign with that name found!")

    def load_character_details(self) -> dict:
        def load_json(filename):
            with open(os.path.join(self.dataPath, filename), 'r', encoding='utf-8') as f:
                return json.load(f)

        return {
            'appearance_options': load_json('appearance.json'),
            'personality_options': load_json('personalities.json'),
            'title_options': load_json('titles.json')
        }

#    def generate_npc_name(self, sex: str) -> str:
#        option = "boy_names" if sex == "Male" else "girl_names"
#        url = f"http://names.drycodes.com/1?nameOptions={option}&format=text&separator=space"
#        response = requests.get(url)
#        response.raise_for_status()
#        return response.text.strip()


    def generate_npc_name(self, sex: str) -> str:
        if sex == "Male":
            return fake.name_male()
        else:
            return fake.name_female()


    def generate_npcs(self, count: int) -> list:
        data = self.load_character_details()
        npcs = []

        for _ in range(count):
            sex = random.choice(['Male', 'Female'])
            name = self.generate_npc_name(sex)

            npc = {
                'name': name,
                'title': random.choice(data['title_options']['data']),
                'age': str(random.randint(14, 99)),
                'sex': sex,
                'type': 'random_npc',
                'is_private': True,
                'personality_name': ['Goals', 'Fears'],
                'personality_entry': [
                    random.choice(data['personality_options']['goals']),
                    random.choice(data['personality_options']['fears'])
                ],
                'appearance_name': ['Hair', 'Eyes', 'Height', 'Marks', 'Body Type'],
                'appearance_entry': [
                    random.choice(data['appearance_options']['hair_type']),
                    random.choice(data['appearance_options']['eyes']),
                    f"{round(random.uniform(4.1, 6.9), 1)} feet",
                    random.choice(data['appearance_options']['marks']),
                    random.choice(data['appearance_options']['body_type'])
                ]
            }
            npcs.append(npc)

        return npcs

    def create_npcs(self, campaign_name: str, count: int = 1):
        self.set_campaign_id(campaign_name)
        npcs = self.generate_npcs(count)

        for npc in npcs:
            print(f"Posting character '{npc['name']}' to Kanka")
            response = requests.post(
                f"{self.apiBaseUrl}campaigns/{self.campaign_id}/characters",
                json=npc,  # modern requests usage
                headers=self.headers
            )

            if response.status_code == 201:
                print(f"✅ Character '{npc['name']}' created successfully.")
            else:
                print(f"❌ Failed to create character '{npc['name']}': {response.status_code} - {response.text}")
