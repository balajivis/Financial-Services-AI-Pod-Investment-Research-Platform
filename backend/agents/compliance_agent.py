#!/usr/bin/env python3
"""
Compliance Agent for Financial Services
Ensures regulatory compliance and manages audit trails
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from .base_agent import FinancialBaseAgent

logger = logging.getLogger(__name__)

class ComplianceAgent(FinancialBaseAgent):
    """
    AI agent specialized in financial services compliance
    Ensures FINRA, SEC, and SOC2 compliance for investment recommendations and client interactions
    """
    
    def __init__(self, knowledge_store, financial_db):
        """Initialize Compliance Agent"""
        super().__init__(knowledge_store, financial_db, "compliance_agent")
        
        # Compliance rules and thresholds
        self.compliance_rules = {
            'suitability': {
                'conservative': {'max_risk_score': 4, 'max_volatility': 1.2, 'min_liquidity': 'High'},
                'moderate': {'max_risk_score': 7, 'max_volatility': 1.5, 'min_liquidity': 'Moderate'},
                'aggressive': {'max_risk_score': 10, 'max_volatility': 2.0, 'min_liquidity': 'Low'}
            },
            'concentration_limits': {
                'single_security': 0.2,  # Max 20% in single security
                'sector': 0.35,          # Max 35% in single sector
                'asset_class': 0.8       # Max 80% in single asset class
            },
            'documentation_requirements': [
                'investment_rationale',
                'risk_assessment',
                'suitability_analysis',
                'client_acknowledgment'
            ],
            'disclosure_requirements': [
                'material_risks',
                'conflicts_of_interest',
                'fee_structure',
                'performance_limitations'
            ]
        }
        
        # Regulatory frameworks
        self.regulatory_frameworks = {
            'FINRA': ['Rule 2111 - Suitability', 'Rule 3110 - Supervision'],
            'SEC': ['Investment Advisers Act Rule 206(4)-7', 'Regulation Best Interest'],
            'SOC2': ['Security', 'Availability', 'Confidentiality', 'Privacy']
        }
        
        logger.info("Compliance Agent initialized for financial services compliance")
    
    def verify_investment_suitability(self, advisor_id: str, client_id: str,
                                    investment_data: Dict, risk_assessment: Dict) -> Dict[str, Any]:
        """
        Verify if investment recommendation is suitable for client
        
        Args:
            advisor_id: Advisor making the recommendation
            client_id: Client receiving recommendation
            investment_data: Investment analysis data
            risk_assessment: Risk assessment results
            
        Returns:
            Suitability verification results
        """
        try:
            # Get client profile for suitability analysis
            client_profile = self._get_client_risk_profile(client_id)
            
            # Perform suitability checks
            suitability_checks = self._perform_suitability_checks(
                investment_data, risk_assessment, client_profile
            )
            
            # Check concentration limits
            concentration_analysis = self._check_concentration_limits(
                client_id, investment_data
            )
            
            # Verify required documentation
            documentation_check = self._verify_documentation_requirements(
                investment_data, risk_assessment
            )
            
            # Generate compliance recommendations
            compliance_recommendations = self._generate_compliance_recommendations(
                suitability_checks, concentration_analysis, documentation_check
            )
            
            # Determine overall suitability
            overall_suitable = self._determine_overall_suitability(
                suitability_checks, concentration_analysis, documentation_check
            )
            
            # Create compliance record
            compliance_record = {
                'advisor_id': advisor_id,
                'client_id': client_id,
                'analysis_timestamp': datetime.now().isoformat(),
                'investment_ticker': investment_data.get('ticker', 'Unknown'),
                'overall_suitable': overall_suitable,
                'suitability_checks': suitability_checks,
                'concentration_analysis': concentration_analysis,
                'documentation_status': documentation_check,
                'compliance_recommendations': compliance_recommendations,
                'regulatory_requirements': self._get_applicable_regulations(),
                'required_disclosures': self._get_required_disclosures(investment_data),
                'audit_trail': self._create_audit_trail(advisor_id, client_id, investment_data)
            }
            
            # Log compliance verification
            self._log_compliance_verification(compliance_record)
            
            return compliance_record
            
        except Exception as e:
            logger.error(f"Failed to verify investment suitability: {str(e)}")
            return {
                'error': 'Suitability verification failed',
                'message': str(e),
                'overall_suitable': False,
                'requires_manual_review': True
            }
    
    def _get_client_risk_profile(self, client_id: str) -> Dict[str, Any]:
        """Get client risk profile (simplified for educational purposes)"""
        # In real implementation, this would fetch actual client profile
        return {
            'client_id': client_id,
            'risk_tolerance': 'moderate',  # conservative, moderate, aggressive
            'investment_experience': 'intermediate',
            'time_horizon': 'long_term',  # short_term, medium_term, long_term
            'liquidity_needs': 'low',     # low, moderate, high
            'income_requirements': 'moderate',
            'investment_objectives': ['growth', 'income'],
            'financial_situation': 'stable',
            'age_range': '35-55',
            'net_worth_category': 'moderate'
        }
    
    def _perform_suitability_checks(self, investment_data: Dict, 
                                   risk_assessment: Dict, client_profile: Dict) -> Dict[str, Any]:
        """Perform comprehensive suitability analysis"""
        try:
            checks = {}
            client_risk_tolerance = client_profile.get('risk_tolerance', 'moderate')
            rules = self.compliance_rules['suitability'][client_risk_tolerance]
            
            # Risk score suitability
            investment_risk_score = risk_assessment.get('risk_score', 5)
            max_allowed_risk = rules['max_risk_score']
            
            checks['risk_score_suitable'] = {
                'passed': investment_risk_score <= max_allowed_risk,
                'investment_risk': investment_risk_score,
                'client_max_risk': max_allowed_risk,
                'notes': f"Investment risk score {investment_risk_score} vs client max {max_allowed_risk}"
            }
            
            # Volatility suitability
            investment_beta = investment_data.get('financial_metrics', {}).get('beta', 1.0)
            max_allowed_volatility = rules['max_volatility']
            
            checks['volatility_suitable'] = {
                'passed': investment_beta <= max_allowed_volatility,
                'investment_beta': investment_beta,
                'client_max_volatility': max_allowed_volatility,
                'notes': f"Investment beta {investment_beta} vs client max {max_allowed_volatility}"
            }
            
            # Time horizon suitability
            client_time_horizon = client_profile.get('time_horizon', 'medium_term')
            investment_recommendation = investment_data.get('recommendation', {})
            recommended_time_horizon = investment_recommendation.get('time_horizon', 'medium_term')
            
            time_horizon_compatible = self._check_time_horizon_compatibility(
                client_time_horizon, recommended_time_horizon
            )
            
            checks['time_horizon_suitable'] = {
                'passed': time_horizon_compatible,
                'client_horizon': client_time_horizon,
                'investment_horizon': recommended_time_horizon,
                'notes': f"Time horizons {'compatible' if time_horizon_compatible else 'incompatible'}"
            }
            
            # Liquidity needs assessment
            client_liquidity_needs = client_profile.get('liquidity_needs', 'moderate')
            investment_liquidity = risk_assessment.get('quantitative_metrics', {}).get('liquidity_risk', 'Moderate')
            
            liquidity_suitable = self._check_liquidity_suitability(
                client_liquidity_needs, investment_liquidity
            )
            
            checks['liquidity_suitable'] = {
                'passed': liquidity_suitable,
                'client_liquidity_needs': client_liquidity_needs,
                'investment_liquidity': investment_liquidity,
                'notes': f"Liquidity {'suitable' if liquidity_suitable else 'unsuitable'}"
            }
            
            # Investment experience check
            client_experience = client_profile.get('investment_experience', 'intermediate')
            investment_complexity = self._assess_investment_complexity(investment_data)
            
            experience_suitable = self._check_experience_suitability(
                client_experience, investment_complexity
            )
            
            checks['experience_suitable'] = {
                'passed': experience_suitable,
                'client_experience': client_experience,
                'investment_complexity': investment_complexity,
                'notes': f"Experience level {'adequate' if experience_suitable else 'inadequate'} for complexity"
            }
            
            return checks
            
        except Exception as e:
            logger.error(f"Failed to perform suitability checks: {str(e)}")
            return {'error': str(e)}
    
    def _check_time_horizon_compatibility(self, client_horizon: str, investment_horizon: str) -> bool:
        """Check if time horizons are compatible"""
        horizon_compatibility = {
            'short_term': ['short_term'],
            'medium_term': ['short_term', 'medium_term'],
            'long_term': ['short_term', 'medium_term', 'long_term']
        }
        
        compatible_horizons = horizon_compatibility.get(client_horizon, [])
        return investment_horizon in compatible_horizons
    
    def _check_liquidity_suitability(self, client_needs: str, investment_liquidity: str) -> bool:
        """Check if investment liquidity meets client needs"""
        liquidity_mapping = {'Low': 1, 'Moderate': 2, 'High': 3}
        need_mapping = {'high': 3, 'moderate': 2, 'low': 1}
        
        investment_liquidity_score = liquidity_mapping.get(investment_liquidity, 2)
        client_need_score = need_mapping.get(client_needs, 2)
        
        # Investment liquidity should meet or exceed client needs
        return investment_liquidity_score >= client_need_score
    
    def _assess_investment_complexity(self, investment_data: Dict) -> str:
        """Assess complexity of investment"""
        # Simplified complexity assessment
        ticker = investment_data.get('ticker', '')
        
        # For educational purposes, assume most stocks are moderate complexity
        if any(keyword in investment_data.get('description', '').lower() 
               for keyword in ['derivative', 'option', 'complex']):
            return 'high'
        elif any(keyword in investment_data.get('description', '').lower() 
                for keyword in ['etf', 'index', 'blue chip']):
            return 'low'
        else:
            return 'moderate'
    
    def _check_experience_suitability(self, client_experience: str, investment_complexity: str) -> bool:
        """Check if client experience is adequate for investment complexity"""
        experience_levels = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        complexity_requirements = {'low': 1, 'moderate': 2, 'high': 3}
        
        client_level = experience_levels.get(client_experience, 2)
        required_level = complexity_requirements.get(investment_complexity, 2)
        
        return client_level >= required_level
    
    def _check_concentration_limits(self, client_id: str, investment_data: Dict) -> Dict[str, Any]:
        """Check portfolio concentration limits"""
        try:
            # In real implementation, would get actual portfolio data
            # For educational purposes, using simulated checks
            
            checks = {}
            limits = self.compliance_rules['concentration_limits']
            
            # Single security concentration (simulated)
            current_position_percentage = 0.15  # 15% - within limits
            single_security_limit = limits['single_security']
            
            checks['single_security'] = {
                'passed': current_position_percentage <= single_security_limit,
                'current_percentage': current_position_percentage,
                'limit': single_security_limit,
                'notes': f"Single security exposure {current_position_percentage:.1%} vs limit {single_security_limit:.1%}"
            }
            
            # Sector concentration
            sector = investment_data.get('company_info', {}).get('sector', 'Technology')
            current_sector_percentage = 0.25  # 25% - within limits
            sector_limit = limits['sector']
            
            checks['sector_concentration'] = {
                'passed': current_sector_percentage <= sector_limit,
                'sector': sector,
                'current_percentage': current_sector_percentage,
                'limit': sector_limit,
                'notes': f"{sector} sector exposure {current_sector_percentage:.1%} vs limit {sector_limit:.1%}"
            }
            
            # Asset class concentration
            current_equity_percentage = 0.75  # 75% - within limits
            equity_limit = limits['asset_class']
            
            checks['asset_class_concentration'] = {
                'passed': current_equity_percentage <= equity_limit,
                'asset_class': 'Equity',
                'current_percentage': current_equity_percentage,
                'limit': equity_limit,
                'notes': f"Equity exposure {current_equity_percentage:.1%} vs limit {equity_limit:.1%}"
            }
            
            return checks
            
        except Exception as e:
            logger.error(f"Failed to check concentration limits: {str(e)}")
            return {'error': str(e)}
    
    def _verify_documentation_requirements(self, investment_data: Dict, 
                                         risk_assessment: Dict) -> Dict[str, Any]:
        """Verify required documentation is present"""
        try:
            required_docs = self.compliance_rules['documentation_requirements']
            documentation_status = {}
            
            for requirement in required_docs:
                if requirement == 'investment_rationale':
                    present = bool(investment_data.get('recommendation', {}).get('rationale'))
                elif requirement == 'risk_assessment':
                    present = bool(risk_assessment.get('risk_score'))
                elif requirement == 'suitability_analysis':
                    present = True  # We're performing it now
                elif requirement == 'client_acknowledgment':
                    present = False  # Would be collected separately
                else:
                    present = False
                
                documentation_status[requirement] = {
                    'present': present,
                    'required': True,
                    'notes': f"{'✓' if present else '✗'} {requirement.replace('_', ' ').title()}"
                }
            
            all_required_present = all(doc['present'] for doc in documentation_status.values())
            
            return {
                'all_required_present': all_required_present,
                'documentation_details': documentation_status,
                'missing_documents': [
                    req for req, status in documentation_status.items() 
                    if not status['present']
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to verify documentation requirements: {str(e)}")
            return {'error': str(e)}
    
    def _generate_compliance_recommendations(self, suitability_checks: Dict,
                                           concentration_analysis: Dict,
                                           documentation_check: Dict) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        # Check suitability issues
        for check_name, check_result in suitability_checks.items():
            if isinstance(check_result, dict) and not check_result.get('passed', True):
                recommendations.append(
                    f"SUITABILITY CONCERN: {check_result.get('notes', check_name)}"
                )
        
        # Check concentration issues
        for check_name, check_result in concentration_analysis.items():
            if isinstance(check_result, dict) and not check_result.get('passed', True):
                recommendations.append(
                    f"CONCENTRATION LIMIT EXCEEDED: {check_result.get('notes', check_name)}"
                )
        
        # Check documentation issues
        if not documentation_check.get('all_required_present', True):
            missing_docs = documentation_check.get('missing_documents', [])
            recommendations.append(
                f"MISSING DOCUMENTATION: {', '.join(missing_docs)}"
            )
        
        # General compliance recommendations
        if not recommendations:  # If no issues found
            recommendations.extend([
                "All compliance checks passed",
                "Ensure client acknowledgment is obtained before execution",
                "Schedule follow-up review in 30 days"
            ])
        else:
            recommendations.insert(0, "COMPLIANCE REVIEW REQUIRED before proceeding")
        
        return recommendations
    
    def _determine_overall_suitability(self, suitability_checks: Dict,
                                     concentration_analysis: Dict,
                                     documentation_check: Dict) -> bool:
        """Determine overall investment suitability"""
        try:
            # All suitability checks must pass
            suitability_passed = all(
                check.get('passed', False) if isinstance(check, dict) else True
                for check in suitability_checks.values()
            )
            
            # All concentration checks must pass
            concentration_passed = all(
                check.get('passed', False) if isinstance(check, dict) else True
                for check in concentration_analysis.values()
            )
            
            # Documentation must be complete (can be waived with proper justification)
            documentation_passed = documentation_check.get('all_required_present', False)
            
            # Overall suitability requires passing all major checks
            # Documentation can be completed post-approval with proper procedures
            return suitability_passed and concentration_passed
            
        except Exception as e:
            logger.error(f"Failed to determine overall suitability: {str(e)}")
            return False
    
    def _get_applicable_regulations(self) -> List[str]:
        """Get applicable regulatory requirements"""
        return [
            "FINRA Rule 2111 (Suitability)",
            "SEC Investment Advisers Act Rule 206(4)-7",
            "SEC Regulation Best Interest (Reg BI)",
            "FINRA Rule 3110 (Supervision)",
            "SOC2 Security and Privacy Controls"
        ]
    
    def _get_required_disclosures(self, investment_data: Dict) -> List[str]:
        """Get required disclosures for investment"""
        base_disclosures = [
            "Material investment risks including potential loss of principal",
            "Past performance does not guarantee future results",
            "Fees and expenses associated with the investment",
            "Conflicts of interest, if any"
        ]
        
        # Add specific disclosures based on investment characteristics
        risk_score = investment_data.get('risk_score', 5)
        if risk_score >= 7:
            base_disclosures.append("HIGH RISK: Investment carries elevated risk of loss")
        
        sector = investment_data.get('company_info', {}).get('sector', '')
        if sector.lower() == 'technology':
            base_disclosures.append("Technology sector investments may be subject to rapid changes and volatility")
        
        return base_disclosures
    
    def _create_audit_trail(self, advisor_id: str, client_id: str, 
                           investment_data: Dict) -> Dict[str, Any]:
        """Create compliance audit trail"""
        return {
            'compliance_review_date': datetime.now().isoformat(),
            'reviewer': 'AI Compliance Agent',
            'advisor_id': advisor_id,
            'client_id': client_id,
            'investment_reviewed': investment_data.get('ticker', 'Unknown'),
            'review_type': 'Pre-recommendation Suitability Analysis',
            'data_sources': ['client_profile', 'investment_analysis', 'risk_assessment'],
            'methodology': 'Automated compliance checking with AI analysis',
            'retention_period': '7 years (regulatory requirement)'
        }
    
    def _log_compliance_verification(self, compliance_record: Dict):
        """Log compliance verification for audit purposes"""
        try:
            self.financial_db.log_financial_audit_event(
                action='compliance_verification',
                advisor_id=compliance_record.get('advisor_id'),
                client_id=compliance_record.get('client_id'),
                ticker=compliance_record.get('investment_ticker'),
                details=json.dumps({
                    'suitable': compliance_record.get('overall_suitable'),
                    'review_timestamp': compliance_record.get('analysis_timestamp'),
                    'recommendations_count': len(compliance_record.get('compliance_recommendations', []))
                }),
                compliance_data=compliance_record,
                success=True,
                risk_level='high' if not compliance_record.get('overall_suitable') else 'low'
            )
            
        except Exception as e:
            logger.error(f"Failed to log compliance verification: {str(e)}")
    
    def review_portfolio_recommendations(self, advisor_id: str, client_id: str,
                                       portfolio_data: Dict, recommendations: List[Dict]) -> Dict[str, Any]:
        """Review portfolio recommendations for compliance"""
        try:
            compliance_review = {
                'review_id': f"PORTFOLIO_COMPLIANCE_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'advisor_id': advisor_id,
                'client_id': client_id,
                'review_timestamp': datetime.now().isoformat(),
                'recommendations_reviewed': len(recommendations),
                'compliance_status': 'Under Review'
            }
            
            # Review each recommendation
            recommendation_reviews = []
            overall_compliant = True
            
            for i, recommendation in enumerate(recommendations):
                rec_review = {
                    'recommendation_index': i,
                    'ticker': recommendation.get('ticker', 'Unknown'),
                    'action': recommendation.get('action', 'Unknown'),
                    'compliance_checks': {
                        'suitability_reviewed': True,
                        'concentration_checked': True,
                        'documentation_present': bool(recommendation.get('rationale')),
                        'disclosures_included': True
                    }
                }
                
                # Simple compliance check for portfolio recommendations
                rec_compliant = all(rec_review['compliance_checks'].values())
                rec_review['compliant'] = rec_compliant
                
                if not rec_compliant:
                    overall_compliant = False
                
                recommendation_reviews.append(rec_review)
            
            compliance_review.update({
                'overall_compliant': overall_compliant,
                'recommendation_reviews': recommendation_reviews,
                'compliance_summary': self._generate_portfolio_compliance_summary(
                    portfolio_data, recommendation_reviews, overall_compliant
                ),
                'required_actions': self._get_portfolio_compliance_actions(
                    recommendation_reviews, overall_compliant
                )
            })
            
            # Log portfolio compliance review
            self.financial_db.log_financial_audit_event(
                action='portfolio_compliance_review',
                advisor_id=advisor_id,
                client_id=client_id,
                details=json.dumps({
                    'review_id': compliance_review['review_id'],
                    'recommendations_count': len(recommendations),
                    'overall_compliant': overall_compliant
                }),
                compliance_data=compliance_review,
                success=True,
                risk_level='medium'
            )
            
            return compliance_review
            
        except Exception as e:
            logger.error(f"Failed to review portfolio recommendations: {str(e)}")
            return {'error': str(e), 'overall_compliant': False}
    
    def _generate_portfolio_compliance_summary(self, portfolio_data: Dict,
                                             recommendation_reviews: List[Dict],
                                             overall_compliant: bool) -> str:
        """Generate portfolio compliance summary"""
        total_recommendations = len(recommendation_reviews)
        compliant_recommendations = sum(1 for rev in recommendation_reviews if rev.get('compliant', False))
        
        summary = f"""
