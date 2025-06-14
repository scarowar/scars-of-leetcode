import json
import os
import hashlib
import requests
import glob
import platform
import subprocess  # nosec: B404


def get_windows_host_ip_from_wsl():
    """
    On WSL, read 'ip route' to find the Windows host IP.
    Returns IP string or None if not found.
    """
    try:
        # subprocess is required here to get host IP in WSL; input is trusted
        output = subprocess.check_output(  # nosec B603, B607
            ["ip", "route"], encoding="utf-8"
        )
        for line in output.splitlines():
            if line.startswith("default via "):
                parts = line.split()
                if len(parts) >= 3:
                    return parts[2]
    except Exception as e:
        # Log the error for debugging, but do not fail automation
        print(f"[WARN] Failed to get Windows host IP: {e}")
    return None


def get_anki_connect_url():
    # Default URL
    default_url = "http://localhost:8765"

    # Detect if running inside WSL
    if platform.system() == "Linux":
        # Check if WSL by reading /proc/version
        try:
            with open("/proc/version", "r") as f:
                version_info = f.read().lower()
            if "microsoft" in version_info or "wsl" in version_info:
                win_ip = get_windows_host_ip_from_wsl()
                if win_ip:
                    return f"http://{win_ip}:8765"
        except Exception as e:
            print(f"[WARN] Failed to detect WSL host: {e}")

    # Otherwise use localhost
    return default_url


ANKI_CONNECT_URL = get_anki_connect_url()

MASTER_DECK_FILE = "anki/scars-of-leetcode.json"
PROBLEMS_FOLDER = "problems"


def load_master_deck():
    if os.path.exists(MASTER_DECK_FILE):
        with open(MASTER_DECK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "problem_id": "merged",
            "problem_title": "Scars of LeetCode",
            "cards": [],
        }


def save_master_deck(data):
    with open(MASTER_DECK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def card_hash(card):
    # Unique string hash of front+back to identify duplicates
    return hashlib.sha256(
        (card["front"] + "\t" + card["back"]).encode("utf-8")
    ).hexdigest()


def merge_cards(master_data, new_data):
    existing_hashes = set(card_hash(c) for c in master_data["cards"])
    new_cards_added = 0
    for card in new_data["cards"]:
        h = card_hash(card)
        if h not in existing_hashes:
            master_data["cards"].append(card)
            existing_hashes.add(h)
            new_cards_added += 1
    return new_cards_added


def invoke(action, params):
    request_json = {"action": action, "version": 6, "params": params}
    try:
        # Add timeout to avoid hanging
        response = requests.post(ANKI_CONNECT_URL, json=request_json, timeout=10)
        response_json = response.json()
    except Exception as e:
        raise Exception(f"Failed to connect to AnkiConnect: {e}")
    if "error" in response_json and response_json["error"] is not None:
        raise Exception(f"AnkiConnect error: {response_json['error']}")
    return response_json["result"]


def prepare_note(card):
    tags = card.get("tags", "")
    if isinstance(tags, list):
        tags_list = tags
    else:
        tags_list = tags.split() if tags else []

    if card.get("card_type", "").lower() == "cloze":
        note_type = "Cloze"
        fields = {"Text": f"{card['front']}\n\n{card['back']}"}
    else:
        note_type = "Basic"
        fields = {"Front": card["front"], "Back": card["back"]}

    return {
        "deckName": "Scars of LeetCode",
        "modelName": note_type,
        "fields": fields,
        "tags": tags_list,
        "options": {"allowDuplicate": False},
    }


def import_to_anki(cards):
    notes = [prepare_note(c) for c in cards]
    batch_size = 50
    for i in range(0, len(notes), batch_size):
        batch = notes[i : i + batch_size]
        params = {"notes": batch}
        result = invoke("addNotes", params)
        print(f"Imported batch {i//batch_size + 1}: {result}")


def ensure_deck_exists(deck_name):
    try:
        invoke("createDeck", {"deck": deck_name})
    except Exception as e:
        # If deck already exists, ignore the error, but log for debugging
        print(f"[INFO] Deck may already exist or error occurred: {e}")


def find_all_cards_json(base_folder=PROBLEMS_FOLDER):
    cards_files = glob.glob(
        os.path.join(base_folder, "**", "cards.json"), recursive=True
    )
    return cards_files


def add_neetcode_tag_if_needed(cards, filepath):
    # Add 'NeetCode150' tag if filepath contains 'NeetCode150'
    if "NeetCode150" in filepath:
        for card in cards:
            tags = card.get("tags", "")
            if isinstance(tags, str):
                tags_list = tags.split()
            else:
                tags_list = tags

            if "NeetCode150" not in tags_list:
                tags_list.append("NeetCode150")

            # Save back as string or list as original
            if isinstance(tags, str):
                card["tags"] = " ".join(tags_list)
            else:
                card["tags"] = tags_list


def main():
    if not os.path.exists("anki"):
        os.makedirs("anki")

    master_data = load_master_deck()
    cards_files = find_all_cards_json()
    total_added = 0

    for file_path in cards_files:
        with open(file_path, "r", encoding="utf-8") as f:
            new_data = json.load(f)
        # Add NeetCode150 tag to cards if applicable
        add_neetcode_tag_if_needed(new_data["cards"], file_path)

        added = merge_cards(master_data, new_data)
        total_added += added
        print(f"Merged {added} new cards from {file_path}")

    if total_added > 0:
        save_master_deck(master_data)
        print(f"Added a total of {total_added} new cards to the master deck.")
    else:
        print("No new cards to add.")

    if len(master_data["cards"]) > 0:
        ensure_deck_exists("Scars of LeetCode")  # Create deck if missing
        import_to_anki(master_data["cards"])
        print("✅ All cards merged and imported into Anki.")
    else:
        print("No cards available to import.")


if __name__ == "__main__":
    main()
