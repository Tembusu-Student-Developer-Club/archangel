#gender tags for csv
GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_NONBINARY = "non-binary"
GENDER_NOPREF = "no preference"

GENDER_SWAP_PREFERENCE_PERCENTAGE = 0.0 #100 if you wanna change all players with no gender pre to have genderpref = opposite gender, 0 if you wanna all to remain as no geneder pref

MINIMUM_MATCHED_PLAYERS_BEFORE_CSVOUTPUT = 0.8 ##Proportion minimum of total player count in accepted csv before 2 csvs will be outputted (1st accepted players list, 2nd rejected players list

# relax requirements for arrange
# Changing this value changes how much we care about the houses of players being the same
# If 1 - we don't care, and house de-conflicting is ignored. 0 means we won't allow any players of the same house to be matched.
RELAX_GENDERPREF_REQUIREMENT_PERCENTAGE = 0.35
RELAX_NO_SAME_HOUSE_REQUIREMENT_PERCENTAGE = 0.35
RELAX_NO_SAME_CG_REQUIREMENT_PERCENTAGE = 0.00 # legacy from med, to remove
# RELAX_NO_SAME_FACULTY_REQUIREMENT_PERCENTAGE = 0.00 #not used

DISPLAY_GRAPH = True
