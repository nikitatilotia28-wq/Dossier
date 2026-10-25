import streamlit as st

TEXT = {
    "English": {
        "language": "Language",
        "switch_hint": "Choose the language for this app",
        "home": "Home",
        "dashboard": "Home",
        "plain_title": "Rent with clarity. Keep your proof.",
        "plain_subtitle": "Simple help for finding, checking, sharing, and leaving a home in Mumbai.",
        "choose_area": "1. Choose an area",
        "check_listing": "2. Check the listing",
        "check_agreement": "3. Check the agreement",
        "protect_home": "4. Protect your home",
        "records": "5. Keep your records",
        "property": "Locality Guide",
        "roommates": "Find Roommates",
        "workspace": "My Rental",
        "scan": "Check Agreement",
        "history": "My Records",
        "listing": "Owner Listings",
        "reviews": "Society Reviews",
    },
}


def setup_language() -> str:
    st.session_state["language"] = "English"
    return "English"


def t(key: str) -> str:
    language = st.session_state.get("language", "English")
    return TEXT.get(language, TEXT["English"]).get(key, TEXT["English"].get(key, key))
