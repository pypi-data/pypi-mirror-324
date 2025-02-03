import pandas as pd


class Growth:

    def __init__(self, **kwargs):
        self.fin_df = kwargs.get('financials_df', 'error')
        self.growth_df = self._growth()


    def _growth(self):
        df1 = self.fin_df
        df = pd.DataFrame(df1[['revenue', 'net_income', 'cash_from_ops', 'free_cash_flow', 'capex']], index=df1.index)


        return df