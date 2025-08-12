import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time_control import get_time_period, DAILY_TIME_ZONES

class MICROGRID_15K:
    def __init__(self, soc, bat_cap):
        self.mppt = 0
        self.load = 0
        self.soc = soc
        self.grid_power = 0
        self.total_grid_power = 0
        self.bat_power = 0
        self.pcs_max_power = 150000
        self.bat_cap = bat_cap
        self.mppt_list = [0]
        self.load_list = [0]
        self.charge = 0
        self.disCharge = 0
        self.failed = False
        self.iterate = 1

    def LoadTable(self, filepath='./Action.xlsx'):
        try:
            df = pd.read_excel(filepath)
        except FileNotFoundError:
            print(f"找不到檔案 {filepath}，請確認檔案存在")
            return

        self.mppt_list = df['MPPT_15kW'].tolist()
        self.load_list = df['LOAD_15kW'].tolist()

    def _CalSOC(self):
        if self.soc <= 0.05 or self.failed:
            self.failed = True
            self.load = 0
            self.mppt = 0
            self.grid_power = 0
            self.soc = 0.05
            return
        if self.soc == 1 and self.mppt >= self.load :
            self.mppt = self.load
        elif self.soc == 1 and self.mppt < self.load :
            self.mppt = self.mppt
            self.grid_power = self.load - self.mppt
        if self.charge == 1 and self.disCharge == 0:
            self.grid_power = 7000 + self.load - self.mppt
            self.bat_power = -7000
            # print(0)
        elif self.disCharge == 1 and self.charge == 0:
            if self.load >= self.pcs_max_power:
                self.bat_power = self.pcs_max_power
                self.grid_power = self.load - self.bat_power
            elif self.load < self.pcs_max_power:
                self.bat_power = self.load - self.mppt
                self.grid_power = 0
                # print(self.bat_power)
            # print(1)
        else:
            if self.load > self.mppt:
                self.grid_power = self.load - self.mppt
                self.bat_power = 0
            else:
                self.bat_power = self.load - self.mppt
                self.grid_power = 0
                
            # print(2)
        # print(self.bat_power)
        self.soc += -self.bat_power / self.bat_cap
        self.total_grid_power += self.grid_power
        # print(self.total_grid_power)
        self.soc = min(1, max(0, self.soc))

    def Run(self):
        minute = self.iterate 
        period = get_time_period(minute)

        if period == 'peak':
            # print('peak')
            self.charge = 0
            self.disCharge = 1
            if self.soc <= 0.2:
                 self.charge = 0
                 self.disCharge = 0
        elif period == 'semi-peak':
            # print('semi-peak')
            self.charge = 0
            self.disCharge = 0
        elif period == 'off-peak':
            # print('off-peak')
            self.charge = 1
            self.disCharge = 0
            if self.soc >=0.8:
                self.charge = 0
                self.disCharge = 0

        self.mppt = self.mppt_list[self.iterate]
        self.load = self.load_list[self.iterate]

        self._CalSOC()
        
        self.iterate += 1
        if self.iterate >= len(self.mppt_list):
            self.iterate = 0

        return {
            'SOC': self.soc, 'GRID_POWER': self.grid_power, 'MPPT': self.mppt, 
            'LOAD': self.load, 'CHARGE': self.charge, 'DISCHARGE': self.disCharge, 'BAT_POWER': self.bat_power
        }



def plot_microgrid_status(soc_list, grid_list, mppt_list, load_list, charge_list, discharge_list, bat_power_list, time_labels, num_days):
    fig, ax1 = plt.subplots(figsize=(14, 6))

    # 畫背景色
    def shade_peak_periods(ax, num_days):
        for day in range(num_days):
            offset = day * 1440
            for start, end, color, label in DAILY_TIME_ZONES:
                ax.axvspan(offset + start, offset + end, facecolor=color, alpha=0.15)


    shade_peak_periods(ax1, num_days)

    ax1.plot(grid_list, label="GRID_POWER", color='tab:blue')
    ax1.plot(mppt_list, label="MPPT", color='tab:orange')
    ax1.plot(load_list, label="LOAD", color='tab:green')
    ax1.plot(bat_power_list, label="BAT_POWER", color='tab:purple')
    ax1.set_ylabel("Power (W)")
    ax1.legend(loc="upper left")

    ax1_r = ax1.twinx()
    ax1_r.plot(soc_list, '--', label="SOC (%)", color='tab:red')
    ax1_r.plot(charge_list, label="CHARGE", color='tab:pink')
    ax1_r.plot(discharge_list, label="DISCHARGE", color='tab:brown')
    ax1_r.set_ylabel("SOC / Charge / Discharge")
    ax1_r.legend(loc="upper right")
    ax1.set_title("15kW Microgrid System Status")

    plt.xlabel("Time (HH:MM)")
    x_ticks = np.arange(0, len(time_labels), 360)
    x_labels = [time_labels[i] for i in x_ticks]
    plt.xticks(ticks=x_ticks, labels=x_labels, rotation=45)

    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === 四、主程式 ===
# 初始化資料記錄清單
# 模擬測試資料
soc_list = []
grid_list = []
mppt_list = []
load_list = []
charge_list = []
discharge_list = []
bat_power_list = []

initial_soc = 0.8
bat_cap = 21000 * 60

microGrid = MICROGRID_15K(initial_soc , bat_cap)
microGrid.LoadTable()

for _ in range(1440):
    result = microGrid.Run()
    soc_list.append(result['SOC'] * 100)
    grid_list.append(result['GRID_POWER'])
    mppt_list.append(result['MPPT'])
    load_list.append(result['LOAD'])
    charge_list.append(result['CHARGE']*10)
    discharge_list.append(result['DISCHARGE']*10)
    bat_power_list.append(result['BAT_POWER'])

# 每筆資料為 1 分鐘，依序產生時間標籤
time_labels = []
for i in range(len(soc_list)):
    total_minutes = i
    day = total_minutes // 1440
    minute_of_day = total_minutes % 1440
    hour = minute_of_day // 60
    minute = minute_of_day % 60
    time_labels.append(f"{hour:02d}:{minute:02d}")

plot_microgrid_status(soc_list, grid_list, mppt_list, load_list, charge_list, discharge_list, bat_power_list, time_labels, num_days = 1)

