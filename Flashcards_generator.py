import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import random


class FlashcardGenerator:
    def __init__(self, notes_file=None, deck_file="flashcards.json"):
        self.notes_file = notes_file
        self.deck_file = deck_file
        self.deck = self.load_deck()
    
    def load_deck(self):
        if Path(self.deck_file).exists():
            with open(self.deck_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"cards": []}
    
    def save_deck(self):
        with open(self.deck_file, 'w', encoding='utf-8') as f:
            json.dump(self.deck, f, indent=2, ensure_ascii=False)
    
    def parse_notes(self, content=None):
        if content is None and self.notes_file:
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                content = f.read()
        elif content is None:
            return []
        
        cards = []
        now = datetime.now().isoformat()
        
        patterns = [
            (r'Q:\s*(.+?)\s*A:\s*(.+?)(?=\n\s*Q:|$)', self._create_card),
            (r'^[\-\*]\s*(.+?):\s*(.+?)$', self._create_card),
        ]
        
        for pattern, create_func in patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for q, a in matches:
                cards.append(create_func(q.strip(), a.strip(), now))
        
        heading_lines = content.split('\n')
        for i, line in enumerate(heading_lines):
            match = re.match(r'^#+\s*(.+?)$', line.strip())
            if match and i + 1 < len(heading_lines):
                heading = match.group(1).strip()
                next_content = []
                for j in range(i + 1, len(heading_lines)):
                    if re.match(r'^#+\s*.+?$', heading_lines[j].strip()):
                        break
                    if heading_lines[j].strip():
                        next_content.append(heading_lines[j].strip())
                    if len(next_content) >= 3:
                        break
                
                if next_content:
                    cards.append(self._create_card(heading, ' '.join(next_content), now))
        
        return cards
    
    def _create_card(self, front, back, timestamp):
        return {
            "front": front,
            "back": back,
            "ease_factor": 2.5,
            "interval": 0,
            "repetitions": 0,
            "next_review": timestamp,
            "created": timestamp
        }
    
    def generate_flashcards(self, content=None):
        if content:
            new_cards = self.parse_notes(content)
        elif self.notes_file:
            new_cards = self.parse_notes()
        else:
            return 0
        
        existing_fronts = {card["front"] for card in self.deck["cards"]}
        added = 0
        
        for card in new_cards:
            if card["front"] not in existing_fronts:
                self.deck["cards"].append(card)
                added += 1
        
        if added > 0:
            self.save_deck()
        
        return added
    
    def add_manual_card(self, front, back):
        card = self._create_card(front, back, datetime.now().isoformat())
        self.deck["cards"].append(card)
        self.save_deck()
        return card
    
    def get_all_cards(self):
        return self.deck.get("cards", [])
    
    def get_due_cards(self):
        now = datetime.now()
        due = []
        for card in self.deck["cards"]:
            next_review = datetime.fromisoformat(card["next_review"])
            if next_review <= now:
                due.append(card)
        return due
    
    def get_card_stats(self):
        total = len(self.deck["cards"])
        due = len(self.get_due_cards())
        mastered = total - due
        return {
            "total": total,
            "due": due,
            "mastered": mastered,
            "mastery_percentage": (mastered / total * 100) if total > 0 else 0
        }


class SpacedRepetition:
    def __init__(self, deck_file="flashcards.json"):
        self.deck_file = deck_file
        self.deck = self.load_deck()
    
    def load_deck(self):
        if Path(self.deck_file).exists():
            with open(self.deck_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"cards": []}
    
    def save_deck(self):
        with open(self.deck_file, 'w', encoding='utf-8') as f:
            json.dump(self.deck, f, indent=2, ensure_ascii=False)
    
    def get_due_cards(self):
        now = datetime.now()
        due = []
        for card in self.deck["cards"]:
            next_review = datetime.fromisoformat(card["next_review"])
            if next_review <= now:
                due.append(card)
        return due
    def get_card_stats(self):  # ADD THIS METHOD
        total = len(self.deck["cards"])
        due = len(self.get_due_cards())
        mastered = total - due
        return {
            "total": total,
            "due": due,
            "mastered": mastered,
            "mastery_percentage": (mastered / total * 100) if total > 0 else 0
        }
    def sm2_algorithm(self, card, quality):
        if quality < 3:
            card["repetitions"] = 0
            card["interval"] = 0
        else:
            if card["repetitions"] == 0:
                card["interval"] = 1
            elif card["repetitions"] == 1:
                card["interval"] = 6
            else:
                card["interval"] = round(card["interval"] * card["ease_factor"])
            
            card["repetitions"] += 1
        
        card["ease_factor"] = max(1.3, card["ease_factor"] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        if card["interval"] == 0:
            card["next_review"] = (datetime.now() + timedelta(minutes=10)).isoformat()
        else:
            card["next_review"] = (datetime.now() + timedelta(days=card["interval"])).isoformat()
        
        return card
    
    def review_card(self, card, quality):
        updated_card = self.sm2_algorithm(card.copy(), quality)
        for i, c in enumerate(self.deck["cards"]):
            if c["front"] == card["front"] and c["back"] == card["back"]:
                self.deck["cards"][i] = updated_card
                break
        self.save_deck()
        return updated_card
    
    def get_review_session(self, shuffle=True):
        due_cards = self.get_due_cards()
        if shuffle:
            random.shuffle(due_cards)
        return due_cards