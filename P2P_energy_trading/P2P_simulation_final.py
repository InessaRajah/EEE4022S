import gurobipy as gb
import time
from Prosumer import Prosumer
import numpy as np
import functions as func
import pandas as pd
from pathlib import Path
import csv


#list description of all agents
agents = []

#keep track of how many runs of the optimisation code result in suboptimal results
suboptimal = 0

#set the season being considered
season = 'Winter'

#read in load data from .csv files
loads = []
data_path = Path('FebProfiles1.csv')
data_file = pd.read_csv(data_path)
data_file = pd.DataFrame(data_file)
data_file = data_file.drop(columns = ['Electricity.Timestep', 'Sum', '[kWh]'])
row1 = data_file[data_file.Time == '2016/02/05']
load1 = row1['Proper kWh'].to_list()
loads.append(load1)
print('Load4', sum(load1))
data_path = Path('FebProfiles2.csv')
data_file = pd.read_csv(data_path)
data_file = pd.DataFrame(data_file)
data_file = data_file.drop(columns = ['Electricity.Timestep', 'Sum', '[kWh]'])
row2 = data_file[data_file.Time == '2016/02/05']
load2 = row2['Proper kWh'].to_list()
loads.append(load2)
print('Load4', sum(load2))
data_path = Path('FebProfiles3.csv')
data_file = pd.read_csv(data_path)
data_file = pd.DataFrame(data_file)
data_file = data_file.drop(columns = ['Electricity.Timestep', 'Sum', '[kWh]'])
row3 = data_file[data_file.Time == '2016/02/05']
load3 = row3['Proper kWh'].to_list()
loads.append(load3)
print('Load4', sum(load3))
data_path = Path('FebProfiles4.csv')
data_file = pd.read_csv(data_path)
data_file = pd.DataFrame(data_file)
data_file = data_file.drop(columns = ['Electricity.Timestep', 'Sum', '[kWh]'])
row4 = data_file[data_file.Time == '2016/02/05']
load4 = row4['Proper kWh'].to_list()
loads.append(load4)
print('Load4', sum(load4))
data_path = Path('FebProfiles5.csv')
data_file = pd.read_csv(data_path)
data_file = pd.DataFrame(data_file)
data_file = data_file.drop(columns = ['Electricity.Timestep', 'Sum', '[kWh]'])
row5 = data_file[data_file.Time == '2016/02/05']
load5 = row5['Proper kWh'].to_list()
print('Load5', sum(load5))
loads.append(load5)


#list of each agents solar panel number
solar_panels = [5, 5, 0, 5, 0]


#service charge (R/month) = 147.74, Capacity Charge = R596.18 -- R24.80/day
# grid tariff structure
grid_price = {'Summer': {'Peak': 172.68, 'Standard': 136.60, 'Off-peak': 107.46}, 'Winter': {'Peak': 397.27, 'Standard': 162.74, 'Off-peak': 114.83}}
time_classification = {0: 'Off-peak', 1: 'Off-peak', 2: 'Off-peak', 3: 'Off-peak', 4: 'Off-peak', 5: 'Off-peak', 6: 'Off-peak', 7: 'Peak', 8: 'Peak', 9: 'Peak', 10: 'Peak', 
                    11: 'Standard', 12: 'Standard', 13: 'Standard', 14: 'Standard', 15: 'Standard', 16: 'Standard', 17: 'Standard', 18: 'Peak', 19: 'Peak', 20: 'Peak', 21:'Standard', 22:'Standard'
                    , 23:'Standard'}

#list containing list of solar radiation (W/m^2) per time period 
data_path = Path('Solar_Radiation_Ordered.csv')
data_file = pd.read_csv(data_path)
data_file = pd.DataFrame(data_file)

row = data_file[data_file.Date == 20160708]
solar = row['G'].to_list()
print('Solar for 01/02/2016:', solar)

#k_tim is the grid c/kwh price for a time period- looking at Standard time period in Summer here.  This is updated in the for loop
k_tim = 136.60
#area of one of the seven solar panels being used in m^2
A = 2*0.994
#one module is 17.64% efficient
n_pv = 0.1764
#efficiency loss parameter. According to [49] eff = 0.08 (inverter losses) + 0.02 (some modules not behaving as well as others) + 0.002 (resistive loss) + assume no temp and suntracking losses + 0.05 (damage + soiling losses )
eff = 1 - 0.152
#setting this for testing purposes
hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18 , 19, 20, 21, 22, 23]


