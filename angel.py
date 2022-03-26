'''
tAngel angel-mortal matching code
Author: Sriram Sami + Elgene 2021 update
Version: 0.0.1



Program input: List of participants
Program output: Participants matched to each other forming either a) one complete ring or b) multiple complete rings. No lone particpants are allowed.

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
'''
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

# Constants
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_NONBINARY = "non-binary"
GENDER_NOPREF = "no preference"

GENDER_SWAP_PREFERENCE_PERCENTAGE = 0.0  # 100 if you wanna change all players with no gender pre to have genderpref = opposite gender, 0 if you wanna all to remain as no geneder pref

# Get Logger
logger = MyLogger()


def read_csv(filename):
    person_list = []

    try:
        csv_file = open(filename, 'r')
        csv_reader = csv.reader(csv_file, delimiter=',')
    except FileNotFoundError as e:
        err_msg = f"Player list csv file does not exist or is incorrectly named. Was specified as {PLAYERFILE}"
        logger.error(err_msg)
        print("Error: " + err_msg)
        exit()

    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            logger.info(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            new_person = convert_to_player(row)
            person_list.append(new_person)
            logger.debug(f'Adding line {line_count + 1}, {str(new_person)}')
            line_count += 1
    logger.info(f'Processed {line_count} players into person_list successfully.')
    return person_list


def convert_to_player(row):
    try:
        config_file = open("config.yml", 'r')
        index_dict = yaml.full_load(config_file)["player_attribute_index"]

        player_username = row[index_dict["telegram_username"]].strip().lower()
        player_name = row[index_dict["name"]].strip().lower()
        gender_pref = row[index_dict["gender_pref"]].strip().lower()
        gender_player = row[index_dict["gender"]].strip().lower()
        interests = row[index_dict["interests"]].strip()
        two_truths_one_lie = row[index_dict["two_truths_one_lie"]].strip()
        introduction = row[index_dict["introduction"]].strip()
        house_number = row[index_dict["house_number"]].strip().lower()
        year_of_study = row[index_dict["year_of_study"]].strip().lower()
        faculty = row[index_dict["faculty"]].strip().lower()
        likes = row[index_dict["likes"]].strip().lower()
        dislikes = row[index_dict["dislikes"]].strip().lower()
        comments = row[index_dict["comments"]].strip().lower()

    except FileNotFoundError as e:
        err_msg = f"Exception {e}: \"config.yml\" was not found."
        logger.error(err_msg)
        print("Error: " + err_msg)
        exit()
    except yaml.YAMLError as e:
        err_msg = f"Invalid yml config file: \n {e}: "
        logger.error(err_msg)
        print("Error: " + err_msg)
        exit()
    except KeyError as e:
        err_msg = f"Exception {e}: Key in player_attribute_index of config.yml should not be changed. Key used here " \
                  f"should match those in the config.yml dictionary. "
        logger.error(err_msg)
        print("Error: " + err_msg)
        exit()
    except IndexError as e:
        err_msg = f"Exception {e}: Index value in player_attribute_index of config.yml is not within range of given " \
                  f"playlist.csv. Pls check if columns correspond to their respective indexes. "
        logger.error(err_msg)
        print("Error: " + err_msg)
        exit()

    return Player(username=player_username,
                  playername=player_name,
                  genderpref=gender_pref,
                  genderplayer=gender_player,
                  interests=interests,
                  twotruthsonelie=two_truths_one_lie,
                  introduction=introduction,
                  housenumber=house_number,
                  yearofstudy=year_of_study,
                  faculty=faculty,
                  likes=likes,
                  dislikes=dislikes,
                  comments=comments, )


def modify_player_list(player_list):
    # Force hetero mix
    for player in player_list:
        if player.genderpref == GENDER_NOPREF:
            random_change_preference = random.random() < GENDER_SWAP_PREFERENCE_PERCENTAGE
            if player.genderplayer == GENDER_MALE and random_change_preference:
                logger.debug(f"Setting preference of {str(player)} Male -> Female")
                player.genderpref = GENDER_FEMALE
            elif player.genderplayer == GENDER_FEMALE and random_change_preference:
                logger.debug(f"Setting preference of {str(player)} Female -> Male")
                player.genderpref = GENDER_MALE


def write_to_csv(index, name01, *player_lists):
    '''
    Writes a variable number of player lists to csv
    '''
    for player_list in player_lists:
        if player_list is not None:
            logger.info(f"Length of list: {len(player_list)}")
            cur_time = time.strftime("%Y-%m-%d %H-%M-%S")
            with open(f"{index} - {name01} - {cur_time}.csv", 'w',
                      newline='') as f:  # In Python 3, if do not put newline='' AND choose 'w' instead of 'wb', you will have an empty 2nd row in output .csv file.
                writer = csv.writer(f, delimiter=',')
                header = ['Telegram Username', 'Name', 'GenderPref', 'Gender', 'Interests', '2truths1lie', 'Intro',
                          'House', 'CG', 'Year', 'Faculty']  # add header to output csv file
                writer.writerow(i for i in header)
                for player in player_list:
                    if '\n' in player.twotruthsonelie:
                        string1 = player.twotruthsonelie
                        string2 = string1.replace('"', "'")  # JUST IN CASE PEOPLE TYPE " which can screw up a csv file
                        string3 = ''.join(('"', string2,
                                           '"'))  # Double quotations are what CSV uses to keep track of newlines within the same cell
                        player.twotruthsonelie = string3

                    if '\n' in player.interests:
                        string11 = player.interests
                        string12 = string11.replace('"', "")  # JUST IN CASE PEOPLE TYPE " which can screw up a csv file
                        string13 = ''.join(('"', string12,
                                            '"'))  # Double quotations are what CSV uses to keep track of newlines within the same cell
                        player.interests = string13

                    if '\n' in player.introduction:
                        string21 = player.introduction
                        string22 = string21.replace('"',
                                                    "'")  # JUST IN CASE PEOPLE TYPE " which can screw up a csv file
                        string23 = ''.join(('"', string22,
                                            '"'))  # Double quotations are what CSV uses to keep track of newlines within the same cell
                        player.introduction = string23

                    f.write(player.to_csv_row())
                    f.write("\n")
                # write the first player again to close the loop
                #     f.write(player_list[0].to_csv_row())
                #     f.write("\n")
                f.close()


def difference_operator_lists(li1, li2):  # Used to find out the rejected players
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


if __name__ == "__main__":
    logger.info(f"=============================================")
    logger.info(f"tAngel 2021 engine initializing..............")
    logger.info(f"=============================================")

    # Get list of Player objects from csv file
    player_list = read_csv(PLAYERFILE)
    # Map the player list through any neccessary transformations
    modify_player_list(player_list)
    # separate the players into player-chains (connected components)
    list_of_player_chains = angel_mortal_arrange(player_list)
    # Write each chain to a separate csv
    logger.info("Writing chains to csvs")
    for index, player_chain in enumerate(list_of_player_chains):
        write_to_csv(index, "accepted", player_chain)
        # creating csv list of rejected players
        rejected_players_list = difference_operator_lists(player_list, player_chain)
        if len(rejected_players_list) == 0:
            logger.info("Rejected players list is empty")
        else:
            write_to_csv(index, "rejected", rejected_players_list)
            logger.info("Rejected players list csv created")
    logger.info("Angel completed successfully - terminating")
