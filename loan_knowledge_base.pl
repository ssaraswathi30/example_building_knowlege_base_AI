% Loan Classification Knowledge Base
% Generated from Decision Tree Rules
% Usage: classify_loan(Sex, Age, LoanTerm, NumAccounts, LoanType, LoanArea, Decision)

% Rule 1: Confidence 1.000, Samples: 1
classify_loan(Sex, Age, LoanTerm, NumAccounts, LoanType, LoanArea, approved) :-
    Age <= 31.00,
    LoanTerm <= 8.50.

% Rule 2: Confidence 0.571, Samples: 1
classify_loan(Sex, Age, LoanTerm, NumAccounts, LoanType, LoanArea, rejected) :-
    Age <= 31.00,
    LoanTerm > 8.50.

% Rule 3: Confidence 0.727, Samples: 1
classify_loan(Sex, Age, LoanTerm, NumAccounts, LoanType, LoanArea, rejected) :-
    Age > 31.00,
    member(LoanType, [home, personal]).

% Rule 4: Confidence 1.000, Samples: 1
classify_loan(Sex, Age, LoanTerm, NumAccounts, LoanType, LoanArea, rejected) :-
    Age > 31.00,
    LoanType = auto.

% Helper predicates
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).