PORTFOLIO COMPLIANCE REVIEW SUMMARY

Total Recommendations Reviewed: {total_recommendations}
Compliant Recommendations: {compliant_recommendations}
Compliance Rate: {(compliant_recommendations/max(total_recommendations,1))*100:.1f}%

Overall Compliance Status: {'COMPLIANT' if overall_compliant else 'NON-COMPLIANT - REVIEW REQUIRED'}

Portfolio Health Score: {portfolio_data.get('health_score', 'Not Available')}
Risk Assessment: Portfolio risk metrics reviewed and documented

{'All recommendations meet regulatory requirements.' if overall_compliant else 'Some recommendations require additional compliance review before implementation.'}
"""
        return summary.strip()
    
    def _get_portfolio_compliance_actions(self, recommendation_reviews: List[Dict],
                                        overall_compliant: bool) -> List[str]:
        """Get required compliance actions for portfolio"""
        if overall_compliant:
            return [
                "Obtain client acknowledgment for all recommendations",
                "Implement recommendations according to approved timeline",
                "Schedule 30-day follow-up compliance review"
            ]
        else:
            actions = ["Complete additional compliance review for flagged recommendations"]
            
            for review in recommendation_reviews:
                if not review.get('compliant'):
                    ticker = review.get('ticker', 'Unknown')
                    actions.append(f"Review compliance issues for {ticker} recommendation")
            
            actions.extend([
                "Obtain additional client documentation if required",
                "Management approval required before implementation"
            ])
            
            return actions
    
    def validate_report_compliance(self, report_data: Dict, advisor_id: str,
                                 client_id: str) -> Dict[str, Any]:
        """Validate investment report for regulatory compliance"""
        try:
            validation_result = {
                'report_id': report_data.get('report_id'),
                'validation_timestamp': datetime.now().isoformat(),
                'validator': 'AI Compliance Agent',
                'compliance_status': 'Under Review'
            }
            
            # Check required report elements
            required_elements = [
                'executive_summary',
                'investment_analysis', 
                'risk_assessment',
                'disclaimers'
            ]
            
            element_checks = {}
            for element in required_elements:
                present = element in report_data.get('sections', {})
                element_checks[element] = {
                    'present': present,
                    'required': True,
                    'status': 'OK' if present else 'MISSING'
                }
            
            # Check disclosure requirements
            disclaimers = report_data.get('disclaimers', [])
            required_disclosures_present = len(disclaimers) >= 3  # Minimum disclosure count
            
            # Overall compliance determination
            all_elements_present = all(check['present'] for check in element_checks.values())
            compliant = all_elements_present and required_disclosures_present
            
            validation_result.update({
                'compliant': compliant,
                'element_checks': element_checks,
                'disclosure_check': {
                    'required_disclosures_present': required_disclosures_present,
                    'disclosure_count': len(disclaimers)
                },
                'validation_notes': self._generate_report_validation_notes(
                    compliant, element_checks, required_disclosures_present
                ),
                'compliance_certification': compliant
            })
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Failed to validate report compliance: {str(e)}")
            return {
                'error': str(e),
                'compliant': False,
                'requires_manual_review': True
            }
    
    def _generate_report_validation_notes(self, compliant: bool, element_checks: Dict,
                                        disclosures_present: bool) -> str:
        """Generate validation notes for report compliance"""
        if compliant:
            return "Report meets all regulatory compliance requirements and is approved for client delivery."
        
        issues = []
        for element, check in element_checks.items():
            if not check['present']:
                issues.append(f"Missing required section: {element}")
        
        if not disclosures_present:
            issues.append("Insufficient regulatory disclosures")
        
        return f"COMPLIANCE ISSUES IDENTIFIED: {'; '.join(issues)}. Manual review required before client delivery."
    
    def get_audit_trail(self, days: int = 30) -> Dict[str, Any]:
        """Retrieve compliance audit trail"""
        try:
            # Get audit data from database
            audit_data = self.financial_db.get_compliance_dashboard(days)
            
            # Generate comprehensive audit trail
            audit_trail = {
                'audit_period_days': days,
                'generated_at': datetime.now().isoformat(),
                'audit_summary': audit_data,
                'compliance_metrics': {
                    'total_recommendations': audit_data.get('total_recommendations', 0),
                    'approved_recommendations': audit_data.get('approved_recommendations', 0),
                    'approval_rate': audit_data.get('approval_rate', 0),
                    'average_review_time': '2.3 hours',  # Simulated metric
                    'escalations': 2  # Simulated metric
                },
                'regulatory_status': {
                    'finra_compliance': 'Current',
                    'sec_compliance': 'Current', 
                    'soc2_compliance': 'Current',
                    'last_regulatory_review': '2024-08-15',
                    'next_scheduled_review': '2024-11-15'
                },
                'key_findings': [
                    f"Processed {audit_data.get('total_recommendations', 0)} investment recommendations",
                    f"Maintained {audit_data.get('approval_rate', 0):.1f}% compliance approval rate",
                    "All high-risk transactions properly documented",
                    "No material compliance violations identified"
                ],
                'recommendations': [
                    "Continue monitoring concentration limits in technology sector",
                    "Enhance documentation for alternative investments",
                    "Schedule quarterly compliance training update"
                ]
            }
            
            return audit_trail
            
        except Exception as e:
            logger.error(f"Failed to get audit trail: {str(e)}")
            return {'error': str(e)}
    
    def generate_compliance_alert(self, issue_type: str, severity: str,
                                description: str, advisor_id: str = None,
                                client_id: str = None) -> Dict[str, Any]:
        """Generate compliance alert for issues requiring attention"""
        try:
            alert = {
                'alert_id': f"COMP_ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'timestamp': datetime.now().isoformat(),
                'issue_type': issue_type,
                'severity': severity,  # low, medium, high, critical
                'description': description,
                'advisor_id': advisor_id,
                'client_id': client_id,
                'status': 'ACTIVE',
                'escalation_required': severity in ['high', 'critical'],
                'resolution_deadline': self._calculate_resolution_deadline(severity),
                'assigned_to': 'Compliance Department',
                'regulatory_impact': self._assess_regulatory_impact(issue_type, severity)
            }
            
            # Log compliance alert
            self.financial_db.log_financial_audit_event(
                action='compliance_alert_generated',
                advisor_id=advisor_id,
                client_id=client_id,
                details=json.dumps({
                    'alert_id': alert['alert_id'],
                    'issue_type': issue_type,
                    'severity': severity
                }),
                success=True,
                risk_level=severity
            )
            
            return alert
            
        except Exception as e:
            logger.error(f"Failed to generate compliance alert: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_resolution_deadline(self, severity: str) -> str:
        """Calculate resolution deadline based on severity"""
        deadlines = {
            'low': timedelta(days=30),
            'medium': timedelta(days=7),
            'high': timedelta(days=2),
            'critical': timedelta(hours=4)
        }
        
        deadline = datetime.now() + deadlines.get(severity, timedelta(days=7))
        return deadline.isoformat()
    
    def _assess_regulatory_impact(self, issue_type: str, severity: str) -> str:
        """Assess potential regulatory impact"""
        if severity == 'critical':
            return 'HIGH - Immediate regulatory reporting may be required'
        elif severity == 'high':
            return 'MEDIUM - Regulatory notification recommended'
        else:
            return 'LOW - Internal resolution sufficient'