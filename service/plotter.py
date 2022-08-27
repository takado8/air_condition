import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.animation as anim
from logger import Logger
import sys

plt.style.use('dark_background')


def plot(args, last_n_hours):
    # create figure and axis objects with subplots()
    # {x, y1, y2, y1_label, y2_label, x_label='Time'}

    fig, ax = plt.subplots(len(args))


    # plt.gca().xaxis.set_major_locator(plt.MultipleLocator(60))
    # plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(15))
    def update(i):
        args.clear()
        args.extend(load_log(last_n_hours))
        i = 0
        for entry in args:
            ax[i].clear()
            # make a plot
            ax[i].plot(entry['x'], entry['y1'], color="red")
            # set x-axis label
            ax[i].set_xlabel(entry['x_label'], fontsize=14)
            # set y-axis label
            ax[i].set_ylabel(entry['y1_label'], color="red", fontsize=14)

            # twin object for two different y-axis on the sample plot
            twin = get_twin(ax[i])
            ax2 = ax[i].twinx() if twin is None else twin
            # make a plot with different y-axis using second axis object
            ax2.plot(entry['x'], entry['y2'], color="blue")
            ax2.set_ylabel(entry['y2_label'], color="blue", fontsize=14)
            myFmt = mdates.DateFormatter('%d.%m %H:%M')
            ax[i].xaxis.set_major_formatter(myFmt)
            # ax[i].xaxis.set_major_locator(mdates.HourLocator(interval=1))
            ax[i].xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
            # plt.rc('grid', linestyle='-', color='grey', linewidth=0.1)
            # plt.grid(color='grey', linestyle=':', linewidth=0.5, axis='both')
            ax[i].grid(b=True, which='major', axis="both", color='grey', linestyle=':', linewidth=0.5)
            i += 1
        plt.gcf().autofmt_xdate()

    a = anim.FuncAnimation(fig, update, repeat=False, interval=1000)
    plt.show()


logger = Logger()

def get_twin(ax):
    for other_ax in ax.figure.axes:
        if other_ax is ax:
            continue
        if other_ax.bbox.bounds == ax.bbox.bounds:
            return other_ax


def load_log(last_n_hours):
    log = logger.load_log()
    dates = []
    temp = []
    humidity = []
    vocs = []
    co2 = []
    avg_temp = []
    avg_humidity = []
    avg_vocs = []
    avg_co2 = []
    i = 0
    for entry in log:
        avg_temp.append(round(entry['temp'], 1))
        avg_humidity.append(round(entry['humidity'], 1))
        avg_vocs.append(round(entry['vocs'], 0))
        avg_co2.append(round(entry['co2'], 0))
        if i == 2:
            i = 0
            date_time_obj = datetime.strptime(entry['date'], "%d.%m.%Y %H:%M:%S")
            dates.append((date_time_obj - timedelta(hours=6)))
            temp.append(round(sum(avg_temp) / len(avg_temp), 1))
            humidity.append(round(sum(avg_humidity) / len(avg_humidity), 1))
            vocs.append(round(sum(avg_vocs) / len(avg_vocs), 0))
            co2.append(round(sum(avg_co2) / len(avg_co2), 0))
            avg_temp = []
            avg_humidity = []
            avg_vocs = []
            avg_co2 = []
        i += 1
    if last_n_hours:
        last_date = dates[-1]

        for i in range(len(dates)-1, 0, -1):
            total_sec_diff = (last_date - dates[i]).total_seconds()
            hours_diff = divmod(total_sec_diff, 3600)[0]
            if hours_diff >= last_n_hours:
                break

        dates = dates[i:]
        vocs = vocs[i:]
        co2 = co2[i:]
        temp = temp[i:]
        humidity = humidity[i:]
    # print(log[-20:])
    # print(dates[-20:])
    # print(temp[-20:])
    # print(humidity[-20:])
    # exit(4)
    # plot(x=dates, y1=temp, y2=humidity)
    # plot(x=dates, y1=temp, y2=humidity, y1_label="Temperature *C", y2_label="Humidity[%]")
    return [{'x': dates, 'y1': vocs, 'y2': co2, 'y1_label': "VOCs [ppb]", 'y2_label': "CO2 [ppm]", 'x_label': 'Time'},
            {'x': dates, 'y1': temp, 'y2': humidity, 'y1_label': "Temp [*C]", 'y2_label': "Humidity [%]",
             'x_label': 'Time'}]


if __name__ == '__main__':
    args = sys.argv

    h = None
    if len(args) > 1:
        if '-h' in args:
            h = int(args[args.index('-h') + 1])

    plot(load_log(h), h)
