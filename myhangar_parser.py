from bs4 import BeautifulSoup
import pandas as pd

class MyHangar_Parser():
    """
    Processes RSI My Hangar (.html) into table (.tsv) of pledges and items.
    
	Precondition:
	 Save each page as 'p1.html', 'p2.html', ... 'pN.html' in working directory.
	Usage:
	 .parse(), or
	 .parse(page_num=False, to_tsv=True, tsv_pledges='pledges.tsv', tsv_items='items.tsv')
	Returns:
	 df_pledges, df_items
    """
    def parse(self, page_num=False, to_tsv=True, tsv_pledges='pledges.tsv', tsv_items='items.tsv'):
        if not(page_num):
            page_num = input("What is N, number of RSI My Hangar (.html) pages, e.g. 'p1.html', ... 'pN.html'?")
        page_num = int(page_num)
        return self.parse_to_page_num(page_num, to_tsv, tsv_pledges, tsv_items)
    
    def parse_to_page_num(self, page_num, to_tsv=True, tsv_pledges='pledges.tsv', tsv_items='items.tsv'):

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

        df_pledges = pd.DataFrame(pledges)
        df_items = pd.concat([df_pledges, df_pledges.explode('items')['items'].apply(pd.Series)], axis=1).drop('items', axis=1)
        if to_tsv:
            df_pledges.to_csv(tsv_pledges, sep='\t')
            df_items.to_csv(tsv_items, sep='\t')
        print('Finished parsing MyHangar pages.')
        return (df_pledges, df_items)

def main():		
    mhp = MyHangar_Parser()
    df_pledges, df_items = mhp.parse(page_num=False, to_tsv=True, tsv_pledges='pledges.tsv', tsv_items='items.tsv')
	
if __name__ == "__main__":
    main()
