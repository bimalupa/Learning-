# 🎬 Recording Script - Insurance Claim Processing System Demo

**Total Duration: 8 minutes**

---

## 0:00-0:30 | INTRO

**[Show application homepage]**

> "Hello, I'm demonstrating the Insurance Claim Processing System. This is an AI-powered platform that automatically processes insurance claims using machine learning, retrieval-augmented generation, and safety guardrails.
>
> The system is built with LangGraph for multi-agent orchestration, ChromaDB for vector storage, Streamlit for the interface, and Azure OpenAI for language understanding.
>
> Let me show you how it works in real time..."

**[Pause 2 seconds]**

---

## 0:30-1:00 | APPLICATION OVERVIEW

**[Point to each navigation item]**

> "The application has four main pages:
> 
> First - 'Process Claim' where users submit new insurance claims
> Second - 'View Results' to see the history of processed claims
> Third - 'System Status' showing the health of all components
> And fourth - 'Knowledge Base' containing all the insurance policies
>
> Let's start by processing a claim..."

**[Click on "Process Claim" page]**

---

## 1:00-3:00 | SCENARIO 1: VALID CLAIM (APPROVED)

**[Navigate to Process Claim page]**

> "First, let's submit a valid medical claim. I'll fill in the details:
>
> Claim Type: Medical
> Amount: $1,500
> Description: Annual physical examination and lab tests
>
> Notice the form also asks for contact information. When we submit this, the system will automatically detect and mask any personally identifiable information like SSN, email, or phone numbers for privacy protection."

**[Fill out form]**

> "Now I'll submit the claim..."

**[Click Submit button]**

**[Wait for processing - 2-3 seconds]**

> "The system is now processing the claim through its workflow. It's:
>
> 1) Detecting any PII and masking it
> 2) Retrieving relevant insurance policies
> 3) Validating against business rules
> 4) Making an intelligent decision
>
> And here's the result..."

**[Show decision]**

> "The system approved this claim with 95% confidence. It's a valid medical claim within the policy limits. The processing took only 2 seconds. Notice the audit trail on the side shows exactly what happened at each step.
>
> Now let's try something more challenging..."

**[Pause 2 seconds]**

---

## 3:00-4:30 | SCENARIO 2: FRAUDULENT CLAIM (REJECTED)

**[Click back to "Process Claim"]**

> "Now let's submit a claim that should be rejected. I'll try to claim $500,000 for cosmetic procedures - which exceeds policy limits and isn't covered."

**[Fill out form with high amount]**

> "Amount: $500,000
> Type: Medical
> Description: Cosmetic procedures"

**[Submit claim]**

**[Wait for processing]**

> "Watch what happens... The system immediately rejects this with 98% confidence. It correctly identified that:
>
> 1) The amount exceeds the maximum claim limit
> 2) Cosmetic procedures aren't covered under medical plans
>
> The system doesn't just make yes/no decisions - it explains why. This helps customers understand the decision and appeals if needed.
>
> But not everything is black and white. Some claims need human judgment..."

**[Pause 2 seconds]**

---

## 4:30-6:00 | SCENARIO 3: AMBIGUOUS CLAIM (REVIEW)

**[Click back to "Process Claim"]**

> "Let's try a more complex case - a pre-existing condition claim. These require careful review because coverage depends on specific policy details."

**[Fill out form]**

> "Amount: $15,000
> Type: Medical  
> Description: Treatment for pre-existing back condition from before policy began"

**[Submit claim]**

**[Wait for processing]**

> "This time the system returns 'REVIEW' with about 65% confidence. This is actually a sign of intelligent AI - it knows when a case needs human expertise.
>
> Rather than making a guess or forcing an automatic decision, it escalates to a human claims processor who can review the specific policy language and make the right call.
>
> This is the key difference between AI that helps and AI that harms - knowing when NOT to decide automatically."

**[Pause 2 seconds]**

---

## 6:00-7:00 | FEATURES SHOWCASE

**[Navigate to "View Results" page]**

