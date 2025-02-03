import pandas as pd


class DividendCoverage:

    def __init__(self, **kwargs):
        self.fin_df = kwargs.get('financials_df', 'error')
        self.div_coverage_df = self._div_coverage_df()
        self.payout_coverage_df = self._payout_coverage_df()
        self.cash_coverage_df = self._cash_coverage_df()


    def _div_coverage_df(self):
        df1 = self.fin_df
        df2 = pd.DataFrame(df1[['cash_for_dividends', 'cash_from_ops', 'net_income', 'free_cash_flow',
                                'cash_equivalents', 'market_securities', 'treasury_stock']], index=df1.index
                           )

        return df2


    def _payout_coverage_df(self):
        df1 = self._div_coverage_df()
        df2 = pd.DataFrame(df1[['cash_for_dividends', 'free_cash_flow', 'net_income']], index=df1.index)

        df2['payout_income'] = abs(df2['cash_for_dividends'] / df2['net_income'])
        df2['payout_fcf'] = abs(df2['cash_for_dividends'] / df2['free_cash_flow'])

        return df2


    def _cash_coverage_df(self):
        df1 = self._div_coverage_df()
        df2 = pd.DataFrame(df1[['cash_for_dividends', 'cash_equivalents', 'market_securities', 'cash_from_ops']], index=df1.index)

        df2['payout_cce'] = abs(df2['cash_for_dividends'] / (df2['cash_equivalents'] + df2['market_securities']))
        df2['payout_cfo'] = abs(df2['cash_for_dividends'] / df2['cash_from_ops'])

        return df2


