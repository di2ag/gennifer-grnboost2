import os
import pandas as pd
from pathlib import Path
import uuid
import json
import numpy as np
import shutil

from .zenodo import load_file

#DATASET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sample_data')


def generateInputs(zenodo_id):
    '''
    Function to generate desired inputs for GRNBOOST2.
    '''

    os.makedirs("/tmp/", exist_ok=True) # Create the /tmp/ directory if it doesn't exist
    uniqueID = str(uuid.uuid4())
    tempUniqueDirPath = "/tmp/" + uniqueID
    os.makedirs(tempUniqueDirPath, exist_ok=True)
    
    ExpressionData = load_file(zenodo_id, 'ExpressionData.csv')

    ExpressionData.T.to_csv(tempUniqueDirPath + "/ConvertedExpressionData.csv", sep = '\t', header  = True, index = True)
    return tempUniqueDirPath
    
def run(tempUniqueDirPath):
    '''
    Function to run GRNBOOST2 algorithm
    '''
    outPath = tempUniqueDirPath + '/outFile.txt'

    cmdToRun = ' '.join(['python runArboreto.py --algo=GRNBoost2', '--inFile=' + tempUniqueDirPath + "/ConvertedExpressionData.csv", '--outFile=' + outPath])
    os.system(cmdToRun)

    return tempUniqueDirPath

def parseOutput(tempUniqueDirPath):
    '''
    Function to parse outputs from SCODE.
    ''' 
    # Read output
    OutDF = pd.read_csv(tempUniqueDirPath+'/outFile.txt', sep = '\t', header = 0)

    results = {'Gene1': [], 
               'Gene2': [],
               'EdgeWeight': []}

    for idx, row in OutDF.iterrows():
        results['Gene1'].append(row[0])
        results['Gene2'].append(row[1])
        results['EdgeWeight'].append(str(row[2]))

    shutil.rmtree(tempUniqueDirPath)
    
    return results
    
