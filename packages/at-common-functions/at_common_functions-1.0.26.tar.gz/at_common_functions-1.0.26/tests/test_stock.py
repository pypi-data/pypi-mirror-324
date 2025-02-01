import pytest
from unittest.mock import MagicMock, patch
from at_common_functions.stock import (
    list_candlesticks,
    list_financials,
    list_indicators,
    analyze_financials,
    get_overview,
    get_quotation,
    get_latest_financials
)
from at_common_models.stock.quotation import QuotationModel
from at_common_models.stock.overview import OverviewModel
from at_common_models.stock.daily_candlestick import DailyCandlestickModel
from at_common_models.stock.daily_indicator import DailyIndicatorModel
from at_common_models.stock.financials.annual_balance_sheet_statement import AnnualBalanceSheetStatementModel
from at_common_models.stock.financials.annual_income_statement import AnnualIncomeStatementModel
from at_common_models.stock.financials.annual_cashflow_statement import AnnualCashFlowStatementModel
from at_common_models.stock.financials.quarter_balance_sheet_statement import QuarterBalanceSheetStatementModel
from at_common_models.stock.financials.quarter_income_statement import QuarterlyIncomeStatementModel
from at_common_models.stock.financials.quarter_cashflow_statement import QuarterCashflowStatementModel
from datetime import datetime, timedelta

TEST_SYMBOL = "AAPL"

