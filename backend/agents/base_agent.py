#!/usr/bin/env python3
"""
Financial Base Agent Class for Investment Analysis System
Provides common functionality for all specialized financial AI agents
"""

import google.generativeai as genai
import os
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
import math

logger = logging.getLogger(__name__)

class FinancialBaseAgent:
    """
    Base class for all financial AI agents in the investment research platform
    Provides common functionality including Gemini API integration,
    financial data processing, compliance logging, and response formatting
    """
    
    def __init__(self, knowledge_store, financial_db, agent_type: str = "financial_base"):
        """Initialize base financial agent with required dependencies"""
        self.knowledge_store = knowledge_store
        self.financial_db = financial_db
        self.agent_type = agent_type
        
        # Initialize Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Financial analysis constants
        self.RISK_FREE_RATE = 0.045  # Current risk-free rate (4.5%)
        self.MARKET_RETURN = 0.10    # Expected market return (10%)
        
        logger.info(f"{agent_type.title()} financial agent initialized successfully")
    
    def _create_financial_system_prompt(self, specific_instructions: str) -> str:
        """Create system prompt with financial analysis guidelines"""
        base_prompt = """
You are a professional financial AI assistant specializing in investment research and analysis.

IMPORTANT FINANCIAL GUIDELINES:
- You are NOT a replacement for professional financial advice
- Always include appropriate risk disclosures and disclaimers
- Base recommendations on data analysis and established financial principles
- Consider client suitability and risk tolerance in all recommendations
- Maintain objectivity and avoid conflicts of interest
- Use only factual, verifiable financial data in analysis
- Always disclose the limitations of your analysis

REGULATORY COMPLIANCE:
- All recommendations must be suitable for the client's risk profile
- Include required disclosures for investment advice
- Maintain detailed audit trails of all investment recommendations
- Follow SOC2 security standards for client data protection
- Ensure FINRA, SEC, and other regulatory compliance

FINANCIAL ANALYSIS STANDARDS:
- Use established financial metrics and ratios
- Consider both quantitative and qualitative factors
- Analyze risk-adjusted returns, not just absolute returns
- Account for market conditions, economic indicators, and sector trends
- Provide transparent reasoning for all investment conclusions
- Include stress testing and scenario analysis where appropriate

DATA SOURCES AND ACCURACY:
- Cite all data sources used in analysis
- Verify data accuracy and timeliness
- Use multiple data points to corroborate findings
- Acknowledge data limitations and uncertainties
- Update analysis based on new information

"""
        return base_prompt + "\n" + specific_instructions
    
    def _generate_financial_response(self, prompt: str, client_context: Dict = None, 
                                   financial_data: Dict = None) -> str:
        """Generate response using Gemini API with financial context"""
        try:
            # Include client context for personalized advice
            if client_context:
                context_str = f"\nCLIENT CONTEXT:\n{json.dumps(client_context, indent=2)}\n"
                prompt = context_str + prompt
            
            # Include relevant financial data
            if financial_data:
                data_str = f"\nFINANCIAL DATA:\n{json.dumps(financial_data, indent=2)}\n"
                prompt = prompt + data_str
            
            # Add regulatory disclaimer
            disclaimer = "\n\nIMPORTANT: This analysis is for informational purposes only and should not be considered as personalized investment advice. Please consult with a qualified financial advisor before making investment decisions.\n"
            prompt = prompt + disclaimer
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Empty response from Gemini API")
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate financial AI response: {str(e)}")
            return self._get_financial_fallback_response()
    
    def _get_financial_fallback_response(self) -> str:
        """Provide fallback response when AI generation fails"""
        return ("I apologize, but I'm experiencing technical difficulties with the financial analysis system. "
                "Please consult with a qualified financial advisor for investment guidance. "
                "For urgent matters, please contact your advisor directly.")
    
    def _extract_financial_metrics(self, text: str, ticker: str = None) -> Dict:
        """Extract structured financial metrics from AI response"""
        try:
            extraction_prompt = f"""
Extract financial metrics from the following analysis and return as JSON:
Text: {text}
Ticker: {ticker}

Extract:
- current_price: current stock price if mentioned
- pe_ratio: price-to-earnings ratio
- market_cap: market capitalization
- dividend_yield: dividend yield percentage
- revenue_growth: revenue growth rate
- profit_margin: profit margin percentage
- debt_to_equity: debt-to-equity ratio
- beta: stock beta (market risk measure)
- analyst_rating: buy/hold/sell consensus
- target_price: analyst target price
- risk_score: overall risk score (1-10)
- confidence_level: confidence in analysis (1-10)

Return only valid JSON with numerical values where applicable:
"""
            
            response = self.model.generate_content(extraction_prompt)
            
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return self._manual_parse_financial_metrics(text, ticker)
                
        except Exception as e:
            logger.error(f"Failed to extract financial metrics: {str(e)}")
            return self._get_default_financial_metrics()
    
    def _manual_parse_financial_metrics(self, text: str, ticker: str = None) -> Dict:
        """Manual parsing fallback for financial metrics extraction"""
        metrics = {
            'current_price': None,
            'pe_ratio': None,
            'market_cap': None,
            'dividend_yield': None,
            'revenue_growth': None,
            'profit_margin': None,
            'debt_to_equity': None,
            'beta': None,
            'analyst_rating': 'hold',
            'target_price': None,
            'risk_score': 5,
            'confidence_level': 5
        }
        
        # Basic text parsing for common financial terms
        text_lower = text.lower()
        
        # Look for P/E ratio
        if 'p/e' in text_lower or 'pe ratio' in text_lower:
            # Extract number following P/E mentions
            import re
            pe_match = re.search(r'p/e.*?(\d+\.?\d*)', text_lower)
            if pe_match:
                try:
                    metrics['pe_ratio'] = float(pe_match.group(1))
                except ValueError:
                    pass
        
        # Look for dividend yield
        if 'dividend' in text_lower and '%' in text:
            dividend_match = re.search(r'(\d+\.?\d*)%', text)
            if dividend_match:
                try:
                    metrics['dividend_yield'] = float(dividend_match.group(1))
                except ValueError:
                    pass
        
        # Determine basic risk assessment from text sentiment
        high_risk_terms = ['volatile', 'risky', 'speculative', 'uncertain', 'declining']
        low_risk_terms = ['stable', 'consistent', 'reliable', 'blue chip', 'defensive']
        
        risk_indicators = 0
        for term in high_risk_terms:
            if term in text_lower:
                risk_indicators += 1
        for term in low_risk_terms:
            if term in text_lower:
                risk_indicators -= 1
        
        metrics['risk_score'] = max(1, min(10, 5 + risk_indicators))
        
        return metrics
    
    def _get_default_financial_metrics(self) -> Dict:
        """Return default financial metrics when extraction fails"""
        return {
            'current_price': None,
            'pe_ratio': None,
            'market_cap': None,
            'dividend_yield': None,
            'revenue_growth': None,
            'profit_margin': None,
            'debt_to_equity': None,
            'beta': 1.0,  # Market average
            'analyst_rating': 'hold',
            'target_price': None,
            'risk_score': 5,  # Medium risk
            'confidence_level': 3  # Low confidence due to lack of data
        }
    
    def _calculate_sharpe_ratio(self, returns: List[float], risk_free_rate: float = None) -> float:
        """Calculate Sharpe ratio for risk-adjusted return analysis"""
        try:
            if not returns or len(returns) < 2:
                return 0.0
            
            if risk_free_rate is None:
                risk_free_rate = self.RISK_FREE_RATE
            
            # Calculate mean return and standard deviation
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
            std_deviation = math.sqrt(variance)
            
            if std_deviation == 0:
                return 0.0
            
            # Sharpe ratio = (Mean return - Risk-free rate) / Standard deviation
            sharpe_ratio = (mean_return - risk_free_rate) / std_deviation
            return round(sharpe_ratio, 3)
            
        except Exception as e:
            logger.error(f"Failed to calculate Sharpe ratio: {str(e)}")
            return 0.0
    
    def _calculate_portfolio_beta(self, holdings: List[Dict], market_data: Dict = None) -> float:
        """Calculate portfolio beta (systematic risk measure)"""
        try:
            if not holdings:
                return 1.0
            
            total_value = sum(holding.get('value', 0) for holding in holdings)
            if total_value == 0:
                return 1.0
            
            weighted_beta = 0.0
            for holding in holdings:
                weight = holding.get('value', 0) / total_value
                beta = holding.get('beta', 1.0)  # Default to market beta
                weighted_beta += weight * beta
            
            return round(weighted_beta, 3)
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio beta: {str(e)}")
            return 1.0
    
    def _assess_investment_suitability(self, investment_data: Dict, client_profile: Dict) -> Dict:
        """Assess if investment is suitable for client profile"""
        try:
            risk_score = investment_data.get('risk_score', 5)
            client_risk_tolerance = client_profile.get('risk_tolerance', 'moderate')
            
            # Map client risk tolerance to numeric scale
            risk_tolerance_map = {
                'conservative': 3,
                'moderate': 5,
                'aggressive': 8
            }
            
            client_risk_score = risk_tolerance_map.get(client_risk_tolerance, 5)
            
            # Investment is suitable if its risk is within client's tolerance
            suitable = risk_score <= client_risk_score + 1  # Allow slight tolerance
            
            # Generate suitability reasoning
            if suitable:
                reasoning = f"Investment risk level ({risk_score}/10) aligns with client's {client_risk_tolerance} risk profile."
            else:
                reasoning = f"Investment risk level ({risk_score}/10) exceeds client's {client_risk_tolerance} risk tolerance."
            
            # Check additional suitability factors
            warnings = []
            if investment_data.get('liquidity_risk', False):
                warnings.append("This investment may have limited liquidity")
            if investment_data.get('complexity_high', False):
                warnings.append("This is a complex investment product")
            
            return {
                'suitable': suitable,
                'suitability_score': min(client_risk_score, risk_score),
                'reasoning': reasoning,
                'warnings': warnings,
                'client_risk_tolerance': client_risk_tolerance,
                'investment_risk_level': risk_score
            }
            
        except Exception as e:
            logger.error(f"Failed to assess investment suitability: {str(e)}")
            return {
                'suitable': False,
                'reasoning': 'Unable to assess suitability due to insufficient data',
                'warnings': ['Suitability assessment failed - manual review required']
            }
    
    def _log_financial_interaction(self, advisor_id: str, client_id: str, 
                                 interaction_type: str, input_data: Dict, 
                                 output_data: Dict, compliance_status: Dict = None,
                                 processing_time: float = None):
        """Log financial agent interaction for SOC2 compliance and audit trail"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'agent_type': self.agent_type,
                'advisor_id': advisor_id,
                'client_id': client_id,
                'interaction_type': interaction_type,
                'processing_time_seconds': processing_time,
                'input_summary': {
                    'keys': list(input_data.keys()),
                    'ticker': input_data.get('ticker', ''),
                    'query_length': len(str(input_data.get('query', '')))
                },
                'output_summary': {
                    'keys': list(output_data.keys()),
                    'recommendation': output_data.get('recommendation', ''),
                    'risk_score': output_data.get('risk_score', 0),
                    'confidence_score': output_data.get('confidence_score', 0)
                },
                'compliance_status': compliance_status or {},
                'success': True
            }
            
            # Log to financial database audit system
            self.financial_db.log_financial_audit_event(
                advisor_id=advisor_id,
                client_id=client_id,
                action=f'{self.agent_type}_analysis',
                details=json.dumps(log_entry),
                compliance_data=compliance_status
            )
            
            # Log specific financial interactions
            if interaction_type == 'investment_analysis':
                self.financial_db.store_investment_recommendation_audit(
                    advisor_id=advisor_id,
                    client_id=client_id,
                    ticker=input_data.get('ticker', ''),
                    recommendation_data=output_data,
                    agent_reasoning=log_entry
                )
            
        except Exception as e:
            logger.error(f"Failed to log financial interaction: {str(e)}")
    
    def _format_financial_response(self, analysis_data: Dict, 
                                 additional_data: Dict = None) -> Dict[str, Any]:
        """Format financial analysis response with consistent structure"""
        base_response = {
            'analysis': analysis_data,
            'agent_type': self.agent_type,
            'timestamp': datetime.now().isoformat(),
            'analysis_id': self._create_analysis_id(),
            'confidence_score': analysis_data.get('confidence_score', 5),
            'risk_assessment_included': True,
            'regulatory_disclaimer': self._get_regulatory_disclaimer()
        }
        
        if additional_data:
            base_response.update(additional_data)
        
        return base_response
    
    def _create_analysis_id(self) -> str:
        """Generate unique analysis ID for tracking"""
        return f"{self.agent_type}_{uuid.uuid4().hex[:12]}_{int(datetime.now().timestamp())}"
    
    def _get_regulatory_disclaimer(self) -> str:
        """Standard regulatory disclaimer for investment analysis"""
        return ("This analysis is provided for informational purposes only and should not be "
                "construed as investment advice. Past performance does not guarantee future results. "
                "All investments carry risk of loss. Please consult with a qualified financial "
                "advisor before making investment decisions. This analysis was generated by AI "
                "and should be reviewed by a licensed professional.")
    
    def _validate_financial_input(self, required_fields: List[str], data: Dict) -> tuple[bool, List[str]]:
        """Validate financial analysis input data"""
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        # Additional financial data validation
        financial_validations = []
        
        if 'ticker' in data:
            ticker = data['ticker'].upper()
            if not ticker.isalpha() or len(ticker) > 5:
                financial_validations.append("Invalid ticker symbol format")
        
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    financial_validations.append("Investment amount must be positive")
            except (ValueError, TypeError):
                financial_validations.append("Invalid investment amount")
        
        if 'risk_tolerance' in data:
            valid_risk_levels = ['conservative', 'moderate', 'aggressive']
            if data['risk_tolerance'].lower() not in valid_risk_levels:
                financial_validations.append("Invalid risk tolerance level")
        
        all_validation_errors = missing_fields + financial_validations
        
        if all_validation_errors:
            logger.error(f"Financial input validation failed: {all_validation_errors}")
            return False, all_validation_errors
        
        return True, []
    
    def health_check(self) -> bool:
        """Check if financial agent is functioning properly"""
        try:
            # Test AI model
            test_response = self.model.generate_content("Test financial analysis system")
            
            # Test database connections
            if hasattr(self.knowledge_store, 'health_check'):
                if not self.knowledge_store.health_check():
                    return False
            
            if hasattr(self.financial_db, 'health_check'):
                if not self.financial_db.health_check():
                    return False
            
            # Test basic financial calculation
            test_sharpe = self._calculate_sharpe_ratio([0.08, 0.12, 0.06, 0.10])
            if test_sharpe == 0:
                logger.warning("Financial calculation test produced unexpected result")
            
            return True
            
        except Exception as e:
            logger.error(f"Financial agent health check failed: {str(e)}")
            return False
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this financial agent"""
        return {
            'agent_type': self.agent_type,
            'model': 'gemini-pro',
            'initialized_at': datetime.now().isoformat(),
            'capabilities': [
                'investment_analysis', 
                'risk_assessment', 
                'financial_metrics_calculation',
                'suitability_analysis', 
                'regulatory_compliance'
            ],
            'regulatory_compliance': ['SOC2', 'FINRA', 'SEC'],
            'risk_free_rate': self.RISK_FREE_RATE,
            'expected_market_return': self.MARKET_RETURN,
            'status': 'active'
        }