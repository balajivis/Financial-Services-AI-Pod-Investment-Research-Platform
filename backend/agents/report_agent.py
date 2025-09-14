#!/usr/bin/env python3
"""
Report Generation Agent for Investment Analysis
Creates professional investment reports and client communications
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import uuid

from .base_agent import FinancialBaseAgent

logger = logging.getLogger(__name__)

class ReportGenerationAgent(FinancialBaseAgent):
    """
    AI agent specialized in generating professional investment reports
    Creates customized reports for clients, compliance documentation, and analysis summaries
    """
    
    def __init__(self, knowledge_store, financial_db):
        """Initialize Report Generation Agent"""
        super().__init__(knowledge_store, financial_db, "report_generation_agent")
        
        # Report templates and configuration
        self.report_templates = {
            'investment_summary': {
                'sections': ['executive_summary', 'investment_analysis', 'risk_assessment', 
                           'recommendation', 'disclosures'],
                'target_audience': 'clients',
                'formality_level': 'professional'
            },
            'portfolio_review': {
                'sections': ['portfolio_overview', 'performance_analysis', 'risk_metrics',
                           'diversification_analysis', 'recommendations', 'action_items'],
                'target_audience': 'clients',
                'formality_level': 'professional'
            },
            'compliance_report': {
                'sections': ['regulatory_summary', 'suitability_analysis', 'risk_disclosures',
                           'audit_trail', 'compliance_checklist'],
                'target_audience': 'compliance',
                'formality_level': 'regulatory'
            },
            'research_report': {
                'sections': ['investment_thesis', 'financial_analysis', 'market_analysis',
                           'risk_factors', 'valuation', 'recommendation'],
                'target_audience': 'advisors',
                'formality_level': 'technical'
            }
        }
        
        logger.info("Report Generation Agent initialized for investment reporting")
    
    def generate_client_report(self, client_id: str, advisor_id: str, report_type: str,
                             analysis_data: List[str], customization: Dict = None) -> Dict[str, Any]:
        """
        Generate comprehensive client investment report
        
        Args:
            client_id: Client identifier
            advisor_id: Advisor identifier  
            report_type: Type of report to generate
            analysis_data: List of analysis IDs to include in report
            customization: Report customization preferences
            
        Returns:
            Generated report data dictionary
        """
        try:
            if report_type not in self.report_templates:
                raise ValueError(f"Unknown report type: {report_type}")
            
            report_id = self._generate_report_id()
            template = self.report_templates[report_type]
            
            # Gather data for report generation
            report_data = self._gather_report_data(client_id, advisor_id, analysis_data)
            
            # Generate report sections
            report_sections = self._generate_report_sections(
                template['sections'], report_data, customization
            )
            
            # Create executive summary
            executive_summary = self._generate_executive_summary(report_sections, report_type)
            
            # Generate visualizations data
            visualizations = self._generate_visualization_data(report_data)
            
            # Compile complete report
            complete_report = {
                'report_id': report_id,
                'report_type': report_type,
                'client_id': client_id,
                'advisor_id': advisor_id,
                'generation_date': datetime.now().isoformat(),
                'executive_summary': executive_summary,
                'sections': report_sections,
                'visualizations': visualizations,
                'disclaimers': self._get_report_disclaimers(report_type),
                'metadata': {
                    'template': template,
                    'customization': customization or {},
                    'data_sources': len(analysis_data),
                    'formality_level': template['formality_level'],
                    'target_audience': template['target_audience']
                }
            }
            
            return complete_report
            
        except Exception as e:
            logger.error(f"Failed to generate client report: {str(e)}")
            return {
                'report_id': self._generate_report_id(),
                'error': 'Report generation failed',
                'message': str(e)
            }
    
    def _generate_report_id(self) -> str:
        """Generate unique report identifier"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        return f"RPT_{timestamp}_{unique_id}"
    
    def _gather_report_data(self, client_id: str, advisor_id: str, 
                           analysis_ids: List[str]) -> Dict[str, Any]:
        """Gather all necessary data for report generation"""
        try:
            report_data = {
                'client_info': {'client_id': client_id},
                'advisor_info': {'advisor_id': advisor_id},
                'analysis_data': [],
                'market_context': {},
                'portfolio_data': {}
            }
            
            # Get market context
            report_data['market_context'] = self.financial_db.get_market_overview()
            
            # Simulate getting analysis data (in real implementation, would fetch from database)
            if analysis_ids:
                # For educational purposes, create sample analysis data
                for analysis_id in analysis_ids:
                    sample_analysis = {
                        'analysis_id': analysis_id,
                        'ticker': 'AAPL',  # Sample ticker
                        'recommendation': 'BUY',
                        'confidence_score': 7,
                        'risk_score': 4,
                        'target_price': 185.0,
                        'analysis_date': datetime.now().isoformat()
                    }
                    report_data['analysis_data'].append(sample_analysis)
            
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to gather report data: {str(e)}")
            return {}
    
    def _generate_report_sections(self, sections: List[str], report_data: Dict,
                                 customization: Dict = None) -> Dict[str, Any]:
        """Generate individual report sections"""
        generated_sections = {}
        
        try:
            for section in sections:
                if section == 'executive_summary':
                    generated_sections[section] = self._generate_executive_summary_section(report_data)
                elif section == 'investment_analysis':
                    generated_sections[section] = self._generate_investment_analysis_section(report_data)
                elif section == 'risk_assessment':
                    generated_sections[section] = self._generate_risk_assessment_section(report_data)
                elif section == 'recommendation':
                    generated_sections[section] = self._generate_recommendation_section(report_data)
                elif section == 'portfolio_overview':
                    generated_sections[section] = self._generate_portfolio_overview_section(report_data)
                elif section == 'performance_analysis':
                    generated_sections[section] = self._generate_performance_analysis_section(report_data)
                elif section == 'disclosures':
                    generated_sections[section] = self._generate_disclosures_section(report_data)
                else:
                    generated_sections[section] = f"Section '{section}' content to be implemented"
            
            return generated_sections
            
        except Exception as e:
            logger.error(f"Failed to generate report sections: {str(e)}")
            return {}
    
    def _generate_executive_summary_section(self, report_data: Dict) -> str:
        """Generate executive summary section"""
        try:
            summary_prompt = self._create_financial_system_prompt(f"""
Generate a professional executive summary for an investment report based on the following data:

Analysis Data: {json.dumps(report_data.get('analysis_data', []), indent=2)}
Market Context: {json.dumps(report_data.get('market_context', {}), indent=2)[:500]}

The executive summary should:
1. Provide a high-level overview of key findings
2. Highlight main investment recommendations
3. Summarize risk assessment
4. Present actionable next steps
5. Be concise and client-friendly (2-3 paragraphs)

Write in a professional, clear tone suitable for client communication.
""")
            
            return self._generate_financial_response(
                prompt=summary_prompt,
                financial_data=report_data.get('market_context', {})
            )
            
        except Exception as e:
            logger.error(f"Failed to generate executive summary section: {str(e)}")
            return "Executive summary generation failed due to technical error."
    
    def _generate_investment_analysis_section(self, report_data: Dict) -> str:
        """Generate investment analysis section"""
        try:
            analysis_prompt = self._create_financial_system_prompt(f"""
Generate a detailed investment analysis section for a client report based on:

Investment Analysis Data: {json.dumps(report_data.get('analysis_data', []), indent=2)}

The analysis section should include:
1. Investment thesis and rationale
2. Key financial metrics and valuation
3. Competitive positioning
4. Growth prospects and catalysts
5. Investment timeline and expectations

Present information in a clear, structured format with specific data points.
Make it informative yet accessible to sophisticated investors.
""")
            
            return self._generate_financial_response(
                prompt=analysis_prompt,
                financial_data=report_data.get('analysis_data', [])
            )
            
        except Exception as e:
            logger.error(f"Failed to generate investment analysis section: {str(e)}")
            return "Investment analysis section generation failed."
    
    def _generate_risk_assessment_section(self, report_data: Dict) -> str:
        """Generate risk assessment section"""
        try:
            risk_prompt = self._create_financial_system_prompt(f"""
Generate a comprehensive risk assessment section for an investment report:

Analysis Data: {json.dumps(report_data.get('analysis_data', []), indent=2)}

The risk assessment should cover:
1. Investment-specific risks and their likelihood
2. Portfolio impact and correlation effects
3. Market and economic risk factors
4. Quantitative risk metrics (VaR, beta, etc.)
5. Risk mitigation strategies
6. Monitoring recommendations

Present risks objectively with specific examples and mitigation strategies.
Use clear language that helps clients understand risk-return trade-offs.
""")
            
            return self._generate_financial_response(
                prompt=risk_prompt,
                financial_data=report_data.get('analysis_data', [])
            )
            
        except Exception as e:
            logger.error(f"Failed to generate risk assessment section: {str(e)}")
            return "Risk assessment section generation failed."
    
    def _generate_recommendation_section(self, report_data: Dict) -> str:
        """Generate recommendation section"""
        try:
            recommendation_prompt = self._create_financial_system_prompt(f"""
Generate specific investment recommendations based on the analysis:

Analysis Data: {json.dumps(report_data.get('analysis_data', []), indent=2)}

The recommendations should include:
1. Specific action items (BUY/HOLD/SELL with rationale)
2. Position sizing guidance
3. Entry and exit strategies
4. Time horizon considerations
5. Portfolio integration advice
6. Monitoring schedule

Be specific and actionable while including appropriate disclaimers.
Format recommendations as clear, prioritized action items.
""")
            
            return self._generate_financial_response(
                prompt=recommendation_prompt,
                financial_data=report_data.get('analysis_data', [])
            )
            
        except Exception as e:
            logger.error(f"Failed to generate recommendation section: {str(e)}")
            return "Recommendation section generation failed."
    
    def _generate_portfolio_overview_section(self, report_data: Dict) -> str:
        """Generate portfolio overview section"""
        try:
            # Sample portfolio overview for educational purposes
            overview = f"""
## Portfolio Overview

**Current Portfolio Value:** ${report_data.get('portfolio_data', {}).get('total_value', 'Not Available')}

**Asset Allocation:**
- Equities: 70% (Target: 65-75%)
- Fixed Income: 25% (Target: 20-30%)
- Cash/Alternatives: 5% (Target: 0-10%)

**Sector Diversification:**
Based on the analysis of your current holdings, your portfolio maintains good diversification across major sectors with appropriate risk-adjusted positioning.

**Key Performance Metrics:**
- Portfolio Beta: {report_data.get('portfolio_data', {}).get('beta', 'Calculating...')}
- Risk-Adjusted Returns: Under evaluation
- Sharpe Ratio: Analysis in progress

**Recent Activity:**
This report analyzes {len(report_data.get('analysis_data', []))} recent investment analyses conducted for your portfolio optimization.
"""
            return overview
            
        except Exception as e:
            logger.error(f"Failed to generate portfolio overview section: {str(e)}")
            return "Portfolio overview section generation failed."
    
    def _generate_performance_analysis_section(self, report_data: Dict) -> str:
        """Generate performance analysis section"""
        try:
            performance_analysis = f"""
## Performance Analysis

**Analysis Period:** {datetime.now().strftime('%B %Y')}

**Investment Performance Summary:**
The portfolio analysis covers {len(report_data.get('analysis_data', []))} investment opportunities evaluated during this period.

**Risk-Return Assessment:**
- Analyzed investments show an average confidence score of {self._calculate_average_confidence(report_data)}
- Risk levels are appropriately matched to investment objectives
- Recommendations align with stated risk tolerance

**Market Context:**
Current market conditions have been factored into all investment recommendations, with particular attention to:
- Economic indicator trends
- Sector-specific developments  
- Interest rate environment impact

**Benchmark Comparison:**
Performance evaluation relative to appropriate benchmarks is ongoing and will be included in subsequent reports.
"""
            return performance_analysis
            
        except Exception as e:
            logger.error(f"Failed to generate performance analysis section: {str(e)}")
            return "Performance analysis section generation failed."
    
    def _generate_disclosures_section(self, report_data: Dict) -> str:
        """Generate regulatory disclosures section"""
        return """
## Important Disclosures

**Investment Advisory Disclosures:**
This report is provided for informational purposes only and should not be construed as investment advice. Past performance does not guarantee future results. All investments carry the risk of loss.

**Risk Considerations:**
- Market risk affects all investments
- Individual securities may experience significant volatility
- Diversification does not eliminate investment risk
- Economic and market conditions can change rapidly

**Regulatory Compliance:**
This analysis complies with applicable securities regulations. All recommendations are based on the client's stated investment objectives, risk tolerance, and financial situation as disclosed.

**Data Sources:**
Information contained in this report is derived from sources believed to be reliable, but accuracy and completeness are not guaranteed.

**Professional Advice:**
Clients should consult with their financial advisor before making investment decisions based on this report.

**Report Date:** {datetime.now().strftime('%B %d, %Y')}
"""
    
    def _calculate_average_confidence(self, report_data: Dict) -> str:
        """Calculate average confidence score from analysis data"""
        try:
            analysis_data = report_data.get('analysis_data', [])
            if not analysis_data:
                return "Not Available"
            
            confidence_scores = [analysis.get('confidence_score', 5) for analysis in analysis_data]
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            
            return f"{avg_confidence:.1f}/10"
            
        except Exception as e:
            logger.error(f"Failed to calculate average confidence: {str(e)}")
            return "Calculation Error"
    
    def _generate_executive_summary(self, sections: Dict, report_type: str) -> str:
        """Generate overall executive summary from all sections"""
        try:
            if 'executive_summary' in sections:
                return sections['executive_summary']
            
            # Generate summary from other sections if executive summary not present
            summary_prompt = self._create_financial_system_prompt(f"""
Create a concise executive summary based on the following report sections:

Report Type: {report_type}
Sections: {json.dumps({k: v[:200] + "..." if len(str(v)) > 200 else v for k, v in sections.items()}, indent=2)}

Provide a 2-3 paragraph executive summary that:
1. Highlights key findings and recommendations
2. Summarizes main risks and opportunities
3. Provides clear next steps for the client

Keep it professional and client-focused.
""")
            
            return self._generate_financial_response(prompt=summary_prompt)
            
        except Exception as e:
            logger.error(f"Failed to generate executive summary: {str(e)}")
            return "Executive summary generation failed."
    
    def _generate_visualization_data(self, report_data: Dict) -> Dict[str, Any]:
        """Generate data for report visualizations"""
        try:
            visualizations = {}
            
            # Portfolio allocation chart data
            if 'portfolio_data' in report_data:
                visualizations['portfolio_allocation'] = {
                    'type': 'pie_chart',
                    'title': 'Portfolio Allocation',
                    'data': {
                        'Equities': 70,
                        'Fixed Income': 25,
                        'Cash': 5
                    }
                }
            
            # Risk metrics chart data
            analysis_data = report_data.get('analysis_data', [])
            if analysis_data:
                risk_scores = [analysis.get('risk_score', 5) for analysis in analysis_data]
                confidence_scores = [analysis.get('confidence_score', 5) for analysis in analysis_data]
                
                visualizations['risk_confidence_scatter'] = {
                    'type': 'scatter_plot',
                    'title': 'Risk vs Confidence Analysis',
                    'x_axis': 'Risk Score',
                    'y_axis': 'Confidence Score',
                    'data': list(zip(risk_scores, confidence_scores))
                }
            
            # Market context chart
            market_context = report_data.get('market_context', {})
            if market_context.get('economic_indicators'):
                visualizations['economic_indicators'] = {
                    'type': 'bar_chart',
                    'title': 'Key Economic Indicators',
                    'data': {
                        indicator['indicator_name']: indicator['value']
                        for indicator in market_context['economic_indicators'][:5]
                    }
                }
            
            return visualizations
            
        except Exception as e:
            logger.error(f"Failed to generate visualization data: {str(e)}")
            return {}
    
    def _get_report_disclaimers(self, report_type: str) -> List[str]:
        """Get appropriate disclaimers for report type"""
        base_disclaimers = [
            "This report is for informational purposes only and does not constitute investment advice.",
            "Past performance does not guarantee future results.",
            "All investments involve risk, including the potential loss of principal.",
            "Please consult with a qualified financial advisor before making investment decisions."
        ]
        
        if report_type == 'compliance_report':
            base_disclaimers.extend([
                "This report complies with applicable regulatory requirements.",
                "All recommendations are based on client suitability analysis.",
                "Investment advice provided is subject to regulatory oversight."
            ])
        elif report_type == 'research_report':
            base_disclaimers.extend([
                "Research analysis is based on information believed to be reliable.",
                "Market conditions and company fundamentals may change rapidly.",
                "Independent verification of information is recommended."
            ])
        
        return base_disclaimers
    
    def generate_portfolio_summary(self, client_id: str, portfolio_data: Dict,
                                 performance_data: Dict = None) -> Dict[str, Any]:
        """Generate concise portfolio summary report"""
        try:
            summary_prompt = self._create_financial_system_prompt(f"""
Generate a concise portfolio summary for client communication:

Portfolio Data: {json.dumps(portfolio_data, indent=2)[:800]}
Performance Data: {json.dumps(performance_data or {}, indent=2)[:400]}

Create a summary that includes:
1. Current portfolio value and key metrics
2. Asset allocation overview
3. Recent performance highlights
4. Key opportunities and concerns
5. Recommended actions

Keep it concise (1-2 pages) and client-friendly.
""")
            
            summary_content = self._generate_financial_response(
                prompt=summary_prompt,
                financial_data=portfolio_data
            )
            
            return {
                'summary_id': self._generate_report_id(),
                'client_id': client_id,
                'report_type': 'portfolio_summary',
                'content': summary_content,
                'generated_at': datetime.now().isoformat(),
                'summary_metrics': self._extract_summary_metrics(portfolio_data),
                'action_items': self._extract_action_items(summary_content)
            }
            
        except Exception as e:
            logger.error(f"Failed to generate portfolio summary: {str(e)}")
            return {'error': str(e)}
    
    def _extract_summary_metrics(self, portfolio_data: Dict) -> Dict[str, Any]:
        """Extract key metrics for portfolio summary"""
        return {
            'total_value': portfolio_data.get('total_value', 0),
            'risk_score': portfolio_data.get('risk_metrics', {}).get('portfolio_beta', 1.0),
            'diversification_score': portfolio_data.get('diversification', {}).get('diversification_score', 5),
            'health_score': portfolio_data.get('health_score', 50)
        }
    
    def _extract_action_items(self, content: str) -> List[str]:
        """Extract action items from report content"""
        action_items = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['recommend', 'should', 'action', 'consider']):
                if len(line) > 20 and len(line) < 150:
                    action_items.append(line)
        
        return action_items[:5]
    
    def generate_compliance_summary(self, advisor_id: str, period_days: int = 30) -> Dict[str, Any]:
        """Generate compliance summary for regulatory review"""
        try:
            # Get compliance data from database
            compliance_data = self.financial_db.get_compliance_dashboard(period_days)
            
            compliance_prompt = self._create_financial_system_prompt(f"""
Generate a regulatory compliance summary for the past {period_days} days:

Compliance Metrics: {json.dumps(compliance_data, indent=2)}

The summary should include:
1. Overall compliance status
2. Key metrics and trends
3. Areas of concern or improvement
4. Regulatory requirement adherence
5. Recommended actions for compliance officers

Format for regulatory review and documentation.
""")
            
            summary_content = self._generate_financial_response(
                prompt=compliance_prompt,
                financial_data=compliance_data
            )
            
            return {
                'compliance_summary_id': self._generate_report_id(),
                'advisor_id': advisor_id,
                'review_period_days': period_days,
                'compliance_status': self._determine_compliance_status(compliance_data),
                'summary_content': summary_content,
                'key_metrics': compliance_data,
                'generated_at': datetime.now().isoformat(),
                'next_review_date': (datetime.now() + timedelta(days=30)).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate compliance summary: {str(e)}")
            return {'error': str(e)}
    
    def _determine_compliance_status(self, compliance_data: Dict) -> str:
        """Determine overall compliance status"""
        try:
            approval_rate = compliance_data.get('approval_rate', 0)
            
            if approval_rate >= 95:
                return 'Excellent'
            elif approval_rate >= 90:
                return 'Good'
            elif approval_rate >= 80:
                return 'Satisfactory'
            else:
                return 'Needs Improvement'
                
        except Exception as e:
            logger.error(f"Failed to determine compliance status: {str(e)}")
            return 'Unknown'
    
    def format_report_for_delivery(self, report_data: Dict, 
                                  output_format: str = 'json') -> Dict[str, Any]:
        """Format report for client delivery"""
        try:
            if output_format == 'json':
                return {
                    'report': report_data,
                    'format': 'json',
                    'delivery_ready': True,
                    'generated_at': datetime.now().isoformat()
                }
            elif output_format == 'summary':
                # Create condensed summary version
                return {
                    'report_id': report_data.get('report_id'),
                    'report_type': report_data.get('report_type'),
                    'executive_summary': report_data.get('executive_summary'),
                    'key_recommendations': self._extract_key_recommendations(report_data),
                    'risk_summary': self._extract_risk_summary(report_data),
                    'format': 'summary',
                    'delivery_ready': True
                }
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
                
        except Exception as e:
            logger.error(f"Failed to format report for delivery: {str(e)}")
            return {'error': str(e), 'delivery_ready': False}
    
    def _extract_key_recommendations(self, report_data: Dict) -> List[str]:
        """Extract key recommendations from report"""
        recommendations = []
        
        sections = report_data.get('sections', {})
        if 'recommendation' in sections:
            content = sections['recommendation']
            lines = content.split('\n')
            
            for line in lines:
                if any(keyword in line.lower() for keyword in ['recommend', 'buy', 'sell', 'hold']):
                    if len(line.strip()) > 20:
                        recommendations.append(line.strip())
        
        return recommendations[:3]
    
    def _extract_risk_summary(self, report_data: Dict) -> str:
        """Extract risk summary from report"""
        sections = report_data.get('sections', {})
        risk_content = sections.get('risk_assessment', '')
        
        # Return first paragraph or first 200 characters
        first_paragraph = risk_content.split('\n\n')[0] if risk_content else ''
        return first_paragraph[:200] + '...' if len(first_paragraph) > 200 else first_paragraph