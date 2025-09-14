#!/usr/bin/env python3
"""
Research Agent for Investment Analysis
Conducts comprehensive investment research using AI and financial data
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import time

from .base_agent import FinancialBaseAgent

logger = logging.getLogger(__name__)

class ResearchAgent(FinancialBaseAgent):
    """
    AI agent specialized in investment research and market analysis
    Provides comprehensive company analysis, market intelligence, and investment insights
    """
    
    def __init__(self, knowledge_store, financial_db):
        """Initialize Research Agent with financial data sources"""
        super().__init__(knowledge_store, financial_db, "research_agent")
        
        # Research-specific configuration
        self.analysis_depth_levels = {
            'quick': {'company_docs': 2, 'analyst_reports': 2, 'market_intel': 1},
            'standard': {'company_docs': 3, 'analyst_reports': 3, 'market_intel': 2},
            'comprehensive': {'company_docs': 5, 'analyst_reports': 4, 'market_intel': 3}
        }
        
        logger.info("Research Agent initialized for investment analysis")
    
    def conduct_investment_research(self, query: str, ticker: str = None, 
                                  analysis_type: str = 'comprehensive',
                                  client_context: Dict = None) -> Dict[str, Any]:
        """
        Conduct comprehensive investment research for a given query or ticker
        
        Args:
            query: Investment research question or focus area
            ticker: Stock ticker symbol (optional)
            analysis_type: Level of analysis depth (quick/standard/comprehensive)
            client_context: Client context for personalized analysis
        
        Returns:
            Dictionary containing comprehensive investment research results
        """
        start_time = time.time()
        
        try:
            # Validate input
            if not query and not ticker:
                raise ValueError("Either query or ticker must be provided")
            
            analysis_id = self._create_analysis_id()
            
            # Step 1: Retrieve relevant financial data
            financial_data = self._gather_financial_data(ticker, query)
            
            # Step 2: Search knowledge base for relevant research
            research_context = self._search_research_knowledge(query, ticker, analysis_type)
            
            # Step 3: Generate comprehensive AI analysis
            investment_analysis = self._generate_investment_analysis(
                query, ticker, financial_data, research_context, client_context
            )
            
            # Step 4: Extract and validate financial metrics
            financial_metrics = self._extract_financial_metrics(
                investment_analysis['raw_analysis'], ticker
            )
            
            # Step 5: Generate investment recommendation
            recommendation = self._generate_investment_recommendation(
                investment_analysis, financial_metrics, client_context
            )
            
            # Step 6: Compile comprehensive research results
            research_results = {
                'analysis_id': analysis_id,
                'ticker': ticker.upper() if ticker else None,
                'query': query,
                'company_info': financial_data.get('company_info', {}),
                'financial_metrics': financial_metrics,
                'market_analysis': investment_analysis.get('market_analysis', {}),
                'growth_analysis': investment_analysis.get('growth_prospects', {}),
                'competitive_analysis': investment_analysis.get('competitive_position', {}),
                'risk_factors': investment_analysis.get('risk_factors', []),
                'catalysts': investment_analysis.get('catalysts', []),
                'recommendation': recommendation,
                'confidence_score': self._calculate_confidence_score(
                    financial_data, research_context, investment_analysis
                ),
                'sources': research_context.get('sources', []),
                'research_depth': analysis_type,
                'generated_at': datetime.now().isoformat()
            }
            
            # Log research interaction
            processing_time = time.time() - start_time
            self._log_financial_interaction(
                advisor_id=client_context.get('advisor_id', '') if client_context else '',
                client_id=client_context.get('client_id', '') if client_context else '',
                interaction_type='investment_research',
                input_data={'query': query, 'ticker': ticker},
                output_data=research_results,
                processing_time=processing_time
            )
            
            return research_results
            
        except Exception as e:
            logger.error(f"Failed to conduct investment research: {str(e)}")
            return {
                'error': 'Investment research failed',
                'message': str(e),
                'analysis_id': self._create_analysis_id()
            }
    
    def _gather_financial_data(self, ticker: str, query: str) -> Dict[str, Any]:
        """Gather relevant financial data from database"""
        try:
            financial_data = {}
            
            if ticker:
                # Get stock fundamental data
                stock_data = self.financial_db.get_stock_data(ticker)
                if stock_data:
                    financial_data['company_info'] = {
                        'ticker': stock_data['ticker'],
                        'company_name': stock_data['company_name'],
                        'sector': stock_data['sector'],
                        'industry': stock_data['industry'],
                        'market_cap': stock_data['market_cap'],
                        'exchange': stock_data['exchange'],
                        'description': stock_data['description']
                    }
                    
                    financial_data['fundamental_metrics'] = {
                        'pe_ratio': stock_data['pe_ratio'],
                        'dividend_yield': stock_data['dividend_yield'],
                        'beta': stock_data['beta'],
                        'price_to_book': stock_data['price_to_book'],
                        'debt_to_equity': stock_data['debt_to_equity'],
                        'roe': stock_data['roe'],
                        'profit_margin': stock_data['profit_margin'],
                        'latest_price': stock_data.get('latest_price'),
                        'latest_volume': stock_data.get('latest_volume')
                    }
                    
                    financial_data['technical_indicators'] = {
                        'rsi': stock_data.get('rsi'),
                        'moving_avg_50': stock_data.get('moving_avg_50'),
                        'moving_avg_200': stock_data.get('moving_avg_200')
                    }
            
            # Get market overview for context
            market_overview = self.financial_db.get_market_overview()
            financial_data['market_context'] = market_overview
            
            return financial_data
            
        except Exception as e:
            logger.error(f"Failed to gather financial data: {str(e)}")
            return {}
    
    def _search_research_knowledge(self, query: str, ticker: str, analysis_type: str) -> Dict[str, Any]:
        """Search knowledge base for relevant research and analysis"""
        try:
            search_config = self.analysis_depth_levels.get(analysis_type, 
                                                         self.analysis_depth_levels['standard'])
            
            # Comprehensive search across knowledge base
            research_context = self.knowledge_store.comprehensive_search(
                query=query,
                context={'ticker': ticker} if ticker else {}
            )
            
            # Extract and organize sources
            sources = []
            total_relevance = 0
            
            for source_type, results in research_context.items():
                for result in results[:search_config.get(source_type.replace('_', ''), 2)]:
                    sources.append({
                        'type': source_type,
                        'id': result['id'],
                        'relevance_score': result['relevance_score'],
                        'metadata': result['metadata']
                    })
                    total_relevance += result['relevance_score']
            
            return {
                'research_data': research_context,
                'sources': sources,
                'total_sources': len(sources),
                'average_relevance': total_relevance / max(len(sources), 1),
                'search_depth': analysis_type
            }
            
        except Exception as e:
            logger.error(f"Failed to search research knowledge: {str(e)}")
            return {'research_data': {}, 'sources': []}
    
    def _generate_investment_analysis(self, query: str, ticker: str, 
                                    financial_data: Dict, research_context: Dict,
                                    client_context: Dict) -> Dict[str, Any]:
        """Generate comprehensive AI-powered investment analysis"""
        try:
            # Construct detailed analysis prompt
            analysis_prompt = self._create_financial_system_prompt(f"""
