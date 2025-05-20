# **Kanka Random NPC Creator**

Hi, and thanks for taking the time to checkout this small project!

This mini project basically allows you to create as many random npcs
as you want in your kanka campaign.

# Setup:
1. [Install python 3.x](https://wiki.python.org/moin/BeginnersGuide/Download)
2. `pip install requirement.txt`
3. Create a Personal Access Token on your kanka account as described [here](https://kanka.io/en-US/docs/1.0/setup)
4. Create a .env file based on the .env_example . The only env variable that you will
probably want to modify is the *APITOKEN*
5. Run `python3 ./npc-gen.py`

By default it will check for a valid APITOKEN and complain if one is not set. 

In additon to setting parameters in `.env` you can also specify some inline with the command. These options can be seen with `--help`
```
python3 ./npc-gen.py --help
usage: npc-gen.py [-h] [--host HOST] [--campaign CAMPAIGN] [--count COUNT]

Generate random NPCs in a Kanka campaign.

options:
  -h, --help           show this help message and exit
  --host HOST          Set API base DOMAINNAME (e.g. kanka.example.com)
  --campaign CAMPAIGN  Specify campaign name directly
  --count COUNT        Number of NPCs to generate
```

If no options are specified, it will use the settings in `.env` to connect to the server and poll the campaigns prompting you to select oee
and how many NPCs you wish to create

The characters created by this script have the "random_npc" type. So that
you can filter them out easily.

The names for the NPCs are requested from names.drycodes.com while the
other details are randomly chosen from the JSONs found in the data folder.

Feel free to add stuff to them OR use your own JSONs by pointing the DATA_PATH
env variable to their location (make sure that they are named like the ones
in the data folder tho!).

If by any chance you want to update and/or enrich the existing JSONs, create a PR.

Have a great time!
