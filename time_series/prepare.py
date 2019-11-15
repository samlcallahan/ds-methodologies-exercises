import pandas as pd
import acquire

def prep_heb(heb):
    heb = heb.drop(columns=['Unnamed: 0_y', 'Unnamed: 0_x', 'Unnamed: 0'])
    fmt = '%a, %d %b %Y %H:%M:%S %Z'
    heb['sale_date'] = pd.to_datetime(heb.sale_date, format=fmt)
    heb = heb.set_index('sale_date')
    heb['month'] = heb.index.strftime('%m-%b')
    heb['weekday'] = heb.index.strftime('%w-%a')
    heb.sale_amount = heb.sale_amount.astype('int')
    heb['sales_total'] = heb.sale_amount * heb.item_price
    return heb

def get_sales_by_day(heb):
    sales_by_day = heb.resample('D')[['sales_total']].sum()
    sales_by_day['diff_last'] = sales_by_day.sales_total.diff()
    return sales_by_day

if __name__ == '__main__':
    heb = acquire.get_heb()
    heb  = prep_heb(heb)
    sales_by_day = get_sales_by_day(heb)