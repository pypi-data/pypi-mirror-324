from at_common_functions.utils.storage import get_storage
from at_common_models.stock.financials.annual_balance_sheet_statement import AnnualBalanceSheetStatementModel
from at_common_models.stock.financials.quarter_balance_sheet_statement import QuarterBalanceSheetStatementModel
from at_common_models.stock.financials.annual_cashflow_statement import AnnualCashFlowStatementModel
from at_common_models.stock.financials.quarter_cashflow_statement import QuarterCashflowStatementModel
from at_common_models.stock.financials.annual_income_statement import AnnualIncomeStatementModel
from at_common_models.stock.financials.quarter_income_statement import QuarterlyIncomeStatementModel
from at_common_functions.stock.impls.overview import get as stock_get_overview
import asyncio
from at_common_functions.stock.impls.financial.analysis import FinancialAnalysis

async def list(*, symbol: str, period: str, statement: str, limit: int) -> list:
    storage = get_storage()

    clazz = None
    if period == 'annual':
        if statement == 'income':
            clazz = AnnualIncomeStatementModel
        elif statement == 'balance_sheet':
            clazz = AnnualBalanceSheetStatementModel
        elif statement == 'cash_flow':
            clazz = AnnualCashFlowStatementModel
    elif period == 'quarterly':
        if statement == 'income':
            clazz = QuarterlyIncomeStatementModel
        elif statement == 'balance_sheet':
            clazz = QuarterBalanceSheetStatementModel
        elif statement == 'cash_flow':
            clazz = QuarterCashflowStatementModel
    
    if clazz is None:
        raise ValueError("Invalid period or statement for financials")

    statements = await storage.query(
        model_class=clazz,
        filters=[clazz.symbol == symbol],
        sort=[clazz.fiscal_date_ending.desc()],
        limit=limit
    )

    return [statement.to_dict() for statement in statements]

async def get_latest(*, symbol: str) -> dict:
    # Fetch the most recent statement of each type (limit=1)
    annual_statements = dict(zip(
        ['balance_sheet', 'income', 'cash_flow'],
        await asyncio.gather(
            list(symbol=symbol, period='annual', statement='balance_sheet', limit=1),
            list(symbol=symbol, period='annual', statement='income', limit=1),
            list(symbol=symbol, period='annual', statement='cash_flow', limit=1)
        )
    ))
    
    quarterly_statements = dict(zip(
        ['balance_sheet', 'income', 'cash_flow'],
        await asyncio.gather(
            list(symbol=symbol, period='quarterly', statement='balance_sheet', limit=1),
            list(symbol=symbol, period='quarterly', statement='income', limit=1),
            list(symbol=symbol, period='quarterly', statement='cash_flow', limit=1)
        )
    ))
    
    return {
        'annual': {
            'balance_sheet': annual_statements['balance_sheet'][0] if annual_statements['balance_sheet'] else None,
            'income': annual_statements['income'][0] if annual_statements['income'] else None,
            'cash_flow': annual_statements['cash_flow'][0] if annual_statements['cash_flow'] else None
        },
        'quarterly': {
            'balance_sheet': quarterly_statements['balance_sheet'][0] if quarterly_statements['balance_sheet'] else None,
            'income': quarterly_statements['income'][0] if quarterly_statements['income'] else None,
            'cash_flow': quarterly_statements['cash_flow'][0] if quarterly_statements['cash_flow'] else None
        }
    }

async def analyze(*, symbol: str) -> dict:
    # Load all required financial statements with named results
    annual_statements = dict(zip(
        ['balance_sheet', 'income', 'cash_flow'],
        await asyncio.gather(
            list(symbol=symbol, period='annual', statement='balance_sheet', limit=12),
            list(symbol=symbol, period='annual', statement='income', limit=12),
            list(symbol=symbol, period='annual', statement='cash_flow', limit=12)
        )
    ))
    
    quarterly_statements = dict(zip(
        ['balance_sheet', 'income', 'cash_flow'],
        await asyncio.gather(
            list(symbol=symbol, period='quarterly', statement='balance_sheet', limit=12),
            list(symbol=symbol, period='quarterly', statement='income', limit=12),
            list(symbol=symbol, period='quarterly', statement='cash_flow', limit=12)
        )
    ))
    
    # Get company overview data
    overview = await stock_get_overview(symbol=symbol)
    
    # Initialize financial analysis with more readable references
    analysis = FinancialAnalysis(
        overview=overview,
        annual_balance_sheets=annual_statements['balance_sheet'],
        quarterly_balance_sheets=quarterly_statements['balance_sheet'],
        annual_incomes=annual_statements['income'],
        quarterly_incomes=quarterly_statements['income'],
        annual_cash_flows=annual_statements['cash_flow'],
        quarterly_cash_flows=quarterly_statements['cash_flow']
    )
    
    # Generate comprehensive analysis for both periods
    return {
        'annual': analysis.get_comprehensive_analysis(period='annual'),
        'quarterly': analysis.get_comprehensive_analysis(period='quarterly')
    }
    