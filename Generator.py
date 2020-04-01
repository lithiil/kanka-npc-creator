import os
import requests
from dotenv import load_dotenv
import json
import sys
import random


class NpcGenerator:
    """
    This class is made to create random NPCs into a specific kanka campaign
    """

    apiToken = None
    apiBaseUrl = None
    headers = None
    campaign_id = None
    dataPath = None

    """
    When instancing the class, the variables from the .env files are loaded and the following class variables are set:
    apiToken, dataPath, apiBaseUrl and headers
    """

    def __init__(self):

        load_dotenv()

        self.apiToken = os.getenv("APITOKEN")
        self.dataPath = os.getenv("DATA_PATH")
        self.apiBaseUrl = os.getenv("API_URL")
        self.headers = {
            'Authorization': self.apiToken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_campaigns(self):
        """
        This method will get a list of all the campaigns created on the account belonging to the owner of the Token
        via a HTTP get request and returns a JSON
        :return: JSON
        """
        campaigns = requests.get("{}campaigns".format(self.apiBaseUrl), headers=self.headers)
        return json.loads(campaigns.content)

    def set_campaign_id(self, campaign_name):
        """
        This method will parse the JSON generated by get_campaigns and set the campaignId with the id of the campaign
        specified in the campaign_name parameter. If no campaign can be found with that name, it will raise an error
        :type campaign_name: str
        """
        campaigns = self.get_campaigns()

        for campaign in campaigns['data']:
            if campaign['name'] == campaign_name:
                print("Found the campaign that you are looking for with id:{}".format(campaign['id']))
                self.campaign_id = campaign['id']

        if self.campaign_id is None:
            sys.exit("ERROR: No campaign with that name found!")

    def load_charater_details(self):
        """
        This method will load the three specified files from the location specified in dataPath and returns a dict
        containing json objects
        @:returns data: dict
        """
        appearance_options = json.load(open('{}appearance.json'.format(self.dataPath)))
        personality_options = json.load(open('{}personalities.json'.format(self.dataPath)))
        title_options = json.load(open('{}titles.json'.format(self.dataPath)))

        data = {
            'appearance_options': appearance_options,
            'personality_options': personality_options,
            'title_options': title_options
        }

        return data

    def genrate_npc_name(self, sex):
        """
        Will get a name via http request from drycodes.com based on the sex specified
        :type sex: str
        :return name: str
        """
        if sex is "Male":
            get_male_name = requests.get(
                'http://names.drycodes.com/1?nameOptions=boy_names&format=text&separator=space')
            name = get_male_name.text
        else:
            get_female_name = requests.get(
                'http://names.drycodes.com/1?nameOptions=girl_names&format=text&separator=space')
            name = get_female_name.text

        return name

    def generate_npcs(self, times):
        """
        Will generate a list of dicts, each dict representing a character. The character details are populated
        from the data retrieved by load_character_details. The number of characters is decided by the times parameter
        :type times: int
        :return npcs: list
        """
        npcs = []

        data = self.load_charater_details()

        for x in range(times):
            sex = random.choice(['Male', 'Female'])
            name = self.genrate_npc_name(sex)

            character = {
                'name': name,
                'title': random.choice(data['title_options']['data']),
                'age': str(random.randrange(14, 100)),
                'sex': sex,
                'type': 'random_npc',
                'is_private': 'true',
                'personality_name': ['Goals', 'Fears'],
                'personality_entry': [random.choice(data['personality_options']['goals']),
                                      random.choice(data['personality_options']['fears'])],
                'appearance_name': ['Hair', 'Eyes', 'Height', 'Marks'],
                'appearance_entry': [random.choice(data['appearance_options']['hair_type']),
                                     random.choice(data['appearance_options']['eyes']),
                                     str(round(random.uniform(4.1, 7.5), 1)) + " feet",
                                     random.choice(data['appearance_options']['marks'])]
            }

            npcs.append(character)

        return npcs

    def create_npcs(self, campaign_name=str, times=1):
        """
        Will search for the specified campaign, generate the npcs and then create then on kanka via http post requests.
        Please note that kanka has a limit of 30 calls per minute at this time
        :type times: int
        :type campaign_name: str
        """
        self.set_campaign_id(campaign_name)

        npcs = self.generate_npcs(times)

        for npc in npcs:

            print('Posting character to kanka')
            response = requests.post(
                "{}campaigns/{}/characters".format(self.apiBaseUrl, self.campaign_id),
                data=json.dumps(npc),
                headers=self.headers)

            if response.status_code is 201:
                print("Character named {} was created successfully!".format(npc['name']))
            else:
                print(
                    "Character was not created because kanka threw an error, got status code {} with error {} ".format(
                        response.status_code, response.text))
