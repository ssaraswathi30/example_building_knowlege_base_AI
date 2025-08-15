#!/usr/bin/env python3
"""
Prolog-Based Interactive Loan Classification System
Run: python prolog_loan_system.py
"""
import os
import re

class PrologLoanClassifier:
    def __init__(self, prolog_file_path='loan_knowledge_base.pl'):
        self.prolog_file_path = prolog_file_path
        self.rules = self._parse_prolog_rules()
    
    def _parse_prolog_rules(self):
        """Parse the Prolog knowledge base file and extract rules"""
        rules = []
        
        try:
            with open(self.prolog_file_path, 'r') as f:
                lines = f.readlines()
            
            current_rule = {}
            in_rule = False
            
            for line in lines:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('%'):
                    # Check if it's a rule comment with confidence
                    if 'Rule' in line and 'Confidence' in line and 'Samples' in line:
                        parts = line.split(',')
                        confidence_str = [p for p in parts if 'Confidence' in p][0]
                        samples_str = [p for p in parts if 'Samples' in p][0]
                        
                        current_rule['confidence'] = float(confidence_str.split()[-1])
                        current_rule['samples'] = int(samples_str.split()[-1])
                    continue
                
                # Start of a rule
                if line.startswith('classify_loan(') and ':-' in line:
                    in_rule = True
                    decision_part = line.split(',')[-1].split(')')[0].strip()
                    current_rule['decision'] = decision_part
                    
                    # Extract conditions if they exist
                    if ':-' in line:
                        conditions_part = line.split(':-')[1].strip()
                        if conditions_part and not conditions_part.endswith('.'):
                            current_rule['conditions'] = [conditions_part]
                        elif conditions_part.endswith('.'):
                            current_rule['conditions'] = [conditions_part[:-1]]
                        else:
                            current_rule['conditions'] = []
                
                # Continue collecting conditions
                elif in_rule and line and not line.startswith('classify_loan('):
                    if line.endswith('.'):
                        if 'conditions' not in current_rule:
                            current_rule['conditions'] = []
                        if line != '.':
                            current_rule['conditions'].append(line[:-1].strip())
                        
                        if 'confidence' not in current_rule:
                            current_rule['confidence'] = 1.0
                        if 'samples' not in current_rule:
                            current_rule['samples'] = 1
                            
                        rules.append(current_rule.copy())
                        current_rule = {}
                        in_rule = False
                    else:
                        if 'conditions' not in current_rule:
                            current_rule['conditions'] = []
                        current_rule['conditions'].append(line.strip())
                
                # Simple rule without conditions
                elif line.startswith('classify_loan(') and line.endswith('.'):
                    decision_part = line.split(',')[-1].split(')')[0].strip()
                    rules.append({
                        'decision': decision_part,
                        'conditions': [],
                        'confidence': current_rule.get('confidence', 1.0),
                        'samples': current_rule.get('samples', 1)
                    })
                    current_rule = {}
            
        except FileNotFoundError:
            print(f"❌ Prolog file not found!")
            return []
        except Exception as e:
            print(f"❌ Error parsing Prolog file: {e}")
            return []
        
        return rules
    
    def _evaluate_condition(self, condition, sex, age, loan_term, num_accounts, loan_type, loan_area):
        """Evaluate a single Prolog condition against input values"""
        condition = condition.strip().rstrip(',')
        
        # Handle Age conditions
        if 'Age' in condition:
            if '<=' in condition:
                threshold = float(condition.split('<=')[1].strip())
                return age <= threshold
            elif '>' in condition:
                threshold = float(condition.split('>')[1].strip())
                return age > threshold
        
        # Handle Sex conditions
        elif 'Sex' in condition:
            if '=' in condition:
                expected_sex = condition.split('=')[1].strip().lower()
                return sex.lower() == expected_sex
        
        # Handle Loan Term conditions
        elif 'LoanTerm' in condition:
            if '<=' in condition:
                threshold = float(condition.split('<=')[1].strip())
                return loan_term <= threshold
            elif '>' in condition:
                threshold = float(condition.split('>')[1].strip())
                return loan_term > threshold
        
        # Handle Number of Accounts conditions
        elif 'NumAccounts' in condition:
            if '<=' in condition:
                threshold = float(condition.split('<=')[1].strip())
                return num_accounts <= threshold
            elif '>' in condition:
                threshold = float(condition.split('>')[1].strip())
                return num_accounts > threshold
        
        # Handle Loan Type conditions
        elif 'LoanType' in condition:
            if '=' in condition and 'member' not in condition:
                expected_type = condition.split('=')[1].strip().lower()
                return loan_type.lower() == expected_type
            elif 'member(LoanType' in condition:
                list_part = condition.split('[')[1].split(']')[0]
                allowed_types = [t.strip().lower() for t in list_part.split(',')]
                return loan_type.lower() in allowed_types
        
        # Handle Loan Area conditions
        elif 'LoanArea' in condition:
            if '<=' in condition:
                threshold = float(condition.split('<=')[1].strip())
                return loan_area <= threshold
            elif '>' in condition:
                threshold = float(condition.split('>')[1].strip())
                return loan_area > threshold
        
        return True
    
    def classify(self, sex, age, loan_term, num_accounts, loan_type, loan_area):
        """Classify using Prolog rules"""
        matching_rules = []
        
        for rule in self.rules:
            all_conditions_met = True
            
            if rule['conditions']:
                for condition in rule['conditions']:
                    if not self._evaluate_condition(condition, sex, age, loan_term, 
                                                 num_accounts, loan_type, loan_area):
                        all_conditions_met = False
                        break
            
            if all_conditions_met:
                matching_rules.append(rule)
        
        if not matching_rules:
            return {
                'decision': 'REJECTED',
                'confidence': 0.5,
                'reasoning': 'No Prolog rule matched - default rejection'
            }
        
        # Use the rule with highest confidence
        best_rule = max(matching_rules, key=lambda r: r['confidence'])
        
        return {
            'decision': best_rule['decision'].upper(),
            'confidence': best_rule['confidence'],
            'reasoning': f"Prolog rule matched (confidence: {best_rule['confidence']:.3f})"
        }

