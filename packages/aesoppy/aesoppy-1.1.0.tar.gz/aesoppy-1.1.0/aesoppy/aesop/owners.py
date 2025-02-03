import pandas as pd


class Owners:

    def __init__(self, **kwargs):
        self.fin_df = kwargs.get('financials_df', 'error')
        self.owners_df = self._owners()


    def _owners(self):
        df1 = self.fin_df
        df2 = pd.DataFrame(df1[['revenue', 'cash_from_ops', 'free_cash_flow', 'cash_for_dividends',
                               'stock_buyback', 'stock_issues', 'shares_outstanding_diluted', 'shares_outstanding_eop'
                               ]], index=df1.index)

        return df2