You are conducting comprehensive investment research for {'ticker symbol ' + ticker if ticker else 'investment query: ' + query}.

Based on the provided financial data and research context, provide a thorough investment analysis covering:

1. COMPANY OVERVIEW & BUSINESS MODEL
   - Core business operations and revenue streams
   - Competitive positioning and market share
   - Key business strengths and differentiators

2. FINANCIAL HEALTH ANALYSIS  
   - Revenue and earnings trends
   - Profitability and margin analysis
   - Balance sheet strength and debt levels
   - Cash flow generation and capital allocation

3. MARKET ANALYSIS
   - Industry trends and growth outlook
   - Market opportunities and challenges
   - Competitive landscape and threats
   - Economic factors affecting the business

4. GROWTH PROSPECTS
   - Near-term and long-term growth drivers
   - Market expansion opportunities
   - New product/service developments
   - Management execution capabilities

5. RISK ASSESSMENT
   - Business-specific risks
   - Industry and market risks
   - Financial and operational risks
   - Regulatory and external risks

6. INVESTMENT CATALYSTS
   - Positive factors that could drive stock performance
   - Upcoming events or developments
   - Potential re-rating opportunities

Provide specific, data-driven insights with quantitative analysis where possible.
Be objective and balanced in your assessment.
""")
            
            # Generate comprehensive analysis
            raw_analysis = self._generate_financial_response(
                prompt=analysis_prompt,
                client_context=client_context,
                financial_data=financial_data
            )
            
            # Structure the analysis into organized components
            structured_analysis = self._structure_investment_analysis(raw_analysis)
            
            return {
                'raw_analysis': raw_analysis,
                'market_analysis': structured_analysis.get('market_analysis', {}),
                'growth_prospects': structured_analysis.get('growth_prospects', {}),
                'competitive_position': structured_analysis.get('competitive_position', {}),
                'risk_factors': structured_analysis.get('risk_factors', []),
                'catalysts': structured_analysis.get('catalysts', []),
                'financial_health': structured_analysis.get('financial_health', {})
            }
            
        except Exception as e:
            logger.error(f"Failed to generate investment analysis: {str(e)}")
            return {'raw_analysis': 'Analysis generation failed due to technical error'}
    
    def _structure_investment_analysis(self, raw_analysis: str) -> Dict[str, Any]:
        """Structure raw AI analysis into organized components"""
        try:
            # Use AI to extract structured components
            structure_prompt = f"""
