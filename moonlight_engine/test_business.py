"""
Testing suite for Moonlight Business system
"""

import logging
import sys
from datetime import datetime

# Import all modules to test
from payment_system import (
    create_payment_processor,
    create_order_manager,
    create_fulfillment_manager,
    create_revenue_tracker
)

logger = logging.getLogger(__name__)


class BusinessSystemTest:
    """Test all business system components"""
    
    def __init__(self):
        """Initialize test suite"""
        self.payment_processor = create_payment_processor()
        self.order_manager = create_order_manager()
        self.fulfillment_manager = create_fulfillment_manager()
        self.revenue_tracker = create_revenue_tracker()
        self.test_results = []
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "=" * 70)
        print("MOONLIGHT BUSINESS SYSTEM - TEST SUITE")
        print(f"Started: {datetime.now()}")
        print("=" * 70)
        
        try:
            self.test_payment_system()
            self.test_order_system()
            self.test_fulfillment_system()
            self.test_revenue_system()
            self.print_results()
        except Exception as e:
            print(f"\n❌ Test suite error: {str(e)}")
            sys.exit(1)
    
    def test_payment_system(self):
        """Test payment processing"""
        print("\n[TEST 1] PAYMENT SYSTEM")
        print("-" * 70)
        
        try:
            # Create payment intent
            print("  → Testing payment intent creation...")
            intent = self.payment_processor.create_payment_intent(
                amount=25.99,
                metadata={"test": "true"}
            )
            
            assert intent['id'], "Payment intent ID missing"
            assert intent['amount'] == 2599, "Amount calculation error"
            assert intent['status'] == "requires_payment_method", "Status incorrect"
            print(f"  ✓ Payment intent created: {intent['id']}")
            print(f"    Amount: ${intent['amount']/100:.2f}")
            print(f"    Status: {intent['status']}")
            
            # Confirm payment
            print("  → Testing payment confirmation...")
            confirmation = self.payment_processor.confirm_payment(intent['id'])
            
            assert confirmation['status'] == "succeeded", "Payment not confirmed"
            print(f"  ✓ Payment confirmed")
            print(f"    Status: {confirmation['status']}")
            
            self.test_results.append(("Payment System", "PASSED"))
            print("  ✓ PAYMENT SYSTEM: PASSED")
            
        except AssertionError as e:
            print(f"  ❌ PAYMENT SYSTEM: FAILED - {str(e)}")
            self.test_results.append(("Payment System", "FAILED"))
    
    def test_order_system(self):
        """Test order management"""
        print("\n[TEST 2] ORDER MANAGEMENT SYSTEM")
        print("-" * 70)
        
        try:
            # Create order
            print("  → Testing order creation...")
            customer = {
                "name": "Test Customer",
                "email": "test@example.com",
                "address": "123 Test St"
            }
            items = [
                {
                    "name": "Test Product",
                    "price": 16.99,
                    "quantity": 1
                }
            ]
            
            order = self.order_manager.create_order(
                customer=customer,
                items=items,
                total_price=16.99
            )
            
            assert order['id'], "Order ID missing"
            assert order['status'] == "pending", "Order status incorrect"
            assert order['total'] == 16.99, "Order total incorrect"
            print(f"  ✓ Order created: {order['id']}")
            print(f"    Status: {order['status']}")
            print(f"    Total: ${order['total']:.2f}")
            
            # Update order status
            print("  → Testing order status update...")
            updated = self.order_manager.update_order_status(
                order['id'],
                'processing'
            )
            
            assert updated['status'] == "processing", "Status not updated"
            print(f"  ✓ Order status updated: {updated['status']}")
            
            # Get order
            print("  → Testing order retrieval...")
            retrieved = self.order_manager.get_order(order['id'])
            assert retrieved is not None, "Order not found"
            print(f"  ✓ Order retrieved: {retrieved['id']}")
            
            self.test_results.append(("Order System", "PASSED"))
            print("  ✓ ORDER SYSTEM: PASSED")
            
        except AssertionError as e:
            print(f"  ❌ ORDER SYSTEM: FAILED - {str(e)}")
            self.test_results.append(("Order System", "FAILED"))
    
    def test_fulfillment_system(self):
        """Test fulfillment management"""
        print("\n[TEST 3] FULFILLMENT SYSTEM")
        print("-" * 70)
        
        try:
            # Create test order first
            customer = {"name": "Test", "email": "test@example.com"}
            order = self.order_manager.create_order(
                customer=customer,
                items=[{"name": "Test"}],
                total_price=25.00
            )
            
            # Create fulfillment
            print("  → Testing fulfillment creation...")
            fulfillment = self.fulfillment_manager.create_fulfillment(
                order=order,
                supplier="printful"
            )
            
            assert fulfillment['id'], "Fulfillment ID missing"
            assert fulfillment['status'] == "pending", "Status incorrect"
            print(f"  ✓ Fulfillment created: {fulfillment['id']}")
            print(f"    Supplier: {fulfillment['supplier']}")
            print(f"    Estimated delivery: {fulfillment['estimated_delivery'][:10]}")
            
            # Send to supplier
            print("  → Testing supplier submission...")
            submitted = self.fulfillment_manager.send_to_supplier(
                fulfillment['id'],
                {"test": "data"}
            )
            
            assert submitted['status'] == "submitted", "Not submitted"
            assert submitted['supplier_order_id'], "Supplier order ID missing"
            print(f"  ✓ Sent to supplier: {submitted['supplier_order_id']}")
            
            # Add tracking
            print("  → Testing tracking update...")
            tracked = self.fulfillment_manager.update_fulfillment_tracking(
                fulfillment['id'],
                "TRACK123456789"
            )
            
            assert tracked['status'] == "shipped", "Status not updated to shipped"
            assert tracked['tracking_number'] == "TRACK123456789", "Tracking not set"
            print(f"  ✓ Tracking added: {tracked['tracking_number']}")
            
            self.test_results.append(("Fulfillment System", "PASSED"))
            print("  ✓ FULFILLMENT SYSTEM: PASSED")
            
        except AssertionError as e:
            print(f"  ❌ FULFILLMENT SYSTEM: FAILED - {str(e)}")
            self.test_results.append(("Fulfillment System", "FAILED"))
    
    def test_revenue_system(self):
        """Test revenue tracking"""
        print("\n[TEST 4] REVENUE TRACKING SYSTEM")
        print("-" * 70)
        
        try:
            # Record sales
            print("  → Testing revenue recording...")
            
            sale1 = self.revenue_tracker.record_sale(
                order_id="ORD_001",
                revenue=25.99,
                cost=10.00,
                platform="ebay",
                product_type="dropship"
            )
            
            assert sale1['profit'] == 15.99, "Profit calculation error"
            assert sale1['margin_percent'] > 0, "Margin calculation error"
            print(f"  ✓ Sale 1 recorded:")
            print(f"    Revenue: ${sale1['revenue']:.2f}")
            print(f"    Profit: ${sale1['profit']:.2f}")
            print(f"    Margin: {sale1['margin_percent']:.1f}%")
            
            # Record another sale
            sale2 = self.revenue_tracker.record_sale(
                order_id="ORD_002",
                revenue=32.99,
                cost=12.00,
                platform="shopify",
                product_type="pod"
            )
            
            print(f"  ✓ Sale 2 recorded:")
            print(f"    Revenue: ${sale2['revenue']:.2f}")
            print(f"    Profit: ${sale2['profit']:.2f}")
            
            # Get summary
            print("  → Testing revenue summary...")
            summary = self.revenue_tracker.get_revenue_summary()
            
            assert summary['total_revenue'] > 0, "Total revenue incorrect"
            assert summary['total_profit'] > 0, "Total profit incorrect"
            assert len(summary['by_platform']) > 0, "Platform breakdown missing"
            
            print(f"  ✓ Revenue summary:")
            print(f"    Total revenue: ${summary['total_revenue']:.2f}")
            print(f"    Total profit: ${summary['total_profit']:.2f}")
            print(f"    Avg margin: {summary['avg_margin']:.1f}%")
            
            self.test_results.append(("Revenue System", "PASSED"))
            print("  ✓ REVENUE SYSTEM: PASSED")
            
        except AssertionError as e:
            print(f"  ❌ REVENUE SYSTEM: FAILED - {str(e)}")
            self.test_results.append(("Revenue System", "FAILED"))
    
    def print_results(self):
        """Print test results summary"""
        print("\n" + "=" * 70)
        print("TEST RESULTS SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for _, result in self.test_results if result == "PASSED")
        failed = sum(1 for _, result in self.test_results if result == "FAILED")
        
        for test_name, result in self.test_results:
            status_icon = "✓" if result == "PASSED" else "❌"
            print(f"{status_icon} {test_name}: {result}")
        
        print("-" * 70)
        print(f"Total: {len(self.test_results)} tests")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print("=" * 70)
        
        if failed == 0:
            print("\n✓ ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION\n")
        else:
            print(f"\n❌ {failed} TEST(S) FAILED - FIX BEFORE DEPLOYMENT\n")


def main():
    """Run test suite"""
    logging.basicConfig(level=logging.INFO)
    tester = BusinessSystemTest()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
