# N1C Ledger Rules

The N1C ledger enforces a set of rules to ensure **secure, consistent, and verifiable transactions** across all nodes in the decentralized network. This document outlines all core ledger rules, wallet behaviors, transaction validations, fees, anchor logic, and synchronization guidelines.

---

## 1. Transaction Rules

### 1.1 Balance Verification
- Sender must have sufficient balance to cover the transaction amount **plus any applicable fee**.
- Formula:
```text
balance(sender) >= amount + fee

### 1.2 Positive Amounts

*   Transaction amount must always be **greater than 0**.
    
*   Transactions with zero or negative amounts are invalid.
    

### 1.3 Unique Transaction IDs

*   Each transaction must have a **unique tx\_id**.
    
*   Prevents **replay attacks** and ensures ledger integrity.
    

### 1.4 Signature Verification

*   All transactions must be **signed by the sender's private key**.
    
*   Nodes verify the signature before applying any transaction.
    

### 1.5 Anchor Validation (Optional)

*   If an **anchor node** is involved, the transaction must comply with:
    
    *   Configured **spread**
        
    *   Configured **tax rate**
        
*   Ensures fees and tax rules are enforced consistently.
    

2\. Wallet Rules
----------------

1.  **Balance Updates**
    
    *   Sender: balance -= amount + fee
        
    *   Receiver: balance += amount
        
2.  **Transaction Recording**
    
    *   Each transaction is recorded in both **sender and receiver wallet histories**.
        
3.  **Consistency**
    
    *   Balances can be recalculated from **transaction history** for verification.
        

3\. Fee and Tax Rules
---------------------

### 3.1 Fee Calculation

*   Fees are calculated based on the anchor’s spread:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   fee = amount * (anchor_spread / 100)   `

### 3.2 Tax Calculation

*   Tax (if applicable) is calculated based on anchor tax rate:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   tax = amount * (anchor_tax_rate / 100)   `

### 3.3 Net Received

*   The receiver receives:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   net_received = amount - (fee + tax)   `

4\. Transaction Validation Flow
-------------------------------

1.  **Receive transaction** from API or peer node.
    
2.  Validate transaction:
    
    *   Sender balance
        
    *   Positive amount
        
    *   Unique transaction ID
        
    *   Signature validity
        
    *   Anchor compliance (if applicable)
        
3.  **Apply transaction** to sender and receiver wallets if valid.
    
4.  **Broadcast transaction** to peer nodes for network synchronization.
    

5\. Ledger Synchronization Rules
--------------------------------

*   Each node maintains an **independent copy** of the ledger.
    
*   Transactions are broadcast to peers and independently validated.
    
*   Conflicts are resolved using:
    
    1.  **Earliest valid timestamp**
        
    2.  **Consensus across nodes**
        
*   Anchors may optionally sign batches of transactions to improve trust.
    

6\. Security Considerations
---------------------------

*   **Cryptographic signatures** ensure authenticity.
    
*   **Unique tx\_ids** prevent replay attacks.
    
*   **Multiple node validations** prevent double-spending.
    
*   Optional **anchor validation** adds an additional layer of trust.
    
*   Ledger integrity can be verified by recalculating balances from transaction history.
    

7\. Advanced Ledger Rules
-------------------------

### 7.1 Transaction Dependencies

*   Transactions may reference previous transactions for:
    
    *   Multi-step payments
        
    *   Conditional transfers
        
*   Nodes must validate dependencies before applying a transaction.
    

### 7.2 Rollback & Recovery

*   In the case of detected inconsistencies:
    
    1.  Identify invalid transactions.
        
    2.  Roll back affected balances.
        
    3.  Reapply valid transactions in correct order.
        

### 7.3 Double-Spend Prevention

*   Before applying a transaction, check:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   tx_id not in ledger_history   `

*   Prevents spending the same funds twice.
    

8\. Pseudocode Example
----------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   def apply_transaction(tx, sender_wallet, receiver_wallet, anchor=None):      if not validate_transaction(tx, sender_wallet, receiver_wallet, anchor):          raise ValueError("Invalid transaction")      fee = calculate_fee(tx.amount, anchor.spread if anchor else 0)      tax = calculate_tax(tx.amount, anchor.tax_rate if anchor else 0)      sender_wallet.balance -= (tx.amount + fee + tax)      receiver_wallet.balance += tx.amount      sender_wallet.transactions.append(tx)      receiver_wallet.transactions.append(tx)   `