Extract and organize the following investment analysis into structured JSON:

Analysis Text: {raw_analysis}

Please extract and return ONLY valid JSON with these sections:
{{
    "market_analysis": {{
        "industry_outlook": "string",
        "market_size": "string",
        "growth_rate": "string",
        "competitive_dynamics": "string"
    }},
    "growth_prospects": {{
        "revenue_growth_drivers": ["list of strings"],
        "expansion_opportunities": ["list of strings"],
        "innovation_pipeline": "string"
    }},
    "competitive_position": {{
        "market_position": "string",
        "competitive_advantages": ["list of strings"],
        "key_competitors": ["list of strings"]
    }},
    "risk_factors": [
        "list of key risk factors as strings"
    ],
    "catalysts": [
        "list of positive catalysts as strings"
    ],
    "financial_health": {{
        "revenue_trend": "string",
        "profitability": "string",
        "balance_sheet": "string",
        "cash_flow": "string"
    }}
}}
"""
            
            structured_response = self.model.generate_content(structure_prompt)
            
            try:
                return json.loads(structured_response.text)
            except json.JSONDecodeError:
                logger.warning("Failed to parse structured analysis, using defaults")
                return self._get_default_analysis_structure()
                
        except Exception as e:
            logger.error(f"Failed to structure investment analysis: {str(e)}")
            return self._get_default_analysis_structure()
    
    def _get_default_analysis_structure(self) -> Dict[str, Any]:
        """Return default analysis structure when parsing fails"""
        return {
            'market_analysis': {
                'industry_outlook': 'Analysis pending',
                'market_size': 'Not specified',
                'growth_rate': 'To be determined',
                'competitive_dynamics': 'Under review'
            },
            'growth_prospects': {
                'revenue_growth_drivers': ['Analysis in progress'],
                'expansion_opportunities': ['Under evaluation'],
                'innovation_pipeline': 'Review required'
            },
            'competitive_position': {
                'market_position': 'Assessment ongoing',
                'competitive_advantages': ['To be identified'],
                'key_competitors': ['Analysis required']
            },
            'risk_factors': ['Comprehensive risk analysis pending'],
            'catalysts': ['Catalyst identification in progress'],
            'financial_health': {
                'revenue_trend': 'Under analysis',
                'profitability': 'Assessment pending',
                'balance_sheet': 'Review in progress',
                'cash_flow': 'Analysis required'
            }
        }
    
    def _generate_investment_recommendation(self, analysis: Dict, metrics: Dict, 
                                          client_context: Dict) -> Dict[str, Any]:
        """Generate specific investment recommendation based on analysis"""
        try:
            recommendation_prompt = f"""
