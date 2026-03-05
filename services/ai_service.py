
"""
AI Assistant Service for ApnaGrocery
Provides intelligent responses and auto-analysis for the grocery management system
"""
import json
from datetime import datetime, timedelta
from models import db, Product, Supplier, Sale, Admin
from sqlalchemy import func


class GroceryAIAssistant:
    """AI Assistant that understands grocery business and provides insights"""
    
    def __init__(self):
        self.context = "grocery_management"
    
    def get_inventory_summary(self):
        """Get current inventory statistics"""
        total_products = Product.query.count()
        total_value = db.session.query(func.sum(Product.price * Product.quantity)).scalar() or 0
        low_stock = Product.query.filter(Product.quantity <= 10).count()
        out_of_stock = Product.query.filter(Product.quantity == 0).count()
        
        return {
            "total_products": total_products,
            "total_value": round(total_value, 2),
            "low_stock": low_stock,
            "out_of_stock": out_of_stock
        }
    
    def get_sales_summary(self):
        """Get sales statistics"""
        total_sales = Sale.query.count()
        
        # Today's sales
        today = datetime.now().date()
        today_sales = Sale.query.filter(func.date(Sale.created_at) == today).all()
        today_revenue = sum(s.quantity * (s.product.price if s.product else 0) for s in today_sales)
        
        # This week's sales
        week_ago = datetime.now().date() - timedelta(days=7)
        week_sales = Sale.query.filter(func.date(Sale.created_at) >= week_ago).all()
        week_revenue = sum(s.quantity * (s.product.price if s.product else 0) for s in week_sales)
        
        return {
            "total_orders": total_sales,
            "today_revenue": round(today_revenue, 2),
            "week_revenue": round(week_revenue, 2)
        }
    
    def get_supplier_summary(self):
        """Get supplier statistics"""
        total_suppliers = Supplier.query.count()
        return {"total_suppliers": total_suppliers}
    
    def get_top_products(self, limit=5):
        """Get top selling products"""
        top = db.session.query(
            Product.name,
            func.sum(Sale.quantity).label('total_sold')
        ).join(Sale).group_by(Product.id, Product.name
        ).order_by(func.sum(Sale.quantity).desc()
        ).limit(limit).all()
        
        return [{"name": p.name, "sold": p.total_sold} for p in top]
    
    def get_low_stock_alerts(self):
        """Get products that need attention"""
        low_stock_products = Product.query.filter(Product.quantity <= 10).order_by(Product.quantity).all()
        alerts = []
        for p in low_stock_products:
            status = "CRITICAL" if p.quantity == 0 else "LOW"
            alerts.append({
                "name": p.name,
                "quantity": p.quantity,
                "status": status
            })
        return alerts
    
    def analyze_business(self):
        """Generate comprehensive business analysis"""
        inventory = self.get_inventory_summary()
        sales = self.get_sales_summary()
        suppliers = self.get_supplier_summary()
        top_products = self.get_top_products()
        alerts = self.get_low_stock_alerts()
        
        # Generate insights
        insights = []
        
        # Inventory insights
        if inventory['out_of_stock'] > 0:
            insights.append(f"⚠️ {inventory['out_of_stock']} products are out of stock! Restock urgently.")
        
        if inventory['low_stock'] > 0:
            insights.append(f"📦 {inventory['low_stock']} products have low stock (≤10 units).")
        
        # Sales insights
        if sales['today_revenue'] > 0:
            insights.append(f"💰 Today's revenue: ₹{sales['today_revenue']:.2f}")
        
        if sales['week_revenue'] > 0:
            insights.append(f"📈 Weekly revenue: ₹{sales['week_revenue']:.2f}")
        
        # Top products
        if top_products:
            top_names = ", ".join([p['name'] for p in top_products[:3]])
            insights.append(f"🏆 Top sellers: {top_names}")
        
        return {
            "inventory": inventory,
            "sales": sales,
            "suppliers": suppliers,
            "top_products": top_products,
            "alerts": alerts,
            "insights": insights,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def process_query(self, query, user_context=None):
        """Process user query and provide intelligent response"""
        query = query.lower().strip()
        
        # Inventory queries
        if any(word in query for word in ['inventory', 'stock', 'products', 'items']):
            inventory = self.get_inventory_summary()
            response = f"📊 **Inventory Summary:**\n\n"
            response += f"• Total Products: {inventory['total_products']}\n"
            response += f"• Total Value: ₹{inventory['total_value']}\n"
            response += f"• Low Stock Items: {inventory['low_stock']}\n"
            response += f"• Out of Stock: {inventory['out_of_stock']}\n"
            
            if inventory['low_stock'] > 0 or inventory['out_of_stock'] > 0:
                response += f"\n⚠️ **Action Needed:** Some products need attention!"
            
            return response
        
        # Sales queries
        elif any(word in query for word in ['sales', 'revenue', 'income', 'money']):
            sales = self.get_sales_summary()
            response = f"💰 **Sales Summary:**\n\n"
            response += f"• Total Orders: {sales['total_orders']}\n"
            response += f"• Today's Revenue: ₹{sales['today_revenue']:.2f}\n"
            response += f"• This Week's Revenue: ₹{sales['week_revenue']:.2f}\n"
            return response
        
        # Supplier queries
        elif any(word in query for word in ['supplier', 'vendor', 'vendor']):
            suppliers = self.get_supplier_summary()
            response = f"🚚 **Supplier Summary:**\n\n"
            response += f"• Total Suppliers: {suppliers['total_suppliers']}\n"
            return response
        
        # Top products
        elif any(word in query for word in ['top', 'best', 'popular', 'selling']):
            top = self.get_top_products()
            response = f"🏆 **Top Selling Products:**\n\n"
            for i, p in enumerate(top, 1):
                response += f"{i}. {p['name']} - {p['sold']} units sold\n"
            return response
        
        # Alerts/Warnings
        elif any(word in query for word in ['alert', 'warning', 'urgent', 'problem']):
            alerts = self.get_low_stock_alerts()
            if not alerts:
                return "✅ **No Alerts!** All products are well-stocked."
            
            response = f"⚠️ **Stock Alerts:**\n\n"
            for alert in alerts:
                emoji = "🔴" if alert['status'] == 'CRITICAL' else "🟡"
                response += f"{emoji} {alert['name']}: {alert['quantity']} units ({alert['status']})\n"
            return response
        
        # Analysis/Business insights
        elif any(word in query for word in ['analyze', 'insight', 'report', 'summary', 'overview']):
            analysis = self.analyze_business()
            response = f"📈 **Business Analysis:**\n\n"
            for insight in analysis['insights']:
                response += f"{insight}\n"
            return response
        
        # Help
        elif any(word in query for word in ['help', 'what can you do', 'commands']):
            return """🤖 **I can help you with:**

📊 **Inventory** - Stock levels, product counts
💰 **Sales** - Revenue, orders, trends  
🚚 **Suppliers** - Supplier information
🏆 **Top Products** - Best selling items
⚠️ **Alerts** - Low stock warnings
📈 **Analysis** - Complete business report

**Try asking:**
• "How's the inventory?"
• "Show me sales"
• "Any alerts?"
• "Analyze my business"
• "Top products"
"""
        
        # Default response
        return """🤔 I didn't understand that. 

**Try these commands:**
• "How's the inventory?"
• "Show me sales"  
• "Any alerts?"
• "Analyze my business"
• "Top products"
• "Help"

Or type anything about your grocery store and I'll try to help!"""
    
    def get_auto_insights(self):
        """Get automatic insights for dashboard"""
        analysis = self.analyze_business()
        
        # Format for display
        formatted_insights = []
        
        # Critical alerts
        if analysis['inventory']['out_of_stock'] > 0:
            formatted_insights.append({
                'type': 'danger',
                'icon': 'exclamation-triangle',
                'title': 'Out of Stock',
                'message': f"{analysis['inventory']['out_of_stock']} products need immediate restocking!"
            })
        
        # Low stock
        if analysis['inventory']['low_stock'] > 0:
            formatted_insights.append({
                'type': 'warning',
                'icon': 'box-seam',
                'title': 'Low Stock',
                'message': f"{analysis['inventory']['low_stock']} products running low"
            })
        
        # Sales performance
        if analysis['sales']['today_revenue'] > 0:
            formatted_insights.append({
                'type': 'success',
                'icon': 'graph-up-arrow',
                'title': 'Today\'s Sales',
                'message': f"₹{analysis['sales']['today_revenue']:.2f} revenue"
            })
        
        # Top product highlight
        if analysis['top_products']:
            formatted_insights.append({
                'type': 'info',
                'icon': 'star',
                'title': 'Top Seller',
                'message': f"{analysis['top_products'][0]['name']} ({analysis['top_products'][0]['sold']} sold)"
            })
        
        return formatted_insights


# Singleton instance
ai_assistant = GroceryAIAssistant()

