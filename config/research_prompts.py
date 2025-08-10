"""
Research Prompts Configuration
Customize these prompts for your specific industry and use case
"""

def get_web_scraping_prompt(company_name: str, industry: str = None) -> str:
    """Get the prompt for web scraping extraction"""
    base_prompt = f"""
    Extract comprehensive information about {company_name}:
    1. Company overview and mission
    2. Products and services offered
    3. Technology stack and tools used
    4. Recent projects and achievements
    5. Leadership team and key executives
    6. News and announcements from the last 12 months
    7. Digital transformation initiatives
    8. Pain points or challenges mentioned
    9. Contact information
    """
    
    # Add industry-specific extraction if provided
    if industry:
        if 'construction' in industry.lower():
            base_prompt += """
    10. Project management tools used (Procore, ACC, Primavera P6, etc.)
    11. Types of construction projects
    12. Safety initiatives and certifications
    """
        elif 'healthcare' in industry.lower():
            base_prompt += """
    10. EHR/EMR systems used
    11. Patient management systems
    12. Compliance and certifications (HIPAA, etc.)
    """
        elif 'technology' in industry.lower():
            base_prompt += """
    10. Development stack and frameworks
    11. Cloud infrastructure providers
    12. Open source contributions
    """
    
    return base_prompt


def get_deep_research_system_prompt(company_name: str, product_name: str = "our solution") -> str:
    """Deprecated: deep research removed in template."""
    return ""


def get_deep_research_user_query(company_name: str, company_data: Dict = None) -> str:
    """Deprecated: deep research removed in template."""
    return ""


def get_industry_pain_points(industry: str) -> List[str]:
    """Get common pain points by industry"""
    pain_points_map = {
        'construction': [
            "Project delays and cost overruns",
            "Knowledge transfer between projects",
            "Risk prediction and mitigation",
            "Document and lessons learned management",
            "Safety incident prevention",
            "Subcontractor coordination",
            "Change order management"
        ],
        'manufacturing': [
            "Supply chain visibility",
            "Quality control and defect tracking",
            "Knowledge management across facilities",
            "Predictive maintenance",
            "Inventory optimization",
            "Compliance tracking",
            "Workforce training and retention"
        ],
        'healthcare': [
            "Patient experience and satisfaction",
            "Clinical workflow efficiency",
            "Regulatory compliance",
            "Cost reduction pressures",
            "Data interoperability",
            "Staff burnout and retention",
            "Quality metrics improvement"
        ],
        'financial services': [
            "Regulatory compliance",
            "Digital transformation",
            "Customer experience",
            "Risk management",
            "Operational efficiency",
            "Data security",
            "Legacy system modernization"
        ],
        'retail': [
            "Omnichannel experience",
            "Inventory management",
            "Customer personalization",
            "Supply chain optimization",
            "Labor management",
            "Loss prevention",
            "Competitive pricing"
        ],
        'technology': [
            "Development velocity",
            "Technical debt",
            "Talent acquisition and retention",
            "Security and compliance",
            "Customer churn",
            "Product-market fit",
            "Scaling challenges"
        ]
    }
    
    # Default pain points if industry not mapped
    default_pain_points = [
        "Operational efficiency",
        "Digital transformation",
        "Data management and insights",
        "Process optimization",
        "Compliance and risk management",
        "Customer experience",
        "Cost reduction"
    ]
    
    # Find matching industry
    industry_lower = industry.lower() if industry else ''
    for key, points in pain_points_map.items():
        if key in industry_lower:
            return points
    
    return default_pain_points


def get_sales_talking_points(industry: str, company_size: str = None) -> List[str]:
    """Get sales talking points based on industry and company size"""
    base_points = [
        "Reduce operational costs by up to 30% through intelligent automation",
        "Improve decision-making with real-time data insights",
        "Streamline workflows and eliminate manual processes",
        "Ensure compliance and reduce risk exposure",
        "Scale efficiently as your business grows"
    ]
    
    # Add industry-specific points
    if industry:
        if 'construction' in industry.lower():
            base_points.extend([
                "Capture and apply lessons learned across all projects",
                "Predict and prevent project delays with AI-powered insights",
                "Improve safety outcomes through predictive analytics",
                "Integrate seamlessly with Procore, Primavera P6, and other tools"
            ])
        elif 'healthcare' in industry.lower():
            base_points.extend([
                "Improve patient outcomes through data-driven insights",
                "Reduce administrative burden on clinical staff",
                "Ensure HIPAA compliance and data security",
                "Integrate with existing EHR/EMR systems"
            ])
    
    # Add size-specific points
    if company_size == 'enterprise':
        base_points.extend([
            "Enterprise-grade security and compliance",
            "Dedicated success team and SLA guarantees",
            "Custom integrations and white-glove onboarding"
        ])
    elif company_size == 'mid-market':
        base_points.extend([
            "Quick implementation with proven ROI in 90 days",
            "Flexible pricing that scales with your growth",
            "Pre-built integrations with common tools"
        ])
    
    return base_points


# Import typing for type hints
from typing import Dict, List