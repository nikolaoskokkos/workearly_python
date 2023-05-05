import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

# Read data
data = pd.read_csv('./exported_database.csv')

# Grouping data by zip_code and item_description
grouped = data.groupby(['zip_code', 'item_description'])

# Computation of the total sales per store and the percentage of sales for each item
totals = grouped[['bottles_sold']].sum()
percentages = totals.groupby(level='zip_code').transform(
    lambda x: x / x.sum()*100)

# Find the most popular item per zip_code
most_popular = percentages.groupby(level='zip_code')['bottles_sold'].idxmax()

# Calculation of the total bottles sold per zip_code for the most popular item
most_popular_data = totals.loc[most_popular].reset_index()

# Calculation of percentage of bottles per store_number
store_percentages = data.groupby('store_number')[
    'bottles_sold'].sum() / data['bottles_sold'].sum()*100

# Creation of chart with 3 subplots
fig, ax = plt.subplots(figsize=(16, 9))

ax1 = plt.subplot(221)
ax2 = plt.subplot(223)
ax3 = plt.subplot(122)

# Scatter chart of bottles_sold for the most popular item per zip_code (upper left plot)
most_popular_data.plot.scatter(
    ax=ax1, x='zip_code', y='bottles_sold', c='bottles_sold', cmap=cm.rainbow)

ax1.set_xticks(np.arange(round(most_popular_data.zip_code.min() /
                               10000)*10000, most_popular_data.zip_code.max(), 500))
ax1.grid(axis='y', ls='--')
ax1.set_xlabel('Zip Code')
ax1.set_ylabel('Bottles Sold')
ax1.set_title('Most Popular Item by Zip Code')

# Lower left plot (table)
headers = ['Zip Code', 'Item Description', 'Bottles Sold']
ax2.axis('off')
table = ax2.table(cellText=np.array(most_popular_data.sort_values(
    'bottles_sold', ascending=False).head(10)),
    colLabels=headers, loc='center')
table.auto_set_font_size(True)
table.scale(1, 1.5)
table.auto_set_column_width(col=list(range(len(most_popular_data.columns))))

# Set header row
for j in range(0, 3):
    header = table.get_celld()[0, j]
    header.set_text_props(weight='bold')

# Set facecolor
for j in range(1, 11):
    cell = table.get_celld()[j, 2]
    if float(cell.get_text().get_text()) > 500:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#e9694a')
    elif float(cell.get_text().get_text()) > 300:
        cell.set_facecolor('#ef744b')
    elif float(cell.get_text().get_text()) > 200:
        cell.set_facecolor('#faa150')
    else:
        cell.set_facecolor('#f5c55e')

ax2.set_title("Data Table", y=0.93)

# Creation if a horizontal bar chart of percentage of bottles per store_number (right plot)
colors = cm.YlOrRd(store_percentages.sort_values())

store_percentages.sort_values().plot(
    kind='barh', ax=ax3, width=.9, color=colors)

# add labels with percentage at the end of the bar
for i, v in enumerate(store_percentages.sort_values()):
    ax3.text(v + 0.5, i-0.3, str(round(v, 2)) + '%',
             color='black', fontsize=8)

ax3.set_xlabel('Percentage of Bottles Sold')
ax3.set_ylabel('Store Number')
ax3.set_title('Percentage of Bottles Sold by Store Number')
ax3.tick_params(axis='y', labelsize=8)
plt.tight_layout()

# Show the plot
plt.show()
