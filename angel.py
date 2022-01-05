"""
tAngel angel-mortal matching code
Author: Sriram Sami + Elgene 2021 update
Version: 0.0.1



Program input: List of participants Program output: Participants matched to each other forming either a) one complete
ring or b) multiple complete rings. No lone particpants are allowed.

Priorities (decreasing order) [must be done]:
1) Forming complete circles (everyone MUST have an angel and mortal)
2) Respecting gender choices

Optimization objective - get people you DON'T KNOW AT ALL
Optimization priorities:
1) Angel - Mortal relationship - they must not know each other as much as possible
- Achieved by separating by HOUSE (floor) and FACULTY

Distance (or whether an edge exists between two nodes) is a function of:
1) Whether they are of different houses
2) Whether their faculties are different
"""
# IMPORTS
import csv
import time
import random
import yaml

# FROMS
from MyLogger import MyLogger
from models import Player
from arrange import angel_mortal_arrange

# GLOBALS
PLAYERFILE = "playerlist.csv"
CONFIGFILE = "config.yml"

# Constants
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_NONBINARY = "non-binary"
GENDER_NOPREF = "no preference"

GENDER_SWAP_PREFERENCE_PERCENTAGE = 0.0  # 100 if you wanna change all players with no gender pre to have genderpref = opposite gender, 0 if you wanna all to remain as no geneder pref

# Get Logger
logger = MyLogger()


def read_csv(filename, column_names_index_dict):
    person_list = []

    try:
        csv_file = open(filename, 'r')
        csv_reader = csv.reader(csv_file, delimiter=',')
    except FileNotFoundError as e:
        print("WARNING: {} file does not exist or is incorrectly named.".format(filename))
        exit()

    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            logger.info(f'Column names are {", ".join(row)}')
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            # new_person = convert_to_player(row, column_names_index_dict)
            new_person = generalized_convert_to_player(row, column_names_index_dict)
            person_list.append(new_person)
            logger.info(f'Adding ' + str(new_person))
            print(f'Adding ' + str(new_person))
            line_count += 1
    print(f'Processed {line_count} players.')
    logger.info(f'Processed {line_count} players.')
    logger.info(f'person_list has been processed successfully')
    return person_list


def generalized_convert_to_player(row, column_names_index_dict):
    player_data = []

    try:
        special_columns = column_names_index_dict["special columns"]
        enum_columns = column_names_index_dict["enum columns"]
        text_columns = column_names_index_dict["text columns"]

        player_data = (generate_column_key_value_pair(special_columns, row) +
                       generate_column_key_value_pair(text_columns, row) +
                       generate_column_key_value_pair(enum_columns, row, check_enum_columns_input_valid))

        print("output is\n", player_data)

    except FileNotFoundError as e:
        print("WARNING: Config file is named incorrectly or does not exist.")
        exit()
    except KeyError as e:
        print("WARNING: Key in generalized_columns of config.yml should not be changed. Key used here should match "
              "those in the config.yml dictionary.")
        exit()
    except IndexError as e:
        print("WARNING: Index value in generalized_columns of config.yml is not within range of given playlist.csv."
              " Pls check if columns correspond to their respective indexes.")
        exit()

    return Player(player_data)


def generate_column_key_value_pair(type_of_column, row, function=None):
    output = []
    for column_name in type_of_column:
        # obtains the value of passsing the column_name
        column_dict = type_of_column[column_name]
        if isinstance(column_dict, int):
            # if it column_dit is an integer, it is because it is from special columns or text columns
            row_input = row[column_dict]
        else:
            row_input = row[column_dict['index']]
        if function is not None:
            valid = function(type_of_column, column_dict, row_input.strip().lower())
            if not valid:
                # outputs the element of which person that is not within the valid range for that
                print(f"ERROR: {row_input.strip().lower()} of the column {column_name} of {row[0]} is not within the "
                      f"allowed values of {column_name}")
                exit()
        output.append({column_name: row_input})
    return output


def check_enum_columns_input_valid(type_of_column, data, row_input):
    column_type = type(data['allowed_values'])
    if column_type is list:
        validity = row_input in data['allowed_values']
        return validity
    elif column_type is dict:
        dict_values_as_list = list(data['allowed_values'].values())
        lower_bound = dict_values_as_list[0]
        upper_bound = dict_values_as_list[-1]
        validity = lower_bound < int(row_input) < upper_bound
        return validity
    else:
        print(f"ERROR: You have provided an invalid column type under allowed values of {type_of_column}")


