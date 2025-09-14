#!/usr/bin/env python3
"""
Financial AI Pod - Investment Research Platform
Provides REST API for investment analysis and AI agent orchestration
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import json

# Import our custom financial modules
from agents.research_agent import ResearchAgent
from agents.risk_agent import RiskAssessmentAgent
from agents.report_agent import ReportGenerationAgent
from agents.compliance_agent import ComplianceAgent
from database.financial_db_manager import FinancialDataManager
from database.chromadb_manager import FinancialKnowledgeStore
from utils.security import SOC2SecurityManager
from utils.monitoring import FinancialAIMonitoring

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app, supports_credentials=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/financial_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize system components
try:
    # Database managers
    financial_db = FinancialDataManager()
    knowledge_store = FinancialKnowledgeStore()
    
    # Security and monitoring
    security_manager = SOC2SecurityManager()
    monitoring = FinancialAIMonitoring()
    
    # AI Agents for financial services
    research_agent = ResearchAgent(knowledge_store, financial_db)
    risk_agent = RiskAssessmentAgent(knowledge_store, financial_db)
    report_agent = ReportGenerationAgent(knowledge_store, financial_db)
    compliance_agent = ComplianceAgent(knowledge_store, financial_db)
    
    logger.info("Financial AI system components initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to initialize financial system components: {str(e)}")
    raise

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connections
        financial_db.health_check()
        knowledge_store.health_check()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'service': 'financial_ai_platform',
            'components': {
                'financial_database': 'ok',
                'knowledge_store': 'ok',
                'ai_agents': 'ok',
                'security': 'ok'
            }
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/advisor/start-session', methods=['POST'])
def start_advisor_session():
    """Initialize a new advisor session"""
    try:
        data = request.get_json()
        advisor_id = data.get('advisor_id')
        client_id = data.get('client_id', None)
        
        if not advisor_id:
            return jsonify({'error': 'Advisor ID required'}), 400
        
        # Create secure session with SOC2 compliance
        session_data = security_manager.create_advisor_session(advisor_id, client_id)
        session['advisor_id'] = advisor_id
        session['client_id'] = client_id
        session['session_token'] = session_data['token']
        
        # Log session start for compliance audit
        security_manager.log_advisor_access(
            advisor_id=advisor_id,
            client_id=client_id,
            action='session_start',
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'session_id': session_data['session_id'],
            'advisor_id': advisor_id,
            'client_id': client_id,
            'message': 'Financial advisory session started successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to start advisor session: {str(e)}")
        return jsonify({'error': 'Failed to start session'}), 500

@app.route('/api/research/analyze', methods=['POST'])
def analyze_investment():
    """Analyze investment opportunity using AI research agent"""
    try:
        data = request.get_json()
        advisor_id = session.get('advisor_id')
        client_id = session.get('client_id')
        query = data.get('query', '')
        ticker = data.get('ticker', '')
        analysis_type = data.get('analysis_type', 'comprehensive')
        
        if not advisor_id:
            return jsonify({'error': 'No active advisor session'}), 401
        
        if not query and not ticker:
            return jsonify({'error': 'Query or ticker symbol is required'}), 400
        
        # Security: Encrypt and audit log the interaction
        encrypted_query = security_manager.encrypt_client_data(query)
        security_manager.log_investment_research(
            advisor_id=advisor_id,
            client_id=client_id,
            query=query,
            ticker=ticker,
            ip_address=request.remote_addr
        )
        
        # Step 1: Research Agent conducts market analysis
        research_result = research_agent.conduct_investment_research(
            query=query,
            ticker=ticker,
            analysis_type=analysis_type,
            client_context={'advisor_id': advisor_id, 'client_id': client_id}
        )
        
        # Step 2: Risk Agent assesses investment risks
        risk_assessment = risk_agent.assess_investment_risk(
            ticker=ticker,
            research_data=research_result,
            client_risk_profile=data.get('client_risk_profile', 'moderate')
        )
        
        # Step 3: Check regulatory compliance
        compliance_check = compliance_agent.verify_investment_suitability(
            advisor_id=advisor_id,
            client_id=client_id,
            investment_data=research_result,
            risk_assessment=risk_assessment
        )
        
        # Prepare comprehensive investment analysis response
        response = {
            'investment_analysis': {
                'ticker': ticker,
                'company_overview': research_result.get('company_info', {}),
                'financial_metrics': research_result.get('financial_metrics', {}),
                'market_position': research_result.get('market_analysis', {}),
                'growth_prospects': research_result.get('growth_analysis', {}),
                'ai_recommendation': research_result.get('recommendation', {}),
                'confidence_score': research_result.get('confidence_score', 0)
            },
            'risk_assessment': {
                'overall_risk_score': risk_assessment.get('risk_score', 0),
                'risk_level': risk_assessment.get('risk_level', 'unknown'),
                'risk_factors': risk_assessment.get('risk_factors', []),
                'portfolio_impact': risk_assessment.get('portfolio_impact', {}),
                'var_analysis': risk_assessment.get('var_analysis', {}),
                'stress_test_results': risk_assessment.get('stress_tests', {})
            },
            'compliance_status': {
                'suitability_check': compliance_check.get('suitable', False),
                'regulatory_warnings': compliance_check.get('warnings', []),
                'required_disclosures': compliance_check.get('disclosures', []),
                'documentation_needed': compliance_check.get('documentation', [])
            },
            'research_sources': research_result.get('sources', []),
            'analysis_id': research_result.get('analysis_id', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        # Store analysis in database for audit trail
        financial_db.store_investment_analysis(
            advisor_id=advisor_id,
            client_id=client_id,
            analysis_data=response,
            compliance_status=compliance_check
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Failed to analyze investment: {str(e)}")
        return jsonify({'error': 'Investment analysis failed'}), 500

@app.route('/api/portfolio/analyze', methods=['POST'])
def analyze_portfolio():
    """Analyze client portfolio using AI risk assessment"""
    try:
        data = request.get_json()
        advisor_id = session.get('advisor_id')
        client_id = session.get('client_id')
        portfolio_holdings = data.get('portfolio', [])
        
        if not advisor_id or not client_id:
            return jsonify({'error': 'No active client session'}), 401
        
        if not portfolio_holdings:
            return jsonify({'error': 'Portfolio holdings required'}), 400
        
        # Security check and audit logging
        if not security_manager.verify_client_access(advisor_id, client_id, session.get('session_token')):
            return jsonify({'error': 'Unauthorized portfolio access'}), 403
        
        # Risk Agent performs comprehensive portfolio analysis
        portfolio_analysis = risk_agent.analyze_portfolio(
            client_id=client_id,
            holdings=portfolio_holdings,
            market_context=data.get('market_context', {})
        )
        
        # Research Agent provides market intelligence
        market_intelligence = research_agent.get_market_intelligence(
            portfolio_holdings=portfolio_holdings,
            analysis_focus='portfolio_optimization'
        )
        
        # Compliance check for portfolio recommendations
        compliance_review = compliance_agent.review_portfolio_recommendations(
            advisor_id=advisor_id,
            client_id=client_id,
            portfolio_data=portfolio_analysis,
            recommendations=market_intelligence.get('recommendations', [])
        )
        
        response = {
            'portfolio_health': {
                'overall_score': portfolio_analysis.get('health_score', 0),
                'diversification_score': portfolio_analysis.get('diversification', {}),
                'risk_metrics': portfolio_analysis.get('risk_metrics', {}),
                'performance_attribution': portfolio_analysis.get('performance', {}),
                'sector_allocation': portfolio_analysis.get('sector_breakdown', {}),
                'asset_allocation': portfolio_analysis.get('asset_allocation', {})
            },
            'market_intelligence': {
                'market_outlook': market_intelligence.get('market_outlook', {}),
                'sector_trends': market_intelligence.get('sector_analysis', {}),
                'opportunities': market_intelligence.get('opportunities', []),
                'threats': market_intelligence.get('threats', []),
                'rebalancing_suggestions': market_intelligence.get('rebalancing', [])
            },
            'compliance_review': compliance_review,
            'action_items': portfolio_analysis.get('action_items', []),
            'client_id': client_id,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        # Store portfolio analysis
        financial_db.store_portfolio_analysis(
            client_id=client_id,
            advisor_id=advisor_id,
            analysis_data=response
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Failed to analyze portfolio: {str(e)}")
        return jsonify({'error': 'Portfolio analysis failed'}), 500

@app.route('/api/reports/generate', methods=['POST'])
def generate_investment_report():
    """Generate professional investment report"""
    try:
        data = request.get_json()
        advisor_id = session.get('advisor_id')
        client_id = session.get('client_id')
        report_type = data.get('report_type', 'investment_summary')
        analysis_ids = data.get('analysis_ids', [])
        
        if not advisor_id:
            return jsonify({'error': 'No active advisor session'}), 401
        
        # Security and compliance check
        security_manager.log_report_generation(
            advisor_id=advisor_id,
            client_id=client_id,
            report_type=report_type,
            ip_address=request.remote_addr
        )
        
        # Report Agent generates comprehensive report
        report_data = report_agent.generate_client_report(
            client_id=client_id,
            advisor_id=advisor_id,
            report_type=report_type,
            analysis_data=analysis_ids,
            customization=data.get('customization', {})
        )
        
        # Compliance Agent ensures regulatory compliance
        compliance_validation = compliance_agent.validate_report_compliance(
            report_data=report_data,
            advisor_id=advisor_id,
            client_id=client_id
        )
        
        response = {
            'report_id': report_data.get('report_id', ''),
            'report_type': report_type,
            'executive_summary': report_data.get('executive_summary', ''),
            'investment_analysis': report_data.get('investment_analysis', {}),
            'risk_assessment': report_data.get('risk_assessment', {}),
            'recommendations': report_data.get('recommendations', []),
            'disclosures': report_data.get('disclosures', []),
            'charts_data': report_data.get('visualizations', {}),
            'compliance_validated': compliance_validation.get('compliant', False),
            'generation_timestamp': datetime.now().isoformat(),
            'advisor_id': advisor_id,
            'client_id': client_id
        }
        
        # Store report for audit trail
        financial_db.store_generated_report(
            report_id=report_data.get('report_id', ''),
            advisor_id=advisor_id,
            client_id=client_id,
            report_data=response,
            compliance_status=compliance_validation
        )
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Failed to generate report: {str(e)}")
        return jsonify({'error': 'Report generation failed'}), 500

@app.route('/api/knowledge/search', methods=['POST'])
def search_financial_knowledge():
    """Search financial knowledge base and market intelligence"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        search_type = data.get('search_type', 'general')  # general, sector, company, economic
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Research Agent searches knowledge base
        search_results = research_agent.search_financial_knowledge(
            query=query,
            search_type=search_type,
            context=data.get('context', {})
        )
        
        return jsonify({
            'query': query,
            'search_type': search_type,
            'results': search_results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Failed to search financial knowledge: {str(e)}")
        return jsonify({'error': 'Knowledge search failed'}), 500

@app.route('/api/admin/dashboard', methods=['GET'])
def get_admin_dashboard():
    """Get administrative dashboard data for platform monitoring"""
    try:
        # This would require admin authentication in production
        dashboard_data = monitoring.get_financial_platform_dashboard()
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve admin dashboard: {str(e)}")
        return jsonify({'error': 'Failed to retrieve dashboard'}), 500

@app.route('/api/compliance/audit', methods=['GET'])
def get_compliance_audit():
    """Retrieve compliance audit data"""
    try:
        # This would require compliance officer authentication in production
        audit_data = compliance_agent.get_audit_trail(
            days=int(request.args.get('days', 30))
        )
        
        return jsonify(audit_data), 200
        
    except Exception as e:
        logger.error(f"Failed to retrieve compliance audit: {str(e)}")
        return jsonify({'error': 'Audit retrieval failed'}), 500

# Error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Financial API endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Financial platform internal server error: {str(error)}")
    return jsonify({'error': 'Financial platform internal server error'}), 500

# Application startup

if __name__ == '__main__':
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Start the Financial AI Platform
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Financial AI Investment Platform on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info("Financial agents: Research, Risk Assessment, Report Generation, Compliance")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )