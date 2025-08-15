#!/usr/bin/env python3
"""
Interactive Loan Classification System
Run this script in terminal for proper interactive experience
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import os

class LoanClassificationSystem:
    def __init__(self):
        self.model = None
        self.feature_names = ['Sex', 'Age', 'Loan Term (Years)', 'Number of Accounts', 'Loan Type', 'Loan Area']
        self.sex_reverse = {'Male': 1, 'Female': 2}
        self.loan_type_reverse = {'Home': 1, 'Personal': 2, 'Auto': 3}
        self.initialize_model()
    
    def initialize_model(self):
        """Initialize the decision tree model"""
        try:
            df = pd.read_csv('data/Loan - Loan dataset.csv')
            feature_columns = ['sex', 'age', 'Loan Term in Years', 'Number_of_Accounts', 
                              'Loan Type', 'Loan Area']
            X = df[feature_columns]
            y = df['Loan Sanctioned']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            
            self.model = DecisionTreeClassifier(max_depth=5, min_samples_split=20, min_samples_leaf=10, random_state=42)
            self.model.fit(X_train, y_train)
            print("✅ Model trained successfully!")
        except Exception as e:
            print(f"❌ Error: {e}")
            exit(1)
    
    def classify_application(self, app):
        sex_encoded = self.sex_reverse[app['sex']]
        loan_type_encoded = self.loan_type_reverse[app['loan_type']]
        features = np.array([[sex_encoded, app['age'], app['loan_term'], app['num_accounts'], loan_type_encoded, app['loan_area']]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        return {'decision': 'APPROVED' if prediction == 1 else 'REJECTED', 'confidence': max(probability), 'prob_approved': probability[1]}
    
    def run_interactive_mode(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("🏦 INTERACTIVE LOAN CLASSIFICATION SYSTEM")
        print("="*60)
        print("🚀 Welcome! Get instant AI-powered loan decisions")
        
        count = 0
        while True:
            try:
                count += 1
                print(f"\n🔢 APPLICATION #{count}")
                print("="*50)
                
                sex = input("👤 Sex (Male/Female): ").strip().title()
                while sex not in ['Male', 'Female']:
                    sex = input("❌ Please enter Male or Female: ").strip().title()
                
                age = int(input("🎂 Age (15-70): "))
                while not (15 <= age <= 70):
                    age = int(input("❌ Age between 15-70: "))
                
                loan_term = int(input("📅 Loan term in years (1-12): "))
                while not (1 <= loan_term <= 12):
                    loan_term = int(input("❌ Loan term between 1-12: "))
                
                num_accounts = int(input("🏛️ Number of accounts (1-12): "))
                while not (1 <= num_accounts <= 12):
                    num_accounts = int(input("❌ Accounts between 1-12: "))
                
                loan_type = input("🏠 Loan type (Home/Personal/Auto): ").strip().title()
                while loan_type not in ['Home', 'Personal', 'Auto']:
                    loan_type = input("❌ Enter Home, Personal, or Auto: ").strip().title()
                
                loan_area = int(input("📍 Loan area code (4-750): "))
                while not (4 <= loan_area <= 750):
                    loan_area = int(input("❌ Area code between 4-750: "))
                
                app = {'sex': sex, 'age': age, 'loan_term': loan_term, 'num_accounts': num_accounts, 'loan_type': loan_type, 'loan_area': loan_area}
                result = self.classify_application(app)
                
                print("\n⏳ Processing...")
                print("="*50)
                print("🎯 RESULT")
                print("="*50)
                
                emoji = "✅" if result['decision'] == 'APPROVED' else "❌"
                print(f"\n{emoji} DECISION: {result['decision']}")
                print(f"📊 Confidence: {result['confidence']:.1%}")
                print(f"📈 Approval Probability: {result['prob_approved']:.1%}")
                
                print("\n💡 Reasoning:")
                if age <= 31 and loan_term <= 8.5:
                    print("   ✓ Young + Short term = Favorable")
                elif age <= 31:
                    print("   ⚠️ Young but long term = Risk")
                else:
                    print("   ⚠️ Older applicant = Higher risk")
                
                print("\n" + "="*50)
                if input("🔄 Another application? (y/n): ").lower() not in ['y', 'yes']:
                    break
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break
            except:
                print("\n❌ Please enter valid inputs")
        
        print(f"\n🙏 Thank you! Processed {count} application(s)")

if __name__ == "__main__":
    LoanClassificationSystem().run_interactive_mode()
