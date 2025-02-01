import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class FinancialMetric:
    """Represents a financial metric with its metadata and analysis."""
    value: float
    description: str
    benchmark: Optional[float] = None
    trend: Optional[str] = None
    period_change: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert the FinancialMetric to a dictionary for JSON serialization."""
        return {
            'value': float(self.value),  # Convert numpy.float64 to native float
            'description': self.description,
            'benchmark': float(self.benchmark) if self.benchmark is not None else None,
            'trend': self.trend,
            'period_change': float(self.period_change) if self.period_change is not None else None
        }

class FinancialAnalysis:
    """
    Comprehensive financial analysis toolkit for processing and analyzing company financial data.
    """
    
    def __init__(
        self,
        overview: Dict,
        annual_balance_sheets: List[Dict],
        quarterly_balance_sheets: List[Dict],
        annual_incomes: List[Dict],
        quarterly_incomes: List[Dict],
        annual_cash_flows: List[Dict],
        quarterly_cash_flows: List[Dict]
    ):
        """Initialize with company financial data."""
        self._validate_input_data(overview, annual_balance_sheets, quarterly_balance_sheets,
                                annual_incomes, quarterly_incomes, annual_cash_flows, quarterly_cash_flows)
        
        self.overview = overview
        self.period_mapping = {
            'annual': 365,
            'quarterly': 90
        }
        
        # Initialize financial statements as DataFrames
        self.statements = {
            'annual': {
                'balance_sheet': self._prepare_dataframe(annual_balance_sheets),
                'income': self._prepare_dataframe(annual_incomes),
                'cash_flow': self._prepare_dataframe(annual_cash_flows)
            },
            'quarterly': {
                'balance_sheet': self._prepare_dataframe(quarterly_balance_sheets),
                'income': self._prepare_dataframe(quarterly_incomes),
                'cash_flow': self._prepare_dataframe(quarterly_cash_flows)
            }
        }

    @staticmethod
    def _validate_input_data(*args) -> None:
        """Validate completeness and basic integrity of input data."""
        for arg in args:
            if arg is None or (isinstance(arg, (list, dict)) and not arg):
                raise ValueError("Missing or empty required financial data")
            
            if isinstance(arg, list):
                if not all(isinstance(item, dict) for item in arg):
                    raise ValueError("Invalid data format in financial statements")

    @staticmethod
    def _prepare_dataframe(data: List[Dict]) -> pd.DataFrame:
        """Convert financial data to DataFrame with appropriate data types and sorting."""
        df = pd.DataFrame(data)
        df['fiscal_date_ending'] = pd.to_datetime(df['fiscal_date_ending'])
        return df.sort_values('fiscal_date_ending').reset_index(drop=True)

    def _safe_division(self, numerator: pd.Series, denominator: pd.Series) -> pd.Series:
        """Perform division with comprehensive error handling."""
        if numerator.isna().any() or denominator.isna().any():
            raise ValueError("Cannot perform division with missing values")
            
        result = np.where(
            denominator != 0,
            numerator / denominator,
            np.nan
        )
        return pd.Series(result, index=numerator.index)

    def _calculate_trend(self, series: pd.Series, metric_name: str, periods: Optional[int] = None, relative_threshold: float = 0.01) -> Optional[str]:
        """Calculate trend direction and strength, returns None if insufficient data."""
        # Determine appropriate number of periods based on data frequency
        if periods is None:
            if isinstance(series.index, pd.DatetimeIndex):
                # Infer if data is quarterly or annual based on average days between dates
                avg_days = (series.index[-1] - series.index[0]).days / (len(series) - 1)
                periods = 4 if avg_days < 120 else 2  # Use 4 periods for quarterly, 2 for annual
            else:
                # Default to 2 periods if we can't determine the frequency
                periods = 2
        
        if len(series) < periods:
            return None
        
        recent_values = series.tail(periods)
        if recent_values.isna().any():
            return None
        
        slope = np.polyfit(range(len(recent_values)), recent_values, 1)[0]
        mean_value = np.abs(recent_values.mean())
        threshold = mean_value * relative_threshold
        
        if abs(slope) < threshold:
            return "stable"
        return "increasing" if slope > 0 else "decreasing"

    def calculate_profitability_metrics(self, period: str = 'annual') -> Dict[str, FinancialMetric]:
        """Calculate comprehensive profitability metrics."""
        income_stmt = self.statements[period]['income']
        balance_sheet = self.statements[period]['balance_sheet']
        
        metrics = {}
        
        # Return Metrics
        roe_series = self._safe_division(
            income_stmt['net_income'],
            balance_sheet['total_stockholders_equity']
        )
        metrics['return_on_equity'] = FinancialMetric(
            value=roe_series.iloc[-1],
            description="Measures company's profitability in relation to stockholders' equity",
            benchmark=0.15,
            trend=self._calculate_trend(roe_series, 'ROE'),
            period_change=roe_series.pct_change(fill_method=None).iloc[-1]
        )
        
        roa_series = self._safe_division(
            income_stmt['net_income'],
            balance_sheet['total_assets']
        )
        metrics['return_on_assets'] = FinancialMetric(
            value=roa_series.iloc[-1],
            description="Measures company's profitability in relation to total assets",
            benchmark=0.05,
            trend=self._calculate_trend(roa_series, 'ROA'),
            period_change=roa_series.pct_change(fill_method=None).iloc[-1]
        )
        
        # Margin Metrics
        operating_margin_series = self._safe_division(
            income_stmt['operating_income'],
            income_stmt['revenue']
        )
        metrics['operating_margin'] = FinancialMetric(
            value=operating_margin_series.iloc[-1],
            description="Measures operating efficiency and pricing strategy",
            benchmark=0.15,
            trend=self._calculate_trend(operating_margin_series, 'Operating Margin'),
            period_change=operating_margin_series.pct_change(fill_method=None).iloc[-1]
        )
        
        net_margin_series = self._safe_division(
            income_stmt['net_income'],
            income_stmt['revenue']
        )
        metrics['net_profit_margin'] = FinancialMetric(
            value=net_margin_series.iloc[-1],
            description="Measures overall profitability after all expenses",
            benchmark=0.10,
            trend=self._calculate_trend(net_margin_series, 'Net Profit Margin'),
            period_change=net_margin_series.pct_change(fill_method=None).iloc[-1]
        )
        
        return metrics

    def calculate_liquidity_metrics(self, period: str = 'annual') -> Dict[str, FinancialMetric]:
        """Calculate comprehensive liquidity metrics.
        
        Args:
            period (str): Time period for analysis ('annual' or 'quarterly')
            
        Returns:
            Dict[str, FinancialMetric]: Dictionary containing liquidity metrics:
                - working_capital: Net working capital amount
                - current_ratio: Current assets / Current liabilities
                - quick_ratio: (Current assets - Inventory) / Current liabilities
                
        Raises:
            ValueError: If required columns are missing or contain invalid data
        """
        balance_sheet = self.statements[period]['balance_sheet']
        
        # Validate required columns and data
        required_columns = ['total_current_assets', 'total_current_liabilities', 'inventory']
        if not all(col in balance_sheet.columns for col in required_columns):
            raise ValueError(f"Missing required columns: {required_columns}")
        
        # Check for NaN values in critical columns
        if balance_sheet[required_columns].isna().any().any():
            raise ValueError("Missing values detected in critical columns")
        
        metrics = {}
        
        # Working Capital (new metric)
        working_capital = balance_sheet['total_current_assets'] - balance_sheet['total_current_liabilities']
        metrics['working_capital'] = FinancialMetric(
            value=working_capital.iloc[-1],
            description="Absolute measure of liquid assets available for operations",
            benchmark=0.0,  # Benchmark should be positive
            trend=self._calculate_trend(working_capital, 'Working Capital'),
            period_change=working_capital.pct_change(fill_method=None).iloc[-1]
        )
        
        # Current Ratio
        current_ratio_series = self._safe_division(
            balance_sheet['total_current_assets'],
            balance_sheet['total_current_liabilities']
        )
        metrics['current_ratio'] = FinancialMetric(
            value=current_ratio_series.iloc[-1],
            description="Measures short-term debt-paying ability",
            benchmark=2.0,
            trend=self._calculate_trend(current_ratio_series, 'Current Ratio'),
            period_change=current_ratio_series.pct_change(fill_method=None).iloc[-1]
        )
        
        # Quick Ratio (with validation)
        quick_assets = balance_sheet['total_current_assets'] - balance_sheet['inventory']
        if (quick_assets < 0).any():
            raise ValueError("Invalid data: Quick assets calculation resulted in negative values")
        
        quick_ratio_series = self._safe_division(
            quick_assets,
            balance_sheet['total_current_liabilities']
        )
        metrics['quick_ratio'] = FinancialMetric(
            value=quick_ratio_series.iloc[-1],
            description="Measures immediate debt-paying ability",
            benchmark=1.0,
            trend=self._calculate_trend(quick_ratio_series, 'Quick Ratio'),
            period_change=quick_ratio_series.pct_change(fill_method=None).iloc[-1]
        )
        
        return metrics

    def calculate_efficiency_metrics(self, period: str = 'annual') -> Dict[str, FinancialMetric]:
        """Calculate comprehensive efficiency metrics."""
        balance_sheet = self.statements[period]['balance_sheet']
        income_stmt = self.statements[period]['income']
        
        metrics = {}
        
        # Asset Management Metrics
        asset_turnover_series = self._safe_division(
            income_stmt['revenue'],
            balance_sheet['total_assets']
        )
        metrics['asset_turnover'] = FinancialMetric(
            value=asset_turnover_series.iloc[-1],
            description="Measures efficiency of asset usage in generating revenue",
            benchmark=1.0,
            trend=self._calculate_trend(asset_turnover_series, 'Asset Turnover'),
            period_change=asset_turnover_series.pct_change(fill_method=None).iloc[-1]
        )
        
        inventory_turnover_series = self._safe_division(
            income_stmt['cost_of_revenue'],
            balance_sheet['inventory']
        )
        metrics['inventory_turnover'] = FinancialMetric(
            value=inventory_turnover_series.iloc[-1],
            description="Measures efficiency of inventory management",
            benchmark=6.0,
            trend=self._calculate_trend(inventory_turnover_series, 'Inventory Turnover'),
            period_change=inventory_turnover_series.pct_change(fill_method=None).iloc[-1]
        )
        
        return metrics

    def calculate_solvency_metrics(self, period: str = 'annual') -> Dict[str, FinancialMetric]:
        """Calculate comprehensive solvency metrics, skipping metrics with insufficient data."""
        balance_sheet = self.statements[period]['balance_sheet']
        income_stmt = self.statements[period]['income']
        
        metrics = {}
        
        # Leverage Metrics
        try:
            debt_to_equity_series = self._safe_division(
                balance_sheet['total_debt'],
                balance_sheet['total_stockholders_equity']
            )
            if not debt_to_equity_series.isna().all():  # Only include if we have some valid data
                metrics['debt_to_equity'] = FinancialMetric(
                    value=debt_to_equity_series.dropna().iloc[-1],
                    description="Measures financial leverage",
                    benchmark=1.5,
                    trend=self._calculate_trend(debt_to_equity_series, 'Debt to Equity'),
                    period_change=debt_to_equity_series.pct_change(fill_method=None).dropna().iloc[-1] if len(debt_to_equity_series.dropna()) > 1 else None
                )
        except (ValueError, IndexError):
            pass  # Skip this metric if calculation fails
        
        try:
            interest_coverage_series = self._safe_division(
                income_stmt['operating_income'],
                income_stmt['interest_expense']
            )
            if not interest_coverage_series.isna().all():  # Only include if we have some valid data
                metrics['interest_coverage'] = FinancialMetric(
                    value=interest_coverage_series.dropna().iloc[-1],
                    description="Measures ability to meet interest payments",
                    benchmark=3.0,
                    trend=self._calculate_trend(interest_coverage_series, 'Interest Coverage'),
                    period_change=interest_coverage_series.pct_change(fill_method=None).dropna().iloc[-1] if len(interest_coverage_series.dropna()) > 1 else None
                )
        except (ValueError, IndexError):
            pass  # Skip this metric if calculation fails
        
        return metrics

    def calculate_cash_flow_metrics(self, period: str = 'annual') -> Dict[str, FinancialMetric]:
        """Calculate comprehensive cash flow metrics."""
        cash_flow = self.statements[period]['cash_flow']
        income_stmt = self.statements[period]['income']
        
        metrics = {}
        
        # Operating Cash Flow Metrics
        operating_cash_flow_ratio_series = self._safe_division(
            cash_flow['operating_cash_flow'],
            income_stmt['revenue']
        )
        metrics['operating_cash_flow_ratio'] = FinancialMetric(
            value=operating_cash_flow_ratio_series.iloc[-1],
            description="Measures operating cash generated relative to revenue",
            benchmark=0.10,
            trend=self._calculate_trend(operating_cash_flow_ratio_series, 'Operating Cash Flow Ratio'),
            period_change=operating_cash_flow_ratio_series.pct_change(fill_method=None).iloc[-1]
        )
        
        free_cash_flow_yield_series = self._safe_division(
            cash_flow['free_cash_flow'],
            income_stmt['revenue']
        )
        metrics['free_cash_flow_yield'] = FinancialMetric(
            value=free_cash_flow_yield_series.iloc[-1],
            description="Measures free cash flow relative to revenue",
            benchmark=0.05,
            trend=self._calculate_trend(free_cash_flow_yield_series, 'Free Cash Flow Yield'),
            period_change=free_cash_flow_yield_series.pct_change(fill_method=None).iloc[-1]
        )
        
        return metrics

    def get_comprehensive_analysis(self, period: str = 'annual') -> Dict[str, Dict[str, dict]]:
        """Generate comprehensive financial analysis across all metric categories."""
        analysis = {
            'profitability': self.calculate_profitability_metrics(period),
            'liquidity': self.calculate_liquidity_metrics(period),
            'efficiency': self.calculate_efficiency_metrics(period),
            'solvency': self.calculate_solvency_metrics(period),
            'cash_flow': self.calculate_cash_flow_metrics(period)
        }
        
        # Convert FinancialMetric objects to dictionaries
        return {
            category: {metric: value.to_dict() for metric, value in metrics.items()}
            for category, metrics in analysis.items()
        }

    def generate_summary_report(self, period: str = 'annual', format_type: str = 'text') -> str:
        """Generate detailed analysis report with insights and trends."""
        analysis = self.get_comprehensive_analysis(period)
        latest_date = self.statements[period]['balance_sheet']['fiscal_date_ending'].max()
        
        if format_type == 'html':
            return self._generate_html_report(analysis, latest_date)
        
        report_sections = [
            f"Financial Analysis Summary for {self.overview['name']}",
            f"As of {latest_date.strftime('%Y-%m-%d')}",
            f"Industry: {self.overview['industry']}",
            "\nKey Performance Indicators:\n"
        ]
        
        for category, metrics in analysis.items():
            report_sections.append(f"\n{category.upper()} ANALYSIS:")
            for name, metric in metrics.items():
                report_sections.append(
                    f"{name}: {metric.value:.2f} | "
                    f"Trend: {metric.trend} | "
                    f"Change: {metric.period_change:.1%} | "
                    f"Benchmark: {metric.benchmark:.2f}"
                )
        
        return "\n".join(report_sections)