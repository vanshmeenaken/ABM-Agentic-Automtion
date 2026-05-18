"""
Test Persona Classifier Agent with mocked Claude responses.
Shows segmentation in action without waiting for Claude CLI.
"""

import json
from agents.schemas import ClassifiedProspect, PersonaAssignment, PersonaClassifierOutput

# Mock Claude responses for test cases
MOCK_RESPONSES = {
    "VP of Engineering": {
        "persona": "Director",
        "confidence_score": 92,
        "seniority_level": "Executive",
        "function": "engineering",
        "rationale": "VP title indicates executive seniority. Engineering function. Clear match to Director persona.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "CXO",
            "confidence_score": 70,
            "rationale": "VP can influence C-level strategic decisions"
        }
    },
    "CEO of my life": {
        "persona": "Unknown",
        "confidence_score": 8,
        "seniority_level": "Unknown",
        "function": "Unknown",
        "rationale": "This appears to be a joke/fake title ('CEO of my life'). Not a legitimate business role. Recommend filtering out.",
        "needs_review": True,
        "secondary_persona": None
    },
    "Head Chef": {
        "persona": "Unknown",
        "confidence_score": 15,
        "seniority_level": "Manager-level",
        "function": "Hospitality/Food Service",
        "rationale": "Head Chef is a hospitality/food service role, not a B2B decision-maker. Non-target industry. Recommend removing from prospect list.",
        "needs_review": True,
        "secondary_persona": None
    },
    "Growth Lead": {
        "persona": "Manager",
        "confidence_score": 68,
        "seniority_level": "Manager",
        "function": "Business Development/Growth",
        "rationale": "Growth Lead suggests mid-level role managing initiatives. Could be Manager or Director depending on company stage. Moderate confidence.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "Director",
            "confidence_score": 60,
            "rationale": "In some startups, Growth Leads report to C-level or are director-equivalent"
        }
    },
    "Marketing Manager": {
        "persona": "Manager",
        "confidence_score": 87,
        "seniority_level": "Manager",
        "function": "marketing",
        "rationale": "Manager title indicates management level. Marketing function. Clear match to Manager persona.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "Director",
            "confidence_score": 68,
            "rationale": "Could be Director-level in smaller companies"
        }
    },
    "Fractional Chief Growth & Revenue Strategy Officer": {
        "persona": "CXO",
        "confidence_score": 92,
        "seniority_level": "Executive",
        "function": "Strategy/Growth",
        "rationale": "Chief-level title (even fractional) indicates C-Suite seniority. Growth & Revenue Strategy = executive function. Clear match to CXO persona.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "Director",
            "confidence_score": 75,
            "rationale": "Fractional roles sometimes operate at Director level depending on org structure"
        }
    },
    "Group Head of Strategic Transformation & Market Expansion": {
        "persona": "Director",
        "confidence_score": 88,
        "seniority_level": "Executive",
        "function": "Strategy",
        "rationale": "Group Head = executive-level role. Strategic Transformation = high-level function. Strong match to Director persona, could be C-level in some orgs.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "CXO",
            "confidence_score": 70,
            "rationale": "In large enterprises, Group Heads report to C-suite"
        }
    },
    "Associate Partner, Commercial Due Diligence & Value Creation": {
        "persona": "Director",
        "confidence_score": 82,
        "seniority_level": "Director",
        "function": "Finance/Strategy",
        "rationale": "Partner-track role in professional services (consulting/investment). Associate Partner = Director-equivalent level. M&A/Due Diligence = strategic function.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "Manager",
            "confidence_score": 65,
            "rationale": "Junior partners sometimes operate at senior manager level"
        }
    },
    "Vice President, New Ventures & Emerging Business Models": {
        "persona": "Director",
        "confidence_score": 95,
        "seniority_level": "Executive",
        "function": "Strategy/Business Development",
        "rationale": "VP title = executive seniority. New Ventures = strategic role. Highest clarity and confidence. Clear Director (almost C-level) match.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "CXO",
            "confidence_score": 75,
            "rationale": "VP of New Ventures often reports to CEO and influences strategy"
        }
    },
    "Global Lead, Enterprise Intelligence & Competitive Foresight": {
        "persona": "Director",
        "confidence_score": 78,
        "seniority_level": "Director",
        "function": "Strategy",
        "rationale": "Global Lead = senior management. Enterprise Intelligence = strategic insight function. Good match to Director, possibly Manager in some contexts.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "Manager",
            "confidence_score": 70,
            "rationale": "Could be senior manager in matrix orgs or younger companies"
        }
    },
    "Principal, Market Access Strategy & Portfolio Expansion": {
        "persona": "Director",
        "confidence_score": 84,
        "seniority_level": "Director",
        "function": "Strategy",
        "rationale": "Principal = senior director-level title (common in consulting/pharma). Market Access & Portfolio = strategic function. Clear Director match.",
        "needs_review": False,
        "secondary_persona": {
            "persona": "CXO",
            "confidence_score": 68,
            "rationale": "Principals in some organizations are C-level equivalent"
        }
    },
    "Business Enthusiast": {
        "persona": "Unknown",
        "confidence_score": 12,
        "seniority_level": "Unknown",
        "function": "Unknown",
        "rationale": "Not a legitimate job title. 'Business Enthusiast' is vague/generic/fake. Not a recognized business role. Recommend filtering out.",
        "needs_review": True,
        "secondary_persona": None
    },
    "Growth Ninja": {
        "persona": "Unknown",
        "confidence_score": 18,
        "seniority_level": "Unknown",
        "function": "Growth/Marketing",
        "rationale": "'Ninja' is a playful/fake job title convention (Growth Ninja, DevOps Ninja). While it may appear in some startup contexts, it's not a legitimate B2B decision-maker title. Low confidence.",
        "needs_review": True,
        "secondary_persona": None
    },
    "Visionary Leader": {
        "persona": "Unknown",
        "confidence_score": 11,
        "seniority_level": "Unknown",
        "function": "Unknown",
        "rationale": "Generic/vague title. 'Visionary Leader' is not a recognized business role. Could apply to anyone. Not specific enough to classify as a buyer persona. Recommend filtering.",
        "needs_review": True,
        "secondary_persona": None
    },
    "Strategic Thinker": {
        "persona": "Unknown",
        "confidence_score": 9,
        "seniority_level": "Unknown",
        "function": "Unknown",
        "rationale": "Generic descriptor, not a job title. 'Strategic Thinker' could be anyone at any level. No legitimate business role mapping. Recommend filtering out.",
        "needs_review": True,
        "secondary_persona": None
    },
}

