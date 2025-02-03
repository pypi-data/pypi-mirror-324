import pandas as pd


class MarketValuation:

    def __init__(self, **kwargs):
        self.fin_df = kwargs.get('financials_df', 'error')
        self.pershare_df = kwargs.get('pershare_df', 'error')
        self.valuation_ps_df = self._mv_ps()
        self.valuation_tc_df = self._mv_tc()


    def _mv_ps(self):
        df1 = self.pershare_df
        df2 = pd.DataFrame(df1[['pershare_revenue', 'pershare_earnings', 'pershare_fcf',
                                'pershare_high_price', 'pershare_low_price']], index=df1.index)

        return df2


    def _mv_tc(self):
        df1 = self.fin_df
        df2 = pd.DataFrame(df1[['revenue', 'net_income', 'free_cash_flow', 'cash_from_ops',
                                'shares_outstanding_eop']], index=df1.index)

        return df2
