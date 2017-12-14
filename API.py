import sys
from itertools import product

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
from sklearn.model_selection import train_test_split
from sklearn import metrics

import time
import os, sys

import csv
from urllib.parse import urljoin
import pickle

##User needs to run the crawler file "17-18 Team Avg.py" first to get up to date 17-18 team stats as .txt file first, then run this file


def UI_port(home, away):

    with open("1718_Team_Avg.txt", "r") as txt_file:
        with open("1718_Team_Avg.csv", "w") as csv_file:
            in_txt = csv.reader(txt_file, delimiter='\t')
            out_csv = csv.writer(csv_file)
            out_csv.writerows(in_txt)

    abs_path = urljoin(os.getcwd(),
                       'project/1718_Team_Avg.csv')

    df_team = pd.read_csv('1718_Team_Avg.csv', header=None,
                          names=['TEAM', 'GP', 'W', 'L', 'WIN%', 'MIN', 'EFG%', 'FTA RATE', 'TOV%', 'OREB%', 'OPP_EFG%','OPP_FTA RATE','OPP_TOV%', 'OPP_OREB%', 'NAN'])

    #print(df_team)
    del df_team['NAN']
    #df_team=df_team['TEAM', 'GP', 'W', 'L', 'WIN%', 'MIN', 'EFG%', 'FTA RATE', 'TOV%', 'OREB%', 'OPP_EFG%','OPP_FTA RATE','OPP_TOV%', 'OPP_OREB%']

    df_team = df_team.reset_index(drop=True)

    dictionary = {'Atlanta Hawks': 'ATL',
                  'Boston Celtics': 'BOS',
                  'Brooklyn Nets': 'BKN',
                  'Charlotte Hornets': 'CHA',
                  'Chicago Bulls': 'CHI',
                  'Cleveland Cavaliers': 'CLE',
                  'Dallas Mavericks': 'DAL',
                  'Denver Nuggets': 'DEN',
                  'Detroit Pistons': 'DET',
                  'Golden State Warriors': 'GSW',
                  'Houston Rockets': 'HOU',
                  'Indiana Pacers': 'IND',
                  'LA Clippers': 'LAC',
                  'Los Angeles Lakers': 'LAL',
                  'Memphis Grizzlies': 'MEM',
                  'Miami Heat': 'MIA',
                  'Milwaukee Bucks': 'MIL',
                  'Minnesota Timberwolves': 'MIN',
                  'New Orleans Pelicans': 'NOP',
                  'New York Knicks': 'NYK',
                  'Oklahoma City Thunder': 'OKC',
                  'Orlando Magic': 'ORL',
                  'Philadelphia 76ers': 'PHI',
                  'Phoenix Suns': 'PHX',
                  'Portland Trail Blazers': 'POR',
                  'Sacramento Kings': 'SAC',
                  'San Antonio Spurs': 'SAS',
                  'Toronto Raptors': 'TOR',
                  'Utah Jazz': 'UTA',
                  'Washington Wizards': 'WAS'}

    team_list = []

    for team in df_team['TEAM']:
        team_list.append(dictionary[team])

    df_team['TEAM'] = team_list

    list_1 = ['TEAM_BKN', 'TEAM_BOS', 'TEAM_CHA', 'TEAM_CHI', 'TEAM_CLE', 'TEAM_DAL', 'TEAM_DEN', 'TEAM_DET',
              'TEAM_GSW', 'TEAM_HOU', 'TEAM_IND', 'TEAM_LAC', 'TEAM_LAL', 'TEAM_MEM', 'TEAM_MIA', 'TEAM_MIL',
              'TEAM_MIN', 'TEAM_NOP', 'TEAM_NYK', 'TEAM_OKC', 'TEAM_ORL', 'TEAM_PHI', 'TEAM_PHX', 'TEAM_POR',
              'TEAM_SAC', 'TEAM_SAS', 'TEAM_TOR', 'TEAM_UTA', 'TEAM_WAS']
    list_2 = ['OPP_BKN', 'OPP_BOS', 'OPP_CHA', 'OPP_CHI', 'OPP_CLE', 'OPP_DAL', 'OPP_DEN', 'OPP_DET', 'OPP_GSW',
              'OPP_HOU', 'OPP_IND', 'OPP_LAC', 'OPP_LAL', 'OPP_MEM', 'OPP_MIA', 'OPP_MIL', 'OPP_MIN', 'OPP_NOP',
              'OPP_NYK', 'OPP_OKC', 'OPP_ORL', 'OPP_PHI', 'OPP_PHX', 'OPP_POR', 'OPP_SAC', 'OPP_SAS', 'OPP_TOR',
              'OPP_UTA', 'OPP_WAS']

    onehot_team = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    onehot_opp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    string_team = 'TEAM_' + home

    #print(type('OPP_'))
    #print(type(away))
    string_opp = 'OPP_' + away

    for i in range(len(list_1)):
        if list_1[i] == string_team:
            onehot_team[i] = 1
            break

    for j in range(len(list_2)):
        if list_2[j] == string_opp:
            onehot_opp[j] = 1
            break

    df_onehot_team = pd.DataFrame([onehot_team])
    df_onehot_team.columns = list_1

    df_onehot_opp = pd.DataFrame([onehot_opp])
    df_onehot_opp.columns = list_2

    df = df_onehot_team.join(df_onehot_opp)

    column_name = ['MIN', 'EFG%', 'FTA RATE', 'TOV%', 'OREB%', 'OPP_EFG%', 'OPP_FTA RATE', 'OPP_TOV%', 'OPP_OREB%',
                   'Home/Away', 'REST', 'OPP_REST']

    list_app = [48]

    for i in range(len(df_team)):
        if df_team['TEAM'][i] == home:
            list_app.extend([df_team['EFG%'][i] * 0.01, df_team['FTA RATE'][i], df_team['TOV%'][i] * 0.01,
                             df_team['OREB%'][i] * 0.01])
            break

    for j in range(len(df_team)):
        if df_team['TEAM'][j] == away:
            list_app.extend([df_team['EFG%'][j] * 0.01, df_team['FTA RATE'][j], df_team['TOV%'][j] * 0.01,
                             df_team['OREB%'][j] * 0.01])
            break

    list_app.extend([1, 1, 1])

    df_app = pd.DataFrame([list_app])
    df_app.columns = column_name

    df = df.join(df_app)

    X = df.values

    classification = pickle.load(open('finalized_model_classification.sav', 'rb'))

    ##regression = pickle.load(open('finalized_model_regression.sav', 'rb'))

    result_1 = classification.predict(X)

    ##result_2 = regression.predict(X)

    return result_1 ##, result_2


