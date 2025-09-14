#!/usr/bin/env python3
"""
Risk Assessment Agent for Investment Analysis
Provides comprehensive portfolio and investment risk analysis
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import math
import time

from .base_agent import FinancialBaseAgent

logger = logging.getLogger(__name__)

class RiskAssessmentAgent(FinancialBaseAgent):
    """
    AI agent specialized in investment and portfolio risk assessment
    Provides risk metrics, stress testing, and portfolio optimization insights
    """
    
    def __init__(self, knowledge_store, financial_db):
        """Initialize Risk Assessment Agent"""
        super().__init__(knowledge_store, financial_db, "risk_assessment_agent")
        
        # Risk assessment configuration
        self.risk_thresholds = {
            'low': {'var_95': 0.05, 'beta': 0.7, 'concentration': 0.2},
            'moderate': {'var_95': 0.10, 'beta': 1.2, 'concentration': 0.35},
            'high': {'var_95': 0.20, 'beta': 1.8, 'concentration': 0.50}
        }
        
        self.sector_correlation_matrix = self._initialize_correlation_matrix()
        
        logger.info("Risk Assessment Agent initialized for portfolio analysis")
    
    def _initialize_correlation_matrix(self) -> Dict[str, Dict[str, float]]:
        """Initialize simplified sector correlation matrix for educational purposes"""
        return {
            'Technology': {'Technology': 1.0, 'Healthcare': 0.3, 'Financial Services': 0.4, 
                          'Consumer Discretionary': 0.6, 'Consumer Staples': 0.1, 'Energy': 0.2},
            'Healthcare': {'Technology': 0.3, 'Healthcare': 1.0, 'Financial Services': 0.2,
                          'Consumer Discretionary': 0.3, 'Consumer Staples': 0.4, 'Energy': 0.1},
            'Financial Services': {'Technology': 0.4, 'Healthcare': 0.2, 'Financial Services': 1.0,
                                  'Consumer Discretionary': 0.5, 'Consumer Staples': 0.3, 'Energy': 0.6},
            'Consumer Discretionary': {'Technology': 0.6, 'Healthcare': 0.3, 'Financial Services': 0.5,
                                     'Consumer Discretionary': 1.0, 'Consumer Staples': 0.4, 'Energy': 0.3},
            'Consumer Staples': {'Technology': 0.1, 'Healthcare': 0.4, 'Financial Services': 0.3,
                               'Consumer Discretionary': 0.4, 'Consumer Staples': 1.0, 'Energy': 0.2},
            'Energy': {'Technology': 0.2, 'Healthcare': 0.1, 'Financial Services': 0.6,
                      'Consumer Discretionary': 0.3, 'Consumer Staples': 0.2, 'Energy': 1.0}
        }
    
    def assess_investment_risk(self, ticker: str, research_data: Dict,
                             client_risk_profile: str = 'moderate') -> Dict[str, Any]:
        """
        Assess risk for a specific investment
        
        Args:
            ticker: Stock ticker symbol
            research_data: Investment research analysis data
            client_risk_profile: Client's risk tolerance (conservative/moderate/aggressive)
        
        Returns:
            Comprehensive risk assessment dictionary
        """
        start_time = time.time()
        
        try:
            # Get stock financial data
            stock_data = self.financial_db.get_stock_data(ticker)
            if not stock_data:
                raise ValueError(f"No financial data found for ticker {ticker}")
            
            # Calculate quantitative risk metrics
            quantitative_risks = self._calculate_quantitative_risks(stock_data)
            
            # Assess qualitative risk factors
            qualitative_risks = self._assess_qualitative_risks(research_data, ticker)
            
            # Generate AI-powered risk analysis
            ai_risk_analysis = self._generate_ai_risk_analysis(
                ticker, stock_data, research_data, client_risk_profile
            )
            
            # Calculate overall risk score
            risk_score = self._calculate_overall_risk_score(
                quantitative_risks, qualitative_risks, ai_risk_analysis
            )
            
            # Determine risk level and suitability
            risk_level = self._determine_risk_level(risk_score)
            suitability = self._assess_investment_suitability(
                {'risk_score': risk_score}, {'risk_tolerance': client_risk_profile}
            )
            
            # Compile comprehensive risk assessment
            risk_assessment = {
                'ticker': ticker.upper(),
                'risk_score': risk_score,
                'risk_level': risk_level,
                'quantitative_metrics': quantitative_risks,
                'qualitative_factors': qualitative_risks,
                'ai_analysis': ai_risk_analysis,
                'var_analysis': self._calculate_var_analysis(stock_data, quantitative_risks),
                'stress_tests': self._perform_stress_tests(stock_data),
                'correlation_analysis': self._analyze_correlations(ticker, stock_data),
                'suitability_assessment': suitability,
                'risk_mitigation': self._suggest_risk_mitigation(risk_score, qualitative_risks),
                'monitoring_recommendations': self._generate_monitoring_recommendations(qualitative_risks),
                'assessment_timestamp': datetime.now().isoformat()
            }
            
            # Log risk assessment
            processing_time = time.time() - start_time
            self._log_financial_interaction(
                advisor_id='system',  # System-generated risk assessment
                client_id='',
                interaction_type='risk_assessment',
                input_data={'ticker': ticker, 'risk_profile': client_risk_profile},
                output_data={'risk_score': risk_score, 'risk_level': risk_level},
                processing_time=processing_time
            )
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Failed to assess investment risk for {ticker}: {str(e)}")
            return {
                'ticker': ticker,
                'error': 'Risk assessment failed',
                'message': str(e),
                'risk_score': 5,  # Default medium risk
                'risk_level': 'unknown'
            }
    
    def _calculate_quantitative_risks(self, stock_data: Dict) -> Dict[str, Any]:
        """Calculate quantitative risk metrics from stock data"""
        try:
            metrics = {
                'beta': stock_data.get('beta', 1.0),
                'volatility_indicator': self._calculate_volatility_indicator(stock_data),
                'financial_leverage': stock_data.get('debt_to_equity', 0),
                'liquidity_risk': self._assess_liquidity_risk(stock_data),
                'valuation_risk': self._assess_valuation_risk(stock_data),
                'profitability_stability': self._assess_profitability_stability(stock_data)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate quantitative risks: {str(e)}")
            return {'beta': 1.0, 'error': str(e)}
    
    def _calculate_volatility_indicator(self, stock_data: Dict) -> float:
        """Calculate volatility indicator from available data"""
        try:
            # Use beta as proxy for volatility when historical data not available
            beta = stock_data.get('beta', 1.0)
            
            # Adjust based on sector volatility (simplified)
            sector = stock_data.get('sector', '').lower()
            sector_multipliers = {
                'technology': 1.3,
                'energy': 1.4,
                'financial': 1.2,
                'healthcare': 0.9,
                'utilities': 0.7,
                'consumer staples': 0.8
            }
            
            multiplier = 1.0
            for sector_key, mult in sector_multipliers.items():
                if sector_key in sector:
                    multiplier = mult
                    break
            
            return round(beta * multiplier, 2)
            
        except Exception as e:
            logger.error(f"Failed to calculate volatility indicator: {str(e)}")
            return 1.0
    
    def _assess_liquidity_risk(self, stock_data: Dict) -> str:
        """Assess liquidity risk based on market cap and trading volume"""
        try:
            market_cap = stock_data.get('market_cap', 0)
            latest_volume = stock_data.get('latest_volume', 0)
            
            # Simplified liquidity assessment
            if market_cap > 10000000000:  # > $10B market cap
                return 'Low'
            elif market_cap > 2000000000:  # > $2B market cap
                return 'Moderate'
            else:
                return 'High'
                
        except Exception as e:
            logger.error(f"Failed to assess liquidity risk: {str(e)}")
            return 'Moderate'
    
    def _assess_valuation_risk(self, stock_data: Dict) -> str:
        """Assess valuation risk based on financial ratios"""
        try:
            pe_ratio = stock_data.get('pe_ratio', 0)
            pb_ratio = stock_data.get('price_to_book', 0)
            
            # Simplified valuation risk assessment
            high_pe_threshold = 30
            high_pb_threshold = 5
            
            if pe_ratio and pe_ratio > high_pe_threshold:
                return 'High'
            elif pb_ratio and pb_ratio > high_pb_threshold:
                return 'High'
            elif pe_ratio and pe_ratio < 15:
                return 'Low'
            else:
                return 'Moderate'
                
        except Exception as e:
            logger.error(f"Failed to assess valuation risk: {str(e)}")
            return 'Moderate'
    
    def _assess_profitability_stability(self, stock_data: Dict) -> str:
        """Assess profitability stability"""
        try:
            profit_margin = stock_data.get('profit_margin', 0)
            roe = stock_data.get('roe', 0)
            
            if profit_margin and profit_margin > 0.15 and roe and roe > 0.15:
                return 'Stable'
            elif profit_margin and profit_margin > 0.05:
                return 'Moderate'
            else:
                return 'Unstable'
                
        except Exception as e:
            logger.error(f"Failed to assess profitability stability: {str(e)}")
            return 'Moderate'
    
    def _assess_qualitative_risks(self, research_data: Dict, ticker: str) -> List[Dict[str, Any]]:
        """Assess qualitative risk factors from research data"""
        try:
            risk_factors = []
            
            # Extract risk factors from research analysis
            if 'risk_factors' in research_data:
                for risk in research_data['risk_factors']:
                    risk_factors.append({
                        'category': 'Business Risk',
                        'description': risk,
                        'severity': 'Medium',  # Default
                        'likelihood': 'Medium'  # Default
                    })
            
            # Add common risk categories
            risk_factors.extend([
                {
                    'category': 'Market Risk',
                    'description': 'Exposure to overall market volatility and economic cycles',
                    'severity': 'Medium',
                    'likelihood': 'High'
                },
                {
                    'category': 'Sector Risk',
                    'description': 'Risks specific to the company\'s industry sector',
                    'severity': 'Medium',
                    'likelihood': 'Medium'
                },
                {
                    'category': 'Company-Specific Risk',
                    'description': 'Risks unique to the individual company\'s operations',
                    'severity': 'Medium',
                    'likelihood': 'Medium'
                }
            ])
            
            return risk_factors[:8]  # Limit to top 8 risk factors
            
        except Exception as e:
            logger.error(f"Failed to assess qualitative risks: {str(e)}")
            return [{'category': 'Assessment Error', 'description': str(e)}]
    
    def _generate_ai_risk_analysis(self, ticker: str, stock_data: Dict,
                                 research_data: Dict, client_risk_profile: str) -> Dict[str, Any]:
        """Generate AI-powered risk analysis"""
        try:
            risk_prompt = self._create_financial_system_prompt(f"""
