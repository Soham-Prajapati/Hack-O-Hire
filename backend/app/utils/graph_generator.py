"""
Graph Generator — Builds network graph data from transactions.
"""

def build_transaction_network(transactions: list) -> dict:
    """
    Convert a list of transactions into a node-link format for visualization.
    
    Returns:
        {
            "nodes": [{"id": "Alice", "type": "customer", "val": 10}, ...],
            "links": [{"source": "Alice", "target": "Bob", "value": 5000}, ...]
        }
    """
    nodes = {}
    links = []
    
    for txn in transactions:
        sender = txn.get("sender", "Unknown")
        receiver = txn.get("receiver", "Unknown")
        try:
            amount = float(txn.get("amount", 0))
        except (ValueError, TypeError):
            amount = 0.0
        
        # Add nodes
        if sender not in nodes:
            nodes[sender] = {"id": sender, "type": "entity", "val": 1.0, "in_amt": 0.0, "out_amt": 0.0}
        if receiver not in nodes:
            nodes[receiver] = {"id": receiver, "type": "entity", "val": 1.0, "in_amt": 0.0, "out_amt": 0.0}
            
        # Update node stats
        nodes[sender]["out_amt"] += amount
        nodes[sender]["val"] += 1
        nodes[receiver]["in_amt"] += amount
        nodes[receiver]["val"] += 1
        
        # Add link
        links.append({
            "source": sender,
            "target": receiver,
            "value": amount,
            "label": f"{amount:,.0f}"
        })
        
    # Format nodes list
    node_list = []
    for name, data in nodes.items():
        # Heuristic: Determine if "Subject" vs "Counterparty"
        # For now, just mark high volume nodes larger
        total_vol = data["in_amt"] + data["out_amt"]
        
        node_list.append({
            "id": name,
            "label": name,
            "val": total_vol, # For visual sizing
            "color": "#ff4b4b" if total_vol > 1000000 else "#00c853" # Red for high volume, Green for low
        })
        
    return {
        "nodes": node_list,
        "links": links
    }