class LoanClassificationSystem:
    def __init__(self):
        self.prolog_classifier = PrologLoanClassifier()
        print(f"🧠 Loaded {len(self.prolog_classifier.rules)} Prolog rules")
    
    def classify(self, sex, age, loan_term, num_accounts, loan_type, loan_area):
        return self.prolog_classifier.classify(sex, age, loan_term, num_accounts, loan_type, loan_area)
    
    def run(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("🏦 PROLOG-BASED LOAN CLASSIFICATION SYSTEM")
        print("="*50)
        print("📚 Using Prolog Knowledge Base for Predictions")
        
        count = 0
        while True:
            try:
                count += 1
                print(f"\nAPPLICATION #{count}")
                
                sex = input("Sex (Male/Female): ").strip().title()
                while sex not in ['Male', 'Female']:
                    sex = input("Enter Male or Female: ").strip().title()
                
                age = int(input("Age (15-70): "))
                loan_term = int(input("Loan term (1-12 years): "))
                num_accounts = int(input("Number of accounts (1-12): "))
                
                loan_type = input("Loan type (Home/Personal/Auto): ").strip().title()
                while loan_type not in ['Home', 'Personal', 'Auto']:
                    loan_type = input("Enter Home, Personal, or Auto: ").strip().title()
                
                loan_area = int(input("Area code (4-750): "))
                
                result = self.classify(sex, age, loan_term, num_accounts, loan_type, loan_area)
                
                emoji = "✅" if result['decision'] == 'APPROVED' else "❌"
                print(f"\n{emoji} DECISION: {result['decision']}")
                print(f"📊 Confidence: {result['confidence']:.1%}")
                print(f"🧠 Reasoning: {result['reasoning']}")
                
                # Show Prolog query equivalent
                sex_prolog = sex.lower()
                loan_type_prolog = loan_type.lower()
                prolog_query = f"classify_loan({sex_prolog}, {age}, {loan_term}, {num_accounts}, {loan_type_prolog}, {loan_area}, Decision)."
                print(f"\n🔍 Prolog Query: {prolog_query}")
                
                if input("\nAnother application? (y/n): ").lower() not in ['y', 'yes']:
                    break
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\nProcessed {count} applications using Prolog rules. Goodbye!")

if __name__ == "__main__":
    LoanClassificationSystem().run()
