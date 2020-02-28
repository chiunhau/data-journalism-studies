import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.close('all')

data = pd.read_csv('yilan-census-modified.csv', encoding='utf-8', converters={'town': str.strip})
data = data.dropna()
data['year'] = data['year'].astype(int)
# towns_data = data[(data['town'] == 'Dongshan') | (data['town'] == 'Luodong') | (data['town'] == 'Suao') | (data['town'] == 'Wujie') | (data['town'] == 'Yilan City')]
towns_data = data[data['town'].isin(['Dongshan', 'Luodong', 'Yilan City', 'Suao', 'Wujie', 'Sanxing', 'Toucheng', 'Jiaoxi', 'Yuanshan', 'Zhuangwei'])]

yilan_pivot = towns_data.pivot_table(values='population', columns='town', index='year')
yilan_pivot.plot(title='Population of Yilan').legend(loc=(1.04,0))
plt.subplots_adjust(right=0.7)
plt.show()