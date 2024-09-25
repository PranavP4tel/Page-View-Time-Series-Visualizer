import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates = ['date'], index_col = 'date')

# Clean data
df = df[(df['value']<= df['value'].quantile(0.975)) & (df['value']>= df['value'].quantile(0.025))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize = (10,6))
    ax.plot(df.index, df.value,'r', linewidth = 1)
    plt.xticks(rotation = 0)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[7,1]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.legend().remove()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df1 = df
    df1['Years'] = df1.index.year
    df1['Months'] = df1.index.month
    df_bar = df1.groupby(['Years','Months'])['value'].mean()
    df_bar = df_bar.unstack()

    fig = df_bar.plot(kind="bar", figsize=(10,6), xlabel = "Years", ylabel="Average Page Views",legend = True).figure
    plt.legend(["January","February","March","April","May","June","July","August","September","October","November","December"])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')

    fig, axes = plt.subplots(1,2, figsize = (18,9))
    axes[0] = sns.boxplot(ax = axes[0], data = df_box, x = df_box.year, y = df_box.value, hue = df_box.year, palette = 'tab20')
    axes[1] = sns.boxplot(ax = axes[1], data = df_box, x = df_box.month, y = df_box.value, hue = df_box.month)
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")

    axes[0].set_xlabel("Year")
    axes[1].set_xlabel("Month")

    axes[0].set_ylabel("Page Views")
    axes[1].set_ylabel("Page Views")

    axes[0].legend().remove()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