> "Now let's look at the 'View Results' page. Here we can see the history of all claims we've processed - it shows the claim ID, type, amount, decision, and confidence score."

**[Click on a claim]**

> "We can click on individual claims to see the complete processing details and audit trail. Every decision is fully documented for compliance."

**[Go back, click "System Status" page]**

> "The System Status page shows the health of all components - the vector database, embeddings model, and language model. It also displays processing metrics like average claim processing time.
>
> Finally, let's look at the Knowledge Base..."

**[Click "Knowledge Base" page]**

> "The Knowledge Base shows all the insurance policies the system has learned. We can search for specific coverage details. The system uses semantic search to find relevant policies even with different wording."

**[Search for something]**

> "Notice how it finds policies based on meaning, not just keyword matching. This is powered by embeddings and vector similarity search."

**[Pause 2 seconds]**

---

## 7:00-8:00 | TECHNICAL EXPLANATION

**[Navigate to System Status or show logs]**

> "Behind the scenes, this system uses a sophisticated multi-agent architecture:
>
> The Intake Agent detects and masks sensitive information
> The Retrieval Agent searches the policy database for relevant coverage
> The Validation Agent checks business rules and claim eligibility  
> The Decision Agent makes the final approval/rejection/review decision
>
> All of this happens in seconds, with full auditability and explainability.
>
> The system also includes safety guardrails that prevent:
> - Injection attacks
> - Fraud patterns  
> - Policy breaches
> - Inconsistent decisions
>
> Everything is logged in JSON format for compliance and debugging."

**[Pause 2 seconds]**

---

## 8:00-8:30 | CLOSING

> "The Insurance Claim Processing System demonstrates how AI can:
>
> ✓ Dramatically improve speed (seconds instead of days)
> ✓ Maintain consistency in decision-making  
> ✓ Protect customer privacy automatically
> ✓ Provide full audit trails for compliance
> ✓ Know when to escalate to humans
> ✓ Handle complex business logic
>
> This is production-ready code that's fully documented and tested. You can deploy it, customize it for your specific policies, and scale it to handle thousands of claims.
>
> Thank you for watching. Feel free to reach out with any questions about the system!"

**[Smile, end recording]**

---

## ⏱️ Timing Checklist

- [ ] 0:00-0:30 - Intro (30 sec)
- [ ] 0:30-1:00 - Overview (30 sec)
- [ ] 1:00-3:00 - Valid Claim Demo (2 min)
- [ ] 3:00-4:30 - Invalid Claim Demo (1.5 min)
- [ ] 4:30-6:00 - Ambiguous Claim Demo (1.5 min)
- [ ] 6:00-7:00 - Features Showcase (1 min)
- [ ] 7:00-8:00 - Technical Details (1 min)
- [ ] 8:00-8:30 - Closing (30 sec)

**Total: 8 minutes**

---

## 🎤 Speaking Tips for This Script

### Pacing
- Read slowly and clearly
- Pause for 2 seconds after each demonstration
- Let the system complete its processing before continuing
- Sound natural, not robotic

### Emphasis
- **Emphasize speed**: "only 2 seconds"
- **Emphasize safety**: "automatically masked", "full audit"
- **Emphasize intelligence**: "knows when NOT to decide"
- **Emphasize completeness**: "production-ready"

### Tone
- Professional but friendly
- Confident in the technology
- Respectful of the complexity
- Enthusiastic about the benefits

---

## 🎬 Visual Cues for Recording

**When you see this text:** | **Do this action:**
---|---
[Show application homepage] | Navigate to localhost:8501
[Point to navigation] | Move mouse to each menu item
[Fill out form] | Type in form fields slowly
[Submit claim] | Click the submit button
[Wait for processing] | Pause 2-3 seconds for animation
[Show decision] | Scroll to show the result clearly
[Click back] | Use back button or navigation

---

## 📝 Print Version

Print this script and have it visible while recording. Check off each section as you complete it.

**Practice reading through this script once before recording for timing.**

---

*Last Updated: 2024-10-29*
*Recording Script v1.0*

**You got this! Start recording!** 🎬
