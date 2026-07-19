import streamlit as st
import urllib.request
import urllib.parse
import json
import pandas as pd

st.set_page_config(page_title="MINDY 16 - UNIFIED CONSOLE", layout="centered")

# ---------------------------------------------------------
# VISUAL OVERRIDE: FIXING THE GLARE & EYE STRAIN
# ---------------------------------------------------------
st.markdown("""
<style>
    p, li, .stMarkdown { font-weight: 400 !important; font-size: 1.05rem !important; }
    .stAlert p { color: #111111 !important; font-weight: 500 !important; }
    h1, h2, h3 { font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🎮 CONSOLE INSTRUMENTS")
    active_console = st.radio(
        "SELECT ACTIVE MODULE:",
        ["1. Constitutional Logic Gates", "2. Working-Class Economic Impact", "3. Political Target Matrix"]
    )
    st.markdown("---")
    st.caption("MINDY 16 // MULTI-MODULE DEPLOYMENT // PROXY PORT 18408")

# =========================================================
# MODULE 1 & 2: INERT FOR API TESTING
# =========================================================
if active_console == "1. Constitutional Logic Gates":
    st.title("🏛️ CONSTITUTIONAL LOGIC GATES")
    st.info("Module 1 Armed. Switch to Module 3 to test the FEC API connection.")

elif active_console == "2. Working-Class Economic Impact":
    st.title("📊 WORKING-CLASS ECONOMIC IMPACT CONSOLE")
    st.info("Module 2 Armed. Switch to Module 3 to test the FEC API connection.")

# =========================================================
# MODULE 3: POLITICAL TARGET MATRIX + INFLUENCE ESTIMATOR
# =========================================================
elif active_console == "3. Political Target Matrix":
    st.title("🎯 POLITICAL TARGET MATRIX")
    st.caption("LIVE DATA FEED & BIG INDUSTRY INFLUENCE ESTIMATOR")

    st.markdown("### 🔑 THE FEDERAL MASTER KEY")
    st.write("Paste your `data.gov` API key to unlock the FEC vault and run the probability scan.")
    fec_api_key = st.text_input("Enter Data.gov API Key:", type="password")

    st.markdown("---")
    st.markdown("### 📡 PULLING BASE TARGETS (RENDER ENGINE)")
    
    try:
        req = urllib.request.Request("https://insight-ageofknowledge.com/api/targets", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            targets = json.loads(response.read())

        if targets:
            df = pd.DataFrame(targets)
            st.success("✅ BASE TARGETS LOADED FROM RENDER.")
            
            target_names = df['name'].tolist()
            selected_name = st.selectbox("Choose Target:", ["-- Select --"] + target_names)
            
            if selected_name != "-- Select --":
                target_row = df[df['name'] == selected_name].iloc[0]
                target_fec_id = target_row['fec_id']
                
                st.markdown(f"**Target Locked:** {selected_name} | **Government ID:** `{target_fec_id}`")
                
                if fec_api_key:
                    st.markdown("---")
                    st.markdown(f"### 🏦 TAPPING THE FEC VAULT FOR COMMITTEES")
                    
                    try:
                        # 1. GET THE BUCKET (COMMITTEE)
                        fec_url = f"https://api.open.fec.gov/v1/candidate/{target_fec_id}/committees/?api_key={fec_api_key}"
                        fec_req = urllib.request.Request(fec_url, headers={'User-Agent': 'Mozilla/5.0'})
                        fec_data = json.loads(urllib.request.urlopen(fec_req).read())
                            
                        if 'results' in fec_data and len(fec_data['results']) > 0:
                            # Grab the primary committee ID
                            primary_committee = fec_data['results'][0]
                            primary_id = primary_committee.get("committee_id")
                            
                            st.success(f"✅ FOUND PRIMARY COMMITTEE: {primary_committee.get('name')} ({primary_id})")
                            
                            st.markdown("---")
                            st.markdown("### 🏭 BIG INDUSTRY INFLUENCE SCANNER")
                            st.info("Scanning federal Schedule A receipts to identify top corporate and employer donors pouring into this committee...")
                            
                            # 2. SCAN THE MONEY FLOW (EMPLOYERS)
                            employer_url = f"https://api.open.fec.gov/v1/schedules/schedule_a/by_employer/?committee_id={primary_id}&api_key={fec_api_key}&per_page=15"
                            emp_req = urllib.request.Request(employer_url, headers={'User-Agent': 'Mozilla/5.0'})
                            emp_data = json.loads(urllib.request.urlopen(emp_req).read())
                            
                            if 'results' in emp_data and len(emp_data['results']) > 0:
                                employers = []
                                for e in emp_data['results']:
                                    employers.append({
                                        "Corporate/Employer Entity": e.get("employer", "Unknown"),
                                        "Total Cash Funneled": f"${e.get('total', 0):,.2f}",
                                        "Number of Donations": e.get("count", 0)
                                    })
                                    
                                emp_df = pd.DataFrame(employers)
                                st.dataframe(emp_df, use_container_width=True)
                                
                                # 3. THE PROBABILITY ESTIMATOR GATE
                                st.markdown("#### 🛠️ REAL-WORLD INFLUENCE PROBABILITIES")
                                flat_text = emp_df.to_string().lower()
                                
                                # Estimator Logic
                                if "lockheed" in flat_text or "boeing" in flat_text or "raytheon" in flat_text or "defense" in flat_text:
                                    st.warning("⚠️ PROBABILITY: HIGH WARTIME SUPPLY LINE INFLUENCE")
                                    st.write("> Corporate defense money detected. High probability this target will vote to expand military hardware spending and international conflict pipelines rather than domestic infrastructure.")
                                    
                                if "google" in flat_text or "microsoft" in flat_text or "amazon" in flat_text or "software" in flat_text:
                                    st.error("🚨 PROBABILITY: HIGH AUTOMATION INSULATION INFLUENCE")
                                    st.write("> Big Tech money detected. High probability this target will protect AI and automation rights, directly threatening household wage defense and working-class job security.")
                                    
                                if "bank" in flat_text or "capital" in flat_text or "investment" in flat_text or "holdings" in flat_text:
                                    st.info("💡 PROBABILITY: HIGH WALL STREET ASSET INFLUENCE")
                                    st.write("> Heavy financial sector money detected. High probability this target will vote to protect corporate equity values and stock buybacks over adjusting flat-tax burdens on the working consumer.")
                                    
                                if "retired" in flat_text:
                                    st.success("✅ PROBABILITY: HIGH FIXED-INCOME BASE")
                                    st.write("> Significant fixed-income money detected. This suggests a reliance on individual human voters rather than concentrated corporate PACs, though the target may lean heavily into protecting legacy entitlements.")

                            else:
                                st.warning("No itemized employer/corporate donor data available for this specific committee yet.")
                        else:
                            st.warning("No financial committees found to scan.")
                            
                    except urllib.error.HTTPError as e:
                        if e.code == 403:
                            st.error("🛑 ACCESS DENIED (403): The API key you entered is incorrect.")
                        else:
                            st.error(f"🛑 FEC COMM LINE DOWN: {e}")
                else:
                    st.warning("⚠️ Enter your `data.gov` API key to run the probability scanner.")
        else:
            st.warning("Radar is clear. No targets currently returned by the engine.")

    except Exception as e:
        st.error(f"🛑 RENDER COMM LINE DOWN: {e}")

st.markdown("---")
st.caption("MINDY 16 // INTEGRATED ENGINE ARCHITECTURE // PORT 18408 RUNNING")
