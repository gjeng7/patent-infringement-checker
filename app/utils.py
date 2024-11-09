import json
import os
import torch
from difflib import SequenceMatcher
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from nltk import ngrams


os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

explanation_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
explanation_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")


DATA_PATH = os.path.join(os.path.dirname(__file__), '../data')

def load_json(filename):
    with open(os.path.join(DATA_PATH, filename), 'r', encoding="utf-8") as f:
        return json.load(f)

def get_patent_data(patent_id, patents):
    for patent in patents:
        if patent['publication_number'] == patent_id:
            # Parse the 'claims' field if it's a JSON string
            if isinstance(patent['claims'], str):
                patent['claims'] = json.loads(patent['claims'])
            return patent
    return None


def get_company_products(company_name, companies_data):
    companies = companies_data.get("companies", [])


    for company in companies:
        if isinstance(company, dict) and 'name' in company:
            if company['name'].lower() == company_name.lower():
                return company['products']
    return []


def extract_features_from_claim(claim_text, product_desc, min_phrase_length=3):
    
    prompt = (
        f"We are analyzing a patent claim that reads as follows: '{claim_text}'. "
        f"Please provide a brief, comma-separated list of the key technical features "
        f"described in this claim. Focus only on the specific technical elements "
        f"mentioned in the claim."
    )
    
    truncated_prompt = truncate_text(prompt)  
    
    # Generate response using LLM
    inputs = explanation_tokenizer(truncated_prompt, return_tensors="pt")
    generated_output = explanation_model.generate(**inputs, max_new_tokens=100)
    features_text = explanation_tokenizer.decode(generated_output[0], skip_special_tokens=True)
    
    # Convert the comma-separated response into a list of features
    features = [feature.strip() for feature in features_text.split(',')]
    
    features = list(set(filter(None, features)))

    return features

def extract_claim_number(claim_text):
    match = re.search(r'^\s*(\d+)\s*\.', claim_text)
    if match:
        return match.group(1)  # Return the claim number as a string
    return None



def check_infringement(patent_claims, product_desc, threshold=0.3, top_n=5):
    relevant_claims = []
    specific_features = []
    claim_scores = []
    
    for claim in patent_claims:
        score = SequenceMatcher(None, claim, product_desc).ratio()
        claim_scores.append((claim, score))
    
    sorted_claims = sorted(claim_scores, key=lambda x: x[1], reverse=True)
    
    for claim, score in sorted_claims:
        if score >= threshold:
            claim_number = extract_claim_number(claim)
            if claim_number:
                relevant_claims.append(claim_number)
            
            # Extract specific features from each relevant claim
            features = extract_features_from_claim(claim, product_desc)
            specific_features.extend(features)  # Collect features across all relevant claims
            
        if len(relevant_claims) >= top_n:
            break

    max_score = max([score for _, score in claim_scores]) if claim_scores else 0
    return max_score, relevant_claims, list(set(specific_features))  # Ensure unique features




def truncate_text(text, max_tokens=512):
    tokens = explanation_tokenizer.encode(text, truncation=True, max_length=max_tokens, return_tensors="pt")
    return explanation_tokenizer.decode(tokens[0], skip_special_tokens=True)

def analyze_infringement(patent_id, company_name, patents, companies):
    patent = get_patent_data(patent_id, patents)
    if not patent:
        print(f"No patent found for ID: {patent_id}")
        return None

    products = get_company_products(company_name, companies)
    if not products:
        print(f"No products found for company: {company_name}")
        return None
    
    results = []
    patent_claim_texts = [claim['text'] for claim in patent['claims']]

    for product in products:
        
        score, relevant_claims_info, specific_features = check_infringement(patent_claim_texts, product['description'])

        if score > 0.3:  

            prompt = (
                f"We are analyzing a potential patent infringement by the product '{product['name']}' "
                f"from '{company_name}'.  "
                f"Can you generate an explanation as to how this product may implement features "
                f"that potentially infringe on these claims?"
                f"This product is described as follows: '{product['description']}'. Our patent claims are as follows: {', '.join(patent_claim_texts)}. "
                f"Based on an initial similarity score of {score}, we suspect that the product may infringe "
                f"on the following specific claims: {[claim['num'] for claim in patent['claims']]}. "

            )

            truncated_prompt = truncate_text(prompt)

            # Tokenize the prompt and generate a response from the model
            inputs = explanation_tokenizer(truncated_prompt, return_tensors="pt")
            generated_output = explanation_model.generate(**inputs, max_new_tokens=100)
            explanation_text = explanation_tokenizer.decode(generated_output[0], skip_special_tokens=True)

            results.append({
                "product_name": product['name'],
                "infringement_likelihood": "High" if score > 0.6 else "Moderate",
                "relevant_claims": relevant_claims_info,
                "explanation": explanation_text,
                "specific_features": specific_features
            })

    results = sorted(results, key=lambda x: x['infringement_likelihood'], reverse=True)[:2]

    return {
        "patent_id": patent_id,
        "company_name": company_name,
        "top_infringing_products": results,
        "overall_risk_assessment": "High risk" if any(r['infringement_likelihood'] == "High" for r in results) else "Moderate risk"
    }

