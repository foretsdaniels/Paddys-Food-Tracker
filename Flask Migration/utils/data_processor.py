"""
Data processing utilities for the Restaurant Ingredient Tracker.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple


class DataProcessor:
    """Handles all data processing operations for ingredient tracking."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.required_columns = {
            'ingredient_info': ['Ingredient', 'Unit Cost'],
            'input_stock': ['Ingredient', 'Received Qty'],
            'usage': ['Ingredient', 'Used Qty'],
            'waste': ['Ingredient', 'Wasted Qty']
        }
    
    def validate_csv_structure(self, file_path: str, file_type: str) -> bool:
        """Validate that CSV has required columns."""
        try:
            df = pd.read_csv(file_path)
            required_cols = self.required_columns[file_type]
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                raise ValueError(f"Missing columns in {file_type}: {missing_cols}")
            
            return True
        except Exception as e:
            raise ValueError(f"Error validating {file_type}: {str(e)}")
    
    def process_files(self, file_paths: Dict[str, str]) -> pd.DataFrame:
        """Process uploaded CSV files and calculate metrics."""
        
        # Validate all files first
        for file_type, file_path in file_paths.items():
            self.validate_csv_structure(file_path, file_type)
        
        # Load data
        ingredient_info = pd.read_csv(file_paths['ingredient_info'])
        input_stock = pd.read_csv(file_paths['input_stock'])
        usage = pd.read_csv(file_paths['usage'])
        waste = pd.read_csv(file_paths['waste'])
        
        # Clean and standardize data
        for df in [ingredient_info, input_stock, usage, waste]:
            df['Ingredient'] = df['Ingredient'].str.strip().str.title()
        
        # Merge all data on ingredient
        merged = ingredient_info.copy()
        merged = merged.merge(input_stock, on='Ingredient', how='left')
        merged = merged.merge(usage, on='Ingredient', how='left')
        merged = merged.merge(waste, on='Ingredient', how='left')
        
        # Fill missing values with 0
        numeric_columns = ['Received Qty', 'Used Qty', 'Wasted Qty']
        for col in numeric_columns:
            merged[col] = pd.to_numeric(merged[col], errors='coerce').fillna(0)
        
        # Calculate metrics
        merged['Expected Use'] = merged['Used Qty'] + merged['Wasted Qty']
        merged['Shrinkage'] = merged['Received Qty'] - merged['Expected Use']
        
        # Calculate costs
        merged['Used Cost'] = merged['Used Qty'] * merged['Unit Cost']
        merged['Waste Cost'] = merged['Wasted Qty'] * merged['Unit Cost']
        merged['Shrinkage Cost'] = merged['Shrinkage'] * merged['Unit Cost']
        merged['Total Cost'] = merged['Used Cost'] + merged['Waste Cost'] + merged['Shrinkage Cost']
        
        # Calculate percentages
        merged['Waste %'] = (merged['Wasted Qty'] / merged['Received Qty'] * 100).fillna(0)
        merged['Shrinkage %'] = (merged['Shrinkage'] / merged['Received Qty'] * 100).fillna(0)
        
        # Round numerical columns
        numeric_cols = ['Unit Cost', 'Used Cost', 'Waste Cost', 'Shrinkage Cost', 'Total Cost']
        for col in numeric_cols:
            merged[col] = merged[col].round(2)
        
        percentage_cols = ['Waste %', 'Shrinkage %']
        for col in percentage_cols:
            merged[col] = merged[col].round(1)
        
        return merged
    
    def apply_filters(self, data: pd.DataFrame, filter_type: str) -> pd.DataFrame:
        """Apply filters to the data."""
        if filter_type == 'high_shrinkage':
            return data[data['Shrinkage Cost'] > 10]
        elif filter_type == 'high_waste':
            return data[data['Waste %'] > 5]
        elif filter_type == 'missing_stock':
            return data[data['Received Qty'] == 0]
        elif filter_type == 'negative_shrinkage':
            return data[data['Shrinkage'] < 0]
        else:
            return data
    
    def sort_results(self, data: pd.DataFrame, sort_by: str, order: str = 'desc') -> pd.DataFrame:
        """Sort results by specified column."""
        ascending = order == 'asc'
        return data.sort_values(by=sort_by, ascending=ascending)
    
    def calculate_summary_stats(self, data: pd.DataFrame) -> Dict:
        """Calculate summary statistics."""
        return {
            'total_ingredients': len(data),
            'total_cost': data['Total Cost'].sum(),
            'total_waste_cost': data['Waste Cost'].sum(),
            'total_shrinkage_cost': data['Shrinkage Cost'].sum(),
            'avg_waste_percentage': data['Waste %'].mean(),
            'avg_shrinkage_percentage': data['Shrinkage %'].mean(),
            'high_shrinkage_items': len(data[data['Shrinkage Cost'] > 10]),
            'missing_stock_items': len(data[data['Received Qty'] == 0])
        }
    
    def get_alerts(self, data: pd.DataFrame) -> List[Dict]:
        """Generate alerts for problematic items."""
        alerts = []
        
        # High shrinkage alerts
        high_shrinkage = data[data['Shrinkage Cost'] > 50]
        for _, item in high_shrinkage.iterrows():
            alerts.append({
                'type': 'high_shrinkage',
                'severity': 'critical',
                'message': f"Critical shrinkage: {item['Ingredient']} has ${item['Shrinkage Cost']:.2f} in missing inventory",
                'ingredient': item['Ingredient'],
                'value': item['Shrinkage Cost']
            })
        
        # High waste alerts
        high_waste = data[data['Waste %'] > 15]
        for _, item in high_waste.iterrows():
            alerts.append({
                'type': 'high_waste',
                'severity': 'warning',
                'message': f"High waste: {item['Ingredient']} has {item['Waste %']:.1f}% waste rate",
                'ingredient': item['Ingredient'],
                'value': item['Waste %']
            })
        
        # Missing stock alerts
        missing_stock = data[data['Received Qty'] == 0]
        for _, item in missing_stock.iterrows():
            alerts.append({
                'type': 'missing_stock',
                'severity': 'warning',
                'message': f"No stock received for {item['Ingredient']} but usage/waste recorded",
                'ingredient': item['Ingredient'],
                'value': 0
            })
        
        return alerts
    
    def get_insights(self, data: pd.DataFrame) -> List[str]:
        """Generate insights from the data."""
        insights = []
        
        # Top cost contributors
        top_cost_items = data.nlargest(3, 'Total Cost')
        total_cost = data['Total Cost'].sum()
        
        for _, item in top_cost_items.iterrows():
            percentage = (item['Total Cost'] / total_cost) * 100
            insights.append(f"{item['Ingredient']} accounts for {percentage:.1f}% of total costs (${item['Total Cost']:.2f})")
        
        # Waste insights
        avg_waste = data['Waste %'].mean()
        if avg_waste > 10:
            insights.append(f"Average waste rate of {avg_waste:.1f}% is above recommended 10% threshold")
        
        # Shrinkage insights
        total_shrinkage = data['Shrinkage Cost'].sum()
        if total_shrinkage > 100:
            insights.append(f"Total shrinkage cost of ${total_shrinkage:.2f} indicates potential theft or inventory management issues")
        
        # Efficiency insights
        efficient_items = data[(data['Waste %'] < 5) & (data['Shrinkage %'].abs() < 5)]
        if len(efficient_items) > 0:
            insights.append(f"{len(efficient_items)} ingredients show excellent inventory management with low waste and shrinkage")
        
        return insights