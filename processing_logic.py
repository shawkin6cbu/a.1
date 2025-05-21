import re
import os
from io import StringIO
from datetime import datetime
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser



def extract_text_from_pdf(pdf_path):
    """
    Extracts text content from a PDF file.
    The extracted text is returned as a single string.
    """
    output_string = StringIO()
    with open(pdf_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, output_string, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        print(f"Processing PDF: {pdf_path}")
        for i, page in enumerate(PDFPage.create_pages(doc)):
            print(f"  Processing page {i + 1}...")
            interpreter.process_page(page)
        print("PDF processing complete.")
    return output_string.getvalue()



def preprocess_text_initial(text):
    """
    Initial preprocessing: Removes DocuSign IDs, DigitalControls, pipe chars.
    DOES NOT NORMALIZE MULTIPLE SPACES TO ONE.
    """
    if text is None:
        return None
    text = re.sub(r"Docusign Envelope ID: [\w-]+\s*\f?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\|[\w-]+DigitalControl_[\w_]+?\s*", " ", text)
    text = re.sub(r"\s+\|\s+", " ", text)
    text = re.sub(r"\|\s+", " ", text)
    text = re.sub(r"\s+\|", " ", text)
    return text.strip()



def normalize_multiple_spaces_in_text(text_segment):
    """Utility to reduce multiple spaces to one for text segments."""
    if text_segment is None:
        return None
    return re.sub(r"\s{2,}", " ", text_segment)



def preprocess_text_globally(text):  # ENSURE THIS FUNCTION IS DEFINED
    """
    General preprocessing: Applies initial cleaning and then normalizes multiple spaces.
    """
    if text is None:
        return None
    text = preprocess_text_initial(text)
    text = normalize_multiple_spaces_in_text(text)
    return text



def parse_any_legacy_contract_text(original_text_from_pdf):
    data = {}

    text_for_sensitive_parsing = preprocess_text_initial(original_text_from_pdf)
    globally_cleaned_text = normalize_multiple_spaces_in_text(text_for_sensitive_parsing)

    def search_and_extract(pattern, text_to_search, group_index=1, default=None, flags=re.DOTALL | re.IGNORECASE):
        if not text_to_search:
            return default
        match = re.search(pattern, text_to_search, flags)
        if match:
            try:
                if group_index <= len(match.groups()) and match.group(group_index) is not None:
                    captured_value = match.group(group_index).strip()
                    captured_value = re.sub(r"Docusign Envelope ID:.*?\f", "", captured_value, flags=re.IGNORECASE | re.DOTALL).strip()
                    captured_value = re.sub(r"\|[\w-]+DigitalControl_[\w_]+?\s*", " ", captured_value).strip()
                    return re.sub(r"\s{2,}", " ", captured_value).strip()
                else:
                    return default
            except IndexError:
                return default
        return default

    def clean_phone(phone_str):
        if phone_str:
            return re.sub(r'\D', '', phone_str)
        return None

    def clean_currency(currency_str):
        if currency_str:
            return currency_str.replace('$', '').replace(',', '').strip()
        return None

    def normalize_state(state_str):
        if not state_str:
            return None
        state_str_upper = state_str.upper().strip()
        state_str_upper = re.sub(r'\s*\f\s*', '', state_str_upper)
        if "MISSISSIPPI" in state_str_upper or state_str_upper == "MS":
            return "MS"
        if "TENNESSEE" in state_str_upper or state_str_upper == "TN":
            return "TN"
        if "TEXAS" in state_str_upper or state_str_upper == "TX":
            return "TX"
        if len(state_str_upper) == 2:
            return state_str_upper
        return state_str.strip()[:2].upper()

    # --- Hardcoded Fields ---
    data['COUNTY'] = "DeSoto"
    data['SLR1ADR1'] = "5740 Getwell Road Building 8B"
    data['SLR1ADR2'] = "Southaven, MS 38672"
    data['AG701FRM'] = "Legacy Homes Realty, LLC"
    data['AG701LIC'] = "24125"
    data['AG701AD1'] = "5740 Getwell Rd Bldg 8B"
    data['AG701AD2'] = "Southaven, MS 38672"
    data['AG701PH'] = "6629322282"
    # --- End Hardcoded Fields ---

    data['INCITY'] = 'X'
    data['INCOUNTY'] = 'X'
    data['DEPHELD'] = 'Seller'
    data['POSSION'] = 'Fee Simple'
    data['UNDNAME'] = 'Chicago Title Insurance Company'
    data['SLR1NAM1'] = search_and_extract(r"Parties\s*-\s*(LEGACY NEW HOMES, LLC.*?)\s*hereafter called SELLER", globally_cleaned_text)
    data['SLR1REL1'], data['SLR1NAM2'] = '', None
    data['SLR1CELL1'], data['SLR1EMAIL'], data['SLR1CELL2'], data['SLR1EMAIL2'] = None, None, None, None
    data['PARCELID'] = None
    data['PLISTINGAGENT'], data['MTDTTYPE'] = '2%', 'Deed of Trust'

    data['SALEPRIC'] = clean_currency(search_and_extract(r"Full Purchase Price\s*\$?([\d,]+\.\d{2})", globally_cleaned_text))
    data['DEPOSIT'] = clean_currency(search_and_extract(r"Deposit held by\s*LEGACY NEW HOMES,LLC\s*\$?([\d,]+\.\d{2})", globally_cleaned_text))
    if not data['DEPOSIT']:
        data['DEPOSIT'] = clean_currency(search_and_extract(r"DEPOSIT Held by Legacy New Homes, LLC\s*\$?([\d,]+\.\d{2})", globally_cleaned_text))

    # --- START: SETTDATE Extraction Logic (Rewritten with user's reliable approach) ---
    data['SETTDATE'] = None
    anchor = "Home is to close on or before"
    idx = original_text_from_pdf.find(anchor)
    if idx != -1:
        after = original_text_from_pdf[idx + len(anchor):]
        for token in re.split(r"\s+", after):            # walk tokens after anchor
            if token.count('/') > 4:                     # first token with >4 “/” ends block
                # keep only digits, slashes, and spaces
                filtered = ''.join(
                    ch if (ch.isdigit() or ch == '/' or ch == ' ') else ' '
                    for ch in token
                )
                # grab **all** date patterns in the filtered string
                dates = re.findall(r"\d{1,2}/\d{1,2}/\d{4}", filtered)
                if dates:
                    def _p(d):
                        try:
                            return datetime.strptime(d, "%m/%d/%Y")
                        except ValueError:
                            return datetime.min
                    data['SETTDATE'] = max(dates, key=_p)   # <-- latest date wins
                break
    # --- END: SETTDATE Extraction Logic ---

    byr1_name, byr2_name, byr1_rel = None, None, ''
    title_block_match = re.search(r"wishes to take title as follows:\s*(.*?)(?=\s*Please List whether BUYER is:|\s*Single Person|\s*Married Person|\s*Investor|$)", text_for_sensitive_parsing, re.IGNORECASE | re.DOTALL)
    if title_block_match:
        raw_names_str = title_block_match.group(1).strip()
        cleaned_names_str = raw_names_str
        if cleaned_names_str.lower().endswith("please"):
            match_please_end = re.match(r"(.*?)(\w*Please)$", cleaned_names_str, re.IGNORECASE)
            if match_please_end:
                word_before_please = match_please_end.group(2)[:-6] if len(match_please_end.group(2)) >= 6 else ""
                cleaned_names_str = (match_please_end.group(1) + word_before_please).strip()
        if " and " in cleaned_names_str.lower():
            parts = re.split(r"\s+and\s+", cleaned_names_str, maxsplit=1, flags=re.IGNORECASE)
            byr1_name = parts[0].strip()
            if len(parts) > 1 and parts[1].strip():
                byr2_name = parts[1].strip()
                byr1_rel = 'and'
        elif re.search(r"\s{3,}", cleaned_names_str):
            parts = re.split(r"\s{3,}", cleaned_names_str, maxsplit=1)
            byr1_name = parts[0].strip()
            if len(parts) > 1 and parts[1].strip():
                byr2_name = parts[1].strip()
                byr1_rel = 'and'
        else:
            byr1_name = cleaned_names_str.strip()
    data['BYR1NAM1'], data['BYR1NAM2'], data['BYR1REL1'] = byr1_name, byr2_name, byr1_rel

    buyer_contact_block_match = re.search(r"hereafter called BUYER\(s\), whose address, phone numbers, and email address(?:es)? are listed below\s*(.*?)\s*hereby agree", globally_cleaned_text, re.DOTALL | re.IGNORECASE)
    if buyer_contact_block_match:
        contact_details_str = buyer_contact_block_match.group(1)
        buyer_contacts_pattern = r"(\d+[\w\s\.,#-]*?(?:Street|St|Road|Rd|Drive|Dr|Avenue|Ave|Lane|Ln|Cove|Cv|Court|Ct|Place|Pl|Boulevard|Blvd))\s+([A-Za-z\s'-]+?)\s+(MS|TN|TX|MISSISSIPPI|TENNESSEE|TEXAS)\s+(\d{5})\s*\(?(\d{3})\)?\s*(\d{3}-\d{4})\s+([\w\.@-]+)"
        buyer_contacts_fallback_pattern = r"(\d+[\w\s\.,#-]*?\s\w+)\s+([A-Za-z\s'-]+?)\s+(MS|TN|TX|MISSISSIPPI|TENNESSEE|TEXAS)\s+(\d{5})\s*\(?(\d{3})\)?\s*(\d{3}-\d{4})\s+([\w\.@-]+)"
        buyer_contacts = re.findall(buyer_contacts_pattern, contact_details_str, re.IGNORECASE)
        if not buyer_contacts:
            buyer_contacts = re.findall(buyer_contacts_fallback_pattern, contact_details_str, re.IGNORECASE)
        if len(buyer_contacts) > 0:
            b1 = buyer_contacts[0]
            data['BYR1ADR1'] = b1[0].strip()
            data['BYR1ADR2'] = f"{b1[1].strip()}, {normalize_state(b1[2])} {b1[3].strip()}"
            data['BYR1CELL1'] = clean_phone(f"{b1[4]}{b1[5]}")
            data['BYR1EMAIL'] = b1[6].strip()
        if len(buyer_contacts) > 1:
            b2 = buyer_contacts[1]
            data['BYR1CELL2'] = clean_phone(f"{b2[4]}{b2[5]}")
            data['BYR1EMAIL2'] = b2[6].strip()
    for k_buyer_contact in ['BYR1ADR1', 'BYR1ADR2', 'BYR1CELL1', 'BYR1EMAIL', 'BYR1CELL2', 'BYR1EMAIL2']:
        data.setdefault(k_buyer_contact, None)

    prop_match = re.search(r"Lot\s+([\w\d]+)(?:\s*Plan/Elevation\s+[\w\s\d.-]+?)?\s*Subdivision\s+([\w\s\d.-]+?Phase\s*\d+|[\w\s\d.-]+?Section\s*\w+\s*Phase\s*\d+|[\w\s\d.-]+?)\s*Address\s+([\d\w\s.-]+?(?:Lane|Drive|Road|Cove|Street|St|Ave|Dr))\s+([A-Za-z\s'-]+?)\s+(MISSISSIPPI|MS|TENNESSEE|TN)\s+(\d{5})", globally_cleaned_text, re.IGNORECASE | re.DOTALL)
    if prop_match:
        data['LORU'], data['LOTUNIT'] = "Lot", prop_match.group(1).strip()
        data['SUBDIVN'] = prop_match.group(2).strip()
        data['PROPSTRE'] = prop_match.group(3).strip()
        data['PROPCITY'] = prop_match.group(4).strip()
        data['STATELET'] = normalize_state(prop_match.group(5))
        data['PROPZIP'] = prop_match.group(6).strip()
    else:
        prop_match_fallback = re.search(r"Lot\s+([\w\d]+).*?Subdivision\s+(.*?)\s*Address\s+([\d\w\s.-]+)\s+([A-Za-z\s'-]+?)\s+(MISSISSIPPI|MS|TENNESSEE|TN)\s+(\d{5})", globally_cleaned_text, re.IGNORECASE | re.DOTALL)
        if prop_match_fallback:
            data['LORU'], data['LOTUNIT'] = "Lot", prop_match_fallback.group(1).strip()
            data['SUBDIVN'] = prop_match_fallback.group(2).strip()
            full_addr = prop_match_fallback.group(3).strip()
            city_prop = prop_match_fallback.group(4).strip()
            if city_prop.lower() in full_addr.lower() and full_addr.lower() != city_prop.lower():
                parts = full_addr.rsplit(city_prop, 1)
                data['PROPSTRE'] = parts[0].strip() if len(parts) > 1 and parts[0].strip() else full_addr
            else:
                data['PROPSTRE'] = full_addr
            data['PROPCITY'] = city_prop
            data['STATELET'] = normalize_state(prop_match_fallback.group(5))
            data['PROPZIP'] = prop_match_fallback.group(6).strip()
        else:
            data['LORU'], data['LOTUNIT'], data['SUBDIVN'], data['PROPSTRE'], data['PROPCITY'], data['STATELET'], data['PROPZIP'] = (
                None, None, None, None, None, None, None)

    agent_section_overall_match = re.search(r"AGENCY DISCLOSURE\s*-\s*\(check one\):(.*?)(?=13\.\s*ARBITRATION|14\.\s*ARBITRATION|SIGNING BELOW|BY SIGNING BELOW|Property Condition Disclosure|$)", globally_cleaned_text, re.DOTALL | re.IGNORECASE)
    agent_text_block_overall = agent_section_overall_match.group(1).strip() if agent_section_overall_match else globally_cleaned_text
    listing_agent_block_match = re.search(r"Listing Agency\s*(.*?)(?=Selling Agency|$)", agent_text_block_overall, re.DOTALL | re.IGNORECASE)
    listing_agent_block_text = listing_agent_block_match.group(1).strip() if listing_agent_block_match else ""
    if listing_agent_block_text:
        data['AG701NAM'] = search_and_extract(r"Listing Agent\s+([\w\s,-]+?)(?=\s*Business Phone)", listing_agent_block_text)
        if data['AG701NAM']:
            data['AG701NAM'] = data['AG701NAM'].replace(',', '').strip()
        l_agent_phone_match = re.search(r"Listing Agent\s+[\w\s,-]+?Business Phone\s*([()\d\s-]+?)(?=\s*Address|\s*Email)", listing_agent_block_text, re.IGNORECASE)
        data['AG701MO'] = clean_phone(l_agent_phone_match.group(1)) if l_agent_phone_match else None
        data['AG701EMAIL'] = search_and_extract(r"Email\s+([\w\.@-]+?)(?=\s+License #:\s*Agent|\s*$)", listing_agent_block_text)
        data['AG701CONTLIC'] = search_and_extract(r"License #:\s*Agent\s*(.*?)(?=Selling Agency|$)", listing_agent_block_text)
    else:
        for k in ['AG701NAM', 'AG701MO', 'AG701EMAIL', 'AG701CONTLIC']:
            data.setdefault(k, None)

    selling_agent_block_match = re.search(r"Selling Agency\s*(.*?)(?=13\.\s*ARBITRATION|14\.\s*ARBITRATION|Revised\s+\d{2}/\d{2}/\d{2}|$)", agent_text_block_overall, re.DOTALL | re.IGNORECASE)
    selling_agent_block_text_for_details = selling_agent_block_match.group(1).strip() if selling_agent_block_match else ""
    if selling_agent_block_text_for_details:
        data['AG702FRM'] = search_and_extract(r"^([\w\s.,'&@#-]+?)(?=\s*Selling Agent|\s*Business Phone)", selling_agent_block_text_for_details)
        data['AG702LIC'] = search_and_extract(r"License #:\s*Firm\s*([S\d][\w-]+?)(?=\s*License #:\s*Agent|\s*Email:|$)", selling_agent_block_text_for_details)
        if data['AG702LIC']: data['AG702LIC'] = data['AG702LIC'].replace(" ", "")
        s_addr_match = re.search(r"Address:\s*([\w\s\.\d#-]+(?:Street|Parkway|Road|Rd)?(?:,\s*\#?\w+)?)\s*,\s*([A-Za-z\s'-]+?)\s*,\s*(MISSISSIPPI|MS|TENNESSEE|TN|TEXAS|TX)(?:,\s*(\d{5})(?:,\s*United States of America)?)?", selling_agent_block_text_for_details, re.IGNORECASE)
        zip_s = None
        if s_addr_match:
            data['AG702AD1'] = s_addr_match.group(1).strip(); city_s = s_addr_match.group(2).strip().replace(',', ''); state_s = normalize_state(s_addr_match.group(3))
            if s_addr_match.group(4): zip_s = s_addr_match.group(4).strip()
            else:
                zip_s_alt_match = re.search(r"(?:MISSISSIPPI|MS|TENNESSEE|TN|TEXAS|TX)(?:,\s*United States of America)?\s*(\d{5})", selling_agent_block_text_for_details, re.IGNORECASE)
                if zip_s_alt_match: zip_s = zip_s_alt_match.group(1).strip()
            data['AG702AD2'] = f"{city_s}, {state_s} {zip_s}" if zip_s else f"{city_s}, {state_s}"
        else: data['AG702AD1'], data['AG702AD2'] = None, None
        data['AG702PH'] = clean_phone(search_and_extract(r"Business Phone\s*([()\d\s-]+?)(?=\s+Address:|\s+Selling Agent)", selling_agent_block_text_for_details))
        data['AG702NAM'] = search_and_extract(r"Selling Agent\s+([\w\s,-]+?)(?=\s*Business Phone|,Business Phone)", selling_agent_block_text_for_details)
        if data['AG702NAM']: data['AG702NAM'] = data['AG702NAM'].replace(',', '').strip()
        sa_phone_match = re.search(r"Selling Agent\s+[\w\s,-]+?Business Phone\s*([()\d\s-]+?)(?=\s*Address|\s*Email)", selling_agent_block_text_for_details, re.IGNORECASE)
        data['AG702MO'] = clean_phone(sa_phone_match.group(1)) if sa_phone_match else None
        data['AG702EMAIL'] = search_and_extract(r"Email:\s*([\w\.@-]+)", selling_agent_block_text_for_details)
    else:
        for k in ['AG702FRM', 'AG702PH', 'AG702AD1', 'AG702AD2', 'AG702LIC', 'AG702NAM', 'AG702MO', 'AG702EMAIL']: data.setdefault(k, None)

    ag702contlic_pattern_full_text = r"Selling Agency.*?License #:\s*Firm\s*(?:[S]-)?\d[\w-]*\s*License #:\s*Agent\s*(.{1,20}?)(?=\s*\d{1,2}\.\s*ARBITRATION)"
    data['AG702CONTLIC'] = search_and_extract(ag702contlic_pattern_full_text, globally_cleaned_text)
    if not data.get('AG702CONTLIC'):
         data['AG702CONTLIC'] = search_and_extract(r"Selling Agency.*?License #:\s*Agent\s*(.{1,20}?)(?=\s*\d{1,2}\.\s*ARBITRATION)", globally_cleaned_text)
    data.setdefault('AG702CONTLIC', None)

    listing_agent_comm_pct = 2.0
    buyer_agent_comm_match = re.search(r"buyer’s agent compensation of\s+(\d+)%", globally_cleaned_text, re.IGNORECASE)
    if buyer_agent_comm_match:
        try: data['COMPCT'] = f"{listing_agent_comm_pct + float(buyer_agent_comm_match.group(1))}%"
        except ValueError: data['COMPCT'] = f"{listing_agent_comm_pct}%"
    else: data['COMPCT'] = f"{listing_agent_comm_pct}%"
    
    return data



def generate_legacy_folder_name(extracted_data):
    """Generates the folder name based on extracted BYR1NAM1."""
    byr1nam1 = extracted_data.get('BYR1NAM1')
    if byr1nam1:
        # Attempt to split into last name, first name if possible
        # This is a simple split, might need refinement based on actual byr1nam1 format
        name_parts = byr1nam1.split(',')
        if len(name_parts) > 1: # "Smith, Joe"
            last_name = name_parts[0].strip()
            first_name = name_parts[1].strip()
        else: # "Joe Smith" or just "Smith Inc"
            name_parts_space = byr1nam1.split()
            if len(name_parts_space) > 1:
                last_name = name_parts_space[-1] # Assume last word is last name
                first_name = " ".join(name_parts_space[:-1])
            else:
                last_name = byr1nam1 # Use the whole thing if it's a single word/company
                first_name = ""
        
        # Sanitize names for folder creation (remove invalid characters)
        first_name_safe = re.sub(r'[<>:"/\\|?*]', '', first_name)
        last_name_safe = re.sub(r'[<>:"/\\|?*]', '', last_name)

        if first_name_safe:
            return f"{last_name_safe}, {first_name_safe}  25-"
        else:
            return f"{last_name_safe}  25-"

    return "Unknown_Entity  25-" # Fallback name



def create_legacy_contract_folder_structure(base_output_dir, folder_name, extracted_data): # Added extracted_data
    """
    Creates the specific folder structure for a Legacy contract.
    """
    full_folder_path = os.path.join(base_output_dir, folder_name)
    print(f"INFO: Creating Legacy contract folder at: {full_folder_path}")

    try:
        os.makedirs(full_folder_path, exist_ok=True)

        # Create "overlay.pxt" with all extracted data
        entity_list_content = []
        for key, value in extracted_data.items():
            entity_list_content.append(f"{key}: {value}")
        
        with open(os.path.join(full_folder_path, "overlay.pxt"), "w") as f:
            f.write("\n".join(entity_list_content))
            f.write("\n\n--- End of Extracted Data ---")

        # Placeholder files (content to be generated later based on extracted_data)
        with open(os.path.join(full_folder_path, "file label.docx"), "w") as f:
            f.write(f"File Label for: {folder_name}\n")
            f.write(f"Property Address: {extracted_data.get('PROPSTRE', 'N/A')}\n")
            # Add more relevant data to the label
        with open(os.path.join(full_folder_path, "setupdocs.docx"), "w") as f:
            f.write(f"Setup Documents for: {folder_name}\n")
            # Add more relevant data

        # Create subfolders
        os.makedirs(os.path.join(full_folder_path, "Setup"), exist_ok=True)
        os.makedirs(os.path.join(full_folder_path, "TitleSearch"), exist_ok=True)

        print(f"SUCCESS: Created folder structure for '{folder_name}'")
        return full_folder_path, True
    except OSError as e:
        print(f"ERROR: Could not create folder structure for '{folder_name}'. Error: {e}")
        return full_folder_path, False



def handle_legacy_contract_processing(pdf_file_paths, user_selected_output_dir):
    """
    Main handler for processing "Legacy" contracts.
    """
    if not pdf_file_paths:
        print("ERROR: No PDF files provided for Legacy processing.")
        return None, "No PDF files provided.", None # Return None for data too

    # For now, process the first PDF. You might need a loop or different logic later.
    main_pdf_path = pdf_file_paths[0]
    
    try:
        print(f"INFO: Starting PDF text extraction for {main_pdf_path}")
        raw_text = extract_text_from_pdf(main_pdf_path)
        if not raw_text:
            error_msg = f"Could not extract any text from {main_pdf_path}."
            print(f"ERROR: {error_msg}")
            return None, error_msg, None
        
        print(f"INFO: Starting parsing for {main_pdf_path}")
        extracted_data = parse_any_legacy_contract_text(raw_text)
        if not extracted_data or not extracted_data.get('BYR1NAM1'): # Check if essential data is present
            error_msg = f"Failed to parse essential data (like BYR1NAM1) from {main_pdf_path}."
            print(f"ERROR: {error_msg}")
            return None, error_msg, extracted_data # Return partial data if any

    except Exception as e:
        error_msg = f"An error occurred during PDF processing or parsing for {main_pdf_path}: {e}"
        print(f"CRITICAL ERROR: {error_msg}")
        # import traceback
        # traceback.print_exc() # For detailed debugging
        return None, error_msg, None

    folder_name = generate_legacy_folder_name(extracted_data)
    created_folder_path, success = create_legacy_contract_folder_structure(
        user_selected_output_dir, folder_name, extracted_data # Pass extracted_data
    )

    if success:
        print(f"INFO: Further processing for files in '{created_folder_path}' would happen here.")
        return created_folder_path, f"Successfully created structure for {folder_name}", extracted_data
    else:
        return None, f"Failed to create structure for {folder_name}", extracted_data