Based on the comprehensive investment analysis provided, generate a specific investment recommendation.

Analysis Summary: {json.dumps(analysis.get('raw_analysis', ''), indent=2)}
Financial Metrics: {json.dumps(metrics, indent=2)}
Client Context: {json.dumps(client_context or {}, indent=2)}

Provide a clear investment recommendation including:
1. Action (BUY/HOLD/SELL)
2. Rationale for the recommendation
3. Price target (if applicable)
4. Time horizon
5. Key risks to monitor
6. Position sizing guidance

Be specific and actionable while including appropriate disclaimers.
"""
            
            recommendation_response = self._generate_financial_response(
                prompt=recommendation_prompt,
                client_context=client_context,
                financial_data=metrics
            )
            
            # Parse recommendation components
            recommendation_data = self._parse_recommendation(recommendation_response, metrics)
            
            return recommendation_data
            
        except Exception as e:
            logger.error(f"Failed to generate investment recommendation: {str(e)}")
            return {
                'action': 'HOLD',
                'rationale': 'Unable to generate recommendation due to technical error',
                'confidence': 'Low',
                'time_horizon': 'Unknown'
            }
    
    def _parse_recommendation(self, recommendation_text: str, metrics: Dict) -> Dict[str, Any]:
        """Parse AI recommendation response into structured format"""
        try:
            # Extract recommendation action
            action = 'HOLD'  # Default
            text_upper = recommendation_text.upper()
            
            if 'BUY' in text_upper and 'NOT' not in text_upper:
                action = 'BUY'
            elif 'SELL' in text_upper:
                action = 'SELL'
            elif 'HOLD' in text_upper:
                action = 'HOLD'
            
            # Extract confidence level
            confidence = 'Medium'  # Default
            if any(word in text_upper for word in ['HIGH CONFIDENCE', 'STRONG', 'COMPELLING']):
                confidence = 'High'
            elif any(word in text_upper for word in ['LOW CONFIDENCE', 'UNCERTAIN', 'LIMITED']):
                confidence = 'Low'
            
            # Extract time horizon
            time_horizon = 'Medium-term (6-18 months)'  # Default
            if any(word in recommendation_text.lower() for word in ['short-term', 'near-term', '3 months']):
                time_horizon = 'Short-term (3-6 months)'
            elif any(word in recommendation_text.lower() for word in ['long-term', 'multi-year', '2+ years']):
                time_horizon = 'Long-term (2+ years)'
            
            return {
                'action': action,
                'rationale': recommendation_text[:500] + '...' if len(recommendation_text) > 500 else recommendation_text,
                'confidence': confidence,
                'time_horizon': time_horizon,
                'target_price': metrics.get('target_price'),
                'current_price': metrics.get('current_price'),
                'upside_potential': self._calculate_upside_potential(
                    metrics.get('current_price'), 
                    metrics.get('target_price')
                )
            }
            
        except Exception as e:
            logger.error(f"Failed to parse recommendation: {str(e)}")
            return {
                'action': 'HOLD',
                'rationale': 'Recommendation parsing error',
                'confidence': 'Low',
                'time_horizon': 'Unknown'
            }
    
    def _calculate_upside_potential(self, current_price: float, target_price: float) -> Optional[float]:
        """Calculate upside potential percentage"""
        try:
            if current_price and target_price and current_price > 0:
                upside = ((target_price - current_price) / current_price) * 100
                return round(upside, 1)
            return None
        except (TypeError, ZeroDivisionError):
            return None
    
    def _calculate_confidence_score(self, financial_data: Dict, 
                                  research_context: Dict, analysis: Dict) -> int:
        """Calculate confidence score for the investment research"""
        try:
            confidence_score = 5  # Base score
            
            # Adjust based on data availability
            if financial_data.get('company_info'):
                confidence_score += 1
            if financial_data.get('fundamental_metrics'):
                confidence_score += 1
            
            # Adjust based on research depth
            avg_relevance = research_context.get('average_relevance', 0)
            if avg_relevance > 0.8:
                confidence_score += 2
            elif avg_relevance > 0.6:
                confidence_score += 1
            
            # Adjust based on source count
            source_count = research_context.get('total_sources', 0)
            if source_count >= 5:
                confidence_score += 1
            elif source_count >= 3:
                confidence_score += 0.5
            
            # Cap at 10
            return min(10, int(confidence_score))
            
        except Exception as e:
            logger.error(f"Failed to calculate confidence score: {str(e)}")
            return 5
    
    def search_financial_knowledge(self, query: str, search_type: str = 'general',
                                 context: Dict = None) -> Dict[str, Any]:
        """Search financial knowledge base for specific information"""
        try:
            if search_type == 'company':
                ticker = context.get('ticker') if context else None
                results = self.knowledge_store.search_company_knowledge(query, ticker=ticker)
            elif search_type == 'analyst':
                results = self.knowledge_store.search_analyst_reports(query)
            elif search_type == 'market':
                results = self.knowledge_store.search_market_intelligence(query)
            elif search_type == 'strategy':
                risk_level = context.get('risk_level') if context else None
                results = self.knowledge_store.search_investment_strategies(query, risk_level=risk_level)
            else:
                results = self.knowledge_store.comprehensive_search(query, context)
            
            return {
                'query': query,
                'search_type': search_type,
                'results': results,
                'result_count': len(results) if isinstance(results, list) else sum(len(v) for v in results.values()),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to search financial knowledge: {str(e)}")
            return {'error': str(e), 'results': []}
    
    def get_market_intelligence(self, portfolio_holdings: List[Dict] = None,
                              analysis_focus: str = 'general') -> Dict[str, Any]:
        """Get market intelligence and investment insights"""
        try:
            # Determine focus areas based on portfolio or general market
            if portfolio_holdings:
                sectors = list(set([holding.get('sector', 'Unknown') 
                                 for holding in portfolio_holdings if holding.get('sector')]))
                focus_query = f"market outlook for {', '.join(sectors)} sectors"
            else:
                focus_query = "current market conditions and investment outlook"
            
            # Search market intelligence
            market_intel = self.knowledge_store.search_market_intelligence(
                query=focus_query,
                n_results=5
            )
            
            # Get economic indicators context
            market_overview = self.financial_db.get_market_overview()
            
            # Generate AI-powered market outlook
            outlook_prompt = self._create_financial_system_prompt(f"""
