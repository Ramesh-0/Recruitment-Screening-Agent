"""
Offer Letter Generator
Generates professional offer letters for selected candidates
"""

from datetime import datetime, timedelta

def generate_offer_letter(candidate_data, job_details, salary_data, company_info=None):
    """
    Generate a professional offer letter
    
    Args:
        candidate_data: Dict with name, email, address
        job_details: Dict with title, department, start_date, manager
        salary_data: Dict with salary, bonus, equity, benefits
        company_info: Dict with company name, address, HR contact
    
    Returns:
        Formatted offer letter text
    """
    
    # Default company info
    if not company_info:
        company_info = {
            'name': 'TechCorp Inc.',
            'address': '123 Innovation Drive, Tech City, TC 12345',
            'hr_contact': 'hr@techcorp.com',
            'hr_phone': '(555) 123-4567'
        }
    
    # Calculate start date if not provided
    if 'start_date' not in job_details or not job_details['start_date']:
        start_date = (datetime.now() + timedelta(days=14)).strftime("%B %d, %Y")
    else:
        start_date = job_details['start_date']
    
    offer_date = datetime.now().strftime("%B %d, %Y")
    
    # Format salary with commas
    annual_salary = f"${salary_data.get('salary', 100000):,}"
    signing_bonus = salary_data.get('signing_bonus', 0)
    bonus_text = f" plus a signing bonus of ${signing_bonus:,}" if signing_bonus > 0 else ""
    
    # Generate equity info if provided
    equity = salary_data.get('equity', {})
    equity_text = ""
    if equity and equity.get('shares', 0) > 0:
        equity_text = f"""
**Equity Compensation:**
You will be granted {equity.get('shares', 0):,} stock options at a strike price of ${equity.get('strike_price', 0):.2f} per share, subject to a {equity.get('vesting_schedule', '4-year vesting schedule with 1-year cliff')}.
"""
    
    # Benefits section
    benefits = salary_data.get('benefits', [])
    if not benefits:
        benefits = [
            "Comprehensive health, dental, and vision insurance",
            "401(k) retirement plan with company match",
            "Flexible PTO policy",
            "Professional development stipend",
            "Remote work options"
        ]
    
    benefits_list = "\n".join([f"• {benefit}" for benefit in benefits])
    
    # Generate offer letter
    offer_letter = f"""
{'='*80}
                              EMPLOYMENT OFFER LETTER
{'='*80}

**{company_info['name']}**
{company_info['address']}

**Date:** {offer_date}

**To:** {candidate_data.get('name', 'Candidate Name')}
**Email:** {candidate_data.get('email', 'candidate@email.com')}

Dear {candidate_data.get('name', 'Candidate').split()[0]},

We are pleased to extend to you an offer of employment with {company_info['name']} for the position of **{job_details.get('title', 'Software Engineer')}** in our {job_details.get('department', 'Engineering')} department.

**Position Details:**

• **Job Title:** {job_details.get('title', 'Software Engineer')}
• **Department:** {job_details.get('department', 'Engineering')}
• **Reports To:** {job_details.get('manager', 'Engineering Manager')}
• **Start Date:** {start_date}
• **Employment Type:** {job_details.get('employment_type', 'Full-time')}
• **Location:** {job_details.get('location', 'Hybrid - Office/Remote')}

**Compensation:**

• **Annual Salary:** {annual_salary}{bonus_text}
• **Payment Schedule:** {salary_data.get('payment_schedule', 'Bi-weekly')}
• **Performance Bonus:** {salary_data.get('performance_bonus', 'Eligible for annual performance-based bonus up to 15% of base salary')}
{equity_text}

**Benefits Package:**

{benefits_list}

**Employment Terms:**

This is an at-will employment relationship, meaning either you or {company_info['name']} may terminate the relationship at any time, with or without cause or notice.

This offer is contingent upon:
• Successful completion of background check
• Verification of eligibility to work in the United States
• Signing of our standard Employee Agreement (including confidentiality and IP assignment clauses)

**Next Steps:**

To accept this offer:
1. Sign and return this letter by {(datetime.now() + timedelta(days=7)).strftime("%B %d, %Y")}
2. Complete the attached onboarding documents
3. Contact HR to schedule your first day

We are excited about the possibility of you joining our team and believe you will make significant contributions to {company_info['name']}.

Please feel free to contact me at {company_info['hr_contact']} or {company_info['hr_phone']} if you have any questions.

We look forward to working with you!

Sincerely,

_______________________________
HR Department
{company_info['name']}


**ACCEPTANCE**

I, {candidate_data.get('name', '_____________________')}, accept the terms and conditions of employment as outlined in this offer letter.

Signature: _______________________________    Date: _______________


{'='*80}
                    This offer is confidential and valid for 7 days
{'='*80}
"""
    
    return {
        'offer_letter': offer_letter,
        'offer_id': generate_offer_id(),
        'generated_at': datetime.now().isoformat(),
        'valid_until': (datetime.now() + timedelta(days=7)).isoformat(),
        'status': 'pending'
    }


def generate_offer_id():
    """Generate unique offer ID"""
    import random
    import string
    timestamp = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"OFFER-{timestamp}-{random_str}"


def generate_quick_offer(candidate_name, job_title, salary):
    """Generate a quick offer with minimal details"""
    candidate_data = {'name': candidate_name, 'email': 'candidate@example.com'}
    job_details = {'title': job_title, 'department': 'Engineering', 'start_date': None}
    salary_data = {'salary': salary}
    
    return generate_offer_letter(candidate_data, job_details, salary_data)