# def convert_to_player(row, column_names_index_dict):
#     try:
#         telegram_username = row[column_names_index_dict["telegram_username"]].strip().lower()
#         player_name = row[column_names_index_dict["name"]].strip().lower()
#         room_number = row[column_names_index_dict["room_number"]].strip().lower()
#         house_number = row[column_names_index_dict["house_number"]].strip().lower()
#         faculty = row[column_names_index_dict["faculty"]].strip().lower()
#         gender_player = row[column_names_index_dict["gender"]].strip().lower()
#         gender_pref = row[column_names_index_dict["gender_pref"]].strip().lower()
#         year_of_study = row[column_names_index_dict["year_of_study"]].strip().lower()
#         likes = row[column_names_index_dict["likes"]].strip().lower()
#         dislikes = row[column_names_index_dict["dislikes"]].strip().lower()
#         comments = row[column_names_index_dict["comments"]].strip().lower()
#
#     except FileNotFoundError as e:
#         print("WARNING: Config file is named incorrectly or does not exist.")
#         exit()
#     except KeyError as e:
#         print("WARNING: Key in player_attribute_index of config.yml should not be changed. Key used here should match "
#               "those in the config.yml dictionary.")
#         exit()
#     except IndexError as e:
#         print("WARNING: Index value in player_attribute_index of config.yml is not within range of given playlist.csv."
#               " Pls check if columns correspond to their respective indexes.")
#         exit()
#
#     return Player(username=telegram_username,
#                   playername=player_name,
#                   housenumber=house_number,
#                   roomnumber=room_number,
#                   faculty=faculty,
#                   genderplayer=gender_player,
#                   genderpref=gender_pref,
#                   yearofstudy=year_of_study,
#                   likes=likes,
#                   dislikes=dislikes,
#                   comments=comments, )


def separate_players(player_list):
    '''
    Separates the list of player list into male_male, male_female, and
    female_female gender preference lists

    CURRENTLY USELESS FUNCTION
    '''
    male_male_list = []
    male_female_list = []
    female_female_list = []

    for player in player_list:
        if (player.genderplayer == 'male' and player.genderpref == 'male') or (
                player.genderplayer == "non-binary" and player.genderpref == "male"):
            male_male_list.append(player)
            print(
                f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to male_male_list')
            logger.info(
                f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to male_male_list')
        elif (player.genderplayer == 'female' and player.genderpref == 'female') or (
                player.genderplayer == "non-binary" and player.genderpref == "female"):
            female_female_list.append(player)
            print(
                f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to female_female_list')
            logger.info(
                f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to female_female_list')
        else:
            male_female_list.append(player)
            print(
                f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to male_female_list')
            logger.info(
                f'Added Player: {player.username}, Gender: {player.genderplayer}, GenderPref: {player.genderpref} to male_female_list')
    return male_male_list, male_female_list, female_female_list


def modify_player_list(player_list):
    # Force hetero mix
    for player in player_list:
        if player.genderpref == GENDER_NOPREF:
            random_change_preference = random.random() < GENDER_SWAP_PREFERENCE_PERCENTAGE
            if player.genderplayer == GENDER_MALE and random_change_preference:
                print(f"Male -> Female")
                player.genderpref = GENDER_FEMALE
            elif player.genderplayer == GENDER_FEMALE and random_change_preference:
                print(f"Female -> Male")
                player.genderpref = GENDER_MALE


def write_to_csv(index, name01, column_names_index_dict, *player_lists):
    '''
    Writes a variable number of player lists to csv
    '''
    for player_list in player_lists:
        if player_list is not None:
            print(f"Length of list: {len(player_list)}")
            cur_time = time.strftime("%Y-%m-%d %H-%M-%S")
            with open(f"{index} - {name01} - {cur_time}.csv", 'w', newline='') as f:  # In Python 3, if do not put newline='' AND choose 'w' instead of 'wb', you will have an empty 2nd row in output .csv file.
                writer = csv.writer(f, delimiter=',')
                index_lst = {k: v for k, v in sorted(column_names_index_dict.items(), key=lambda item: item[1])}

                header = []  # add header to output csv file
                for key, value in index_lst.items():
                    capitalised_first_letter_key = key.replace('_', " ").title()
                    header.append(capitalised_first_letter_key)

                writer.writerow(i for i in header)
                for player in player_list:
                    f.write(player.to_csv_row())
                    f.write("\n")
                # write the first player again to close the loop
                #     f.write(player_list[0].to_csv_row())
                #     f.write("\n")
                f.close()


def difference_operator_lists(li1, li2):  # Used to find out the rejected players
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


if __name__ == "__main__":
    print(f"\n\n")
    print(f"=============================================")
    print(f"tAngel 2021 engine initializing..............")
    print(f"=============================================")
    print(f"\n\n")

    # Read config_file to obtain the header column header names
    try:
        config_file = open(CONFIGFILE, 'r')
        yaml_config = yaml.full_load(config_file)
    except FileNotFoundError:
        print("ERROR: {} file does not exist".format(CONFIGFILE))
        exit()

    try:
        column_names_index_dict = yaml_config["generalized_columns"]
    except KeyError:
        print("ERROR: play_attribute_index key does not exist")
        exit()

    # Get list of Player objects from csv file
    player_list = read_csv(PLAYERFILE, column_names_index_dict)
    # Map the player list through any neccessary transformations
    modify_player_list(player_list)

    # separate the players into player-chains (connected components)
    list_of_player_chains = angel_mortal_arrange(player_list)
    # Write each chain to a separate csv
    print("done")
    for index, player_chain in enumerate(list_of_player_chains):
        write_to_csv(index, "accepted", yaml_config, player_chain)
        # creating csv list of rejected players
        rejected_players_list = difference_operator_lists(player_list, player_chain)
        if len(rejected_players_list) == 0:
            print("rejected players list is empty")
        else:
            write_to_csv(index, "rejected", column_names_index_dict, rejected_players_list)
            print("rejected players list csv created")