def test_mock_classification():
    """Test classification with mocked Claude responses."""

    test_cases = [
        {
            'email': 'john@techcorp.com',
            'designation': 'VP of Engineering',
            'company_name': 'TechCorp Inc',
            'expected_persona': 'Director',
            'expected_confidence_min': 85,
        },
        {
            'email': 'fake@test.com',
            'designation': 'CEO of my life',
            'company_name': 'MyLife Inc',
            'expected_persona': 'Unknown',
            'expected_confidence_max': 20,
        },
        {
            'email': 'chef@restaurant.com',
            'designation': 'Head Chef',
            'company_name': 'Restaurant XYZ',
            'expected_persona': 'Unknown',
            'expected_confidence_max': 30,
        },
        {
            'email': 'growth@startup.com',
            'designation': 'Growth Lead',
            'company_name': 'Startup Co',
            'expected_persona': 'Manager',
            'expected_confidence_min': 60,
        },
        {
            'email': 'jane@marketing.com',
            'designation': 'Marketing Manager',
            'company_name': 'MarketingCo',
            'expected_persona': 'Manager',
            'expected_confidence_min': 80,
        },
        {
            'email': 'fractional@consulting.com',
            'designation': 'Fractional Chief Growth & Revenue Strategy Officer',
            'company_name': 'Consulting Firm',
            'expected_persona': 'CXO',
            'expected_confidence_min': 85,
        },
        {
            'email': 'grouphead@enterprise.com',
            'designation': 'Group Head of Strategic Transformation & Market Expansion',
            'company_name': 'Enterprise Corp',
            'expected_persona': 'Director',
            'expected_confidence_min': 80,
        },
        {
            'email': 'partner@advisory.com',
            'designation': 'Associate Partner, Commercial Due Diligence & Value Creation',
            'company_name': 'Advisory Partners',
            'expected_persona': 'Director',
            'expected_confidence_min': 75,
        },
        {
            'email': 'vp.ventures@tech.com',
            'designation': 'Vice President, New Ventures & Emerging Business Models',
            'company_name': 'Tech Innovations',
            'expected_persona': 'Director',
            'expected_confidence_min': 90,
        },
        {
            'email': 'globallead@intel.com',
            'designation': 'Global Lead, Enterprise Intelligence & Competitive Foresight',
            'company_name': 'Intelligence Co',
            'expected_persona': 'Director',
            'expected_confidence_min': 75,
        },
        {
            'email': 'principal@strategy.com',
            'designation': 'Principal, Market Access Strategy & Portfolio Expansion',
            'company_name': 'Strategy Group',
            'expected_persona': 'Director',
            'expected_confidence_min': 80,
        },
        {
            'email': 'enthusiast@fake.com',
            'designation': 'Business Enthusiast',
            'company_name': 'Fake Corp',
            'expected_persona': 'Unknown',
            'expected_confidence_max': 20,
        },
        {
            'email': 'ninja@startup.com',
            'designation': 'Growth Ninja',
            'company_name': 'Startup Ninja',
            'expected_persona': 'Unknown',
            'expected_confidence_max': 25,
        },
        {
            'email': 'visionary@fake.com',
            'designation': 'Visionary Leader',
            'company_name': 'Vision Inc',
            'expected_persona': 'Unknown',
            'expected_confidence_max': 20,
        },
        {
            'email': 'thinker@fake.com',
            'designation': 'Strategic Thinker',
            'company_name': 'Think Tank',
            'expected_persona': 'Unknown',
            'expected_confidence_max': 15,
        },
    ]

    print("\n" + "="*90)
    print("PERSONA CLASSIFIER AGENT — MOCK TEST (15 COMPREHENSIVE CASES)")
    print("="*90)

    classified = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*90}")
        print(f"TEST {i}: {test_case['designation']} at {test_case['company_name']}")
        print(f"{'='*90}")

        # Get mock response
        response = MOCK_RESPONSES.get(
            test_case['designation'],
            {"persona": "Unknown", "confidence_score": 0, "needs_review": True}
        )

        # Create ClassifiedProspect
        primary = PersonaAssignment(
            persona=response['persona'],
            confidence_score=response['confidence_score'],
            rationale=response['rationale'],
        )

        secondary = None
        if response.get('secondary_persona'):
            sec = response['secondary_persona']
            secondary = PersonaAssignment(
                persona=sec['persona'],
                confidence_score=sec['confidence_score'],
                rationale=sec['rationale'],
            )

        prospect = ClassifiedProspect(
            email=test_case['email'],
            designation=test_case['designation'],
            company_name=test_case['company_name'],
            primary_persona=primary,
            secondary_persona=secondary,
            seniority_level=response.get('seniority_level', 'Unknown'),
            function=response.get('function', 'Unknown'),
            needs_review=response['needs_review'],
        )

        classified.append(prospect)

        # Print results
        print(f"\n[+] Email: {prospect.email}")
        print(f"[+] Designation: {prospect.designation}")
        print(f"[+] Company: {prospect.company_name}")
        print(f"\n[CLASSIFICATION]:")
        print(f"  PRIMARY PERSONA: {prospect.primary_persona.persona}")
        print(f"  CONFIDENCE: {prospect.primary_persona.confidence_score}%")
        print(f"  SENIORITY LEVEL: {prospect.seniority_level}")
        print(f"  FUNCTION: {prospect.function}")
        print(f"  NEEDS REVIEW: {prospect.needs_review}")

        if prospect.secondary_persona:
            print(f"\n  SECONDARY PERSONA: {prospect.secondary_persona.persona}")
            print(f"  Secondary Confidence: {prospect.secondary_persona.confidence_score}%")

        print(f"\n[RATIONALE]:")
        print(f"  {prospect.primary_persona.rationale}")

        # Verify expectations
        if test_case['expected_persona'] == prospect.primary_persona.persona:
            print(f"\n[PASS] Persona is '{test_case['expected_persona']}' (expected)")
        else:
            print(f"\n[FAIL] Persona is '{prospect.primary_persona.persona}' but expected '{test_case['expected_persona']}'")

        if 'expected_confidence_min' in test_case:
            if prospect.primary_persona.confidence_score >= test_case['expected_confidence_min']:
                print(f"[PASS] Confidence {prospect.primary_persona.confidence_score}% >= {test_case['expected_confidence_min']}%")
            else:
                print(f"[FAIL] Confidence {prospect.primary_persona.confidence_score}% < {test_case['expected_confidence_min']}%")

        if 'expected_confidence_max' in test_case:
            if prospect.primary_persona.confidence_score <= test_case['expected_confidence_max']:
                print(f"[PASS] Confidence {prospect.primary_persona.confidence_score}% <= {test_case['expected_confidence_max']}%")
            else:
                print(f"[FAIL] Confidence {prospect.primary_persona.confidence_score}% > {test_case['expected_confidence_max']}%")

    # Summary statistics
    print(f"\n\n{'='*90}")
    print("SUMMARY STATISTICS")
    print(f"{'='*90}\n")

    persona_dist = {}
    confidence_scores = []
    low_confidence = 0

    for prospect in classified:
        persona = prospect.primary_persona.persona
        persona_dist[persona] = persona_dist.get(persona, 0) + 1
        confidence_scores.append(prospect.primary_persona.confidence_score)
        if prospect.primary_persona.confidence_score < 60:
            low_confidence += 1

    print(f"Total Classified: {len(classified)}")
    print(f"Average Confidence: {int(sum(confidence_scores) / len(confidence_scores))}%")
    print(f"Low Confidence (<60%): {low_confidence}")
    print(f"\nPersona Distribution:")
    for persona, count in sorted(persona_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"  {persona}: {count} prospect(s)")

    print(f"\n{'='*90}")
    print("SEGMENTATION ANALYSIS")
    print(f"{'='*90}\n")

    print("[X] UNCONTACTABLE (Unknown segment):")
    for p in classified:
        if p.primary_persona.persona == 'Unknown':
            print(f"  [REJECT] {p.email} — {p.designation} at {p.company_name}")
            print(f"      Reason: {p.primary_persona.rationale[:80]}...")

    print("\n[OK] CONTACTABLE SEGMENTS:")
    for p in classified:
        if p.primary_persona.persona != 'Unknown':
            icon = "[STAR]" if p.primary_persona.confidence_score >= 80 else "[+]"
            print(f"  {icon} {p.email} — {p.designation}")
            print(f"      Persona: {p.primary_persona.persona} ({p.primary_persona.confidence_score}%)")
            print(f"      Deal Size: ", end="")
            if p.primary_persona.persona == 'CXO':
                print("$100K+")
            elif p.primary_persona.persona == 'Director':
                print("$25K-$100K")
            elif p.primary_persona.persona == 'Manager':
                print("$5K-$25K")
            else:
                print("$0-$5K (research only)")