Based on current market intelligence and economic indicators, provide investment market outlook covering:

1. Overall market conditions and trends
2. Sector-specific opportunities and risks  
3. Economic factors affecting investments
4. Investment strategy recommendations
5. Key themes and catalysts to watch

Focus: {analysis_focus}
Market Data: {json.dumps(market_overview, indent=2)}
Recent Intelligence: {json.dumps([r['content'][:200] for r in market_intel[:3]], indent=2)}

Provide actionable insights for investment decision making.
""")
            
            market_outlook = self._generate_financial_response(
                prompt=outlook_prompt,
                financial_data=market_overview
            )
            
            return {
                'market_outlook': {
                    'summary': market_outlook,
                    'key_themes': self._extract_market_themes(market_outlook),
                    'risk_factors': self._extract_market_risks(market_outlook)
                },
                'sector_analysis': self._analyze_sector_trends(market_intel),
                'economic_context': market_overview.get('economic_indicators', []),
                'opportunities': self._identify_opportunities(market_intel),
                'threats': self._identify_threats(market_intel),
                'recommendations': self._generate_market_recommendations(market_outlook),
                'intelligence_sources': len(market_intel),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get market intelligence: {str(e)}")
            return {'error': str(e)}
    
    def _extract_market_themes(self, outlook_text: str) -> List[str]:
        """Extract key market themes from outlook text"""
        themes = []
        common_themes = [
            'artificial intelligence', 'ai', 'technology innovation',
            'interest rates', 'federal reserve', 'monetary policy',
            'inflation', 'economic growth', 'recession', 
            'energy transition', 'renewable energy',
            'geopolitical', 'supply chain', 'demographics'
        ]
        
        outlook_lower = outlook_text.lower()
        for theme in common_themes:
            if theme in outlook_lower:
                themes.append(theme.title())
        
        return themes[:5]  # Return top 5 themes
    
    def _extract_market_risks(self, outlook_text: str) -> List[str]:
        """Extract key market risks from outlook text"""
        risks = []
        risk_keywords = [
            'risk', 'concern', 'challenge', 'headwind', 'uncertainty',
            'volatility', 'downturn', 'pressure', 'threat'
        ]
        
        sentences = outlook_text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in risk_keywords):
                risks.append(sentence.strip())
        
        return risks[:3]  # Return top 3 risks
    
    def _analyze_sector_trends(self, market_intel: List[Dict]) -> Dict[str, Any]:
        """Analyze sector trends from market intelligence"""
        sector_mentions = {}
        for intel in market_intel:
            content = intel.get('content', '').lower()
            metadata = intel.get('metadata', {})
            
            # Count sector mentions
            sectors = ['technology', 'healthcare', 'financial', 'energy', 
                      'consumer', 'industrial', 'utilities', 'materials']
            
            for sector in sectors:
                if sector in content:
                    sector_mentions[sector] = sector_mentions.get(sector, 0) + 1
        
        return {
            'trending_sectors': sorted(sector_mentions.items(), key=lambda x: x[1], reverse=True)[:5],
            'total_mentions': sum(sector_mentions.values())
        }
    
    def _identify_opportunities(self, market_intel: List[Dict]) -> List[str]:
        """Identify investment opportunities from market intelligence"""
        opportunities = []
        opportunity_keywords = [
            'opportunity', 'growth', 'potential', 'expansion', 'innovation',
            'emerging', 'catalyst', 'driver', 'upside'
        ]
        
        for intel in market_intel:
            content = intel.get('content', '')
            sentences = content.split('.')
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in opportunity_keywords):
                    opportunities.append(sentence.strip())
        
        return opportunities[:3]  # Return top 3 opportunities
    
    def _identify_threats(self, market_intel: List[Dict]) -> List[str]:
        """Identify investment threats from market intelligence"""
        threats = []
        threat_keywords = [
            'threat', 'risk', 'concern', 'challenge', 'headwind',
            'pressure', 'decline', 'disruption', 'competition'
        ]
        
        for intel in market_intel:
            content = intel.get('content', '')
            sentences = content.split('.')
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in threat_keywords):
                    threats.append(sentence.strip())
        
        return threats[:3]  # Return top 3 threats
    
    def _generate_market_recommendations(self, market_outlook: str) -> List[str]:
        """Generate investment recommendations from market outlook"""
        recommendations = [
            'Monitor Federal Reserve policy decisions and interest rate changes',
            'Focus on companies with strong competitive moats and pricing power',
            'Consider defensive positioning in uncertain market environments',
            'Maintain diversification across sectors and asset classes',
            'Stay informed on geopolitical developments affecting markets'
        ]
        
        # Customize based on outlook content
        outlook_lower = market_outlook.lower()
        
        if 'technology' in outlook_lower or 'ai' in outlook_lower:
            recommendations.insert(1, 'Consider technology sector opportunities, particularly AI-enabled companies')
        
        if 'dividend' in outlook_lower:
            recommendations.append('Evaluate dividend-paying stocks for income generation')
        
        if 'growth' in outlook_lower:
            recommendations.insert(2, 'Focus on companies with sustainable earnings growth')
        
        return recommendations[:5]  # Return top 5 recommendations