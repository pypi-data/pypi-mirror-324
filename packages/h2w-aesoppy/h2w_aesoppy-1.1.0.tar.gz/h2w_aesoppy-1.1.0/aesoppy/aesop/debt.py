import pandas as pd


class Debt:

    def __init__(self, **kwargs):
        self.fin_df = kwargs.get('financials_df', 'error')
        self.debt_df = self._debt()


    def _debt(self):
        df1 = self.fin_df
        df = pd.DataFrame(df1[['revenue', 'cash_from_ops', 'free_cash_flow', 'net_income',
                               'cash_for_dividends', 'capex', 'debt_paid', 'debt_issued', 'taxes_paid',
                               'cash_equivalents', 'market_securities', 'treasury_stock',
                               'current_assets', 'long_assets',
                               'short_debt', 'long_debt', 'current_liabilities', 'long_liabilities']], index=df1.index)


        return df