def test_campaign_fit_validation():
    """Test campaign fit validation for K-12 Education campaign."""

    # Campaign context: K-12 Education
    # Preferred functions: Curriculum, Instruction, Education Technology, School Administration
    # Avoid: Finance (unless CFO), HR, Operations

    campaign_fit_responses = {
        "VP of Curriculum Development": {
            "persona": "Director",
            "confidence_score": 94,
            "seniority_level": "Executive",
            "function": "Education/Curriculum",
            "rationale": "VP of Curriculum is a key decision-maker in K-12 education.",
            "needs_review": False,
            "campaign_fit_score": 95,
            "campaign_fit_valid": True,
            "campaign_fit_rationale": "Perfect fit for K-12 education campaign. Curriculum development is core to education institutions.",
            "secondary_persona": {
                "persona": "CXO",
                "confidence_score": 72,
                "rationale": "VP can influence strategic education initiatives"
            }
        },
        "Finance Director": {
            "persona": "Director",
            "confidence_score": 90,
            "seniority_level": "Executive",
            "function": "Finance",
            "rationale": "Finance Director is executive-level seniority.",
            "needs_review": False,
            "campaign_fit_score": 45,
            "campaign_fit_valid": False,
            "campaign_fit_rationale": "While Director-level, Finance function is not a primary target for K-12 education solutions (unless financial management software). Better to focus on curriculum/instruction roles.",
            "secondary_persona": None
        },
        "Head of Instruction & Learning": {
            "persona": "Director",
            "confidence_score": 92,
            "seniority_level": "Executive",
            "function": "Education/Instruction",
            "rationale": "Head of Instruction is core education decision-maker.",
            "needs_review": False,
            "campaign_fit_score": 98,
            "campaign_fit_valid": True,
            "campaign_fit_rationale": "Excellent fit. Instruction/learning is core function for K-12 education institutions.",
            "secondary_persona": None
        },
        "Chief Learning Officer": {
            "persona": "CXO",
            "confidence_score": 96,
            "seniority_level": "C-Suite",
            "function": "Education/Strategy",
            "rationale": "CLO is C-level role focused on learning and education strategy.",
            "needs_review": False,
            "campaign_fit_score": 99,
            "campaign_fit_valid": True,
            "campaign_fit_rationale": "Perfect fit. CLO directly responsible for education strategy and curriculum decisions.",
            "secondary_persona": None
        },
        "HR Manager": {
            "persona": "Manager",
            "confidence_score": 85,
            "seniority_level": "Manager",
            "function": "Human Resources",
            "rationale": "HR Manager is mid-level role in HR function.",
            "needs_review": False,
            "campaign_fit_score": 30,
            "campaign_fit_valid": False,
            "campaign_fit_rationale": "HR function is not aligned with K-12 education solutions. Focus should be on curriculum/instruction/learning roles.",
            "secondary_persona": None
        },
        "Educational Technology Coordinator": {
            "persona": "Manager",
            "confidence_score": 78,
            "seniority_level": "Manager",
            "function": "Education Technology",
            "rationale": "EdTech Coordinator manages technology adoption in education.",
            "needs_review": False,
            "campaign_fit_score": 92,
            "campaign_fit_valid": True,
            "campaign_fit_rationale": "Strong fit for K-12 education. EdTech adoption is key to modern education solutions.",
            "secondary_persona": None
        },
        "Principal": {
            "persona": "Director",
            "confidence_score": 88,
            "seniority_level": "Executive",
            "function": "School Administration",
            "rationale": "Principal is school leader with authority over education decisions.",
            "needs_review": False,
            "campaign_fit_score": 96,
            "campaign_fit_valid": True,
            "campaign_fit_rationale": "Excellent fit. Principal is key decision-maker for school operations and curriculum implementation.",
            "secondary_persona": None
        },
    }

    test_cases_k12 = [
        {
            'email': 'alice@school.edu',
            'designation': 'VP of Curriculum Development',
            'company_name': 'Jefferson High School',
            'expected_persona': 'Director',
            'expected_campaign_fit_min': 90,
        },
        {
            'email': 'bob@school.edu',
            'designation': 'Finance Director',
            'company_name': 'Lincoln Middle School',
            'expected_persona': 'Director',
            'expected_campaign_fit_max': 50,
        },
        {
            'email': 'carol@school.edu',
            'designation': 'Head of Instruction & Learning',
            'company_name': 'Roosevelt Elementary',
            'expected_persona': 'Director',
            'expected_campaign_fit_min': 95,
        },
        {
            'email': 'david@district.edu',
            'designation': 'Chief Learning Officer',
            'company_name': 'County School District',
            'expected_persona': 'CXO',
            'expected_campaign_fit_min': 95,
        },
        {
            'email': 'emma@school.edu',
            'designation': 'HR Manager',
            'company_name': 'Madison High School',
            'expected_persona': 'Manager',
            'expected_campaign_fit_max': 40,
        },
        {
            'email': 'frank@school.edu',
            'designation': 'Educational Technology Coordinator',
            'company_name': 'Washington Academy',
            'expected_persona': 'Manager',
            'expected_campaign_fit_min': 85,
        },
        {
            'email': 'grace@school.edu',
            'designation': 'Principal',
            'company_name': 'Adams High School',
            'expected_persona': 'Director',
            'expected_campaign_fit_min': 90,
        },
    ]

    print("\n" + "="*90)
    print("CAMPAIGN FIT VALIDATION TEST — K-12 EDUCATION CAMPAIGN")
    print("="*90)
    print("\nCampaign: K-12 Education Solutions")
    print("Target Industry: K-12 Education")
    print("Preferred Functions: Curriculum, Instruction, Education Technology, Administration")
    print("Avoid Functions: Finance (unless exec), HR, General Operations\n")

    classified_k12 = []

    for i, test_case in enumerate(test_cases_k12, 1):
        print(f"{'='*90}")
        print(f"TEST {i}: {test_case['designation']} at {test_case['company_name']}")
        print(f"{'='*90}")

        # Get mock response
        response = campaign_fit_responses.get(
            test_case['designation'],
            {
                "persona": "Unknown",
                "confidence_score": 0,
                "campaign_fit_score": 0,
                "campaign_fit_valid": False,
                "needs_review": True
            }
        )

        # Create ClassifiedProspect with campaign fit fields
        primary = PersonaAssignment(
            persona=response['persona'],
            confidence_score=response['confidence_score'],
            rationale=response['rationale'],
        )

        secondary = None
        if response.get('secondary_persona'):
            sec = response['secondary_persona']
            secondary = PersonaAssignment(
                persona=sec['persona'],
                confidence_score=sec['confidence_score'],
                rationale=sec['rationale'],
            )

        prospect = ClassifiedProspect(
            email=test_case['email'],
            designation=test_case['designation'],
            company_name=test_case['company_name'],
            primary_persona=primary,
            secondary_persona=secondary,
            seniority_level=response.get('seniority_level', 'Unknown'),
            function=response.get('function', 'Unknown'),
            needs_review=response['needs_review'],
            campaign_fit_score=response.get('campaign_fit_score', 0),
            campaign_fit_valid=response.get('campaign_fit_valid', False),
            campaign_fit_rationale=response.get('campaign_fit_rationale', ''),
        )

        classified_k12.append(prospect)

        # Print results
        print(f"\n[+] Email: {prospect.email}")
        print(f"[+] Designation: {prospect.designation}")
        print(f"[+] Company: {prospect.company_name}")

        print(f"\n[CLASSIFICATION]:")
        print(f"  PRIMARY PERSONA: {prospect.primary_persona.persona}")
        print(f"  CONFIDENCE: {prospect.primary_persona.confidence_score}%")
        print(f"  SENIORITY: {prospect.seniority_level}")
        print(f"  FUNCTION: {prospect.function}")

        print(f"\n[CAMPAIGN FIT - K-12 EDUCATION]:")
        print(f"  FIT SCORE: {prospect.campaign_fit_score}%")
        print(f"  VALID FOR CAMPAIGN: {prospect.campaign_fit_valid}")
        print(f"  RATIONALE: {prospect.campaign_fit_rationale}")

        # Verify campaign fit expectations
        if 'expected_campaign_fit_min' in test_case:
            if prospect.campaign_fit_score >= test_case['expected_campaign_fit_min']:
                print(f"\n[PASS] Fit Score {prospect.campaign_fit_score}% >= {test_case['expected_campaign_fit_min']}%")
            else:
                print(f"\n[FAIL] Fit Score {prospect.campaign_fit_score}% < {test_case['expected_campaign_fit_min']}%")

        if 'expected_campaign_fit_max' in test_case:
            if prospect.campaign_fit_score <= test_case['expected_campaign_fit_max']:
                print(f"[PASS] Fit Score {prospect.campaign_fit_score}% <= {test_case['expected_campaign_fit_max']}%")
            else:
                print(f"[FAIL] Fit Score {prospect.campaign_fit_score}% > {test_case['expected_campaign_fit_max']}%")

    # Segmentation by campaign fit
    print(f"\n\n{'='*90}")
    print("CAMPAIGN FIT SEGMENTATION FOR K-12 EDUCATION")
    print(f"{'='*90}\n")

    high_fit = [p for p in classified_k12 if p.campaign_fit_score >= 80 and p.campaign_fit_valid]
    medium_fit = [p for p in classified_k12 if 60 <= p.campaign_fit_score < 80 and p.campaign_fit_valid]
    low_fit = [p for p in classified_k12 if p.campaign_fit_score < 60 or not p.campaign_fit_valid]

    print(f"[TIER 1] HIGH FIT (Score >= 80, Valid=True): {len(high_fit)} prospects")
    for p in high_fit:
        print(f"  [STAR] {p.email} — {p.designation}")
        print(f"        Fit: {p.campaign_fit_score}% | Persona: {p.primary_persona.persona} ({p.primary_persona.confidence_score}%)")

    print(f"\n[TIER 2] MEDIUM FIT (Score 60-79, Valid=True): {len(medium_fit)} prospects")
    for p in medium_fit:
        print(f"  [+] {p.email} — {p.designation}")
        print(f"        Fit: {p.campaign_fit_score}% | Persona: {p.primary_persona.persona}")

    print(f"\n[TIER 3] LOW/NO FIT (Score < 60 OR Valid=False): {len(low_fit)} prospects")
    for p in low_fit:
        print(f"  [SKIP] {p.email} — {p.designation}")
        print(f"        Fit: {p.campaign_fit_score}% | Valid: {p.campaign_fit_valid}")
        print(f"        Reason: {p.campaign_fit_rationale}")

    print(f"\n{'='*90}")
    print("BIFURCATION SUMMARY")
    print(f"{'='*90}\n")
    print(f"Total Prospects: {len(classified_k12)}")
    print(f"  -> High Fit (Target): {len(high_fit)} (priority outreach)")
    print(f"  -> Medium Fit: {len(medium_fit)} (secondary outreach)")
    print(f"  -> Low/No Fit (Skip): {len(low_fit)} (exclude from campaign)")
    print(f"\nCampaign Penetration: {len(high_fit) + len(medium_fit)}/{len(classified_k12)} ({int(100*(len(high_fit) + len(medium_fit))/len(classified_k12))}%)")


if __name__ == '__main__':
    print("\n[MODE 1] Original Test — 15 Generic Cases")
    test_mock_classification()

    print("\n\n[MODE 2] Campaign Fit Validation — K-12 Education Campaign")
    test_campaign_fit_validation()
