import asyncio
from typing import Dict, List
import ccxt.pro as ccxt
import time
from bjarkan.models import OrderbookConfig, OrderConfig, APIConfig
from bjarkan.utils.logger import logger, catch_exception
from bjarkan.exceptions import BjarkanError


class OrderExecutor:
    @catch_exception
    def __init__(self, orderbook_config: OrderbookConfig, api_configs: List[APIConfig]):
        if not orderbook_config.aggregated or len(orderbook_config.symbols) != 1:
            raise ValueError("OrderExecutor requires aggregated data and exactly one symbol in orderbook_config")

        self.orderbook_config = orderbook_config
        self.api_configs = {config.exchange: config for config in api_configs}
        self.exchanges = {}
        self.symbol = orderbook_config.symbols[0]
        self.latest_orderbook = None

        # Initialize exchanges
        self._initialize_exchanges()

    @catch_exception
    def _initialize_exchanges(self):
        """Initialize exchange connections."""
        for exchange_id in self.orderbook_config.exchanges:
            if exchange_id not in self.api_configs:
                continue

            config = self.api_configs[exchange_id]
            exchange_class = getattr(ccxt, exchange_id)

            try:
                # Add timestamp adjustment options
                options = {
                    'adjustForTimeDifference': True,
                    'recvWindow': 10000  # Increased from default 5000
                }
                if self.order_config.margin_mode:
                    options['defaultType'] = 'margin'

                exchange = exchange_class({
                    'apiKey': config.api_key,
                    'secret': config.secret,
                    'password': config.password,
                    'enableRateLimit': True,
                    'options': options
                })

                # Test authentication
                exchange.check_required_credentials()

                is_sandbox = self.orderbook_config.sandbox_mode.get(exchange_id, False)
                exchange.set_sandbox_mode(is_sandbox)

                self.exchanges[exchange_id] = exchange

            except BjarkanError as e:
                logger.error(f"Authentication failed for {exchange_id}: {str(e)}")
                raise BjarkanError(f"Invalid API credentials for {exchange_id}")
            except Exception as e:
                logger.error(f"Failed to initialize {exchange_id}: {str(e)}")
                raise BjarkanError(f"Failed to initialize {exchange_id}: {str(e)}")

        if not self.exchanges:
            raise BjarkanError("No exchanges could be initialized with provided API configurations")

    @catch_exception
    def _prepare_margin_params(self, exchange_id: str, margin_mode: bool) -> Dict:
        """Prepare exchange-specific parameters."""
        if not margin_mode:
            return {}  # Return empty params for spot trading

        # Return margin params only if margin_mode is True
        if exchange_id == 'binance':
            return {
                'marginMode': 'cross',
                'sideEffectType': 'AUTO_BORROW_REPAY'
            }
        elif exchange_id == 'bybit':
            return {
                'isLeverage': 1,
                'leverageType': 'cross_margin',
                'spotMarginTrading': True,
                'marginTrading': True
            }
        elif exchange_id == 'gate':
            return {
                'account': 'cross_margin',
                'auto_borrow': True,
                'marginMode': 'cross',
                'unifiedAccount': True
            }
        return {}

    @catch_exception
    async def update_orderbook(self, orderbook: Dict):
        """Update the latest orderbook data."""
        if self.symbol not in orderbook:
            raise BjarkanError(f"No orderbook data available for symbol {self.symbol}")
        self.latest_orderbook = orderbook[self.symbol]

    @catch_exception
    async def execute_order(self, order: OrderConfig) -> Dict:
        """Execute market orders across available exchanges."""
        if not self.latest_orderbook:
            raise BjarkanError("No orderbook data available")

        if not self.exchanges:
            raise BjarkanError("No exchanges initialized with valid API keys")

        execution_plan = self._create_execution_plan(order)
        if not execution_plan:
            raise BjarkanError("Could not create valid execution plan with available liquidity")

        start_time = time.time()

        # Execute all orders in parallel
        execution_tasks = [
            self.execute_single_order(exchange_id, amount, order)
            for exchange_id, amount in execution_plan
        ]
        execution_results = await asyncio.gather(*execution_tasks)

        # Calculate totals
        total_filled_amount = sum(
            result['filled_amount']
            for result in execution_results
            if result['status'] == 'success'
        )
        remaining_amount = max(0, order.amount - total_filled_amount)

        # Get execution times
        execution_times = {
            'total': round((time.time() - start_time) * 1000, 2)
        }
        for result in execution_results:
            execution_times[result['exchange']] = result['execution_time']

        return {
            "status": "completed" if remaining_amount <= 1e-8 else "partially_filled",
            "original_amount": order.amount,
            "filled_amount": total_filled_amount,
            "remaining_amount": remaining_amount,
            "execution_results": execution_results,
            "execution_plan": execution_plan,
            "execution_times": execution_times
        }

    @catch_exception
    async def execute_single_order(self, exchange_id: str, amount: float, order: OrderConfig):
        """Execute a single market order on one exchange."""
        execution_start_time = time.time()
        try:
            exchange = self.exchanges[exchange_id]
            params = self._prepare_margin_params(exchange_id, order.margin_mode)

            logger.info(f"Executing market order on {exchange_id}: {order.side} | {amount} | {self.symbol}")

            executed_order = await exchange.createOrder(
                self.symbol,
                'market',
                order.side,
                amount,
                0,  # Price doesn't matter for market orders
                params
            )

            execution_time = round((time.time() - execution_start_time) * 1000, 2)
            filled_amount = float(executed_order.get('filled', 0) or 0)

            return {
                "exchange": exchange_id,
                "order": executed_order,
                "status": "success",
                "planned_amount": amount,
                "filled_amount": filled_amount,
                "execution_time": execution_time
            }

        except Exception as e:
            execution_time = round((time.time() - execution_start_time) * 1000, 2)
            logger.error(f"Error executing order on {exchange_id}: {str(e)}")
            return {
                "exchange": exchange_id,
                "error": str(e),
                "status": "failed",
                "planned_amount": amount,
                "execution_time": execution_time
            }

    @catch_exception
    def _create_execution_plan(self, order: OrderConfig) -> List[tuple]:
        """Create an execution plan for market orders based on available liquidity."""
        execution_plan = {}  # Use dict to aggregate by exchange
        remaining_amount = order.amount
        book_side = self.latest_orderbook['bids'] if order.side == 'sell' else self.latest_orderbook['asks']

        # Sort asks by price ascending (for buys) or bids by price descending (for sells)
        sorted_levels = sorted(book_side, key=lambda x: x[0], reverse=(order.side == 'sell'))

        # Process each price level in order
        for price, size, exchange in sorted_levels:
            if remaining_amount <= 0:
                break

            if exchange in self.exchanges:
                executable_amount = min(remaining_amount, size)
                exchange_instance = self.exchanges[exchange]
                market = exchange_instance.market(self.symbol)
                amount_precision = float(market['precision']['amount'])

                # Round according to exchange's precision
                executable_amount = (executable_amount // amount_precision) * amount_precision
                if executable_amount == 0:
                    continue

                # Aggregate amounts by exchange
                if exchange in execution_plan:
                    execution_plan[exchange] += executable_amount
                else:
                    execution_plan[exchange] = executable_amount

                remaining_amount -= executable_amount

        # Convert to list of tuples
        final_plan = []
        for exchange, amount in execution_plan.items():
            if amount > 0:
                final_plan.append((exchange, amount))

        # Log the execution plan
        logger.info(f"Created market order execution plan:")
        for exchange, amount in final_plan:
            logger.info(f"{exchange}: {amount}")

        return final_plan

    @catch_exception
    async def close(self):
        """Close all exchange connections."""
        close_tasks = []
        for exchange in self.exchanges.values():
            if hasattr(exchange, 'close'):
                close_tasks.append(exchange.close())

        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)
