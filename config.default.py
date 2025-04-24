################
# Instructions #
################

# 1. Rename this file to config.py
# 
# 2. Fill in the variables in the Canvas API Connections
#    There are instructions provided for how to get each value
#
# 3. Change variables that pertain to the assignment grading
#
# 4. Set the percentages for each part that the autograder checks

##########################
# Canvas API Connections #
##########################

# This is already set for the Stevens Canvas URL
API_URL = "https://sit.instructure.com/"

# https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312
API_TOKEN = "ENTER YOUR API TOKEN HERE"

# https://13kb.helpscoutdocs.com/article/551-how-to-locate-canvas-course-and-section-id
COURSE_ID = "ENTER COURSE ID HERE"

# Same process as getting course id, navigate to assignment and check the URL
ASSIGNMENT_ID = "ENTER ASSIGNMENT ID HERE"

########################
# Assignment Variables #
########################

# Ex: BANNED_SQL_KEYWORDS = ["Coalesce", "Limit", "Row_number", "Case", "While"]
BANNED_SQL_KEYWORDS = ["ENTER BANNED SQL KEYWORDS HERE"]

#####################
# Grading Variables #
#####################

# Values represent percentages and must add to 100
# Ex:
# CORRECT_NUM_HEADERS_PERCENTAGE = 5
# CORRECT_HEADERS_PERCENTAGE = 10
# CORRECT_NUM_RECORDS_PERCENTAGE = 5
# CORRECT_RECORDS_PERCENTAGE = 75
# CORRECT_ORDER_PERCENTAGE = 5
CORRECT_NUM_HEADERS_PERCENTAGE = 0
CORRECT_HEADERS_PERCENTAGE = 0
CORRECT_NUM_RECORDS_PERCENTAGE = 0
CORRECT_RECORDS_PERCENTAGE = 0
CORRECT_ORDER_PERCENTAGE = 0

###############
# DO NOT EDIT #
###############

RED    = "\033[31m"  
YELLOW = "\033[33m"
GREEN  = "\033[32m"
RESET  = "\033[0m"