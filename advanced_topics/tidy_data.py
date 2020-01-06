import pandas as pd

directory = 'untidy_data/'

csvs = ['attendance', 'cake_recipes', 'coffee_levels', 'melted', 'sales', 'students', 'treatments']

data = {csv: pd.read_csv(directory + csv + '.csv') for csv in csvs}

attendance = data['attendance']
attendance.columns = ['name', '1', '2', '3', '4', '5', '6', '7', '8']
attendance = attendance.melt(id_vars='name', var_name='day', value_name='attendance').pivot(index='day', columns='name')

def decode(attendance_code):
    if attendance_code == 'P':
        return 1
    elif attendance_code == 'A':
        return 0
    elif attendance_code == 'T':
        return .9
    else:
        return .5

for column in attendance.columns:
    attendance[column] = attendance[column].apply(decode)

attendance.mean()

coffee = data['coffee_levels']
coffee.pivot(index='hour', columns='coffee_carafe')
# I think this is the best shape of the data

cake = data['cake_recipes']
cake = cake.melt(id_vars='recipe:position', var_name='temperature')
cake['recipe'] = cake['recipe:position'].str[0]
cake['position'] = cake['recipe:position'].str[2:]
cake = cake.drop(columns='recipe:position')

cake.groupby('recipe').value.mean().idxmax() # B
cake.groupby('temperature').value.mean().idxmax() # 275
cake.iloc[cake.value.idxmax()] # temp: 300, recipe: B, position: bottom