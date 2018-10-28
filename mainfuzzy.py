import csv
from typing import NamedTuple

input_crisp = []
output      = []

class Income (NamedTuple):
    min : float
    max : float

class Debt (NamedTuple):
    min : float
    max : float

lowIncome = Income(0.1, 0.7)
avgIncome = Income(0.7, 1.4)
hghIncome = Income(1.4, 2.0)

lowDebt = Debt(0.0, 25.0)
avgDebt = Debt(25.0, 75.0)
hghDebt = Debt(50, 75.0)

def calcLowIncome(x): #linear membership functon for low income
    if( x >= (lowIncome.max)):
        return float(0)
    elif(x <= (lowIncome.max + lowIncome.min)/2):
        hasil = 1 - 2*((x-lowIncome.min) / (lowIncome.max-lowIncome.min))**2
        return hasil
    elif(x <= (lowIncome.max)):
        hasil = 2 * ((x-lowIncome.max) / (lowIncome.max-lowIncome.min))**2
        return hasil
    return float(0)

def calcAvgIncome(x): #linear membership functon for avg income
    if( x <= avgIncome.min):
        return float(0)
    elif(x <= (avgIncome.min+avgIncome.max)/2):
        hasil = (x-avgIncome.min)/(1.0-avgIncome.min)
        return hasil
    elif((x <= avgIncome.max) and (x > 1.0)):
        hasil = (-x+avgIncome.max)/(avgIncome.max-1.0)
        return hasil
    elif(x >= avgIncome.max):
        return float(0)
    return float(0)

def calcHghIncome(x): #linear membership functon for high income
    if(x <= hghIncome.min):
        return float(0)
    elif(x <= (hghIncome.min+hghIncome.max) / 2):
        hasil = 2 * ((x-hghIncome.min) / (hghIncome.max-hghIncome.min))**2
        return hasil
    elif (x <= hghIncome.max):
        hasil = 1 - 2 * ((x-hghIncome.max) / (hghIncome.max-hghIncome.min))**2
        return hasil
    return float(1)

def calcLowDebt(y): #linear membership functon for low debt
    if( y >= (lowDebt.max)):
        return float(0)
    elif(y <= (lowDebt.max + lowDebt.min)/2):
        hasil = 1 - 2*((y-lowDebt.min) / (lowDebt.max-lowDebt.min))**2
        return hasil
    elif(y <= (lowDebt.max)):
        hasil = 2 * ((y-lowDebt.max) / (lowDebt.max-lowDebt.min))**2
        return hasil
    return 0

def calcAvgDebt(y): #linear membership functon for avg debt
    if( y <= avgDebt.min):
        return float(0)
    elif(y <= (avgDebt.min+avgDebt.max)/2):
        hasil = (y-avgDebt.min)/(50.0-avgDebt.min)
        return hasil
    elif((y <= avgDebt.max) and (y > 1.0)):
        # hasil = (-y+avgDebt.max)/(avgDebt.max-50.0)
        hasil = -1*(y-avgDebt.max)/(avgDebt.max-50.0)
        return hasil
    elif(y >= avgDebt.max):
        return float(0)
    return float(0)

def calcHghDebt(y):
    if(y <= hghDebt.min): #linear membership functon for high debt
        return float(0)
    elif(y <= (hghDebt.min+hghDebt.max) / 2):
        hasil = 2 * ((y-hghDebt.min) / (hghDebt.max-hghDebt.min))**2
        return hasil
    elif (y <= hghDebt.max):
        hasil = 1 - 2 * ((y-hghDebt.max) / (hghDebt.max-hghDebt.min))**2
        return hasil
    return float(1)

#input data from 'DataTugas.csv'
with open('DataTugas2.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, skipinitialspace=True)
    for data in csv_reader:
        no          = int(data['No'])
        income      = float(data['Pendapatan'])
        debt        = float(data['Hutang'])
        input_crisp.append({'no': no, 'income': income, 'debt': debt})

#inference <- Membership Function, apply rule
inference_data = []
for data in input_crisp:
    membership_result = {
        'lIncome' : calcLowIncome(data['income']),
        'aIncome' : calcAvgIncome(data['income']),
        'hIncome' : calcHghIncome(data['income']),
        'lDebt'   : calcLowDebt(data['debt']),
        'aDebt'   : calcAvgDebt(data['debt']),
        'hDebt'   : calcHghDebt(data['debt'])
    }
    inference = { #apply to rules
        'accepted'      : max(
            min(membership_result['lIncome'], membership_result['hDebt']),
            min(membership_result['lIncome'], membership_result['aDebt']),
            min(membership_result['aIncome'], membership_result['hDebt'])
        ),
        'considered'    : max(
            min(membership_result['lIncome'], membership_result['lDebt']),
            min(membership_result['aIncome'], membership_result['lDebt']),
            min(membership_result['aIncome'], membership_result['aDebt']),
            min(membership_result['hIncome'], membership_result['hDebt'])
        ),
        'rejected'      : max(
            min(membership_result['hIncome'], membership_result['lDebt']),
            min(membership_result['hIncome'], membership_result['aDebt'])
        )
    }
        #defuzzyfication using takagi-sugeno style
    scoreInference = inference['accepted'] + inference['considered'] + inference['rejected']
    scoreAccepted  = inference['accepted'] * (100 * (data['income'] - data['debt']))
    scoreConsidered= inference['considered'] * (70 * (data['income'] - data['debt']))
    scoreRejected  = inference['rejected'] * (50 * (data['income'] - data['debt']))

    #mencari rata-rata untuk defuzzifikasi sugeno
    totalInference = (scoreAccepted + scoreConsidered + scoreRejected) / scoreInference
    print("No: ",data," totalInference: ",totalInference)

    inference_data.append({
        'no'    : data['no'],
        'income': data['income'],
        'debt'  : data['debt'],
        'score' : totalInference
    })
inference_data.sort(key = lambda x: x['score'])
output = map(lambda x: ["No: ",x['no']," | Pendapatan: ", x['income']," | Hutang: ",x['debt']," | Inference: ",x['score']], inference_data[:20])

with open('TebakanTugas2.csv', mode='w', newline='') as csv_file: #crisp output
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL   )
    csv_writer.writerows(output)
