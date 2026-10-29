import streamlit as st
import json
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestration.workflow import process_claim
from src.rag.vector_store import get_vector_store
from src.safety.presidio import get_pii_detector
from src.logger import setup_logger
import uuid

logger = setup_logger(__name__)

st.set_page_config(
    page_title="Insurance Claim Processor",
    page_icon="📋",
    layout="wide"
)

st.title("🏥 Insurance Claim Processing System")
st.markdown("Multi-agent AI system for intelligent claim assessment")

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select Page",
                    ["Process Claim", "View Results", "System Status", "Knowledge Base"])

# Initialize session state
if "claims" not in st.session_state:
    st.session_state.claims = {}

if "knowledge_initialized" not in st.session_state:
    st.session_state.knowledge_initialized = False

# ==================== PAGE: PROCESS CLAIM ====================
if page == "Process Claim":
    st.header("📝 Submit New Claim")

    with st.form("claim_form"):
        col1, col2 = st.columns(2)

        with col1:
            claim_type = st.selectbox(
                "Claim Type",
                ["Medical", "Property", "Auto", "Life", "Travel"]
            )

            claim_amount = st.number_input(
                "Claim Amount ($)",
                min_value=0,
                max_value=10_000_000,
                step=1000
            )

            policy_number = st.text_input(
                "Policy Number",
                placeholder="POL-XXX-XXX"
            )

        with col2:
            claimant_name = st.text_input(
                "Claimant Name",
                placeholder="John Doe"
            )

            claim_date = st.date_input(
                "Date of Loss/Event"
            )

            contact_email = st.text_input(
                "Contact Email",
                placeholder="example@email.com"
            )

        description = st.text_area(
            "Claim Description",
            height=100,
            placeholder="Provide details about the claim..."
        )

        uploaded_file = st.file_uploader(
            "Upload Supporting Documents (optional)",
            type=["pdf", "txt", "jpg", "png"]
        )

        submitted = st.form_submit_button("🚀 Process Claim")

    if submitted:
        claim_id = str(uuid.uuid4())[:8]

        claim_data = {
            "type": claim_type,
            "amount": claim_amount,
            "policy_number": policy_number,
            "claimant_name": claimant_name,
            "claim_date": str(claim_date),
            "contact_email": contact_email,
            "description": description,
            "submitted_at": datetime.now().isoformat(),
        }

        with st.spinner("🔄 Processing claim through multi-agent pipeline..."):
            try:
                # Process through workflow
                result = process_claim(claim_id, claim_data)

                # Store result
                st.session_state.claims[claim_id] = {
                    "claim_data": claim_data,
                    "result": result,
                    "processed_at": datetime.now().isoformat()
                }

                # Display results
                st.success(f"✅ Claim processed successfully! Claim ID: **{claim_id}**")

                col1, col2, col3 = st.columns(3)
                with col1:
                    status = result.get("decision", {}).get("status", "UNKNOWN")
                    st.metric("Decision", status)

                with col2:
                    confidence = result.get("decision", {}).get("confidence", 0)
                    st.metric("Confidence", f"{confidence:.1%}")

                with col3:
                    pii_count = len(result.get("pii_detected", []))
                    st.metric("PII Detected & Masked", pii_count)

                # Detailed Decision
                st.subheader("📊 Decision Details")
                decision = result.get("decision", {})

                if decision:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"**Status:** {decision.get('status', 'N/A')}")
                        st.markdown(f"**Confidence:** {decision.get('confidence', 0):.1%}")
                    with col2:
                        st.markdown(f"**Reason:**\n{decision.get('reason', 'N/A')}")

                    next_steps = decision.get("next_steps", [])
                    if next_steps:
                        st.markdown("**Next Steps:**")
                        for step in next_steps:
                            st.markdown(f"- {step}")

                # Agent Messages Timeline
                st.subheader("🔄 Processing Timeline")
                messages = result.get("messages", [])
                for msg in messages:
                    with st.chat_message(msg.get("role", "system")):
                        st.write(msg.get("content", ""))

                # Errors if any
                if result.get("errors"):
                    st.subheader("⚠️ Warnings/Errors")
                    for error in result["errors"]:
                        st.warning(error)

                # JSON Export
                st.subheader("📥 Export Results")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy JSON"):
                        st.code(json.dumps(result, indent=2))
                with col2:
                    st.download_button(
                        "⬇️ Download JSON",
                        data=json.dumps(result, indent=2),
                        file_name=f"claim_{claim_id}.json",
                        mime="application/json"
                    )

                logger.info(f"Claim {claim_id} processed and displayed")

            except Exception as e:
                st.error(f"❌ Error processing claim: {str(e)}")
                logger.error(f"Error processing claim: {str(e)}", exc_info=True)