You are conducting a comprehensive risk analysis for investment in {ticker}.

Stock Data: {json.dumps(stock_data, indent=2)[:1000]}
Research Context: {json.dumps(research_data, indent=2)[:1000]}
Client Risk Profile: {client_risk_profile}

Provide detailed risk analysis covering:

1. PRIMARY RISK FACTORS
   - Top 3 most significant risks for this investment
   - Probability and potential impact of each risk

2. RISK CATEGORIZATION
   - Systematic vs. unsystematic risks
   - Controllable vs. uncontrollable factors
   - Short-term vs. long-term risk horizon

3. RISK SCENARIOS
   - Best case scenario and probability
   - Base case scenario and probability  
   - Worst case scenario and probability

4. RISK-RETURN ASSESSMENT
   - Is the expected return adequate for the risk level?
   - How does risk compare to similar investments?

5. RISK MANAGEMENT RECOMMENDATIONS
   - Position sizing suggestions
   - Hedging strategies if applicable
   - Monitoring requirements

Be specific and quantitative where possible. Provide actionable risk management insights.
""")
            
            ai_response = self._generate_financial_response(
                prompt=risk_prompt,
                financial_data=stock_data
            )
            
            # Structure AI response
            return {
                'comprehensive_analysis': ai_response,
                'primary_risks': self._extract_primary_risks(ai_response),
                'risk_scenarios': self._extract_risk_scenarios(ai_response),
                'management_recommendations': self._extract_risk_management_recommendations(ai_response)
            }
            
        except Exception as e:
            logger.error(f"Failed to generate AI risk analysis: {str(e)}")
            return {
                'comprehensive_analysis': 'AI risk analysis unavailable due to technical error',
                'primary_risks': [],
                'risk_scenarios': {},
                'management_recommendations': []
            }
    
    def _extract_primary_risks(self, analysis_text: str) -> List[str]:
        """Extract primary risks from AI analysis"""
        risks = []
        lines = analysis_text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['risk', 'threat', 'concern', 'challenge']):
                if len(line.strip()) > 20 and len(line.strip()) < 150:
                    risks.append(line.strip())
        
        return risks[:5]  # Top 5 primary risks
    
    def _extract_risk_scenarios(self, analysis_text: str) -> Dict[str, str]:
        """Extract risk scenarios from AI analysis"""
        scenarios = {
            'best_case': 'Analysis pending',
            'base_case': 'Analysis pending',
            'worst_case': 'Analysis pending'
        }
        
        text_lower = analysis_text.lower()
        
        # Simple extraction based on keywords
        if 'best case' in text_lower:
            scenarios['best_case'] = 'Positive market conditions and strong execution'
        if 'base case' in text_lower:
            scenarios['base_case'] = 'Normal market conditions and expected performance'
        if 'worst case' in text_lower:
            scenarios['worst_case'] = 'Adverse market conditions and execution challenges'
        
        return scenarios
    
    def _extract_risk_management_recommendations(self, analysis_text: str) -> List[str]:
        """Extract risk management recommendations from AI analysis"""
        recommendations = []
        
        # Default recommendations
        default_recs = [
            'Maintain position size within risk tolerance limits',
            'Monitor key financial metrics and market conditions',
            'Consider diversification to reduce concentration risk',
            'Set stop-loss levels based on risk parameters',
            'Review investment thesis regularly'
        ]
        
        return default_recs[:3]
    
    def _calculate_overall_risk_score(self, quantitative: Dict, qualitative: List,
                                    ai_analysis: Dict) -> int:
        """Calculate overall risk score (1-10 scale)"""
        try:
            score = 5  # Base score
            
            # Adjust for quantitative factors
            beta = quantitative.get('beta', 1.0)
            if beta > 1.5:
                score += 2
            elif beta > 1.2:
                score += 1
            elif beta < 0.8:
                score -= 1
            
            # Adjust for financial leverage
            debt_to_equity = quantitative.get('financial_leverage', 0)
            if debt_to_equity > 1.0:
                score += 1
            elif debt_to_equity > 0.5:
                score += 0.5
            
            # Adjust for qualitative factors
            high_risk_count = len([r for r in qualitative 
                                 if r.get('severity', '').lower() == 'high'])
            score += high_risk_count * 0.5
            
            # Ensure score is within bounds
            return max(1, min(10, int(score)))
            
        except Exception as e:
            logger.error(f"Failed to calculate overall risk score: {str(e)}")
            return 5
    
    def _determine_risk_level(self, risk_score: int) -> str:
        """Determine risk level based on score"""
        if risk_score <= 3:
            return 'Low'
        elif risk_score <= 6:
            return 'Moderate'
        elif risk_score <= 8:
            return 'High'
        else:
            return 'Very High'
    
    def _calculate_var_analysis(self, stock_data: Dict, quantitative_risks: Dict) -> Dict[str, Any]:
        """Calculate Value at Risk analysis"""
        try:
            # Simplified VaR calculation for educational purposes
            current_price = stock_data.get('latest_price', 100)
            volatility = quantitative_risks.get('volatility_indicator', 1.0)
            
            # Calculate 1-day VaR at 95% confidence level
            var_95_1day = current_price * 0.016 * volatility * 1.65  # 1.65 = 95% z-score
            
            # Calculate 10-day VaR
            var_95_10day = var_95_1day * math.sqrt(10)
            
            return {
                'var_95_1_day': round(var_95_1day, 2),
                'var_95_10_day': round(var_95_10day, 2),
                'var_95_1_day_percent': round((var_95_1day / current_price) * 100, 2),
                'confidence_level': '95%',
                'time_horizon': '1-10 days',
                'methodology': 'Parametric VaR (simplified)',
                'assumptions': 'Normal distribution, constant volatility'
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate VaR analysis: {str(e)}")
            return {'error': str(e)}
    
    def _perform_stress_tests(self, stock_data: Dict) -> Dict[str, Any]:
        """Perform stress testing scenarios"""
        try:
            current_price = stock_data.get('latest_price', 100)
            beta = stock_data.get('beta', 1.0)
            
            # Define stress scenarios
            scenarios = {
                'market_crash_20': {
                    'description': '20% market decline',
                    'market_impact': -20,
                    'stock_impact': -20 * beta,
                    'probability': 'Low (5-10%)'
                },
                'sector_decline_15': {
                    'description': '15% sector decline',
                    'market_impact': -5,
                    'stock_impact': -15,
                    'probability': 'Medium (15-25%)'
                },
                'interest_rate_shock': {
                    'description': 'Interest rates rise 2%',
                    'market_impact': -10,
                    'stock_impact': -10 * min(beta, 1.5),
                    'probability': 'Medium (20-30%)'
                },
                'recession_scenario': {
                    'description': 'Economic recession',
                    'market_impact': -30,
                    'stock_impact': -30 * beta,
                    'probability': 'Low (10-15%)'
                }
            }
            
            # Calculate price impacts
            for scenario_name, scenario in scenarios.items():
                impact_price = current_price * (1 + scenario['stock_impact'] / 100)
                scenario['projected_price'] = round(impact_price, 2)
                scenario['dollar_loss'] = round(current_price - impact_price, 2)
            
            return {
                'scenarios': scenarios,
                'current_price': current_price,
                'methodology': 'Scenario-based stress testing',
                'assumptions': 'Historical correlation patterns hold'
            }
            
        except Exception as e:
            logger.error(f"Failed to perform stress tests: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_correlations(self, ticker: str, stock_data: Dict) -> Dict[str, Any]:
        """Analyze correlations with market and sectors"""
        try:
            sector = stock_data.get('sector', 'Unknown')
            beta = stock_data.get('beta', 1.0)
            
            # Get sector correlations from simplified matrix
            sector_correlations = self.sector_correlation_matrix.get(sector, {})
            
            return {
                'market_correlation': beta,
                'sector': sector,
                'sector_correlations': sector_correlations,
                'diversification_benefit': 'High' if beta < 0.8 else 'Moderate' if beta < 1.2 else 'Low',
                'correlation_analysis': f'Beta of {beta} indicates {"low" if beta < 0.8 else "moderate" if beta < 1.2 else "high"} correlation with market movements'
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze correlations: {str(e)}")
            return {'error': str(e)}
    
    def _suggest_risk_mitigation(self, risk_score: int, qualitative_risks: List) -> List[str]:
        """Suggest risk mitigation strategies"""
        suggestions = []
        
        # Base suggestions based on risk score
        if risk_score >= 8:
            suggestions.extend([
                'Consider reducing position size due to high risk level',
                'Implement strict stop-loss orders',
                'Monitor investment closely with daily check-ins'
            ])
        elif risk_score >= 6:
            suggestions.extend([
                'Maintain moderate position sizing',
                'Set trailing stop-loss orders',
                'Review investment monthly'
            ])
        else:
            suggestions.extend([
                'Standard position sizing acceptable',
                'Monitor quarterly earnings and key metrics',
                'Review investment quarterly'
            ])
        
        # Add specific suggestions based on qualitative risks
        risk_categories = [risk.get('category', '') for risk in qualitative_risks]
        
        if 'Market Risk' in risk_categories:
            suggestions.append('Consider hedging against market downturns')
        
        if 'Sector Risk' in risk_categories:
            suggestions.append('Diversify across multiple sectors')
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _generate_monitoring_recommendations(self, qualitative_risks: List) -> List[str]:
        """Generate monitoring recommendations based on risks"""
        return [
            'Track quarterly earnings reports and guidance',
            'Monitor sector performance and trends',
            'Watch for changes in market sentiment',
            'Review analyst upgrades/downgrades',
            'Track key business metrics and KPIs'
        ]
    
    def analyze_portfolio(self, client_id: str, holdings: List[Dict],
                         market_context: Dict = None) -> Dict[str, Any]:
        """Analyze portfolio risk and provide optimization insights"""
        start_time = time.time()
        
        try:
            if not holdings:
                raise ValueError("Portfolio holdings are required")
            
            # Calculate portfolio metrics
            portfolio_metrics = self._calculate_portfolio_risk_metrics(holdings)
            
            # Analyze diversification
            diversification_analysis = self._analyze_portfolio_diversification(holdings)
            
            # Perform correlation analysis
            correlation_analysis = self._analyze_portfolio_correlations(holdings)
            
            # Calculate Value at Risk for portfolio
            portfolio_var = self._calculate_portfolio_var(holdings)
            
            # Generate AI-powered portfolio insights
            ai_insights = self._generate_portfolio_ai_insights(
                holdings, portfolio_metrics, diversification_analysis
            )
            
            # Provide optimization recommendations
            optimization_recommendations = self._generate_optimization_recommendations(
                holdings, portfolio_metrics, diversification_analysis
            )
            
            # Calculate overall portfolio health score
            health_score = self._calculate_portfolio_health_score(
                portfolio_metrics, diversification_analysis
            )
            
            # Compile comprehensive portfolio analysis
            portfolio_analysis = {
                'client_id': client_id,
                'total_holdings': len(holdings),
                'total_value': sum([holding.get('value', 0) for holding in holdings]),
                'health_score': health_score,
                'risk_metrics': portfolio_metrics,
                'diversification': diversification_analysis,
                'correlation_analysis': correlation_analysis,
                'var_analysis': portfolio_var,
                'ai_insights': ai_insights,
                'optimization_recommendations': optimization_recommendations,
                'action_items': self._generate_action_items(portfolio_metrics, diversification_analysis),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            # Log portfolio analysis
            processing_time = time.time() - start_time
            self._log_financial_interaction(
                advisor_id='system',
                client_id=client_id,
                interaction_type='portfolio_analysis',
                input_data={'holdings_count': len(holdings)},
                output_data={'health_score': health_score, 'total_value': portfolio_analysis['total_value']},
                processing_time=processing_time
            )
            
            return portfolio_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze portfolio for client {client_id}: {str(e)}")
            return {
                'client_id': client_id,
                'error': 'Portfolio analysis failed',
                'message': str(e)
            }
    
    def _calculate_portfolio_risk_metrics(self, holdings: List[Dict]) -> Dict[str, Any]:
        """Calculate comprehensive portfolio risk metrics"""
        try:
            total_value = sum([holding.get('value', 0) for holding in holdings])
            if total_value == 0:
                raise ValueError("Portfolio has no value")
            
            # Calculate weighted metrics
            weighted_beta = 0
            weighted_pe_ratio = 0
            weighted_debt_equity = 0
            
            for holding in holdings:
                weight = holding.get('value', 0) / total_value
                weighted_beta += weight * holding.get('beta', 1.0)
                weighted_pe_ratio += weight * holding.get('pe_ratio', 20)
                weighted_debt_equity += weight * holding.get('debt_to_equity', 0.5)
            
            # Calculate concentration risk
            largest_position = max([holding.get('value', 0) for holding in holdings])
            concentration_ratio = largest_position / total_value
            
            return {
                'portfolio_beta': round(weighted_beta, 3),
                'weighted_pe_ratio': round(weighted_pe_ratio, 2),
                'weighted_debt_equity': round(weighted_debt_equity, 2),
                'concentration_ratio': round(concentration_ratio, 3),
                'number_of_positions': len(holdings),
                'average_position_size': round(total_value / len(holdings), 2),
                'risk_concentration': 'High' if concentration_ratio > 0.3 else 'Moderate' if concentration_ratio > 0.15 else 'Low'
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio risk metrics: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_portfolio_diversification(self, holdings: List[Dict]) -> Dict[str, Any]:
        """Analyze portfolio diversification across sectors and other dimensions"""
        try:
            # Sector analysis
            sector_allocation = {}
            total_value = sum([holding.get('value', 0) for holding in holdings])
            
            for holding in holdings:
                sector = holding.get('sector', 'Unknown')
                value = holding.get('value', 0)
                sector_allocation[sector] = sector_allocation.get(sector, 0) + value
            
            # Convert to percentages
            sector_percentages = {
                sector: round((value / total_value) * 100, 2) 
                for sector, value in sector_allocation.items()
            }
            
            # Calculate diversification score
            num_sectors = len(sector_allocation)
            largest_sector_allocation = max(sector_percentages.values()) if sector_percentages else 0
            
            diversification_score = self._calculate_diversification_score(
                num_sectors, largest_sector_allocation
            )
            
            return {
                'sector_allocation': sector_percentages,
                'number_of_sectors': num_sectors,
                'largest_sector_allocation': largest_sector_allocation,
                'diversification_score': diversification_score,
                'diversification_level': self._get_diversification_level(diversification_score),
                'recommendations': self._get_diversification_recommendations(sector_percentages)
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze portfolio diversification: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_diversification_score(self, num_sectors: int, largest_allocation: float) -> int:
        """Calculate diversification score (1-10)"""
        try:
            score = 5  # Base score
            
            # Adjust for number of sectors
            if num_sectors >= 8:
                score += 2
            elif num_sectors >= 5:
                score += 1
            elif num_sectors <= 2:
                score -= 2
            
            # Adjust for concentration
            if largest_allocation > 50:
                score -= 3
            elif largest_allocation > 30:
                score -= 2
            elif largest_allocation > 20:
                score -= 1
            elif largest_allocation < 15:
                score += 1
            
            return max(1, min(10, score))
            
        except Exception as e:
            logger.error(f"Failed to calculate diversification score: {str(e)}")
            return 5
    
    def _get_diversification_level(self, score: int) -> str:
        """Get diversification level description"""
        if score >= 8:
            return 'Excellent'
        elif score >= 6:
            return 'Good'
        elif score >= 4:
            return 'Fair'
        else:
            return 'Poor'
    
    def _get_diversification_recommendations(self, sector_allocations: Dict[str, float]) -> List[str]:
        """Generate diversification recommendations"""
        recommendations = []
        
        # Check for over-concentration
        for sector, allocation in sector_allocations.items():
            if allocation > 40:
                recommendations.append(f'Consider reducing {sector} allocation (currently {allocation}%)')
        
        # Check for missing major sectors
        major_sectors = ['Technology', 'Healthcare', 'Financial Services', 'Consumer Discretionary']
        present_sectors = list(sector_allocations.keys())
        
        for sector in major_sectors:
            if sector not in present_sectors:
                recommendations.append(f'Consider adding exposure to {sector} sector')
        
        return recommendations[:3]  # Limit to 3 recommendations
    
    def _analyze_portfolio_correlations(self, holdings: List[Dict]) -> Dict[str, Any]:
        """Analyze correlations within portfolio"""
        try:
            # Simplified correlation analysis using sector correlations
            total_correlation_risk = 0
            pair_count = 0
            
            for i, holding1 in enumerate(holdings):
                for j, holding2 in enumerate(holdings[i+1:], i+1):
                    sector1 = holding1.get('sector', 'Unknown')
                    sector2 = holding2.get('sector', 'Unknown')
                    
                    correlation = self.sector_correlation_matrix.get(sector1, {}).get(sector2, 0.3)
                    weight1 = holding1.get('value', 0) / sum(h.get('value', 0) for h in holdings)
                    weight2 = holding2.get('value', 0) / sum(h.get('value', 0) for h in holdings)
                    
                    weighted_correlation = correlation * weight1 * weight2
                    total_correlation_risk += weighted_correlation
                    pair_count += 1
            
            avg_correlation = total_correlation_risk / max(pair_count, 1)
            
            return {
                'average_correlation': round(avg_correlation, 3),
                'correlation_risk': 'High' if avg_correlation > 0.6 else 'Moderate' if avg_correlation > 0.3 else 'Low',
                'analysis': f'Average portfolio correlation of {avg_correlation:.3f} indicates {"high" if avg_correlation > 0.6 else "moderate" if avg_correlation > 0.3 else "low"} interconnectedness'
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze portfolio correlations: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_portfolio_var(self, holdings: List[Dict]) -> Dict[str, Any]:
        """Calculate portfolio Value at Risk"""
        try:
            total_value = sum([holding.get('value', 0) for holding in holdings])
            portfolio_beta = self._calculate_portfolio_beta(holdings)
            
            # Simplified portfolio VaR calculation
            daily_var_95 = total_value * 0.016 * portfolio_beta * 1.65
            
            return {
                'portfolio_var_95_1day': round(daily_var_95, 2),
                'portfolio_var_95_1day_percent': round((daily_var_95 / total_value) * 100, 2),
                'portfolio_value': total_value,
                'methodology': 'Simplified parametric VaR'
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio VaR: {str(e)}")
            return {'error': str(e)}
    
    def _generate_portfolio_ai_insights(self, holdings: List[Dict], 
                                      metrics: Dict, diversification: Dict) -> Dict[str, Any]:
        """Generate AI insights for portfolio"""
        try:
            portfolio_summary = {
                'total_positions': len(holdings),
                'portfolio_beta': metrics.get('portfolio_beta', 1.0),
                'concentration_ratio': metrics.get('concentration_ratio', 0.2),
                'diversification_score': diversification.get('diversification_score', 5)
            }
            
            insight_prompt = self._create_financial_system_prompt(f"""
