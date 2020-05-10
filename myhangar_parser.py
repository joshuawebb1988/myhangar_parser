from bs4 import BeautifulSoup
import pandas as pd

"""
Process RSI My Hangar (.html) into table (.tsv) of pledges and items.
Save each page as 'p1.html', 'p2.html', ... 'pN.html' in working directory.
"""

page_num = input("What is N, number of RSI My Hangar (.html) pages, e.g. 'p1.html', ... 'pN.html'?")
page_num = int(page_num)

pledges = list()

for page_file in ['p{}.html'.format(x) for x in range(1, page_num + 1)]:
	print(page_file)

	with open(page_file, encoding='utf-8') as page:
		soup = BeautifulSoup(page, 'html.parser')

	results = soup.find_all('li')
	for r in results:
		pledge_id = r.find('input', class_='js-pledge-id')
		if pledge_id:
			pledge_id = pledge_id['value']
		else:
			continue
		pledge_name = r.find('input', class_='js-pledge-name')
		if pledge_name:
			pledge_name = pledge_name['value']
		pledge_value = r.find('input', class_='js-pledge-value')
		if pledge_value:
			pledge_value = pledge_value['value']
		pledge_configuration_value = r.find('input', class_='js-pledge-configuration-value')
		if pledge_configuration_value:
			pledge_configuration_value = pledge_configuration_value['value']

		items = list()
		ri = r.find_all('div', class_='item')
		for i in ri:
			item_title = i.find('div', class_='title')
			if item_title:
				item_title = item_title.text.strip()
			item_kind = i.find('div', class_='kind')
			if item_kind:
				item_kind = item_kind.text.strip()
			item_liner = i.find('div', class_='liner')
			if item_liner:
				item_liner = item_liner.text.strip()

			item = {'title':item_title, 'kind':item_kind, 'liner':item_liner}
			items.append(item)

		pledge = {'id':pledge_id, 'name':pledge_name, 'value':pledge_value, 'configuration_value':pledge_configuration_value,
				 'items':items}
		pledges.append(pledge)

df = pd.DataFrame(pledges)
df2 = pd.concat([df, df.explode('items')['items'].apply(pd.Series)], axis=1).drop('items', axis=1)
df.to_csv('pledges.tsv', sep='\t')
df2.to_csv('items.tsv', sep='\t')
print('Script finished')