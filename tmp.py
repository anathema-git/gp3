import pandas as pd

# Заданные заголовки
csv_headers = ["review_text", "review_date", "rating", "like_count"]

# Список файлов: data1.csv, data2.csv, ..., data8.csv
file_names = [f"data{i}.csv" for i in range(1, 9)]

# Чтение и объединение
df_list = [pd.read_csv(file, usecols=csv_headers) for file in file_names]
combined_df = pd.concat(df_list, ignore_index=True)

# Сохранение в data.csv
combined_df.to_csv("data.csv", index=False)
