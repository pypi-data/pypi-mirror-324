import pandas as pd


class Margins:

    def __init__(self, **kwargs):
        self.fin_df = kwargs.get('financials_df', 'error')
        self.income_margins_df = self._income_margins()
        self.cash_margins_df = self._cash_margins()
        self.cost_margins_df = self._cost_margins()


    def _income_margins(self):
        df1 = self.fin_df
        df = pd.DataFrame(df1[['revenue', 'gross_profit', 'operating_income', 'net_income']], index=df1.index)
        df['gross_margin'] = df['gross_profit'] / df['revenue']
        df['operating_margin'] = df['operating_income'] / df['revenue']
        df['net_margin'] = df['net_income'] / df['revenue']

        return df


    def _cash_margins(self):
        df1 = self.fin_df
        df = pd.DataFrame(df1[['revenue', 'cash_from_ops', 'free_cash_flow']], index=df1.index)
        df['cfo_margin'] = df['cash_from_ops'] / df['revenue']
        df['fcf_margin'] = df['free_cash_flow'] / df['revenue']

        return df


    def _cost_margins(self):
        df1 = self.fin_df
        df = pd.DataFrame(df1[['revenue', 'gross_profit', 'rnd', 'sga', 'capex']], index=df1.index)
        df['cogs_margin'] = (df['revenue'] - df['gross_profit']) / df['revenue']
        df['sga_margin'] = df['sga'] / df['revenue']
        df['rnd_margin'] = df['rnd'] / df['revenue']
        df['capex_margin'] = abs(df['capex'] / df['revenue'])

        return df


