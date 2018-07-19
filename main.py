def import_data(account_name,
                num_periods,
                start_year=2016,
                start_period=1,
                end_year=2018,
                end_period=-1,
                append_year=False,
                skiprows=0,
                credit=False):
	"""
	Reads all files in data/{account_name} subdirectory that follow the intervals defined by number of periods in a year,
	start year, end year, start period and end period. Taking into account if the account is Credit card or savings,
	it formats the DataFrame, returning all data for that account.
	:param account_name: subdirectory from which the files are going to be read
	:param num_periods: logical subdivisions of a year. If the extract is given every trimester, then there are four
	periods.
	:param start_year: Year from which the first known extract is known and is going to be read.
	:param start_period: Period of the starting year from which there are extracts to read.
	:param end_year: Year or the last extract to read.
	:param end_period: Period of the last extract to read.
	:param append_year: Determines if the  year value has to be appended to de Date column. For example, in savings
	account, the date is only given with format dd/mm, therefore it is highly recommended to include manually the year.
	:param skiprows: Number of rows to skip in the files to read. Important if they have some headings.
	:param credit: Is it a credit account? Used principally for formatting
	:return: DataFrame with account's financial movements
	"""
	end_period = num_periods if end_period == -1 else end_period

	data = pd.read_excel(f'data/{account_name}/{start_year}-{start_period}.xlsx', skiprows=skiprows)
	data = data.drop(len(data) - 1)
	if append_year:
		data['FECHA'] = data['FECHA'] + f"/{start_year}"
	if credit:
		data.dropna(axis=0, how='any', inplace=True)
		data = data[(data.columns[0] != data[data.columns[0]]) &
		            (data[data.columns[0]] != ' ')]
	steps = period_steps(num_periods, start_year, start_period, end_year, end_period)
	for i in steps[1:]:
		path = f'data/{account_name}/' + i + '.xlsx'
		temp_data = pd.read_excel(path, skiprows=skiprows)
		if append_year:
			temp_data['FECHA'] = temp_data['FECHA'] + "/" + i[:i.find('-')]
		if credit:
			temp_data.dropna(axis=0, how='any', inplace=True)
			temp_data = temp_data[(temp_data.columns[0] != temp_data[temp_data.columns[0]]) &
			                      (temp_data[temp_data.columns[0]] != ' ')]
		data = data.append(temp_data, ignore_index=True)
		data = data.drop(len(data) - 1)
	data.dropna(axis=1, how='any', inplace=True)
	return data

