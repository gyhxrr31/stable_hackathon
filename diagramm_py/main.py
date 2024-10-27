import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('C:\\test.csv', encoding='UTF-8')


status_counts = data['new_value'].value_counts()


threshold = 0.05 * status_counts.sum() 
major_statuses = status_counts[status_counts >= threshold]
other_statuses = pd.Series({'Другие': status_counts[status_counts < threshold].sum()})


status_counts_normalized = pd.concat([major_statuses, other_statuses])

plt.figure(figsize=(8, 8))
plt.pie(status_counts_normalized.values, labels=status_counts_normalized.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("viridis", len(status_counts_normalized)))
plt.title('Процентное соотношение новых статусов (нормализовано)')
plt.show()


plt.figure(figsize=(12, 6))
sns.barplot(x=status_counts.index, y=status_counts.values, palette="viridis")
plt.title('Количество изменений для каждого нового статуса')
plt.xlabel('Новый статус')
plt.ylabel('Количество изменений')
plt.xticks(rotation=45)
plt.show()