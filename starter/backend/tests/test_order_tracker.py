import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

# --- Unit Tests ---

def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")
    
    # We expect save_order to be called once
    mock_storage.save_order.assert_called_once()

def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    # Simulate that the storage finds an existing order
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    with pytest.raises(ValueError, match="Order with ID 'ORD_EXISTING' already exists."):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")

def test_get_order_by_id_success(order_tracker, mock_storage):
    """Tests getting an order by ID successfully."""
    mock_storage.get_order.return_value = {"order_id": "ORD001", "status": "pending"}
    order = order_tracker.get_order_by_id("ORD001")
    assert order["order_id"] == "ORD001"
    mock_storage.get_order.assert_called_once_with("ORD001")

def test_get_order_by_id_not_found(order_tracker, mock_storage):
    """Tests getting an order by ID when it doesn't exist raises ValueError."""
    mock_storage.get_order.return_value = None
    with pytest.raises(ValueError, match="Order with ID 'ORD001' not found."):
        order_tracker.get_order_by_id("ORD001")

def test_update_order_status_success(order_tracker, mock_storage):
    """Tests updating an order status successfully."""
    mock_storage.get_order.return_value = {"order_id": "ORD001", "status": "pending"}
    order_tracker.update_order_status("ORD001", "shipped")
    mock_storage.save_order.assert_called_once_with("ORD001", {"order_id": "ORD001", "status": "shipped"})

def test_update_order_status_not_found(order_tracker, mock_storage):
    """Tests updating an order status when it doesn't exist raises ValueError."""
    mock_storage.get_order.return_value = None
    with pytest.raises(ValueError, match="Order with ID 'ORD001' not found."):
        order_tracker.update_order_status("ORD001", "shipped")

def test_list_all_orders(order_tracker, mock_storage):
    """Tests listing all orders."""
    mock_storage.get_all_orders.return_value = {
        "ORD001": {"order_id": "ORD001", "status": "pending"},
        "ORD002": {"order_id": "ORD002", "status": "shipped"}
    }
    orders = order_tracker.list_all_orders()
    assert len(orders) == 2
    assert "ORD001" in [o["order_id"] for o in orders]
    mock_storage.get_all_orders.assert_called_once()

def test_list_orders_by_status(order_tracker, mock_storage):
    """Tests listing orders filtered by status."""
    mock_storage.get_all_orders.return_value = {
        "ORD001": {"order_id": "ORD001", "status": "pending"},
        "ORD002": {"order_id": "ORD002", "status": "shipped"},
        "ORD003": {"order_id": "ORD003", "status": "pending"}
    }
    pending_orders = order_tracker.list_orders_by_status("pending")
    assert len(pending_orders) == 2
    assert all(o["status"] == "pending" for o in pending_orders)