Analyze this portfolio and provide insights:

Portfolio Summary: {json.dumps(portfolio_summary, indent=2)}
Sector Allocation: {json.dumps(diversification.get('sector_allocation', {}), indent=2)}

Provide analysis covering:
1. Overall portfolio risk assessment
2. Key strengths and weaknesses
3. Risk-adjusted return potential
4. Rebalancing priorities
5. Strategic recommendations

Be specific and actionable in your recommendations.
""")
            
            ai_response = self._generate_financial_response(
                prompt=insight_prompt,
                financial_data=portfolio_summary
            )
            
            return {
                'comprehensive_analysis': ai_response,
                'key_insights': self._extract_key_insights(ai_response),
                'strategic_recommendations': self._extract_strategic_recommendations(ai_response)
            }
            
        except Exception as e:
            logger.error(f"Failed to generate portfolio AI insights: {str(e)}")
            return {'error': str(e)}
    
    def _extract_key_insights(self, analysis_text: str) -> List[str]:
        """Extract key insights from AI analysis"""
        insights = []
        lines = analysis_text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['strength', 'weakness', 'opportunity', 'risk']):
                if len(line.strip()) > 20:
                    insights.append(line.strip())
        
        return insights[:5]
    
    def _extract_strategic_recommendations(self, analysis_text: str) -> List[str]:
        """Extract strategic recommendations from AI analysis"""
        recommendations = []
        lines = analysis_text.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'consider', 'should']):
                if len(line.strip()) > 20:
                    recommendations.append(line.strip())
        
        return recommendations[:4]
    
    def _generate_optimization_recommendations(self, holdings: List[Dict],
                                            metrics: Dict, diversification: Dict) -> List[str]:
        """Generate portfolio optimization recommendations"""
        recommendations = []
        
        # Check concentration risk
        concentration_ratio = metrics.get('concentration_ratio', 0)
        if concentration_ratio > 0.3:
            recommendations.append('Reduce concentration risk by limiting individual positions to <20% of portfolio')
        
        # Check diversification
        diversification_score = diversification.get('diversification_score', 5)
        if diversification_score < 5:
            recommendations.append('Improve diversification by adding positions in underrepresented sectors')
        
        # Check portfolio beta
        portfolio_beta = metrics.get('portfolio_beta', 1.0)
        if portfolio_beta > 1.3:
            recommendations.append('Consider adding defensive positions to reduce portfolio beta')
        elif portfolio_beta < 0.7:
            recommendations.append('Portfolio may be too conservative - consider adding growth positions')
        
        # General recommendations
        recommendations.extend([
            'Rebalance portfolio quarterly to maintain target allocations',
            'Monitor correlation changes during market stress periods'
        ])
        
        return recommendations[:5]
    
    def _calculate_portfolio_health_score(self, metrics: Dict, diversification: Dict) -> int:
        """Calculate overall portfolio health score (1-100)"""
        try:
            score = 60  # Base score
            
            # Diversification component (30 points)
            div_score = diversification.get('diversification_score', 5)
            score += (div_score - 5) * 3
            
            # Concentration risk component (20 points)
            concentration = metrics.get('concentration_ratio', 0.2)
            if concentration < 0.15:
                score += 10
            elif concentration < 0.25:
                score += 5
            elif concentration > 0.4:
                score -= 15
            elif concentration > 0.3:
                score -= 10
            
            # Risk-adjusted returns component (20 points)
            portfolio_beta = metrics.get('portfolio_beta', 1.0)
            if 0.8 <= portfolio_beta <= 1.2:
                score += 10
            elif 0.6 <= portfolio_beta <= 1.4:
                score += 5
            else:
                score -= 5
            
            return max(1, min(100, score))
            
        except Exception as e:
            logger.error(f"Failed to calculate portfolio health score: {str(e)}")
            return 50
    
    def _generate_action_items(self, metrics: Dict, diversification: Dict) -> List[str]:
        """Generate specific action items for portfolio improvement"""
        action_items = []
        
        # Priority actions based on analysis
        concentration_ratio = metrics.get('concentration_ratio', 0)
        if concentration_ratio > 0.3:
            action_items.append('PRIORITY: Reduce largest position to under 20% of portfolio')
        
        diversification_score = diversification.get('diversification_score', 5)
        if diversification_score < 4:
            action_items.append('PRIORITY: Add positions in at least 2 additional sectors')
        
        # Standard maintenance actions
        action_items.extend([
            'Review and rebalance portfolio quarterly',
            'Monitor sector allocations monthly',
            'Assess correlation changes during market volatility'
        ])
        
        return action_items[:5]