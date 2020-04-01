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
5. Create a python script that uses the Generator class as shown in the example.py
file

Below is an example of how to create 5 random NPCs in the campaign called "My Cool Campaign":

```python
from Generator import NpcGenerator

gen = NpcGenerator()

gen.create_npcs('My Cool Campaign', 5)
```

The characters created by this script have the "random_npc" type. So that
you can filter them out easily.

The names for the NPCs are requested from names.drycodes.com while the
other details are randomly chosen from the JSONs found in the data folder.

Feel free to add stuff to them OR use your own JSONs by pointing the DATA_PATH
env variable to their location (make sure that they are named like the ones
in the data folder tho!).

If by any chance you want to update and/or enrich the existing JSONs, create a PR.

Have a great time!