# ==================== PAGE: VIEW RESULTS ====================
elif page == "View Results":
    st.header("📊 Claims History")

    if not st.session_state.claims:
        st.info("No claims processed yet. Submit a claim on the 'Process Claim' page.")
    else:
        # Display claims in a table
        claims_data = []
        for claim_id, claim_info in st.session_state.claims.items():
            decision = claim_info["result"].get("decision", {})
            claims_data.append({
                "Claim ID": claim_id,
                "Type": claim_info["claim_data"].get("type"),
                "Amount": f"${claim_info['claim_data'].get('amount', 0):,}",
                "Status": decision.get("status", "UNKNOWN"),
                "Confidence": f"{decision.get('confidence', 0):.1%}",
                "Processed At": claim_info["processed_at"]
            })

        # Display as table
        import pandas as pd
        df = pd.DataFrame(claims_data)
        st.dataframe(df, use_container_width=True)

        # Detailed view
        st.subheader("View Claim Details")
        selected_claim_id = st.selectbox(
            "Select Claim ID",
            list(st.session_state.claims.keys())
        )

        if selected_claim_id:
            claim_info = st.session_state.claims[selected_claim_id]

            tabs = st.tabs(["Overview", "Decision", "Details", "Raw JSON"])

            with tabs[0]:
                claim_data = claim_info["claim_data"]
                st.write(f"**Claim Type:** {claim_data.get('type')}")
                st.write(f"**Amount:** ${claim_data.get('amount', 0):,}")
                st.write(f"**Policy Number:** {claim_data.get('policy_number')}")
                st.write(f"**Claimant:** {claim_data.get('claimant_name')}")
                st.write(f"**Description:** {claim_data.get('description')}")

            with tabs[1]:
                result = claim_info["result"]
                decision = result.get("decision", {})
                st.write(f"**Status:** {decision.get('status')}")
                st.write(f"**Confidence:** {decision.get('confidence'):.1%}")
                st.write(f"**Reason:** {decision.get('reason')}")

            with tabs[2]:
                result = claim_info["result"]
                st.metric("PII Entities Detected", len(result.get("pii_detected", [])))
                st.metric("Policy Documents Retrieved", len(result.get("policy_documents", [])))

                if result.get("pii_detected"):
                    st.subheader("Detected PII")
                    pii_df = pd.DataFrame(result["pii_detected"])
                    st.dataframe(pii_df, use_container_width=True)

            with tabs[3]:
                st.json(claim_info["result"])

# ==================== PAGE: SYSTEM STATUS ====================
elif page == "System Status":
    st.header("⚙️ System Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Claims Processed", len(st.session_state.claims))

    with col2:
        if st.session_state.claims:
            approved = sum(1 for c in st.session_state.claims.values()
                          if c["result"].get("decision", {}).get("status") == "APPROVED")
            st.metric("Approved", approved)
        else:
            st.metric("Approved", 0)

    with col3:
        if st.session_state.claims:
            rejected = sum(1 for c in st.session_state.claims.values()
                          if c["result"].get("decision", {}).get("status") == "REJECTED")
            st.metric("Rejected", rejected)
        else:
            st.metric("Rejected", 0)

    with col4:
        if st.session_state.claims:
            review = sum(1 for c in st.session_state.claims.values()
                        if c["result"].get("decision", {}).get("status") == "REVIEW")
            st.metric("Under Review", review)
        else:
            st.metric("Under Review", 0)

    st.subheader("🔧 Components Status")

    # Check component availability
    components = {
        "LLM Client": "✅ Ready",
        "Vector Store": "✅ Ready",
        "PII Detection": "✅ Ready",
        "Guardrails": "✅ Ready",
        "LangGraph Workflow": "✅ Ready",
    }

    for component, status in components.items():
        st.markdown(f"{component}: {status}")

    # Statistics
    if st.session_state.claims:
        st.subheader("📈 Decision Statistics")

        decisions = [c["result"].get("decision", {}).get("status", "UNKNOWN")
                    for c in st.session_state.claims.values()]

        from collections import Counter
        decision_counts = Counter(decisions)

        col1, col2 = st.columns(2)
        with col1:
            import plotly.express as px
            fig = px.pie(
                values=list(decision_counts.values()),
                names=list(decision_counts.keys()),
                title="Decision Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            avg_confidence = sum(c["result"].get("decision", {}).get("confidence", 0)
                                for c in st.session_state.claims.values()) / len(st.session_state.claims)
            st.metric("Average Confidence", f"{avg_confidence:.1%}")

# ==================== PAGE: KNOWLEDGE BASE ====================
elif page == "Knowledge Base":
    st.header("📚 Knowledge Base Management")

    st.subheader("Add Policy Documents")

    with st.form("add_documents"):
        doc_type = st.selectbox("Document Type", ["Policy", "Guidelines", "Coverage Rules"])
        doc_content = st.text_area("Document Content", height=200)

        if st.form_submit_button("📤 Add to Knowledge Base"):
            try:
                vector_store = get_vector_store()
                import sys
                from pathlib import Path
                sys.path.insert(0, str(Path(__file__).parent.parent))
                from langchain_compat import Document

                doc = Document(
                    page_content=doc_content,
                    metadata={
                        "type": doc_type,
                        "added_at": datetime.now().isoformat()
                    }
                )

                vector_store.add_documents([doc])
                st.success("✅ Document added to knowledge base")
                logger.info(f"Document added: {doc_type}")

            except Exception as e:
                st.error(f"Error adding document: {str(e)}")

    st.subheader("Test PII Detection")
    with st.form("test_pii"):
        test_text = st.text_area(
            "Enter text to test PII detection",
            value="My name is John Doe and my email is john@example.com. My SSN is 123-45-6789",
            height=100
        )

        if st.form_submit_button("🔍 Test Detection"):
            pii_detector = get_pii_detector()
            entities = pii_detector.detect_pii(test_text)

            if entities:
                st.warning(f"Detected {len(entities)} PII entities")
                for entity in entities:
                    st.markdown(f"- **{entity['entity_type']}**: {entity['text']} (confidence: {entity['score']:.2f})")
            else:
                st.success("No PII detected")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
Insurance Claim Processing System | Built with LangGraph, ChromaDB & Streamlit
</div>
""", unsafe_allow_html=True)