num_agents = len(solar_panels)
print('Num Agents', num_agents)

#starting SOC_bat for all agents
# SOC_bat = 2*0.65*np.ones([num_agents, 1])

# #get battery SOC data from the previous day 
data_path = Path('SOC_Tests.csv')
data_file = pd.read_csv(data_path)
data_file = pd.DataFrame(data_file)
SOC = data_file[data_file.Time_Period == 23]
SOC = SOC['SOC (%)'].to_list()
num_agents = 5
SOC_bat = np.zeros([num_agents, 1])


for i in range(num_agents):
   SOC_bat[i] = SOC[i]/100 * 2

#create dataframes to store info you'd like to save to .csv files
TradesDF = pd.DataFrame(columns=['Agent#','Time Period', 'TradeID', 'Quantity (kWh)', 'Price (c/kWh)', 'Avg. Price for Time Period (c/kwh)', 'Amount paid/received for Trade Transaction (c)'])
PowerPointsDF = pd.DataFrame(columns = ['Agent#', 'Time Period', 'Battery Charge (kWh)', 'Grid Export (kWh)', 'Grid Household Load (kWh)', 'Battery Discharge (kWh)', 'Solar Output (kWh)', 'Grid Import (kWh)', 'SolarUsed', 'LoadUsed', 'Social Welfare (R)', 'Cost Batt Discharge (R)', 'Cost Batt Charge (R)'])
TotalSocialWelfareDF = pd.DataFrame(columns = ['Time Period', 'Total Social Welfare (R/kwh)'])
SolarDF = pd.DataFrame(columns=['Agent#','Time Period', 'Solar Irradiation (W/m^2)', 'Num_solar panels', 'Solar Output energy (kWh)'])
SOC_DF = pd.DataFrame(columns=['Agent#', 'Time Period', 'SOC (%)'])
Metrics_DF = pd.DataFrame(columns = ['Time Period', 'Num Iterations', 'Time (s)'])
Price_DF = pd.DataFrame(columns = ['Time Period', 'Avg Price (c/kwh)'])
Test_Residuals = pd.DataFrame(columns = ['Iteration', 'Global Prim', 'Global Dual'])
Test_Trades = pd.DataFrame(columns=['Agent#','Time Period', 'TradeID', 'Quantity (kWh)', 'Price (c/kWh)', 'Avg. Price for Time Period (c/kwh)', 'Amount paid/received for Trade Transaction (c)', 'Iteration'])
#cycle through and create agents
for t in range(len(hours)):
    agents = []
    time_period = hours[t]
    tim = time_classification[t]
    k_tim = grid_price[season][tim] * 0.9
    
    for i in range(num_agents):
        agent, agents = func.createAgent(loads[i][time_period], SOC_bat[i][0], solar_panels[i], agents, solar, time_period, k_tim)
        SolarDF = func.createSolarFile(agent, time_period, solar, SOC_bat[i][0], solar_panels[i], SolarDF)

    print("TIME PERIOD:", t)
    print('SOC:', SOC_bat)
    max_Iter = 500
    Commission_Fees = 0 # 0 - for P2P (Blockchain Simulations), 0.1 for P2P (Centralised Simulations)
    penalty_factor = 0.01
    residual_primal = 1e-4
    resiudal_dual = 1e-4

    preferences = Commission_Fees* np.ones(len(agents)-1)

    Trades = np.zeros([num_agents, num_agents])
    Prices = np.zeros([num_agents, num_agents])
    
    #array of trade partners- set index to 1 if trade is happening e.g. part[0][1] = 1 if customer 0 is trading with customer 1
    part = np.ones([num_agents, num_agents])
    for i in range(num_agents):
        for j in range(num_agents):
            if (i == j):
                part[i][j] = 0
    print('Part', part)

    #create players for this optimisation run - uses Prosumer class
    players = func.createPlayers(agents, part, preferences, penalty_factor)
    prim = float('inf')
    dual = float('inf')
    iteration = 0
    SW = 0
    simulation_time = 0
    prim_previous = 0
    lapsed = 0
    start_time = time.time()
    ouch = 0
    prim_list = []
    window = 25
    #local optimisation function
    while ((prim > residual_primal or dual>resiudal_dual) and iteration< max_Iter):
        iteration+=1
        temp = np.copy(Trades)
        for i in range(num_agents):
            temp[:,i] = players[i].optimize(Trades[i,:])
            Prices[:,i][part[i,:].nonzero()] = players[i].y
        temp = temp*10000
        temp = np.round(temp, 0)
        temp = temp / 10000
        Trades = np.copy(temp)
        prim = sum([players[i].Res_primal for i in range(num_agents)])
        dual = sum([players[i].Res_dual for i in range(num_agents)])
        prim_list.append(prim*10000)    
        if (len(prim_list) ==  window):
            prim_list, penalty_factor, players = func.checkRho(prim_list, penalty_factor, players)   
        #storing the local residuals for the first time period for testing purposes
        if t== 0:
            test_prim = sum(round(players[i].Res_primal * 10000) for i in range(num_agents))
            test_dual = sum(round(players[i].Res_dual * 10000) for i in range(num_agents))
            row = Test_Residuals.shape[0]
            Test_Residuals.loc[row, 'Iteration'] = iteration
            Test_Residuals.loc[row, 'Global Prim'] = test_prim
            Test_Residuals.loc[row, 'Global Dual'] = test_dual
            Test_Residuals.to_csv(r'C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\Test Residuals.csv')
            row = Test_Trades.shape[0]
            Test_Trades.loc[row, 'Iteration'] = iteration
            Test_Trades = func.createTradeFile(players, Test_Trades, time_period, 0, part)
            Test_Trades.to_csv(r'C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\Test Trades.csv')
        lapsed = time.time()-start_time
    print('iterations:', iteration)
    simulation_time += lapsed
    Price_avg = Prices[Prices!=0].mean()
    print("Avg Price:", Price_avg)
    SW = sum([players[i].SW for i in range(num_agents)])
    ind_row = TotalSocialWelfareDF.shape[0]
    TotalSocialWelfareDF.loc[ind_row, 'Time Period'] = time_period
    TotalSocialWelfareDF.loc[ind_row, 'Total Social Welfare (R/kwh)'] = SW
    print("Total Social Welfare:", SW)
    print(iteration)
    #if the number of iterations reaches 1000 - then an optimal solution was not reached
    if iteration == 1000:
        suboptimal = suboptimal + 1
    print(simulation_time)
    pbd = []
    pbc = []
    for i in range(num_agents):
        pbd.append([players[i].variables.p[3].x])
        pbc.append([players[i].variables.p[0].x])
    pbd = np.asarray(pbd)
    pbc = np.asarray(pbc)
    #update state of all batteries
    SOC_bat = SOC_bat - pbc*0.99 - pbd*0.99

    PowerPointsDF = func.createPowerPoints(players, time_period, PowerPointsDF, solar, loads, solar_panels)
    TradesDF = func.createTradeFile(players, TradesDF, time_period, Price_avg, part)
    SOC_DF = func.createSOCFile(SOC_bat, SOC_DF, time_period)
    Metrics_DF = func.createMetricsFile(Metrics_DF, simulation_time, time_period, iteration)
    ind_row = Price_DF.shape[0]
    Price_DF.loc[ind_row, 'Time Period'] = time_period
    Price_DF.loc[ind_row, 'Avg Price (c/kwh)'] = Price_avg*100






#save values to .csv files
TradesDF.to_csv(r"C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\Trade_Tests.csv")
SolarDF.to_csv(r'C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\Solar_Tests.csv')
SOC_DF.to_csv(r'C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\SOC_Tests.csv')
Metrics_DF.to_csv(r'C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\Overall Optimisation Metrics Test.csv') 
Price_DF.to_csv(r'C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\Average Trading Prices.csv')
PowerPointsDF.to_csv(r'C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\Power Set Points.csv')
TotalSocialWelfareDF.to_csv(r'C:\Users\Inessa\Desktop\4th_Year\FYP\Methodology_Eth\optimisation\Final optimisation\Faster Attempts\Results\Social Welfare.csv')