@pytest.fixture
def mock_storage():
    storage = MagicMock()
    
    # Sample test data
    overview = OverviewModel(
        symbol=TEST_SYMBOL,
        name="Apple Inc.",
        sector="Technology",
        industry="Consumer Electronics"
    )
    
    quotation = QuotationModel(
        symbol=TEST_SYMBOL,
        price=150.0,
        volume=1000000,
        share_outstanding=16000000000,
        timestamp=datetime.now()
    )
    
    candlesticks = [
        DailyCandlestickModel(
            symbol=TEST_SYMBOL,
            time=datetime.now(),
            open=150.0,
            high=155.0,
            low=149.0,
            close=152.0,
            volume=1000000
        )
        for _ in range(5)
    ]
    
    indicators = [
        DailyIndicatorModel(
            symbol=TEST_SYMBOL,
            time=datetime.now(),
            sma10=150.0,
            sma20=148.0,
            rsi=65.0
        )
        for _ in range(5)
    ]
    
    financials = {
        'annual_income': [
            AnnualIncomeStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime(2023 - i, 12, 31),
                revenue=394328000000 * (1 + i * 0.1),
                gross_profit=170782000000 * (1 + i * 0.1),
                operating_income=119437000000 * (1 + i * 0.1),
                net_income=96995000000 * (1 + i * 0.1),
                cost_of_revenue=223546000000 * (1 + i * 0.1),
                interest_expense=2500000000 * (1 + i * 0.1)
            )
            for i in range(8)
        ],
        'annual_balance': [
            AnnualBalanceSheetStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime(2023 - i, 12, 31),
                total_assets=352755000000 * (1 + i * 0.05),
                total_liabilities=287912000000 * (1 + i * 0.05),
                total_stockholders_equity=64843000000 * (1 + i * 0.05),
                total_current_assets=135405000000 * (1 + i * 0.05),
                total_current_liabilities=153982000000 * (1 + i * 0.05),
                inventory=6163000000 * (1 + i * 0.05),
                cash_and_cash_equivalents=29965000000 * (1 + i * 0.05),
                total_debt=287912000000 * (1 + i * 0.05)
            )
            for i in range(8)
        ],
        'annual_cashflow': [
            AnnualCashFlowStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime(2023 - i, 12, 31),
                operating_cash_flow=300000 * (1 + i * 0.1),
                free_cash_flow=250000 * (1 + i * 0.1)
            )
            for i in range(8)
        ],
        'quarter_income': [
            QuarterlyIncomeStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime(2023, 12, 31) - timedelta(days=90 * i),
                revenue=250000 * (1 + i * 0.05),
                gross_profit=125000 * (1 + i * 0.05),
                net_income=75000 * (1 + i * 0.05),
                operating_income=100000 * (1 + i * 0.05),
                cost_of_revenue=125000 * (1 + i * 0.05),
                interest_expense=5000 * (1 + i * 0.05)
            )
            for i in range(8)
        ],
        'quarter_balance': [
            QuarterBalanceSheetStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime(2023, 12, 31) - timedelta(days=90 * i),
                total_assets=2000000 * (1 + i * 0.05),
                total_liabilities=1000000 * (1 + i * 0.05),
                total_stockholders_equity=1000000 * (1 + i * 0.05),
                total_current_assets=800000 * (1 + i * 0.05),
                total_current_liabilities=600000 * (1 + i * 0.05),
                inventory=200000 * (1 + i * 0.05),
                cash_and_cash_equivalents=300000 * (1 + i * 0.05),
                total_debt=800000 * (1 + i * 0.05)
            )
            for i in range(8)
        ],
        'quarter_cashflow': [
            QuarterCashflowStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime(2023, 12, 31) - timedelta(days=90 * i),
                operating_cash_flow=75000 * (1 + i * 0.05),
                free_cash_flow=60000 * (1 + i * 0.05)
            )
            for i in range(8)
        ]
    }

    async def mock_query(model_class, filters, sort=None, limit=None):
        symbol_value = filters[0].right.value if hasattr(filters[0].right, 'value') else filters[0].right
        if model_class == OverviewModel:
            should_return = symbol_value == TEST_SYMBOL
            print(f"Should return overview: {should_return}")
            return [overview] if should_return else []
        elif model_class == QuotationModel:
            return [quotation] if symbol_value == TEST_SYMBOL else []
        elif model_class == DailyCandlestickModel:
            return candlesticks if symbol_value == TEST_SYMBOL else []
        elif model_class == DailyIndicatorModel:
            return indicators if symbol_value == TEST_SYMBOL else []
        elif model_class == AnnualIncomeStatementModel:
            return financials['annual_income'] if symbol_value == TEST_SYMBOL else []
        elif model_class == AnnualBalanceSheetStatementModel:
            return financials['annual_balance'] if symbol_value == TEST_SYMBOL else []
        elif model_class == AnnualCashFlowStatementModel:
            return financials['annual_cashflow'] if symbol_value == TEST_SYMBOL else []
        elif model_class == QuarterlyIncomeStatementModel:
            return financials['quarter_income'] if symbol_value == TEST_SYMBOL else []
        elif model_class == QuarterBalanceSheetStatementModel:
            return financials['quarter_balance'] if symbol_value == TEST_SYMBOL else []
        elif model_class == QuarterCashflowStatementModel:
            return financials['quarter_cashflow'] if symbol_value == TEST_SYMBOL else []
        return []

    storage.query = mock_query
    return storage

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.overview.get_storage')
async def test_get_overview_success(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    result = await get_overview(symbol=TEST_SYMBOL)
    assert isinstance(result, dict)
    assert result["symbol"] == TEST_SYMBOL
    assert result["name"] == "Apple Inc."
    assert result["sector"] == "Technology"

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.overview.get_storage')
async def test_stock_get_overview_invalid_symbol(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    with pytest.raises(ValueError, match="No overview found for symbol"):
        await get_overview(symbol="INVALID_SYMBOL")

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.quotation.get_storage')
async def test_stock_get_quotation_success(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    result = await get_quotation(symbol=TEST_SYMBOL)
    assert isinstance(result, dict)
    assert result["symbol"] == TEST_SYMBOL
    assert result["price"] == 150.0
    assert result["volume"] == 1000000

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.candlestick.get_storage')
async def test_list_candlesticks_daily(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    result = await list_candlesticks(
        symbol=TEST_SYMBOL,
        type="daily",
        limit=5
    )
    assert isinstance(result, list)
    assert len(result) == 5
    for candlestick in result:
        assert candlestick["symbol"] == TEST_SYMBOL
        assert candlestick["open"] == 150.0
        assert candlestick["high"] == 155.0
        assert candlestick["low"] == 149.0
        assert candlestick["close"] == 152.0

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.indicator.get_storage')
async def test_stock_get_indicators_daily(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    result = await list_indicators(
        symbol=TEST_SYMBOL,
        type="daily",
        limit=5
    )
    assert isinstance(result, list)
    assert len(result) == 5
    for indicator in result:
        assert indicator["symbol"] == TEST_SYMBOL
        assert indicator["sma10"] == 150.0
        assert indicator["sma20"] == 148.0
        assert indicator["rsi"] == 65.0

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.financial.get_storage')
@patch('at_common_functions.stock.impls.quotation.get_storage')
@pytest.mark.parametrize("period,statement", [
    ("annual", "income"),
    ("annual", "balance_sheet"),
    ("annual", "cash_flow"),
    ("quarterly", "income"),
    ("quarterly", "balance_sheet"),
    ("quarterly", "cash_flow"),
])
async def test_stock_list_financials_success(mock_get_storage, mock_get_quotation_storage, mock_storage, period, statement):
    mock_get_storage.return_value = mock_storage
    mock_get_quotation_storage.return_value = mock_storage
    result = await list_financials(
        symbol=TEST_SYMBOL,
        period=period,
        statement=statement,
        limit=3
    )
    assert isinstance(result, list)
    assert len(result) == 8
    for financial in result:
        assert financial["symbol"] == TEST_SYMBOL
        assert "fiscal_date_ending" in financial

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.financial.get_storage')
@patch('at_common_functions.stock.impls.overview.get_storage')
async def test_analyze_financials_success(mock_overview_storage, mock_financial_storage, mock_storage):
    mock_overview_storage.return_value = mock_storage
    mock_financial_storage.return_value = mock_storage
    
    result = await analyze_financials(symbol=TEST_SYMBOL)
    
    import json
    print(json.dumps(result, indent=4))

    # Check basic structure
    assert isinstance(result, dict)
    assert 'annual' in result
    assert 'quarterly' in result
    
    # Check that both annual and quarterly analyses exist and have data
    for period in ['annual', 'quarterly']:
        analysis = result[period]
        assert isinstance(analysis, dict)
        # Add assertions for expected analysis fields based on your FinancialAnalysis implementation
        # For example:
        assert 'profitability' in analysis
        assert 'liquidity' in analysis
        assert 'efficiency' in analysis

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.financial.get_storage')
@patch('at_common_functions.stock.impls.overview.get_storage')
async def test_analyze_financials_invalid_symbol(mock_overview_storage, mock_financial_storage, mock_storage):
    mock_overview_storage.return_value = mock_storage
    mock_financial_storage.return_value = mock_storage
    
    with pytest.raises(ValueError, match="No overview found for symbol"):
        await analyze_financials(symbol="INVALID_SYMBOL")

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.financial.get_storage')
async def test_get_latest_financials_success(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    
    result = await get_latest_financials(symbol=TEST_SYMBOL)
    
    # Check basic structure
    assert isinstance(result, dict)
    assert 'annual' in result
    assert 'quarterly' in result
    
    # Check annual statements
    annual = result['annual']
    assert 'balance_sheet' in annual
    assert 'income' in annual
    assert 'cash_flow' in annual
    
    # Check quarterly statements
    quarterly = result['quarterly']
    assert 'balance_sheet' in quarterly
    assert 'income' in quarterly
    assert 'cash_flow' in quarterly
    
    # Verify content of latest annual statements
    assert annual['balance_sheet']['symbol'] == TEST_SYMBOL
    assert annual['income']['symbol'] == TEST_SYMBOL
    assert annual['cash_flow']['symbol'] == TEST_SYMBOL
    
    # Verify content of latest quarterly statements
    assert quarterly['balance_sheet']['symbol'] == TEST_SYMBOL
    assert quarterly['income']['symbol'] == TEST_SYMBOL
    assert quarterly['cash_flow']['symbol'] == TEST_SYMBOL

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.financial.get_storage')
async def test_get_latest_financials_empty_result(mock_get_storage, mock_storage):
    # Modify storage to return empty results
    async def mock_empty_query(*args, **kwargs):
        return []
    
    mock_storage.query = mock_empty_query
    mock_get_storage.return_value = mock_storage
    
    result = await get_latest_financials(symbol=TEST_SYMBOL)
    
    # Check that all fields are None when no data is found
    assert result['annual']['balance_sheet'] is None
    assert result['annual']['income'] is None
    assert result['annual']['cash_flow'] is None
    assert result['quarterly']['balance_sheet'] is None
    assert result['quarterly']['income'] is None
    assert result['quarterly']['cash_flow'] is None

@pytest.mark.asyncio
@patch('at_common_functions.stock.impls.financial.get_storage')
async def test_get_latest_financials_invalid_symbol(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    
    result = await get_latest_financials(symbol="INVALID_SYMBOL")
    
    # Check that all fields are None for invalid symbol
    assert result['annual']['balance_sheet'] is None
    assert result['annual']['income'] is None
    assert result['annual']['cash_flow'] is None
    assert result['quarterly']['balance_sheet'] is None
    assert result['quarterly']['income'] is None
    assert result['quarterly']['cash_flow'] is None